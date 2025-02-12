import unittest
from queue import Empty
from threading import Thread
from time import sleep
from stiqueue.peekqueue import PeekQueue


class TestPeekQueue(unittest.TestCase):

    def test_peek_single_item(self):
        """Test peeking at a single item."""
        queue = PeekQueue()
        queue.put(42)
        self.assertEqual(queue.peek(), [42])
        self.assertEqual(queue.get(), 42)  # Ensure the item is still there

    def test_peek_multiple_items(self):
        """Test peeking multiple items."""
        queue = PeekQueue()
        queue.put(1)
        queue.put(2)
        queue.put(3)
        self.assertEqual(queue.peek(3), [1, 2, 3])  # Peek first 2 items
        self.assertEqual(queue.get(), 1)  # Ensure order is preserved
        self.assertEqual(queue.peek(), [2, 3])  # Next item should still be 2

    def test_peek_more_than_available(self):
        """Test peeking more items than available in the queue."""
        queue = PeekQueue()
        queue.put(10)
        queue.put(20)
        self.assertEqual(queue.peek(5), [10, 20])  # Peek more than present
        self.assertEqual(queue.get(), 10)
        self.assertEqual(queue.get(), 20)
        self.assertTrue(queue.empty())  # Queue should be empty now

    def test_peek_empty_queue(self):
        """Test peeking on an empty queue."""
        queue = PeekQueue()
        self.assertEqual(queue.peek(3), [])  # Should return empty list

    def test_queue_order_after_peek(self):
        """Ensure the queue maintains order after peeking."""
        queue = PeekQueue()
        queue.put("A")
        queue.put("B")
        queue.put("C")
        queue.peek(2)  # Peek first two items
        items = ["A", "B", "C"]
        self.assertIn(queue.get(), items)
        self.assertIn(queue.get(), items)
        self.assertIn(queue.get(), items)
        self.assertTrue(queue.empty())

    def test_peek_with_multithreading(self):
        queue = PeekQueue()
        """Test peeking in a multithreaded environment."""
        def worker(q: PeekQueue):
            """Worker thread function to insert elements."""
            sleep(0.1)  # Simulate delay
            q.put(100)

        # Start a thread that inserts an item with delay
        t = Thread(target=worker, args=(queue,))
        t.start()

        self.assertEqual(queue.peek(), [])  # Should be None (empty queue)
        t.join()  # Wait for thread to finish
        self.assertEqual(queue.peek(), [100])  # Now it should be 100

    def test_peek_does_not_remove_items(self):
        """Ensure that peek() does not remove items from the queue."""
        queue = PeekQueue()
        queue.put(99)
        queue.peek()
        self.assertEqual(queue.get(), 99)  # Item should still be retrievable

    def test_exceptions_on_empty_queue(self):
        queue = PeekQueue()
        """Test behavior when trying to get from an empty queue."""
        with self.assertRaises(Empty):  # Should raise queue.Empty when calling get()
            queue.get_nowait()


if __name__ == "__main__":
    unittest.main()
