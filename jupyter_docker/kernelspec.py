"""Tools for managing kernel specs"""

# Copyright (c) Marius van Niekerk
# Distributed under the terms of the Modified BSD License.

from jupyter_client.kernelspec import KernelSpec, KernelSpecManager
from traitlets import Unicode, List, Type
from traitlets.config import LoggingConfigurable
import os

class DockerKernelSpec(KernelSpec):

    docker_image_name = Unicode()
    docker_args = List()

class DockerKernelSpecManager(KernelSpecManager):
    kernel_spec_class = Type(DockerKernelSpec, config=True,
        help="""The kernel spec class.  This is configurable to allow
        subclassing of the KernelSpecManager for customized behavior.
        """
    )

class DockerKernelManagerMixin(LoggingConfigurable):

    docker_executable = Unicode("docker")
    docker_default_options = List(["--rm", "--net=host"])

from jupyter_client.ioloop.manager import IOLoopKernelManager


class DockerKernelManager(IOLoopKernelManager, DockerKernelManagerMixin):

    def format_kernel_cmd(self, extra_arguments=None):
        cmd = super(DockerKernelManager, self).format_kernel_cmd(extra_arguments)
        # Prepend all the docker stuff.  This seems to be sufficient.
        if self.kernel_spec.docker_image_name:
            connection_path, _ = os.path.split(self.connection_file)
            # Right now environment variables are dropped on the floor


            docker_prefix = [self.docker_executable] \
                            + self.docker_default_options \
                            + self.kernel_spec.docker_args \
                            + ['--user={}:{}'.format(os.getuid(), os.getgid()),
                               '-v', '{c}:{c}'.format(c=connection_path),
                               '-v', '{c}:{c}'.format(c=os.path.expanduser('~')),
                               self.kernel_spec.docker_image_name,
                               ]
            return docker_prefix + cmd
        else:
            return cmd