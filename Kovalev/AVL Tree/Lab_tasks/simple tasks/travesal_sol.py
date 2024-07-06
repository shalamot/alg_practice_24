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

    def pre_order(self, root, result=None):
        if result is None:
            result = []
        if root:
            result.append(root.value)
            self.pre_order(root.left, result)
            self.pre_order(root.right, result)
        return result

    def in_order(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.in_order(root.left, result)
            result.append(root.value)
            self.in_order(root.right, result)
        return result

    def post_order(self, root, result=None):
        if result is None:
            result = []
        if root:
            self.post_order(root.left, result)
            self.post_order(root.right, result)
            result.append(root.value)
        return result