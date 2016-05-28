# encoding: utf-8
import time
import pygame
import sys

from render import RenderManager, DebugText
from utils import BLACK, WHITE, Vec2d


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        ":type : Node"
        self.right = None
        ":type : Node"
        self.parent = None
        ":type : Node"

    def set_right(self, node):
        self.right = node
        if node:
            node.parent = self

    def set_left(self, node):
        self.left = node
        if node:
            node.parent = self

    def __str__(self):
        return "[%s]" % self.value


class Tree:
    def __init__(self):
        self.root = None

    def set_root(self, node):
        self.root = node
        if node:
            node.parent = None

    def add(self, value):
        """Добавляет элементы в дерево"""
        if self.root is None:
            self.set_root(Node(value))
            return
        add_in_tree(value, self.root)

    @staticmethod
    def find_node(value, root):
        """
        :type value: float
        :type root: Node
        :return Node
        """
        if root is None:
            return None
        if value == root.value:
            return root
        elif value > root.value:
            return Tree.find_node(value, root.right)
        else:
            return Tree.find_node(value, root.left)

    def delete(self, value):
        node = self.find_node(value, self.root)
        ":type node: Node"
        if node is None:
            return

        if node.parent is None:
            # удаляем корень дерева
            set_node_func = self.set_root
        elif node is node.parent.left:
            # удаляемая вершина - левый ребенок
            set_node_func = node.parent.set_left
        else:
            # удаляемая вершина - правый ребенок
            set_node_func = node.parent.set_right

        if node.left is None:
            if node.right is None:
                set_node_func(None)
            else:
                set_node_func(node.right)
        else:
            if node.right is None:
                set_node_func(node.left)
            else:
                new_node_value = Tree.min_node(node.right).value
                self.delete(new_node_value)
                node.value = new_node_value

    @staticmethod
    def rotate_left(node):
        """Делает левый поворот
        """
        new_node = Node(node.value)
        node.value = node.right.value

        left_subtree = node.left
        central_subtree = node.right.left
        right_subtree = node.right.right

        node.set_right(right_subtree)
        node.set_left(new_node)

        new_node.set_right(central_subtree)
        new_node.set_left(left_subtree)

    @staticmethod
    def rotate_right(node):
        """Делает правый поворот
        """
        new_node = Node(node.value)
        node.value = node.left.value

        left_subtree = node.left.left
        central_subtree = node.left.right
        right_subtree = node.right

        node.set_left(left_subtree)
        node.set_right(new_node)

        new_node.set_left(central_subtree)
        new_node.set_right(right_subtree)

    @staticmethod
    def min_node(node):
        """Ищет ноду с минимальным значением
        :type node: Node
        """
        while node.left:
            node = node.left
        return node

    @staticmethod
    def max_node(node):
        """Ищет ноду с максимальным значением
        :type node: Node
        """
        while node.right:
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

    def render(self, screen):
        """
        :type screen: screen.Screen
        """
        w, h = screen.get_size()
        draw_subtree(self.root, 0, 0, w, h, Tree.height(self.root), screen)


def add_in_tree(value, root):
    """
    :type root: Node
    """
    if root.value == value:
        return
    elif root.value < value:
        if root.right is None:
            root.set_right(Node(value))
        elif root.right:
            add_in_tree(value, root.right)
        return
    elif value < root.value:
        if root.left is None:
            root.set_left(Node(value))
        elif root.left:
            add_in_tree(value, root.left)
        return


class GeneratorStepper:
    def __init__(self, generator_func):
        self.generator = generator_func()

    def step(self):
        if not self.generator:
            return False
        try:
            self.generator.send(None)
            return True
        except StopIteration:
            self.generator = None
            return False


tree = Tree()


def tree_progress():
    yield tree.add(1)
    yield tree.delete(1)
    yield tree.add(1)
    yield tree.add(0)
    yield tree.delete(0)
    yield tree.add(2)
    yield tree.add(1.5)
    yield tree.delete(1)
    yield tree.add(3)
    yield tree.add(1)
    yield tree.add(1.2)
    yield tree.add(2.3)
    yield tree.add(2.2)
    yield tree.add(2.1)
    yield tree.add(4)
    yield tree.delete(3)
    yield tree.add(4)
    yield tree.add(5)
    yield tree.add(6)
    yield tree.add(7)
    yield tree.delete(2)
    yield exit()

stepper = GeneratorStepper(tree_progress)


def global2local(x, y, w, h):
    x += PADDING * w
    y += PADDING * h
    h /= 2
    w /= 2
    return x, y, w, h


def draw_subtree(node, x, y, w, h, l, screen):
    """Рисует дерево
    :type screen: screen.Screen
    :type node: Node
    """
    if node is None:
        return
    level_h = h / l
    draw_subtree(node.left, x, y + level_h, w / 2, h - level_h, l - 1, screen)
    draw_subtree(node.right, x + w / 2, y + level_h, w / 2, h - level_h, l - 1, screen)
    rect = global2local(x, y, w, level_h)
    screen.draw_frame(WHITE, *rect)
    screen.draw_text(str(node.value), screen.get_font('Arial', 20), WHITE, *rect)
    x, y, w, h = rect
    if node.left is not None:
        screen.draw_arrow(WHITE, Vec2d(x + w / 4, y + h), Vec2d(x, y + 2*h))
    if node.right is not None:
        screen.draw_arrow(WHITE, Vec2d(x + 3 * w / 4, y + h), Vec2d(x + w, y + 2 * h))


def handle_input():
    """Обработка input от игрока
    """
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # клавиатура
            print('event', event)
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                stepper.step()


def process_game(elapsed):
    pass


pygame.init()

WINDOW_SIZE = (1280, 720)  # размер окна в пикселах
WINDOW_BG_COLOR = BLACK  # цвет окна

render_manager = RenderManager(WINDOW_SIZE, WINDOW_BG_COLOR)

PADDING = 1/4

MAX_FPS = 50
clock = pygame.time.Clock()
clock.tick()

debug_text = DebugText()

render_manager.add_drawables(tree)
render_manager.add_drawables(debug_text)

# игровой цикл
while True:
    elapsed = clock.tick(MAX_FPS)

    frame_start = time.time()

    handle_input()
    process_game(elapsed / 1000)
    render_manager.render()

    frame_time = (time.time() - frame_start) * 1000
    debug_text.add_line('frame time %.2f ms' % frame_time)
