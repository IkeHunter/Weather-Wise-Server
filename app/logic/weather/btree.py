from node import Node

# TODO: Test Insert Function


class BPlusTree:
    # Constructor for B+ Tree
    def __init__(self, order: int, days=[]) -> None:
        self.order = order
        self.root = Node()
        for day in days:
            self.insert(day['data'][0]['temp'], day)

    # Insert a key, value pair into the B+ Tree
    def insert(self, key, value) -> None:
        self.root = self._insert(None, self.root, key, value)

    # Recursively call insert until we find a leaf node
    def _insert(self, parent, child: Node, key, value):
        # Base Case: At leaf node insert key value pair
        if child.is_leaf:
            child.keys.append(key)
            child.keys.sort(key=lambda x: x[0])

            # Add value into the dict
            if key not in child.values:
                child.values[key] = []
            child.values[key].append(value)

            # Return unmodified node if order satisfied
            if len(child.keys) < self.order:
                # Check if the lead node has a parent
                if not parent:
                    return child
                else:   # Return the parent
                    return parent

            # Order is violated
            return self._split_leaf(parent, child)
        else:
            # Choose the next child node to traverse down
            next_child = self._select_child(child, key)
            p_node = self._insert(child, next_child, key, value)

            # internal nodes may only have up to order - 1 keys
            if len(p_node.keys) < self.order - 1:
                return p_node

            # Order is violated
            return self._split_internal(parent, child)

    # Transfers the keys between split nodes and returns new_right_child
    def _transferKeys(self, node: Node):
        new_right_child = Node()
        midpoint = len(node.keys) // 2

        # Transfer keys
        new_right_child.keys = node.keys[midpoint:]
        node.keys = node.keys[:midpoint]

        # Transfer values
        for key in new_right_child.keys:
            new_right_child.values[key] = node.values.pop(key)

        return new_right_child

    # Returns the parent of the split leaf nodes
    def _split_leaf(self, parent: Node, child: Node):

        new_right_child = self._transferKeys(child)

        # Connect leaf nodes in linked list
        new_right_child.next = child.next       # Will maintain the linked list order
        child.next = new_right_child            # Connect split nodes

        # Check if the leaf node is a root
        if parent is None:
            new_root = Node()
            new_root.children.extend([child, new_right_child])
            new_root.keys.append(new_right_child.keys[0])
            return new_root
        else:
            # parent exists
            parent.children.extend([child, new_right_child])
            parent.keys.append(new_right_child.keys[0])
            parent.keys.sort(key=lambda x: x[0])
            return parent

    # Returns the parent of split internal nodes
    def _split_internal(self, parent: Node, child: Node):

        new_right_child = self._transferKeys(child)

        # Internal node is the root
        if parent is None:
            new_root = Node()
            new_root.children.extend([child, new_right_child])
            new_root.keys.append(new_right_child.keys.pop(0))
            return new_root
        else:
            # parent exists
            parent.children.extend([child, new_right_child])
            parent.keys.append(new_right_child.keys.pop(0))
            parent.keys.sort(key=lambda x: x[0])
            return parent

    # Copied from Khai, selects next child to be traversed
    def _select_child(self, parent: Node, key):
        # Iterate through the node's keys to find the appropriate child node for the key
        # Bug here
        for i, k in enumerate(parent.keys):
            if key < k[0]:
                return parent.children[i]
        # If the key is greater than all of the node's keys, return the last child node
        return parent.children[-1]
