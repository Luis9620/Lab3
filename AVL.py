class Node:
    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def get_balance(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        return left_height - right_height

    def update_height(self):
        left_height = -1
        if self.left is not None:
            left_height = self.left.height

        right_height = -1
        if self.right is not None:
            right_height = self.right.height

        self.height = max(left_height, right_height) + 1

    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child is not None:
            child.parent = self

        self.update_height()
        return True

    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)

        # If neither of the above cases applied, then the new child
        # could not be attached to this node.
        return False


class AVLTree:
    def __init__(self):
        self.root = None

    def rotate_left(self, node):
        right_left_child = node.right.left

        if node.parent is not None:
            node.parent.replace_child(node, node.right)
        else:  # node is root
            self.root = node.right
            self.root.parent = None

        node.right.set_child('left', node)

        node.set_child('right', right_left_child)

        return node.parent

    def rotate_right(self, node):
        left_right_child = node.left.right

        if node.parent is not None:
            node.parent.replace_child(node, node.left)
        else:  # node is root
            self.root = node.left
            self.root.parent = None

        node.left.set_child('right', node)

        node.set_child('left', left_right_child)

        return node.parent

    def rebalance(self, node):

        node.update_height()

        if node.get_balance() == -2:

            if node.right.get_balance() == 1:
                self.rotate_right(node.right)

            return self.rotate_left(node)

        elif node.get_balance() == 2:

            if node.left.get_balance() == -1:
                self.rotate_left(node.left)

            return self.rotate_right(node)

        return node

    def insert(self, node):
        if self.root is None:
            self.root = node
            node.parent = None

        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:

                    if current_node.left is None:
                        current_node.left = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.right = node
                        node.parent = current_node
                        current_node = None
                    else:
                        current_node = current_node.right

            node = node.parent
            while node is not None:
                self.rebalance(node)
                node = node.parent

    def search(self, key):
        current_node = self.root
        while current_node is not None:
            if current_node.key == key:
                return True
            elif current_node.key < key:
                current_node = current_node.right
            else:
                current_node = current_node.left
        return False


