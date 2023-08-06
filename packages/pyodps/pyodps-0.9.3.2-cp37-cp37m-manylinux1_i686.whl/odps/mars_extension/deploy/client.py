#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 1999-2017 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import time
import requests
import json

from cupid import CupidSession
from mars.session import new_session

from ...utils import write_log
from ...models import Instance
from ...config import options
from ... import errors

NOTEBOOK_NAME = 'MarsNotebook'
CUPID_APP_NAME = 'MarsWeb'
DEFAULT_RESOURCES = ['public.mars-0.4.6.zip', 'public.pyodps-0.9.3.2.zip', 'public.pyarrow.zip']
logger = logging.getLogger(__name__)


def _build_namespace_config(namespace):
    config = {
        'kind': 'Namespace',
        'metadata': {
            'name': namespace,
            'labels': {
                'name': namespace
            }
        },
    }
    return config


class MarsCupidClient(object):
    def __init__(self, odps, inst=None, project=None):
        self._odps = odps
        self._cupid_session = CupidSession(odps, project=project)
        self._kube_instance = inst
        self._kube_url = None
        self._kube_client = None
        self._kube_namespace = None

        self._scheduler_key = None
        self._scheduler_config = None
        self._worker_config = None
        self._web_config = None
        self._endpoint = None
        self._has_notebook = False
        self._notebook_endpoint = None

        self._mars_session = None
        self._req_session = None

    @property
    def endpoint(self):
        return self._endpoint

    @property
    def notebook_endpoint(self):
        return self._notebook_endpoint

    @property
    def session(self):
        return self._mars_session

    @property
    def instance_id(self):
        return self._kube_instance.id

    def submit(self, worker_num=1, worker_cpu=8, worker_mem=32, disk_num=1, min_worker_num=None, cache_mem=None,
               resources=None, module_path=None, create_session=True, priority=None, running_cluster=None,
               scheduler_num=1, notebook=None, task_name=None, **kw):
        try:
            async_ = kw.pop('async_', None)
            default_resources = kw.pop('default_resources', None) or DEFAULT_RESOURCES
            if notebook is not None:
                self._has_notebook = bool(notebook)
            else:
                self._has_notebook = options.mars.launch_notebook
            if self._kube_instance is None:
                if module_path is not None:
                    if isinstance(module_path, (tuple, list)):
                        module_path = list(module_path) + ['odps.mars_extension']
                    else:
                        module_path = [module_path, 'odps.mars_extension']

                if resources is not None:
                    if isinstance(resources, (tuple, list)):
                        resources = list(resources)
                        resources.extend(default_resources)
                    else:
                        resources = [resources] + default_resources
                else:
                    resources = default_resources

                if cache_mem is None:
                    cache_mem = str(worker_mem * 0.48) + 'G'
                else:
                    cache_mem = str(cache_mem) + 'G'
                mars_config = {
                    'scheduler_num': scheduler_num,
                    'worker_num': worker_num,
                    'worker_cpu': worker_cpu,
                    'worker_mem': worker_mem,
                    'cache_mem': cache_mem or '',
                    'disk_num': disk_num,
                    'resources': resources,
                    'module_path': module_path or ['odps.mars_extension'],
                }
                if 'mars_app_image' in kw:
                    mars_config['mars_app_image'] = kw.pop('mars_app_image')
                if 'mars_image' in kw:
                    mars_config['mars_image'] = kw.pop('mars_image')
                if 'proxy_endpoint' in kw:
                    mars_config['proxy_endpoint'] = kw.pop('proxy_endpoint')
                if 'major_task_version' in kw:
                    mars_config['major_task_version'] = kw.pop('major_task_version')
                mars_config['scheduler_mem'] = kw.pop('scheduler_mem', 32)
                mars_config['scheduler_cpu'] = kw.pop('scheduler_cpu', 8)

                if self._has_notebook:
                    mars_config['notebook'] = True
                self._kube_instance = self._cupid_session.start_kubernetes(
                    async_=True, running_cluster=running_cluster, priority=priority,
                    app_name='mars', app_config=mars_config, task_name=task_name, **kw)
                write_log(self._kube_instance.get_logview_address())
            if async_:
                return self
            else:
                self.wait_for_success(create_session=create_session, min_worker_num=min_worker_num or worker_num)
                return self

        except KeyboardInterrupt:
            self.stop_server()
            return self

    def check_service_ready(self, timeout=1):
        try:
            resp = self._req_session.get(self._endpoint + '/api', timeout=timeout)
        except (requests.ConnectionError, requests.Timeout):
            return False
        if resp.status_code >= 400:
            return False
        return True

    def count_workers(self):
        resp = self._req_session.get(self._endpoint + '/api/worker?action=count', timeout=1)
        return json.loads(resp.text)

    def get_logview_address(self):
        return self._kube_instance.get_logview_address()

    def get_mars_endpoint(self):
        return self._cupid_session.get_proxied_url(self._kube_instance.id, CUPID_APP_NAME)

    def get_notebook_endpoint(self):
        return self._cupid_session.get_proxied_url(self._kube_instance.id, NOTEBOOK_NAME)

    def get_req_session(self):
        from ...rest import RestClient

        if options.mars.use_common_proxy:
            return RestClient(self._odps.account, self._endpoint, self._odps.project)
        else:
            return requests.Session()

    def check_instance_status(self):
        if self._kube_instance.is_terminated():
            for task_name, task in (self._kube_instance.get_task_statuses()).items():
                exc = None
                if task.status == Instance.Task.TaskStatus.FAILED:
                    exc = errors.parse_instance_error(self._kube_instance.get_task_result(task_name))
                elif task.status != Instance.Task.TaskStatus.SUCCESS:
                    exc = errors.ODPSError('%s, status=%s' % (task_name, task.status.value))
                if exc:
                    exc.instance_id = self._kube_instance.id
                    raise exc

    def wait_for_success(self, min_worker_num=0, create_session=True):
        while True:
            self.check_instance_status()
            try:
                if self._endpoint is None:
                    self._endpoint = self.get_mars_endpoint()
                    write_log('Mars UI: ' + self._endpoint)
                    self._req_session = self.get_req_session()

                    self._req_session.post(self._endpoint.rstrip('/') + '/api/logger', data=dict(
                        content='Mars UI from client: ' + self._endpoint
                    ))
                if self._has_notebook and self._notebook_endpoint is None:
                    self._notebook_endpoint = self.get_notebook_endpoint()
                    write_log('Notebook UI: ' + self._notebook_endpoint)

                    self._req_session.post(self._endpoint.rstrip('/') + '/api/logger', data=dict(
                        content='Notebook UI from client: ' + self._notebook_endpoint
                    ))
            except KeyboardInterrupt:
                raise
            except:
                time.sleep(1)
                continue

            if not self.check_service_ready():
                continue
            try:
                if self.count_workers() >= min_worker_num:
                    break
                else:
                    time.sleep(1)
            except:
                continue

        if create_session:
            try:
                self._mars_session = new_session(self._endpoint, req_session=self._req_session).as_default()
            except KeyboardInterrupt:
                raise
            except:
                if self._kube_instance and self._kube_instance.status == self._kube_instance.Status.RUNNING:
                    self._kube_instance.stop()
                raise

    def stop_server(self):
        if self._kube_instance:
            self._kube_instance.stop()
            self._kube_instance = None
