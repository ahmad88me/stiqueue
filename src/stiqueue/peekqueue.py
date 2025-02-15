import queue
import copy


class PeekQueue(queue.Queue):
    """
    A thread-safe queue that extends `Queue` to allow peeking at elements
    without removing them.

    .. warning::
        This implementation provides a non-intrusive `peek` method, but
        **it still creates a deep copy of the internal queue**. This operation
        may be expensive for large queues.
    """

    def peek(self, n=0):
        """
        Returns up to `n` items from the queue **without removing them**.

        Unlike previous implementations, this method **creates a deep copy** of
        the queue's internal `deque`, ensuring that the original queue remains
        unmodified.

        .. note::
            - This method **does not** affect the order of items in the queue.
            - If `n=0`, it returns **all** available elements.
            - If `n > queue size`, it returns all elements.

        Args:
            n (int, optional): The number of elements to peek. Defaults to `0` (all items).

        Returns:
            List[Any]: A list containing up to `n` items from the queue.

        Example:
            >>> pq = PeekQueue()
            >>> pq.put(10)
            >>> pq.put(20)
            >>> pq.peek(1)
            [10]
            >>> pq.peek()
            [10, 20]
            >>> pq.get()
            10
            >>> pq.peek()
            [20]
        """
        copied_queue = copy.deepcopy(self.queue)
        qsize = len(copied_queue)
        if n < 1:
            n = qsize
        else:
            n = min(n, qsize)
        items = []
        for _ in range(n):
            items.append(copied_queue.popleft())
        return items
