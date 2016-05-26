# encoding: utf-8


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def __str__(self):
        return "[%s]" % self.value


class Tree:
    def __init__(self):
        self.root = None

    def add(self, value):
        """Добавляет элементы в дерево"""
        if self.root is None:
            self.root = Node(value)
            return
        checker(value, self.root)


def checker(value, root):
    if root.value == value:
        return
    elif root.value < value:
        if root.right is None:
            root.right = Node(value)
        elif root.right:
            checker(value, root.right)
        return
    elif value < root.value:
        if root.left is None:
            root.left = Node(value)
        elif root.left:
            checker(value, root.left)
        return


tree = Tree()
print(tree)
tree.add(5)
print(tree)
tree.add(2)
print(tree)
tree.add(7)
print(tree)
tree.add(3)
tree.add(4.5)
tree.add(4.6)
tree.add(4.7)
print(tree)
