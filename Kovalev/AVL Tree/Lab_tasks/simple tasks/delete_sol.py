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

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def update_height(self, root):
        if root is not None:
            root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

    def rotate_left(self, root):
        new_root = root.right
        root.right = new_root.left
        new_root.left = root
        self.update_height(root)
        self.update_height(new_root)
        return new_root

    def rotate_right(self, root):
        new_root = root.left
        root.left = new_root.right
        new_root.right = root
        self.update_height(root)
        self.update_height(new_root)
        return new_root

    def min_value(self, root):
        if root is None or root.left is None:
            return root
        return self.min_value(root.left)

    def check_balance(self, root):
        if root is None:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def get_balance(self, root):
        balance = self.check_balance(root)

        if balance > 1 and self.check_balance(root.left) >= 0:
            return self.rotate_right(root)
        if balance < -1 and self.check_balance(root.right) <= 0:
            return self.rotate_left(root)
        if balance > 1 and self.check_balance(root.left) < 0:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and self.check_balance(root.right) > 0:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)

        return root

    def delete(self, root, value):
        if not root:
            return root
        elif value < root.value:
            root.left = self.delete(root.left, value)
        elif value > root.value:
            root.right = self.delete(root.right, value)
        else:
            if root.left is None:
                tmp = root.right
                root = None
                return tmp
            elif root.right is None:
                tmp = root.left
                root = None
                return tmp
            tmp = self.min_value(root.right)
            root.value = tmp.value
            root.right = self.delete(root.right, tmp.value)
        if root is None:
            return root
        self.update_height(root)

        return self.get_balance(root)
