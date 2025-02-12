
![tests](../../actions/workflows/python-package.yml/badge.svg)
[![docs](../../actions/workflows/sphinx-docs.yml/badge.svg)](https://ahmad88me.github.io/stiqueue/)
[![PyPI version](https://badge.fury.io/py/stiqueue.svg?kill-cache=1)](https://badge.fury.io/py/stiqueue)


<img src="https://github.com/ahmad88me/stiqueue/raw/main/stiqueue.svg" width="200">


StiQueue, short for "stick queue," is inspired by the simplicity of a stick figure.
Just as a stick figure represents minimalism and clarity, StiQueue is a lightweight messaging queue system
designed to be simple, flexible, and easy to use.


## Documentation 
Explore the full [StiQueue Documentation](https://ahmad88me.github.io/stiqueue/) for in-depth code references and usage guides.


## Getting Started 

### SQServer
`SQServer` is the core of StiQueue and manages the messaging queue. It can be run directly with minimal setup.

#### Running the Server

Once the code is downloaded, you can start the server with:

```python src/stiqueue/sqserver.py --host 0.0.0.0 --port 1234 --debug```

The `--debug` flag is useful during the first run to monitor incoming and outgoing messages.



#### Server Options
Below are the available command-line options for the server:

```
usage: StiQueue Server [-h] [--debug] [--host HOST] [--port PORT] [--buff-size BUFF_SIZE]

A message queue server

options:
  -h, --help                show this help message and exit
  --debug                   Showing debug messages
  --host HOST               The host address of the server
  --port PORT               The port to listen on
  --buff-size BUFF_SIZE     The size of the buffer
  --log LOG                 The log file

```

### SQClient

The `SQClient` allows you to interact with the server to enqueue (send) and dequeue (receive) messages. 
Ensure the host and port of the client match the server configuration.

**Blocking Dequeue**: The deq method is blocking, which is more resource-efficient than polling.

#### Quick Start
1. Initialize the Client:
```python
from stiqueue import SQClient
client = SQClient()
```
2. Enqueue a Message:
```python
client.enq("Hello, World!")
```
3. Dequeue a Message:
```python
msg = client.deq().decode()
print("Received:", msg)
```

Often, the client that sends the messages is different from the one receiving them. For instance, one client (or app) 
might send requests, while another client fetches these messages or requests when a resource becomes available. 
It is also helpful to use a Thread Pool, such as [TPool](https://github.com/oeg-upm/TPool), to manage the number
of running threads.


#### Methods

The following methods are supported by `stiqueue`:
* `enq(msg: bytes)`: Adds a message to the queue. 
* `deq() -> bytes`: Retrieves the next message from the queue (blocking call). 
* `cnt() -> int`: Returns the number of messages currently in the queue. 
* `ack()`: Acknowledges a message when `ack_required=True`. If not acknowledged within `ack_timeout`, 
the server re-enqueues the message.
* `peek(n: int = 0, sep: str = ",") -> bytes`: Retrieves up to `n` messages from the queue **without removing them**.
  - If `n=0`, returns **all available messages**.
  - Otherwise, returns up to `n` messages, separated by `sep`.
  - If the queue is empty, returns an empty byte string (`b""`).

> **Note**: When `ack_required=True` and the client process crashes after calling `deq`, messages are automatically 
re-queued to ensure they are not lost.




### Examples

#### Basic Client Usage
The following is a simple example of how to use the `SQClient` to enqueue and dequeue messages from the server:

```python
from stiqueue import SQClient

# Initialize the client
client = SQClient()

# Enqueue messages
client.enq(b"First message")
client.enq(b"Second message")

# Dequeue and process messages
print(client.deq().decode())  # Output: First message
print(client.deq().decode())  # Output: Second message

```

**Note:** The `decode()` method is used because the `deq()` method returns the messages as `bytes`, 
which need to be decoded to a string for readability. 


##### Using a Thread Pool 
You can integrate a thread pool, such as [TPool](https://github.com/oeg-upm/TPool), for managing concurrent client operations.


### Extending StiQueue

StiQueue is designed to be flexible and extensible. You can add custom functionality to the server or client as needed. 
Examples of extending StiQueue are available in the
[examples](https://github.com/ahmad88me/stiqueue/tree/main/example) directory.


### Testing

Run the unit tests to ensure everything is working as expected.

```python -m unittest discover```

### Run a Specific Test
Replace `<test_file_name>` with the desired test file:

```
python -m unittest tests.<test_file_name>
```



## Key Highlights
* **Lightweight and Flexible**: Minimal dependencies and easy to integrate. 
* **Blocking Dequeue**: Efficient for resource-limited systems. 
* **Reliable Messaging**: Optional message acknowledgments to ensure no data loss. 
 
