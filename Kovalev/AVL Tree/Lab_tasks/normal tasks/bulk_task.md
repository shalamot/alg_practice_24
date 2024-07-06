# Массовая вставка и удаление из АВЛ-дерева
Дано АВЛ-дерево. Реализуйте методы **bulk_insert** и **bulk_delete**, который вставляют/удалают несколько значений из дерева.
Сигнатуры функций:
```py
def bulk_insert(self, root, values)

def bulk_delete(self, root, values)
```
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
