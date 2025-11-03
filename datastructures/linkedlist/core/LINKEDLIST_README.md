# Linked Lists

## Why Use a Linked List?

A **Linked List** is a fundamental data structure where elements are stored in **nodes**, and each node contains the data plus a **pointer** (or link) to the next node in the sequence. Unlike an Array, elements are not stored at contiguous memory locations.

The primary benefits of a Linked List are:

| Benefit | Description |
| :--- | :--- |
| **Dynamic Size** | Linked Lists can grow or shrink in size **dynamically** at runtime. You don't need to specify their capacity beforehand. |
| **Ease of Insertion/Deletion** | Inserting or deleting an element is **very efficient** (constant time, $O(1)$) once you have a pointer to the previous node. This avoids shifting all subsequent elements. |


## Why Not Just Use Arrays? (Where Linked Lists Shine)

Arrays are stored in a contiguous block of memory. This allows for **fast random access** (you can access any element instantly by its index, $O(1)$).

However, Arrays suffer in the following scenarios, which are exactly where Linked Lists excel:

### Scenario 1: Frequent Insertions and Deletions

Imagine you have a list of tasks that you constantly add, complete, and remove in the middle of the list.

| Action | Array ($O(N)$) | Linked List ($O(1)$) |
| :--- | :--- | :--- |
| **Insert** (in the middle) | Requires shifting all subsequent elements. **Slow.** | Only requires changing a few pointers. **Fast.** |
| **Delete** (in the middle) | Requires shifting all subsequent elements to close the gap. **Slow.** | Only requires changing a few pointers. **Fast.** |

#### **Simple Example: The Movie Theater Seating**
The Array Scenario (The Empty Theater): The teacher reserves seats in a single, contiguous block (like Row 5, Seats 1-10). The students sit right next to each other.

Pro: If the teacher needs to quickly find the 5th student, they know exactly where they are (Seat 5). Fast access.

Con (Insertion/Deletion Pain): If a new student arrives, or one needs to leave, and the seats must remain together, all students after that spot must shift to the next seat to make room or close the gap. This "shifting" is computationally expensive.

The Linked List Scenario (The Full Theater): The theater is packed, so the students are seated wherever an empty seat can be found (scattered throughout the room). To keep track, the teacher tells the first student, "When it's time to go, ask the next student where they're sitting." The first student always holds the "link" to the second student, and so on.

Pro (Insertion/Deletion Ease): If a new student arrives, the teacher just finds an empty spot (a new node) and tells the last student in the group, "Now point to this new student." No one else has to move their seat! Instantaneous insertion.

Con (Access Pain): To find the 5th student, the teacher must start at the first student and follow the links one by one. Slow access.

### Scenario 2: Implementing Other Data Structures

Linked Lists are the foundational structure for building more complex data types where sequential access is common:

  * **Stacks:** Linked Lists (especially Singly Linked Lists) are excellent for implementing a **Stack** (Last-In, First-Out or LIFO), as both push (insert at the beginning) and pop (delete at the beginning) operations are $O(1)$.
  * **Queues:** **Doubly Linked Lists** are the most common and efficient way to implement a **Queue** (First-In, First-Out or FIFO), as inserting at the end and deleting from the beginning are both $O(1)$.

#### **Simple Example: Browser History**

A **Doubly Linked List** is perfect for managing a user's browser history.

  * You can easily go **"Back"** (traverse to the previous node).
  * You can easily go **"Forward"** (traverse to the next node).
  * If you visit a new page, it's quickly **inserted** at the end.


## Simple Python Code Illustration

The core difference is *how* the data is connected:

### Array (Python `list`)

```python
# Array (Python List)
my_list = ['A', 'B', 'C', 'D']

# Insert 'X' at index 1
# Python's list 'insert' is O(N) because 'B', 'C', and 'D' must be shifted.
my_list.insert(1, 'X') 
print(my_list) # Output: ['A', 'X', 'B', 'C', 'D']
```

### Linked List (Conceptual Structure)

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None # Pointer to the next node

# Conceptual Linked List Setup: A -> B -> D
node_A = Node('A')
node_B = Node('B')
node_D = Node('D')

node_A.next = node_B # A points to B
node_B.next = node_D # B points to D

# --- Action: Insert 'C' between B and D (O(1) operation) ---

node_C = Node('C')

# 1. B now points to C
node_B.next = node_C 
# 2. C now points to D (the old B.next)
node_C.next = node_D

# New Sequence: A -> B -> C -> D. No data was shifted!
```


## 🛑 Trade-offs (When to use an Array)

A Linked List's biggest drawback is **slow access time** ($O(N)$). To find the $i$-th element, you must start from the head and follow $i$ links.

**You should use an Array (Python `list`) when:**

1.  You need **fast random access** (e.g., "get the element at index 5").
2.  The size of the data structure is **mostly static** or changes very rarely.
3.  You have sufficient **contiguous memory** available.