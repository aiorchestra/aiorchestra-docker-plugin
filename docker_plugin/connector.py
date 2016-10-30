#    Author: Denys Makogon
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import docker


class DockerConnector(object):

    def __init__(self, base_url):
        self._client = docker.Client(base_url=base_url, timeout=60)

    @property
    def connection(self):
        return self._client

    @connection.setter
    def connection(self, newcon):
        raise Exception("Connection modification is forbidden")


class DockerContainer(object):

    def __init__(self, name, image, port_bindings, docker_daemon_url):
        self.port_binding = port_bindings
        self.name = name
        self.image = image
        self.connection = DockerConnector(docker_daemon_url).connection

    def _create_host_config(self, volumes=None):
        return self.connection.create_host_config(
            port_bindings=self.port_binding, binds=volumes)

    def create_container(self, env):
        return self.connection.create_container(
            self.image, name=self.name, environment=env, ports=self.port_binding)
