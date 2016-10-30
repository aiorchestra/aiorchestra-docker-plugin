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
from docker import errors


class DockerConnector(object):

    def __init__(self, base_url):
        try:
            self._client = docker.Client(base_url=base_url, timeout=60)
        except errors.DockerException as e:
            pass

    @property
    def connection(self):
        return self._client

    @connection.setter
    def connection(self, newcon):
        raise Exception("Connection modification is forbidden")


class DockerContainer(object):

    def __init__(self, name, image, host_bind_port, container_bind_port, docker_daemon_url):
        self.port_binding = {host_bind_port, container_bind_port}
        self.name = name
        self.image = image
        self.connection = DockerConnector(docker_daemon_url).connection

    def _get_exposed_ports(self, ports):
        return dict(ports).values() if ports else None

    def _create_host_config(self, bind_ports=None, volumes=None):
        return self.connection.create_host_config(
            port_bindings=bind_ports, binds=volumes)

    def create_container(self, name, image, env=None, volumes=None):
        return self.connection.create_container(
            image, name=name, environment=env,
            volumes=volumes, ports=self.port_binding)
