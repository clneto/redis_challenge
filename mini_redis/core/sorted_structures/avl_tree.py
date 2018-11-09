from random import sample

class AVLNode:
    def __init__(self, score, value):
        # data
        self._value = value

        # tree values
        self._score = score # for ordering
        self._height = 0 # leaf

        # childs
        self._left = None
        self._right = None


    # force cache recalculation
    def recalculate_height(self):
        has_left_child = self._left is not None
        has_right_child = self._right is not None
        if not has_left_child and not has_right_child:
            self._height = 0
            return
        max_child_height = max(0 if self._left is None else self._left.height(),
                               0 if self._right is None else self._right.height())
        self._height = max_child_height + 1

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
        return self._height

    def left_child(self):
        return self._left

    def right_child(self):
        return self._right

    def balance(self):
        left_height = 1 + self._left.height() if self._left is not None else 0
        right_height = 1 + self._right.height() if self._right is not None else 0
        return left_height - right_height

class AVLTree:

    def __init__(self, **kwargs):
        self._root = None

    def height(self):
        return 0 if self._root is None else self._root.height()

    def _score_function(self, value):
        return int(value)

    def _insert_parent(self, parent, new_child):
        if parent is None:
            self._root = new_child
        elif parent.score() > new_child.score():
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
        self.rebalance_tree(path, 2)

    def _left_rotation(self, parent, node):
        new_node = node.right_child()
        node.set_right_child(new_node.left_child())
        new_node.set_left_child(node)
        node.recalculate_height()
        new_node.recalculate_height()
        self._insert_parent(parent, new_node)

    def _right_rotation(self, parent, node):
        new_node = node.left_child()
        node.set_left_child(new_node.right_child())
        new_node.set_right_child(node)
        node.recalculate_height()
        new_node.recalculate_height()
        self._insert_parent(parent, new_node)

    def _left_right_roration(self, parent, node):
        self._left_rotation(node, node.left_child())
        self._right_rotation(parent, node)

    def _right_left_roration(self, parent, node):
        self._right_rotation(node, node.right_child())
        self._left_rotation(parent, node)

    def rebalance_tree(self, affected_nodes, start):
        # exclusive for AVL
        # time to balance
        for offset in range(start, len(affected_nodes)+1):
            node = affected_nodes[-offset]
            node.recalculate_height()
            if abs(node.balance()) > 1: # unbalanced

                parent = affected_nodes[-offset-1] if offset < len(affected_nodes) else None
                node_score = node.score()
                child_score = affected_nodes[1-offset].score()
                grand_child_score = affected_nodes[2 - offset].score()

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
        stack = []
        it = self._root
        ans = []
        while len(stack) > 0 or it is not None:
            while it is not None:
                stack.append(it)
                it = it.left_child()
            it = stack.pop()
            if it is not None:
                ans.append(it)
                it = it.right_child()

        return [x.value() for x in ans]

    def print(self):
        print(self._rec_print(self._root))

    def _rec_print(self, node):
        if node is None:
            return "(nil)"
        return "({0}{1}{2})".format(self._rec_print(node.left_child()), node.value(), self._rec_print(node.right_child()))



if __name__ == "__main__":
    tree = AVLTree()
    #values = ["386", "756", "397", "639", "643", "829"]
    # tweeks must be made to support repeated keys
    values = sample([x for x in range(1000)], 16)
    #values = ["293", "293", "293", "292"]
    for value in values:
        tree.add_value(value)
        trav = tree.in_order_traversal_list()
        print(str(len(trav)) + ":" + str(trav) + ":" + str(value))
        tree.print()
    print(tree.height())