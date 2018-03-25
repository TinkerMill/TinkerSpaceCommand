This folder contains the SpaceCommand Server.

The python folder contains the Python components of the server.

Install the following packages:

* pip3 install zeroconf
* pip3 install paho-mqtt
* pip3 install pyyaml
* pip3 install django


To Run the Example Server
=========================
```linux
$ conda info --envs
$ source activate IOT
$ python ExampleServer.py server.yaml
```

What Happens at Startup?
========================
* Config file is loaded into `config`
* `entity registry` object is created from `EntityRegistry()` class
  * _SpacdCommandServer/TinkerSpaceCommandServer/entities/EntityRegistry.py_
  * Imports `Entities` class
* `YamlEntityRegistryReader`
  
