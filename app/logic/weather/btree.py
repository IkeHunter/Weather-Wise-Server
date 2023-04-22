import requests
import json
from node import Node


class BPlusTree:
    # Constructor for B+ Tree
    def __init__(self, days=[], order=3) -> None:
        self.order = order
        self.root = None
        self.head: Node
        self.tail: Node
        for day in days:
            self.insert(day['data'][0]['temp'], day)

    # Insert a key, value pair into the B+ Tree
    def insert(self, key, value) -> None:
        self.root = self._insert(None, self.root, key, value)

    # Recursively call insert until we find a leaf node
    def _insert(self, parent, child: Node, key, value) -> Node:
        # Base Case: Empty tree
        if child is None:
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
        # Base Case: At leaf node insert key value pair
        if child.is_leaf():
            # Check if the temperature already exists in tree
            if key not in child.keys:
                child.keys.append(key)
                child.keys.sort()

            # Add day obj into the dict
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

            # internal nodes may only have up to order
            if len(p_node.keys) < self.order:
                return p_node

            # Order is violated
            return self._split_internal(p_node, child)

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
    # FIXME: Parent is never none from _insert
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
            parent.children.extend([child, new_right_child])
            parent.keys.append(new_right_child.keys.pop(0))
            parent.keys.sort()
            return parent

    # Copied from Khai, selects next child to be traversed
    def _select_child(self, parent: Node, key):
        # Iterate through the node's keys to find the appropriate child node for the key
        for i, k in enumerate(parent.keys):
            if key < k:
                return parent.children[i]
        # If the key is greater than all of the node's keys, return the last child node
        return parent.children[-1]

    def search(self, temp):
        return self._search(self.root, temp)

    def _search(self, node: Node, key):
        # If the node is a leaf, search for the key in its keys
        if node.is_leaf():
            for k in node.keys:
                if k is key:
                    return node.values.get(key)
            # Return None
            return None
        # If the node is not a leaf, recursively search for the key in the appropriate child node
        else:
            child = self._select_child(node, key)
            return self._search(child, key)

    # TODO: Create functionality to recreate tree with new data
    # When given a new array of days rebuild the tree
    def rebuild(self, days=[], order=3) -> None:
        self._reset
        self.__init__(days, order)

    def _reset(self) -> None:
        # Delete tree via automatic garbage collection
        self.root = None

        # Delete the linked list
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


# ============= Test =========== #


def testMain():
    apiKey = '11d1d9e83f342ffd3863eec2bdabe3a8'
    # date = 1618525688
    date = 1572687311
    lat = '33.44'
    lon = '-94.04'

    # Checking if API call works
    # url = 'https://api.openweathermap.org/data/3.0/onecall?lat=' + \
    #    lat + '&lon=' + lon + '&appid=' + apiKey
    # https: // api.openweathermap.org/data/3.0/onecall/timemachine?lat = 39.099724 & lon = -94.578331 & dt = 1643803200 & appid = {API key}

    days = [{'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
             'data': [{'dt': 1644062400, 'sunrise': 1644066553, 'sunset': 1644105068, 'temp': 269.44, 'feels_like': 267.09,
                       'pressure': 1035, 'humidity': 83, 'dew_point': 267.26, 'clouds': 0, 'visibility': 10000, 'wind_speed': 1.54,
                       'wind_deg': 240,
                           'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}]}]},

            {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
             'data': [{'dt': 1644321600, 'sunrise': 1644325606, 'sunset': 1644364441, 'temp': 274.04, 'feels_like': 272.35,
                       'pressure': 1025, 'humidity': 75, 'dew_point': 270.47, 'clouds': 0, 'visibility': 10000, 'wind_speed': 1.54,
                       'wind_deg': 200,
                           'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}]}]},

            {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
             'data': [{'dt': 1643889600, 'sunrise': 1643893845, 'sunset': 1643932152, 'temp': 274.7, 'feels_like': 270.1,
                       'pressure': 1014, 'humidity': 95, 'dew_point': 273.99, 'clouds': 100, 'visibility': 10000, 'wind_speed': 5.14,
                       'wind_deg': 30,
                       'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10n'}], 'rain': {'1h': 1.98}}]},

            {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
             'data': [{'dt': 1644667200, 'sunrise': 1644670990, 'sunset': 1644710268, 'temp': 284.66, 'feels_like': 283.15,
                       'pressure': 1022, 'humidity': 49, 'dew_point': 274.33, 'clouds': 100, 'visibility': 10000, 'wind_speed': 4.63,
                       'wind_deg': 20, 'wind_gust': 7.72,
                       'weather': [{'id': 500, 'main': 'Rain', 'description': 'light rain', 'icon': '10n'}], 'rain': {'1h': 0.21}}]},

            {'lat': 33.44, 'lon': -94.04, 'timezone': 'America/Chicago', 'timezone_offset': -21600,
             'data': [{'dt': 1643803200, 'sunrise': 1643807488, 'sunset': 1643845693, 'temp': 287.67, 'feels_like': 287.63,
                       'pressure': 1009, 'humidity': 94, 'dew_point': 286.72, 'clouds': 100, 'visibility': 10000, 'wind_speed': 4.12,
                       'wind_deg': 210,
                       'weather': [{'id': 804, 'main': 'Clouds', 'description': 'overcast clouds', 'icon': '04n'}]}]}
            ]

    days2 = []
    for i in range(10):
        # The next day is date + 86400
        date += 86400
        url = 'https://api.openweathermap.org/data/3.0/onecall/timemachine?lat=' + \
            lat + '&lon=' + lon + '&dt=' + str(date) + '&appid=' + apiKey
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        weatherDict = json.loads(response.text)
        sunrise = weatherDict['data'][0]['sunrise'] % 86400
        sunset = weatherDict['data'][0]['sunset'] % 86400
        weatherDict['data'][0]['sunrise'] = sunrise
        weatherDict['data'][0]['sunset'] = sunset
        days2.append(weatherDict)

    for days in days2:
        print(days['data'][0]['temp'])

        print("")
# Bug here: leaf layer not in order
    tree = BPlusTree(days2)
    tree.forward_traverse_leafs()
    # print("")
    # tree.rebuild(days)
    # tree.forward_traverse_leafs()
#     # print(tree.search(269.44)[0]['data'][0]['temp'])
#     # print(tree.search(274.04)[0]['data'][0]['temp'])
#     # print(tree.search(274.7)[0]['data'][0]['temp'])
#     # print(tree.search(284.66)[0]['data'][0]['temp'])
#     # print(tree.search(287.67)[0]['data'][0]['temp'])
#     tree.backward_traverse_leafs()


testMain()
