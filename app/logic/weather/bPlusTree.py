import json
from node import Node


class BPlusTree:
    order: int
    root: Node = None
    head: Node = None
    tail: Node = None

    # Constructor for B+ Tree
    def __init__(self) -> None:
        pass

    # Called by frontend, given a list of day objects create a tree structure
    def create(self, yearDays=[], order=3) -> None:
        self.rebuild(yearDays, order)

    # Called by frontend, given parameters, return a list of days that best matches the search terms
    def find(self, average_temp, humidity, precipitation) -> json:
        # Search the tree for days with matching average temperatures
        matching_days = self.search(average_temp)

        # Filter and rank days based on input parameters
        ranked_days = self.search_by_parameters(
            matching_days, average_temp, humidity, precipitation)

        # Return the ranked results as a JSON object
        return json.dumps(ranked_days)

    def search_by_parameters(self, matching_days, average_temp, humidity, precipitation) -> list:
        ranked_days = []  # Initialize an empty list to store ranked days

        # Iterate through the matching_days
        for day in matching_days:
            if day is None:  # Skip if the day is None
                continue

            # Iterate through the day values
            for day_data in day.values():
                # Iterate through each day_data (dictionary)
                for d in day_data:
                    # Calculate the squared difference for average temperature
                    temp_diff = (d['average_temp'] - average_temp) ** 2
                    # Calculate the squared difference for humidity
                    humidity_diff = (d['humidity'] - humidity) ** 2
                    # Calculate the squared difference for precipitation
                    precipitation_diff = (
                        d['rain_levels'] - precipitation) ** 2
                    # Calculate the total difference by summing up the individual squared differences
                    total_diff = temp_diff + humidity_diff + precipitation_diff

                    # Append the total difference and day_data (dictionary) as a tuple to ranked_days
                ranked_days.append((total_diff, d))

        # Sort days based on total difference (ranking)
        ranked_days.sort(key=lambda x: x[0])

        # Return the ranked list of days (dictionaries)
        return [day_data[1] for day_data in ranked_days]

    # Insert a key, value pair into the B+ Tree
    def insert(self, key, value) -> None:
        self.root = self._insert(None, self.root, key, value)

    # Recursively call insert until we find a leaf node
    def _insert(self, parent: Node, child: Node, key, value) -> Node:
        # Base Case: Empty tree
        if child is None:
            return self._insert_new_root(child, key, value)
        # Base Case: At leaf node insert key value pair
        if child.is_leaf():
            # Check if the temperature already exists in tree
            self._insert_at_leaf(child, key, value)
            # Return unmodified node if order satisfied
            if len(child.keys) < self.order:
                # Check if the lead node has a parent
                if parent is None:
                    return child
                else:   # Return the parent
                    return parent
            else:
                # Order is violated
                return self._split_leaf(parent, child)
        else:
            # Choose the next child node to traverse down
            next_child = self._select_child(child, key)
            self._insert(child, next_child, key, value)
            # internal nodes may only have up to order
            if len(child.keys) < self.order:
                return child
            # Order is violated
            return self._split_internal(parent, child)

    # Insert a new root node
    def _insert_new_root(self, child: Node, key, value) -> Node:
        # Create a new node and populate it with key and value
        child = Node()
        child.keys.append(key)
        child.values[key] = []
        child.values[key].append(value)
        # Initialize head and tail pointers to child
        self.head = child
        self.tail = child
        # Return child as the root
        return child

    def _insert_at_leaf(self, child: Node, key, value) -> Node:
        # Check if the temperature already exists in tree
        if key not in child.keys:
            child.keys.append(key)
            child.keys.sort()
        # Add day obj into the dict
        if key not in child.values:
            child.values[key] = []
        # Duplicates will be added into the list
        child.values[key].append(value)

    # Transfers the keys between split nodes and returns new_right_child
    def _transferKeys(self, node: Node) -> Node:
        new_right_child = Node()
        midpoint = len(node.keys) // 2
        # Transfer keys
        new_right_child.keys = node.keys[midpoint:]
        node.keys = node.keys[:midpoint]
        return new_right_child

    # Returns the parent of the split leaf nodes
    def _split_leaf(self, parent: Node, child: Node) -> Node:
        new_right_child: Node = self._transferKeys(child)
        # Transfer values
        for key in new_right_child.keys:
            new_right_child.values[key] = child.values.pop(key)
        # Connect leaf nodes in linked list
        self._connectLeafNode(child, new_right_child)
        # Check if the leaf node is a root
        if parent is None:
            new_root = Node()
            new_root.children.extend([child, new_right_child])
            new_root.keys.append(new_right_child.keys[0])
            return new_root
        else:
            # parent exists
            parent.children.extend([new_right_child])
            # # Sort the children by the first key value that the have
            parent.children.sort(key=lambda child: child.keys[0])
            parent.keys.append(new_right_child.keys[0])
            parent.keys.sort()
            return parent

    # Connect the leaf child to the right child
    def _connectLeafNode(self, left_child: Node, right_child: Node) -> None:
        # Only two general cases, since we will never add a new head
        # Insert new tail
        if left_child is self.tail:
            right_child.prev = left_child
            right_child.next = left_child.next
            left_child.next = right_child
            self.tail = right_child
        else:  # Insert in middle
            right_child.prev = left_child
            right_child.next = left_child.next
            left_child.next.prev = right_child
            left_child.next = right_child

    # Returns the parent of split internal nodes
    def _split_internal(self, parent: Node, child: Node) -> Node:
        new_right_child = self._transferKeys(child)
        # Change pointers for children node
        midpoint = len(child.children) // 2
        for _ in range(0, midpoint):
            new_right_child.children.append(child.children.pop(midpoint))
        # Internal node is the root
        if parent is None:
            new_root = Node()
            new_root.children.extend([child, new_right_child])
            new_root.keys.append(new_right_child.keys.pop(0))
            return new_root
        else:
            # parent exists
            parent.children.extend([new_right_child])
            # Sort children by the first key that they have
            parent.children.sort(key=lambda child: child.keys[0])
            parent.keys.append(new_right_child.keys.pop(0))
            parent.keys.sort()
            return parent

    # Copied from Khai, selects next child to be traversed
    def _select_child(self, parent: Node, key) -> Node:
        # Iterate through the node's keys to find the appropriate child node for the key
        for i, k in enumerate(parent.keys):
            if key < k:
                return parent.children[i]
        # If the key is greater than all of the node's keys, return the last child node
        return parent.children[-1]

    def search(self, temp) -> list[Node]:
        return self._search(self.root, temp)

    def _search(self, node: Node, key) -> list[Node]:
        # If the node is a leaf, search for the key in its keys
        if node.is_leaf():
            if node is self.head and node is self.tail:
                return [None, node.values, None]
            if node is self.head:
                return [None, node.values, node.next.values]
            if node is self.tail:
                return [node.prev.values, node.values, None]
            return [node.prev.values, node.values, node.next.values]
        # If the node is not a leaf, recursively search for the key in the appropriate child node
        else:
            child = self._select_child(node, key)
            return self._search(child, key)

    # When given a new array of days rebuild the tree
    def rebuild(self, days=[], order=3) -> None:
        self._reset()
        self.order = order
        self.root = None
        self.head: Node
        self.tail: Node
        for day in days:
            self.insert(day['average_temp'], day)

    def _reset(self) -> None:
        # Delete tree via automatic garbage collection
        self.root = None
        # Delete the linked list
        if self.head is None:
            return
        while self.head.next is not None:
            self.head = self.head.next
            self.head.prev = None
        self.head = None
        self.tail = None

    def forward_traverse_leafs(self) -> None:
        curr_node = self.head
        while curr_node is not None:
            print(curr_node.keys)
            curr_node = curr_node.next

    def backward_traverse_leafs(self) -> None:
        curr_node = self.tail
        while curr_node is not None:
            print(curr_node.keys)
            curr_node = curr_node.prev
