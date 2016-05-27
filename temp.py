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

    @staticmethod
    def rotate_left(node):
        """Делает левый поворот
        """
        new_node = Node(node.value)
        node.value = node.right.value
        left_subtree = node.left
        central_subtree = node.right.left
        node.right = node.right.right
        node.left = new_node
        new_node.right = central_subtree
        new_node.left = left_subtree

    @staticmethod
    def rotate_right(node):
        """Делает правый поворот
        """
        new_node = Node(node.value)
        node.value = node.left.value
        right_subtree = node.right
        central_subtree = node.left.right
        node.left = node.left.left
        node.right = new_node
        new_node.left = central_subtree
        new_node.right = right_subtree

    @staticmethod
    def min_node(node):
        """Ищет ноду с минимальным значением
        :type node: Node
        """
        while node.left is not None:
            node = node.left
        return node

    @staticmethod
    def max_node(node):
        """Ищет ноду с максимальным значением
        :type node: Node
        """
        while node.right is not None:
            node = node.right
        return node

    @staticmethod
    def height(node):
        """
        Ищет максимальную высоту дерева
        :type node: Node
        """
        if node is None:
            return 0
        return max(Tree.height(node.left), Tree.height(node.right)) + 1

    def __str__(self):
        return 'Tree of height %s' % Tree.height(self.root)


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
tree.rotate_left(tree.root)
tree.rotate_right(tree.root)
print(tree.min_node(tree.root))
print(tree.max_node(tree.root))
print(tree)
