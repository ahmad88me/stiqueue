
![stiqueue](https://github.com/ahmad88me/stiqueue/raw/main/stiqueue.png)


# stiqueue

![tests](../../actions/workflows/python-package.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/stiqueue.svg?kill-cache=1)](https://badge.fury.io/py/stiqueue)


Stands for stick queue which is a simple messaging queue. It is developed with simplicity and flexibility in mind.  


## Usage 

### Methods
The followings are a set of methods supported by stiqueue
* **enq**: to add to the queue (enqueue).
* **deq**: to get a value from the queue (dequeue).
* **cnt**: number of items in the queue.

### Examples

#### Client example

```
from stiqueue.sqclient import SQClient

c = SQClient()
c.enq(b"This is message one")
c.enq(b"This is message two")
c.enq(b"This is message three")
msg = c.deq().decode()
print("msg1: ")
print(msg)
msg = c.deq().decode()
print("msg2: ")
print(msg)
msg = c.deq().decode()
print("msg3: ")
print(msg)
```

#### Server example
```
from stiqueue.sqserver import SQServer

server = SQServer()
server.listen()
```

### Extend
We provide two samples extending stiqueue with more functionality. [examples](https://github.com/ahmad88me/stiqueue/tree/main/example)

### Server
You can run the server `sqserver.py` as is. 
```
python src/stiqueue/sqserver --host 0.0.0.0 --port 1234
```
You can also change the port to any of your choice.
The default one used in Docker is `27017`. You can also 
extend the server and add additional methods to meet your needs.

### Client
Most probably you want to extend the class `SQClient`, located in `stiqueue/sqclient.py`.
You can see an example of this in `example.client.py`.

## Run tests
```python -m unittest discover```




