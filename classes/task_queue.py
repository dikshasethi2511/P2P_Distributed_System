# The Master Node maintains a task queue. The task queue is a list of tasks that the Master Node wants to initiate.
class TaskQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, task):
        # Add a task to the queue.
        self.queue.append(task)

    def dequeue(self):
        # Remove and return the task from the front of the queue.
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            return None

    def is_empty(self):
        # Check if the queue is empty.
        return len(self.queue) == 0

    def size(self):
        # Return the size of the queue.
        return len(self.queue)
