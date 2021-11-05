<!--![stiqueue](stiqueue.png)-->
![stiqueue](https://github.com/ahmad88me/stiqueue/raw/main/stiqueue.png)

[![Build Status](https://ahmad88me.semaphoreci.com/badges/stiqueue/branches/main.svg)](https://ahmad88me.semaphoreci.com/projects/stiqueue)
[![codecov](https://codecov.io/gh/ahmad88me/stiqueue/branch/main/graph/badge.svg?token=mfqJCVLNXc)](https://codecov.io/gh/ahmad88me/stiqueue)


# stiqueue
Stands for stick queue which is a simple messaging queue

## Usage 

### Methods
The followings are a set of methods supported by stiqueue
* **enq**: to add to the queue (enqueue).
* **deq**: to get a value from the queue (dequeue).
* **cnt**: number of items in the queue.


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
