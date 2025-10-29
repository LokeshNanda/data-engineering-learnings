# Dynamic Array Logic Implementation:

The key is to provide means to grows an array A that stores the elements of a list. We can't actually grow the array, its capacity is fixed. If an element is appended to a list at a time, when the underlying array is full, we need to perform following steps.

1. Allocate a new array B with larger capacity (A commonly used rule for the new array is to have twice the capacity of the existing array )
2. Set B[i]=A[i], for i=0 to n-1 where n denotes the current no of items.
3. Set A=B that is, we hence forth use B as the array of supporting list.
4. Insert new element in the new array.

![alt text](image.png)
credits: geeksforgeeks.org


## PREREQUISITES:
```python
# Outbound is exclusive in range
for i in range(5, 10):
    print(i)

# Output - 5,6,7,8,9

for i in range(10, 0, -2):
    print(i)

# Ouptut - 10, 8, 6, 4, 2
```