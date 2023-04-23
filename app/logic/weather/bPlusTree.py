
import requests

# The Node class represents a single node in the B+ tree, containing keys and children.


class Node:
    def __init__(self, order):
        self.order = order  # Order of the B+ tree
        self.keys = []  # List of keys in the node
        self.children = []  # List of child nodes

    # Returns True if the node is a leaf, otherwise False
    def is_leaf(self):
        return not bool(self.children)
        ############### ---------------kevin part #############

# The BPlusTree class represents the entire B+ tree structure.

# Make a new leaf node class that stores temp key and a linked list of day objects
#   The linked list will be cut into 4 arrays
#       0 - 24, 25 - 49, 50 - 74, and 75 - 100 % humidity
# In Node add temperature attribute as the key value to be compared

# The website will ask to search for temperatures from a specific range of days that the user inputs
# Isaac will call the api on his end and create an array of day objects from that range
# The b+ tree will be instantiated with the array
# Taking in the temperature value that the user wants to look for we will search the tree for the set of values that matches
# The b+ tree is one part of the overall search algorithm
# When the search is done it should return a linked list

# A simple search of the linked list with the correct humidity will return an array of days that match the precipitation

      ############### ---------------kevin part #############

# The BPlusTree class represents the entire B+ tree structure.


class BPlusTree:
    def __init__(self, days=[], order=3):
        self.order = order  # Order of the B+ tree
        self.root = Node(order)  # The root node of the tree

        # Initialize the b+ tree with an array of day objects if their are days
        ############### ---------------kevin part #############
      # TODO: test this addition
        for i in range(len(days)):
            # insert the temp as the key,           dict object as value
            self.insert(days[i]['data'][0]['temp'], days[i])
        ############### ---------------kevin part #############

    # Inserts a key-value pair into the B+ tree.
    def insert(self, key, value):
        # Create a new root node
        new_child = self._insert(self.root, key, value)
        if new_child:
            new_root = Node(self.order)
            # Changed this line to not pop the first element in the new node
            new_root.keys = [new_child.keys[0]]
            new_root.children = [self.root, new_child]
            self.root = new_root

    # Recursive insert
        # Check if the tree is empty
            # just make a new node and insert
        # Check if the node is a child node
            # traverse down the correct branch to child node
        # else
            # insert into the node

        # Check if node requires splitting
            # return false if not
            # this false will prevent splitting in the rest of the recursion
        # else
            # split the node
            # differentiate between leaf nodes and internal nodes
            # leaf can maintain the middle value
            # internal must delete middle value
            # both will provide middle value to parent node
            #

    # FIXME: Make it so that whenever we split internal nodes we pop the middle value
    # the middle node is copied to the node above it
    # and we check to see if we need to split that new node

    # Searches for a key in the B+ tree and returns the temperature of the city.
    def search(self, key, api_key):
        coordinates = self._search(self.root, key)
        if coordinates:
            return self._get_temperature(coordinates, api_key)
        return None

    # Helper method to insert a key-value pair into a node.
    def _insert(self, node, key, value):
        if node.is_leaf():  # Check if node is a leaf
            node.keys.append((key, value))  # Add key-value pair to node's keys
            # Sort node's keys by the first element of each tuple
            node.keys.sort(key=lambda x: x[0])
            if len(node.keys) < self.order:  # Check if node is not full
                return None
            # Call _split_leaf_node method with node as parameter
            return self._split_leaf_node(node)
        else:
            # Call _select_child method with node and key as parameters
            child = self._select_child(node, key)
            # Recursively call _insert method with child node, key, and value as parameters
            new_child = self._insert(child, key, value)
            if not new_child:
                return None
            # Get the index of the child node in the node's children list
            i = node.children.index(child)
            # Insert the popped key from new_child at the i-th index of the node's keys list
            # Changed from popping key to just inserting it
            node.keys.insert(i, new_child.keys[0])
            # Insert new_child at the (i+1)th index of the node's children list
            node.children.insert(i + 1, new_child)
            if len(node.keys) < self.order:  # Check if node is not full
                return None
            # Call _split_internal_node method with node as parameter
            return self._split_internal_node(node)

    def _split_leaf_node(self, node):
        # Create a new node with the same order as the original node
        new_node = Node(self.order)

        # Determine the midpoint of the node's keys
        midpoint = len(node.keys) // 2

        # Move the second half of the keys to the new node
        new_node.keys = node.keys[midpoint:]

        # Remove the second half of the keys from the original node
        node.keys = node.keys[:midpoint]

        # Return the new node
        return new_node

    def _split_internal_node(self, node):
        # Create a new node with the same order as the original node
        new_node = Node(self.order)

        # Determine the midpoint of the node's keys
        midpoint = len(node.keys) // 2

        # Move the second half of the keys and children to the new node
        # Changed the midpoint + 1 to just midpoint
        new_node.keys = node.keys[midpoint:]
        new_node.children = node.children[midpoint + 1:]

        # Remove the second half of the keys and children from the original node
        # Changed the midpoint + 1 to just midpoint
        node.keys = node.keys[:midpoint]
        node.children = node.children[:midpoint + 1]

        # Return the new node
        return new_node

    def _search(self, node, key):
        # If the node is a leaf, search for the key in its keys
        if node.is_leaf():
            for k, v in node.keys:
                if k == key:
                    return v
            # If the key is not found, return None
            return None
        # If the node is not a leaf, recursively search for the key in the appropriate child node
        else:
            child = self._select_child(node, key)
            return self._search(child, key)

    def _select_child(self, node, key):
        # Iterate through the node's keys to find the appropriate child node for the key
        # Bug here
        for i, k in enumerate(node.keys):
            if key < k[0]:
                return node.children[i]
        # If the key is greater than all of the node's keys, return the last child node
        return node.children[-1]

    def _get_temperature(self, coordinates, api_key):
        lat, lon = coordinates
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=imperial"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            print(f"Error fetching temperature data: {data['message']}")
            return None

        temperature = data["main"]["temp"]
        return temperature

    def dbg_search(self, temp):
        result_day = self._search(self.root, temp)
        if result_day:
            print(result_day)
        else:
            print("Temperature Not Found")
            return None


def fetch_cities(search_term, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={search_term}&limit=5&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if not data:
        print(f"No cities found with the search term: {search_term}")
        return []

    cities = [{"name": city["name"], "coord": {
        "lat": city["lat"], "lon": city["lon"]}} for city in data]
    return cities


# Example usage
bplus_tree = BPlusTree(order=5)
api_key = "22a4a6b8c95cae3bd78f317a1094c245"

# Fetch cities using a search term and insert them into the B+ tree
search_term = "Austin"
cities = fetch_cities(search_term, api_key)

for city in cities:
    bplus_tree.insert(city["name"].lower(),
                      (city["coord"]["lat"], city["coord"]["lon"]))

# Search for a city and display its temperature
city_name = "Austin"
temperature = bplus_tree.search(city_name.lower(), api_key)

if temperature:
    print(f"Temperature in {city_name}: {temperature} F")
else:
    print(f"City '{city_name}' not found in the B+ tree.")