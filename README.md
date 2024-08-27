
![stiqueue](https://github.com/ahmad88me/stiqueue/raw/main/stiqueue.png)

# stiqueue

![tests](../../actions/workflows/python-package.yml/badge.svg)
[![docs](../../actions/workflows/sphinx-docs.yml/badge.svg)](https://ahmad88me.github.io/stiqueue/)
[![PyPI version](https://badge.fury.io/py/stiqueue.svg?kill-cache=1)](https://badge.fury.io/py/stiqueue)


StiQueue, which stands for "stick queue," is inspired by the simplicity of a stick figure. Just as a stick figure represents simplicity in design, StiQueue is designed to be a simple, lightweight messaging queue system that is both easy to use and flexible.


## Code Documentation 
For detailed code documentation, visit the [StiQueue Documentation](https://ahmad88me.github.io/stiqueue/).”

## Guide 

### SQServer
You can run the `SQServer` directly without writing any additional code. The server will handle the messaging queue.
Once the code is downloaded, you can start the server as follows: 

```python src/stiqueue/sqserver.py --host 0.0.0.0 --port 1234 --debug```

It is recommended to use the `--debug` flag during the first run to monitor when the server receives a message or
when a message leaves the queue.


#### Usage
The following are the command-line options for running the server:

```
usage: StiQueue Server [-h] [--debug] [--host HOST] [--port PORT] [--buff-size BUFF_SIZE]

A message queue server

options:
  -h, --help                show this help message and exit
  --debug                   Showing debug messages
  --host HOST               The host address of the server
  --port PORT               The port to listen on
  --buff-size BUFF_SIZE     The size of the buffer
```

### SQClient

The `SQClient` is intended for use within your code. Once you install the `stiqueue` package in your Python project,
you can use the client to send and receive messages from the messaging queue. Ensure that the client's host and port
match those of your `SQServer`.

_Note that the `deq` method is blocking, which can save computation power compared 
to the polling method._


#### Client Code Sample
1. Import and initiate the client:
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
hello_msg = c.deq().decode()
```

Often, the client that sends the messages is different from the one receiving them. For instance, one client (or app) 
might send requests, while another client fetches these messages or requests when a resource becomes available. 
It is also helpful to use a Thread Pool, such as [TPool](https://github.com/oeg-upm/TPool), to manage the number
of running threads.


#### Methods

The following methods are supported by `stiqueue`: 
* **`enq`**: Add a message to the queue (enqueue). 
* **`deq`**: Retrieve a message from the queue (dequeue). 
* **`cnt`**: Get the number of items in the queue.

### Examples

#### Client example
The following is a simple example of how to use the `SQClient` to enqueue and dequeue messages from the server:

```python
from stiqueue import SQClient

# Initialize the client
client = SQClient()

# Enqueue messages
client.enq(b"This is message one")
client.enq(b"This is message two")
client.enq(b"This is message three")

# Dequeue and print messages
msg1 = client.deq().decode()
print("msg1:", msg1)

msg2 = client.deq().decode()
print("msg2:", msg2)

msg3 = client.deq().decode()
print("msg3:", msg3)

```

**Note:** The `decode()` method is used because the `deq()` method returns the messages as `bytes`, 
which need to be decoded to a string for readability. 


### Extending StiQueue
While StiQueue is designed to be simple and flexible, you might want to extend its functionality for specific use cases.
We provide examples of how to extend StiQueue with additional features in the 
[examples](https://github.com/ahmad88me/stiqueue/tree/main/example) directory. 

### Running Tests
To run the unit tests for StiQueue, use the following command:

```python -m unittest discover```





