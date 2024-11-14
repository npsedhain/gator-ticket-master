

class HeapNode:
    def __init__(self, priority, user_id, timestamp):
        self.priority = priority
        self.user_id = user_id
        self.timestamp = timestamp


class BinaryMinHeap:
    def __init__(self):
        self.heap = []
        self.position = {}  # To track positions of users in heap

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i].user_id] = i
        self.position[self.heap[j].user_id] = j

    def heapify_up(self, i):
        while i > 0:
            parent = self.parent(i)
            if (self.heap[i].priority > self.heap[parent].priority or
               (self.heap[i].priority == self.heap[parent].priority and
                    self.heap[i].timestamp < self.heap[parent].timestamp)):
                self.swap(i, parent)
                i = parent
            else:
                break

    def heapify_down(self, i):
        min_index = i
        size = len(self.heap)

        while True:
            left = self.left_child(i)
            right = self.right_child(i)

            if left < size and (
                self.heap[left].priority > self.heap[min_index].priority or
                (self.heap[left].priority == self.heap[min_index].priority and
                 self.heap[left].timestamp < self.heap[min_index].timestamp)
            ):
                min_index = left

            if right < size and (
                self.heap[right].priority > self.heap[min_index].priority or
                (self.heap[right].priority == self.heap[min_index].priority and
                 self.heap[right].timestamp < self.heap[min_index].timestamp)
            ):
                min_index = right

            if min_index != i:
                self.swap(i, min_index)
                i = min_index
            else:
                break

    def insert(self, priority, user_id, timestamp):
        node = HeapNode(priority, user_id, timestamp)
        self.heap.append(node)
        index = len(self.heap) - 1
        self.position[user_id] = index
        self.heapify_up(index)

    def extract_max(self):
        if not self.heap:
            return None

        max_node = self.heap[0]
        last_node = self.heap.pop()

        if self.heap:
            self.heap[0] = last_node
            self.position[last_node.user_id] = 0
            self.heapify_down(0)

        del self.position[max_node.user_id]
        return max_node

    def update_priority(self, user_id, new_priority):
        if user_id not in self.position:
            return False

        index = self.position[user_id]
        old_priority = self.heap[index].priority
        self.heap[index].priority = new_priority

        if new_priority > old_priority:
            self.heapify_up(index)
        else:
            self.heapify_down(index)
        return True

    def remove(self, user_id):
        if user_id not in self.position:
            return False

        index = self.position[user_id]
        self.heap[index] = self.heap[-1]
        self.position[self.heap[-1].user_id] = index
        self.heap.pop()

        if index < len(self.heap):
            self.heapify_down(index)
            self.heapify_up(index)

        del self.position[user_id]
        return True

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)

    def contains(self, user_id):
        return user_id in self.position
