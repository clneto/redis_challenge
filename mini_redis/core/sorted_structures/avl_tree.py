
class AVLNode:
    def __init__(self, score, value):
        # data
        self._value = value

        # tree values
        self._score = score; # for ordering
        self._height = 0

        # childs
        self._left = None
        self._right = None

        # caching height values
        self._height_updated = True

    def _update_height(self):
        has_left_child = self._left is None
        has_right_child = self._right is None
        if not has_left_child and not has_right_child:
            return
        max_child_height = max(0 if self._left is None else self._left.height(),
                               0 if self._right is None else self._right.height())
        self._height = max_child_height + 1
        self._height_updated = True

    def set_left_child(self, left):
        self._left = left
        self._height_updated = False

    def set_right_child(self, right):
        self._right = right
        self._height_updated = False

    def score(self):
        return self._score

    def value(self):
        return self._value

    def height(self):
        if not self._height_updated:
            self._update_height()
        return self._height

    def left_child(self):
        return self._left

    def right_child(self):
        return self._right

    def balance(self):
        left_height = self._left.height() if self._left is not None else 0
        right_height = self._right.height() if self._right is not None else 0
        return abs(left_height - right_height)

class AVLTree:

    def __init__(self, **kwargs):
        self._root = None

    def _score_function(self, value):
        return int(value)

    def _insert_parent(self, parent, new_child):
        if parent is None:
            self._root = new_child
        if parent.score() > new_child.score():
            parent.set_left_child(new_child)
        else:
            parent.set_right_child(new_child)

    def add_value(self, value):
        insert_score = self._score_function(value)
        new_node = AVLNode(insert_score, value)

        # default insertion on BST
        it = self._root
        path = []
        while it is not None:
            path.append(it)
            if it.score() > insert_score:
                it = it.left_child()
            else:
                it = it.right_child()

        insertion_node = path[-1] if len(path) > 0 else None
        self._insert_parent(insertion_node, new_node)
        path.append(new_node)

        # exclusive for AVL
        # time to balance
        for offset in range(2, len(path)+1):
            node = path[-offset]
            if node.balance() > 1: # unbalanced

                parent = path[-offset-1] if offset < len(path) else None
                node_score = node.score()
                child_score = path[1-offset].score()
                grand_child_score = path[2 - offset].score()

                # rotation time
                if node_score > child_score:
                    #a/b/c
                    if child_score > grand_child_score:
                        self._right_rotation(parent, node)
                    #a/b\c
                    else:
                        self._left_right_roration(parent, node)
                else:
                    # a\b/c
                    if child_score > grand_child_score:
                        self._right_left_roration(parent, node)
                    # a\b\c
                    else:
                        self._left_rotation(parent, node)

    def _left_rotation(self, parent, node):
        new_node = node.right
        new_node.set_left_child(node)
        node.set_right_child(None)
        self._insert_parent(parent, new_node)

    def _right_rotation(self, parent, node):
        new_node = node.left
        new_node.set_right_child(node)
        node.set_left_child(None)
        self._insert_parent(parent, new_node)

    def _left_right_roration(self, parent, node):
        self._left_rotation(node, node.left_child())
        self._right_rotation(parent, node)

    def _right_left_roration(self, parent, node):
        self._right_rotation(node, node.right_child())
        self._left_rotation(parent, node)

    def get_value(self, value):
        target_score = self._score_function(value)
        it = self._root
        while it is not None and it.score() != target_score:
            if it.score() > target_score:
                it = it.left_child()
            else:
                it = it.right_child()
        return it.value() if it is not None else None


    def remove_value(self, value):
        pass

    def get_range(self, lower_bound, upper_bound):
        pass

    def in_order_traversal_list(self):
        traverse = []
        traversed = set()
        ans = []

        def node_traverse(node):
            if node is not None:
                if node not in traversed:
                    traverse.append(node)
                    traversed.add(node)
                else:
                    ans.append(node.value())

        if self._root is not None:
            traverse = [self._root]

        while len(traverse) != 0:
            it = traverse.pop()
            node_traverse(it.right_child())
            node_traverse(it)
            node_traverse(it.left_child())

        return ans