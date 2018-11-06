class RBTNode:
    def __init__(self, key, parent, is_red=False, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
        self.parent = parent

        if is_red:
            self.color = "red"
        else:
            self.color = "black"

    def are_both_children_black(self):
        if self.left != None and self.left.is_red():
            return False
        if self.right != None and self.right.is_red():
            return False
        return True

    def count(self):
        count = 1
        if self.left != None:
            count = count + self.left.count()
        if self.right != None:
            count = count + self.right.count()
        return count

    def get_grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def get_predecessor(self):
        node = self.left
        while node.right is not None:
            node = node.right
        return node

    def get_sibling(self):
        if self.parent is not None:
            if self is self.parent.left:
                return self.parent.right
            return self.parent.left
        return None

    def get_uncle(self):
        grandparent = self.get_grandparent()
        if grandparent is None:
            return None
        if grandparent.left is self.parent:
            return grandparent.right
        return grandparent.left

    def is_black(self):
        return self.color == "black"

    def is_red(self):
        return self.color == "red"

    def replace_child(self, current_child, new_child):
        if self.left is current_child:
            return self.set_child("left", new_child)
        elif self.right is current_child:
            return self.set_child("right", new_child)
        return False

    def set_child(self, which_child, child):
        if which_child != "left" and which_child != "right":
            return False

        if which_child == "left":
            self.left = child
        else:
            self.right = child

        if child != None:
            child.parent = self

        return True


class RedBlackTree:
    def __init__(self):
        self.root = None

    def __len__(self):
        if self.root is None:
            return 0
        return self.root.count()

    def insert(self, key):
        new_node = RBTNode(key, None, True, None, None)
        self.insert_node(new_node)

    def insert_node(self, node):
        if self.root is None:
            self.root = node
        else:
            current_node = self.root
            while current_node is not None:
                if node.key < current_node.key:
                    if current_node.left is None:
                        current_node.set_child("left", node)
                        break
                    else:
                        current_node = current_node.left
                else:
                    if current_node.right is None:
                        current_node.set_child("right", node)
                        break
                    else:
                        current_node = current_node.right

        node.color = "red"

        # Balance
        self.insertion_balance(node)

    def insertion_balance(self, node):
        if node.parent is None:
            node.color = "black"
            return

        if node.parent.is_black():
            return

        parent = node.parent
        grandparent = node.get_grandparent()
        uncle = node.get_uncle()

        if uncle is not None and uncle.is_red():
            parent.color = uncle.color = "black"
            grandparent.color = "red"
            self.insertion_balance(grandparent)
            return

        if node is parent.right and parent is grandparent.left:
            self.rotate_left(parent)
            node = parent
            parent = node.parent

        elif node is parent.left and parent is grandparent.right:
            self.rotate_right(parent)
            node = parent
            parent = node.parent

        parent.color = "black"
        grandparent.color = "red"

        if node is parent.left:
            self.rotate_right(grandparent)
        else:
            self.rotate_left(grandparent)

    def rotate_left(self, node):
        right_left_child = node.right.left
        if node.parent != None:
            node.parent.replace_child(node, node.right)
        else:
            self.root = node.right
            self.root.parent = None
        node.right.set_child("left", node)
        node.set_child("right", right_left_child)

    def rotate_right(self, node):
        left_right_child = node.left.right
        if node.parent != None:
            node.parent.replace_child(node, node.left)
        else:
            self.root = node.left
            self.root.parent = None
        node.left.set_child("right", node)
        node.set_child("left", left_right_child)

    def _bst_remove(self, key):
        node = self.search(key)
        self._bst_remove_node(node)

    def _bst_remove_node(self, node):
        if node is None:
            return

        if node.left is not None and node.right is not None:
            successor_node = node.right
            while successor_node.left is not None:
                successor_node = successor_node.left

            successor_key = successor_node.key

            self._bst_remove_node(successor_node)

            node.key = successor_key

        elif node is self.root:
            if node.left is not None:
                self.root = node.left
            else:
                self.root = node.right

            if self.root is not None:
                self.root.parent = None

        elif node.left is not None:
            node.parent.replace_child(node, node.left)

        else:
            node.parent.replace_child(node, node.right)

    def is_none_or_black(self, node):
        if node is None:
            return True
        return node.is_black()

    def is_not_none_and_red(self, node):
        if node is None:
            return False
        return node.is_red()


    def search(self, key):
        current_node = self.root
        while current_node is not None:
            if current_node.key == key:
                return True

            elif key < current_node.key:
                current_node = current_node.left

            else:
                current_node = current_node.right

        return False

    def try_case1(self, node):
        if node.is_red() or node.parent is None:
            return True
        return False

    def try_case2(self, node, sibling):
        if sibling.is_red():
            node.parent.color = "red"
            sibling.color = "black"
            if node is node.parent.left:
                self.rotate_left(node.parent)
            else:
                self.rotate_right(node.parent)
            return True
        return False

    def try_case3(self, node, sibling):
        if node.parent.is_black() and sibling.are_both_children_black():
            sibling.color = "red"
            self.prepare_for_removal(node.parent)
            return True
        return False

    def try_case4(self, node, sibling):
        if node.parent.is_red() and sibling.are_both_children_black():
            node.parent.color = "black"
            sibling.color = "red"
            return True
        return False

    def try_case5(self, node, sibling):
        if self.is_not_none_and_red(sibling.left):
            if self.is_none_or_black(sibling.right):
                if node is node.parent.left:
                    sibling.color = "red"
                    sibling.left.color = "black"
                    self.rotate_right(sibling)
                    return True
        return False

    def try_case6(self, node, sibling):
        if self.is_none_or_black(sibling.left):
            if self.is_not_none_and_red(sibling.right):
                if node is node.parent.right:
                    sibling.color = "red"
                    sibling.right.color = "black"
                    self.rotate_left(sibling)
                    return True
        return False