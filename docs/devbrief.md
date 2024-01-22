## topics

1. about hydra config: it is a powerful tool for config complex, i thought i may use it, but it is too complex to use for me.

2. The only way to ioslate user space is to use virtual machine, but it is too heavy to use.

following items should be ioslated:
* standard library which can be connected to the system interface. (os, sys, etc.)
* bytecode might access and control other memory space by using out of border.
* global variables

3. necessary components for subapp

* load up function list sequence
* unfinish task list
* comfirm and report platform

> after compare with the complexity of message queue and callback, it is better to use a simple way to dispatch function,(callback).

4. about vms

load vm by vm tools is slow, the best way is to copy files and env configs, in this case the only factor is the size of files.

copy venv files and cfg ,run a specific python file, it is the best way to run a python script.

a question is, how does swagger api's schema generated?

if a class can be parse to a json schema, what function can make it ?
