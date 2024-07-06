# Поиск узла в АВЛ-дереве
Дано АВЛ-дерево. Реализуйте метод **search**, который удаляет узел с заданным значением.
Сигнатура функции на python:
```py
def search(self, root, value)
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
Пример использования функции **search**
```py
tree = avl_tree()
root = None
tree.search(root, 5)
```