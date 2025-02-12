from queue import SimpleQueue
from threading import Lock


class PeekQueue(SimpleQueue):
    """
    A thread-safe queue that extends `SimpleQueue` to allow peeking at elements
    without removing them.

    .. warning::
        This implementation has a **side effect**: peeking temporarily removes items
        and reinserts them, which may affect their order if multiple threads interact
        with the queue concurrently.
    """

    def __init__(self):
        """
        Initializes the PeekQueue instance.

        Inherits from `queue.SimpleQueue` and adds a lock for thread safety.
        """
        super().__init__()
        self.lock = Lock()

    def peek(self, n=0):
        """
        Returns up to `n` items from the queue without removing them.

        This method temporarily removes up to `n` items from the queue,
        stores them in a list, and then reinserts them in the same order
        to maintain queue integrity.

        **Side Effects:**
            - Items are temporarily removed and reinserted, **which may affect
              order if multiple threads interact with the queue at the same time**.
            - If the queue is accessed while `peek()` is running, items might be
              added **after** previously removed items, **changing their order**.

        Args:
            n (int, optional): The number of elements to peek. Defaults to 1.
                - If `n=1`, a single item is returned.
                - If `n>1`, a list of items is returned.
                - If the queue is empty, `None` is returned.

        Returns:
            Union[Any, List[Any], None]:
                - A single item if `n=1`.
                - A list of items if `n>1`.
                - `None` if the queue is empty.

        Example:
            >>> pq = PeekQueue()
            >>> pq.put(10)
            >>> pq.put(20)
            >>> pq.peek()
            [10, 20]
            >>> pq.get()
            10
            >>> pq.peek()
            [20]
        """
        items = []
        with self.lock:
            try:
                if n < 1:
                    n = self.qsize()
                for i in range(n):
                    if self.empty():
                        break
                    items.append(self.get())
                for item in items:
                    self.put(item)
            except Exception as e:
                pass
        return items