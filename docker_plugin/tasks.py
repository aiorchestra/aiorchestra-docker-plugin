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

from aiorchestra.core import utils

from docker_plugin import connector


@utils.operation
async def create(node, inputs):
    parameters = node.properties
    docker_daemon_url = parameters.get('docker_daemon_url')
    if not docker_daemon_url:
        raise Exception("Docker daemon URL was specified")
    port_binds = parameters.get('port_bindings')
    if not isinstance(port_binds, dict):
        raise Exception("Invalid type of `port_bindings`")
    image = parameters.get('image')
    if not image:
        raise Exception("Image was not specified")
    env = parameters.get('environment', {})
    if not (env and isinstance(env, dict)):
        raise Exception("Invalid `environment` type of value")
    name = parameters.get("name")
    if not name:
        raise Exception("`name was not specified`")

    container = connector.DockerContainer(name, image,
                                          port_binds, docker_daemon_url)
    result = container.create_container(env)
    node.update_runtime_properties(result)


@utils.operation
async def start(node, inputs):
    pass


@utils.operation
async def stop(node, inputs):
    pass


@utils.operation
async def delete(node, inputs):
    pass
