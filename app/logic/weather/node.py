
# The Node class represents a single node in the B+ tree, containing keys and children.
class Node:
    def __init__(self):
        # self.order = order  # Order of the B+ tree
        self.keys = []  # List of keys in the node
        # Dict of keys values will be a list of days corresponding to specific key # , only filled if node is a leaf
        self.values = {}
        self.children = []  # List of child nodes
        self.next = None    # Pointer to next leaf node
        self.prev = None    # Pointer to prev lead node

    # def insert(self, key) -> None:
    #     self.keys.append(key)
    #     self.keys.sort(key=lambda x: x[0])

    # Returns True if the node is a leaf, otherwise False

    def is_leaf(self):
        return len(self.children) == 0
