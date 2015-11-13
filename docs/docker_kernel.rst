.. _docker_kernel:

=======================================
Configuring and using the docker Kernel
=======================================

The docker kernel adds two new keys to the `kernel.json` files used to configure kernels

 - **docker_image_name**: The name of the docker container to launch with `docker run`.
 - **docker_args**: A list of additional parameters to pass to `docker run`

In addition to these configurable options the docker kernels will always pass on uid:gid and will volume mount the
user's home directory.


========================
Configuring the notebook
========================

In the notebook's configuration files "jupyter_notebook_config.py"

    c.MultiKernelManager.kernel_manager_class = 'jupyter_docker_kernel.DockerKernelManager'





