class Node():
    def __init__(self, value):
        self.data = value
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None #Empty Linkedlist
        self.n = 0 #No of Nodes
            
    def __len__(self):
        '''
        Find length of the linked list
        '''
        return self.n
    
    def insert_head(self, new_value):
        '''
        Insert from head
        '''
        new_node = Node(new_value) # new node creation
        new_node.next = self.head # create connection
        
        self.head = new_node # Reassign Head
        self.n += 1
        
    def append(self, new_value):
        # Can't go directly to tail, need to start from head and traverse
        new_node = Node(new_value)
        
        if self.head == None:
            self.head = new_node
            self.n += 1
            return
        
        curr = self.head
        while curr.next != None:
            curr = curr.next
            
            # we are at last node
        curr.next = new_node
        self.n += 1
        
    def insert_after(self, after, value):
        # To-do
        pass
        
    def __str__(self):
        result = ''
        curr = self.head
        while curr != None:
            result += str(curr.data) + '->'
            curr = curr.next
        return result[0:-2]
            
    
L = LinkedList()
L.insert_head(1)
L.insert_head(2)
L.insert_head(3)
L.insert_head(4)
print(len(L))
print(L)
L.append(5)
print(L)
