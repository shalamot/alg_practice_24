# Поддержка дублирующихся элементов в АВЛ-дереве
Дано АВЛ-дерево. Необходимо реализовать поддержку дублирующихся элементов. Для этого необходимо переписать имеющиеся методы вставки и удаления.(класс **tree_node** изменен)
Определение классов **tree_node** и **avl_tree**:
```py
class tree_node(object):  
    def __init__(self, value, left=None, right=None):  
        self.value = value  
		self.left = left  
		self.right = right  
		self.height = 1 
        self.count = 1 
  
  
class avl_tree(object):  
  
    def __init__(self):  
        self.root = None  
		self.height = -1  
		self.balance = 0
```