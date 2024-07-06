Реализуйте метод build_avl_tree, который принимает список чисел и строит сбалансированное бинарное дерево поиска AVL. Метод должен вернуть корень построенного дерева.
Примечание: нельзя использовать метод insert.
Определение классов **tree_node** и **avl_tree**:
```py
class tree_node(object):  
    def __init__(self, value, left=None, right=None):  
        self.value = value  
		self.left = left  
		self.right = right  
		self.height = 1 
  
  
class avl_tree(object):  
  
    def __init__(self):  
        self.root = None  
		self.height = -1  
		self.balance = 0
```