<!--![stiqueue](stiqueue.png)-->
![stiqueue](https://github.com/ahmad88me/stiqueue/raw/main/stiqueue.png)

[![Build Status](https://ahmad88me.semaphoreci.com/badges/stiqueue/branches/main.svg)](https://ahmad88me.semaphoreci.com/projects/stiqueue)
[![codecov](https://codecov.io/gh/ahmad88me/stiqueue/branch/main/graph/badge.svg?token=mfqJCVLNXc)](https://codecov.io/gh/ahmad88me/stiqueue)


# stiqueue
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
msg = c.deq()
print("msg1: ")
print(msg)
msg = c.deq()
print("msg2: ")
print(msg)
msg = c.deq()
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
python -m stiqueue.sqserver 0.0.0.0 1234
```
You can also change the port to any of your choice.
The default one used in Docker is `27017`. You can also 
extend the server and add additional methods to meet your needs.

### Client
Most probably you want to extend the class `SQClient`, located in `stiqueue/sqclient.py`.
You can see an example of this in `example.client.py`.


# Development
## Run coverage
```sh run_coverage.sh```

## Run tests
```sh run_tests.sh```
*Note: Rerunning the tests again (within a few seconds from the previous test) have 3% probability of failing as the
operating system might need a few seconds to release the port of the stiqueue server. You can wait a few seconds after
the test if you want to ensure that the tests won't fail due to unreleased port*


## Run Docker
Example of running the server from Docker
```docker container run --interactive -p "1234:1234" --tty --rm --name stiqueue ahmad88me/stiqueue```


# Update Docker
For example, to update docker image with version `v1.0`
`sh scripts/update_docker_image.sh v1.0`

*Note: the tests will use the default port and would
start and the server automatically, so you don't
need to run it before running the tests. Also note that
after running the tests, the operating system might take
a couple of seconds to release the port.*
