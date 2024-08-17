
![stiqueue](https://github.com/ahmad88me/stiqueue/raw/main/stiqueue.png)


# stiqueue

![tests](../../actions/workflows/python-package.yml/badge.svg)
[![PyPI version](https://badge.fury.io/py/stiqueue.svg?kill-cache=1)](https://badge.fury.io/py/stiqueue)


Stands for stick queue which is a simple messaging queue. It is developed with simplicity and flexibility in mind. 

## Code docs
[stiqueue doc](https://ahmad88me.github.io/stiqueue/)

## Guide 

### SQServer
You can run the SQServer directly without the need to write any piece of code.
The server will handle the messaging queue. Once the code is downloaded, you can run it as follows:
```
python src/stiqueue/sqserver.py --host 0.0.0.0 --port 1234 --debug
```
It is recommended to use the `--debug` if you are running it for the first time to 
see when the server is getting a message or once a message is leaving the queue.

#### Usage
The following is the command line options
```
usage: StiQueue Server [-h] [--debug] [--host HOST] [--port PORT] [--buff-size BUFF_SIZE]

A message queue server

options:
  -h, --help            show this help message and exit
  --debug               Showing debug messages
  --host HOST           The host address of the server
  --port PORT           The port to listen on
  --buff-size BUFF_SIZE
                        The size of the buffer
```

### SQClient
The client is meant to be used inside your code. Once you install the `stiqueue` package
inside your python project, you can use the client to send and receive messages from the 
messaging queue. But make sure that the client host and port matches your SQServer.

#### Client Code Sample
1. Import and initiate
```
from stiqueue.sqclient import SQClient
c = SQClient()
```
2. Send a message
```
c.enq("Hello World!")
```
3. Fetch the message
```
hello_msg = c.deq()
```

Note that often the client that is sending the messages is different than the one receiving them.
For example, one client (or app) might be sending the requests and the second client is 
fetching these messages/requests once a resource becomes available.

#### Methods
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
Note that the reason that `decode` is used because the `deq` returns `bytes`. 

#### Server example
In case you want to extend the server code or want to use it, you can use the following code.
```
from stiqueue.sqserver import SQServer

server = SQServer()
server.listen()
```
Note that in most cases you do not want to call the server from your code. You can just run the 
server script as explained in the guide.

### Extend
In most cases, you won't need to extend any of the classes, but in case you want to do so,
we provide two samples extending stiqueue with more functionality (optional). [examples](https://github.com/ahmad88me/stiqueue/tree/main/example)


## Run tests
```python -m unittest discover```




