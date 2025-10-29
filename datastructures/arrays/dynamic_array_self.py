import ctypes

class DynamicArray(object):
    def __init__(self):
        self.n = 0
        self.capacity = 1
        self.A = self.create_array(self.capacity)
    
    def __len__(self):
        return self.n
    
    def __getitem__(self, k):
        if not 0 <= k < self.n:
            return IndexError(f'{k} is Out of bound')
        
        return self.A[k]
        
    def create_array(self, new_cap):
        '''
        code is generating a C-style array of Python objects and 
        then returning an instance of that array.
        '''
        return (new_cap * ctypes.py_object)() 
    
    def append(self, item):
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
        
        self.A[self.n] = item
        self.n += 1
    
    def insertAt(self, item, index):
        print(f'Trying to insert {item} value to index {index} and current size is {self.n}')
        if index < 0 or index >= self.n:
            print('Please add proper index to insert')
            
        if self.n == self.capacity:
            self._resize(2 * self.capacity)
            
        for i in range(self.n-1, index-1, -1):
            self.A[i+1] = self.A[i]
            
        self.A[index] = item
        self.n += 1
    
    def delete(self):
        if self.n == 0:
            print('Nothing to delete, array is empty')
        
        self.A[self.n-1] = 0
        self.n -= 1
    
    def removeAt(self, index):
        if self.n == 0:
            print('Nothing to delete, array is empty')
        
        if index < 0 or index >= self.n:
            return IndexError("Array index is out of bound")
        
        if index == self.n-1:
            self.A[index] = 0
            self.n -= 1
            return
        
        for i in range(index, self.n-1):
            self.A[i] = self.A[i+1]
        
        self.A[self.n-1] = 0
        self.n -= 1
    
    def _resize(self, new_cap):
        B = self.create_array(new_cap)
        for k in range(self.n):
            B[k] = self.A[k]
        
        self.A = B
        self.capacity = new_cap
    
arr = DynamicArray()
# print(len(arr))
# print(arr[1])
arr.append(4)
arr.append(10)
arr.append(6)
# print(arr[0])
# print(len(arr))
# print(arr[1])
arr.insertAt(11,1)
arr.removeAt(1)
print(arr[0], arr[1], arr[2])