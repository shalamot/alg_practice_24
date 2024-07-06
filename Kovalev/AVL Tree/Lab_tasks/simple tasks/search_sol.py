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

    def search(self, root, value):
        if root is None:
            return False
        elif root.value == value:
            return True
        elif value < root.value:
            return self.search(root.left, value)
        else:
            return self.search(root.right, value)