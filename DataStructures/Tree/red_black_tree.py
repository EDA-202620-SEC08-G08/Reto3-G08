from DataStructures.Tree import rbt_node as rbt_node
from DataStructures.List import single_linked_list as sl
from DataStructures.List import array_list as al

def new_map():
    rbt = {'root': None, 
           'type': "RBT"}
    return rbt

def insert_node(root,key,value):
    if root is None:
        return rbt_node.new_node(key,value)

    cmp= default_compare(key,root)
    if cmp < 0:
        root['left'] = insert_node(root['left'],key,value)
    elif cmp > 0:
        root['right'] = insert_node(root['right'],key,value)
    else:
        root['value'] = value
        
    if is_red(root['right']) and not is_red(root['left']):
        root = rotate_left(root)
    if is_red(root['left']) and is_red(root['left']['left']):
        root = rotate_right(root)
    if is_red(root['left']) and is_red(root['right']):
        flip_colors(root)
    
    
    root["size"] = 1 + size_tree(root['left']) + size_tree(root['right'])
    return root
def default_compare(key,element):
    element_key = rbt_node.get_key(element)
    if key == element_key:
        return 0
    elif key > element_key:
        return 1
    return -1

def rotate_left(node_rbt):
    x = node_rbt['right']
    node_rbt['right'] = x['left']
    x['left'] = node_rbt
    x['color'] = node_rbt['color']
    node_rbt['color'] = rbt_node.RED
    x['size'] = node_rbt['size']
    node_rbt['size'] = 1 + size_tree(node_rbt['left']) + size_tree(node_rbt['right'])
    return x   
def rotate_right(node_rbt):
    x = node_rbt["left"]
    node_rbt["left"] = x["right"]
    x["right"] = node_rbt
    x["color"] = node_rbt["color"]
    node_rbt["color"] = rbt_node.RED
    x["size"] = node_rbt["size"]
    node_rbt["size"] = size_tree(node_rbt["left"]) + size_tree(node_rbt["right"]) + 1
    return x


def flip_node_color(node_rbt):
    if node_rbt is not None:
        if is_red(node_rbt):
            rbt_node.change_color(node_rbt, rbt_node.BLACK)
        else:
            rbt_node.change_color(node_rbt, rbt_node.RED)
def flip_colors(node_rbt):
    flip_node_color(node_rbt)
    flip_node_color(node_rbt["left"])
    flip_node_color(node_rbt["right"])


def size_tree(root):
    if root is None:
        return 0
    return root["size"]


def is_red(node_rbt):
    if node_rbt is None:
        return False
    return rbt_node.is_red(node_rbt)

def put(my_rbt, key, value):
    my_rbt["root"] = insert_node(my_rbt["root"], key, value)
    rbt_node.change_color(my_rbt["root"], rbt_node.BLACK)
    return my_rbt

def get(my_rbt, key):
    node = get_node(my_rbt["root"], key)
    return rbt_node.get_value(node)

def get_node(node_rbt, key):
    if node_rbt is None:
        return None
    cmp = default_compare(key, node_rbt)
    if cmp < 0:
        return get_node(node_rbt["left"], key)
    elif cmp > 0:
        return get_node(node_rbt["right"], key)
    else:
        return node_rbt

def contains(my_rbt, key):
    return get(my_rbt, key) is not None

def size(my_rbt):
    return size_tree(my_rbt["root"])


def is_empty(my_rbt):
    return my_rbt["root"] is None


def key_set(my_rbt):
    key_list = sl.new_list()
    key_set_tree(my_rbt["root"], key_list)
    return key_list


def key_set_tree(root, key_list):
    if root is not None:
        key_set_tree(root["left"], key_list)
        sl.add_last(key_list, root["key"])
        key_set_tree(root["right"], key_list)
    return key_list
def value_set(my_rbt):
    value_list = sl.new_list()
    value_set_tree(my_rbt["root"], value_list)
    return value_list


def value_set_tree(root, value_list):
    if root is not None:
        value_set_tree(root["left"], value_list)
        sl.add_last(value_list, root["value"])
        value_set_tree(root["right"], value_list)
    return value_list


def get_min(my_rbt):
    node = get_min_node(my_rbt["root"])
    return rbt_node.get_key(node)


def get_min_node(root):
    if root is None:
        return None
    if root["left"] is None:
        return root
    return get_min_node(root["left"])


def get_max(my_rbt):
    node = get_max_node(my_rbt["root"])
    return rbt_node.get_key(node)


def get_max_node(root):
    if root is None:
        return None
    if root["right"] is None:
        return root
    return get_max_node(root["right"])


def height(my_rbt):
    return height_tree(my_rbt["root"])


def height_tree(root):
    if root is None:
        return -1
    return 1 + max(height_tree(root["left"]), height_tree(root["right"]))


def keys(my_rbt, key_initial, key_final):
    key_list = al.new_list()
    keys_range(my_rbt["root"], key_initial, key_final, key_list)
    return key_list


def keys_range(root, key_initial, key_final, key_list):
    if root is not None:
        if default_compare(key_initial, root) < 0:
            keys_range(root["left"], key_initial, key_final, key_list)
        if default_compare(key_initial, root) <= 0 and default_compare(key_final, root) >= 0:
            al.add_last(key_list, root["key"])
        if default_compare(key_final, root) > 0:
            keys_range(root["right"], key_initial, key_final, key_list)
    return key_list


def values(my_rbt, key_initial, key_final):
    value_list = al.new_list()
    values_range(my_rbt["root"], key_initial, key_final, value_list)
    return value_list


def values_range(root, key_initial, key_final, value_list):
    if root is not None:
        if default_compare(key_initial, root) < 0:
            values_range(root["left"], key_initial, key_final, value_list)
        if default_compare(key_initial, root) <= 0 and default_compare(key_final, root) >= 0:
            al.add_last(value_list, root["value"])
        if default_compare(key_final, root) > 0:
            values_range(root["right"], key_initial, key_final, value_list)
    return value_list


def left_key(my_rbt):
    return get_min(my_rbt)


def right_key(my_rbt):
    return get_max(my_rbt)
