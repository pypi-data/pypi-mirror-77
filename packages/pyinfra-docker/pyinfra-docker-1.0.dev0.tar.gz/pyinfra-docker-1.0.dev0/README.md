# pyinfra Docker

A basic [pyinfra](https://github.com/Fizzadar/pyinfra) deploy that installs and optionally configures Docker on the target hosts. Officially tested & supported Linux distributions:

+ Ubuntu 16/18/20
+ Debian 8/9/10
+ CentOS 7/8

## Usage

See [the example](./example) for a more complete example.

```py
from pyinfra_docker import deploy_docker
deploy_docker()
```
