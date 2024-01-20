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