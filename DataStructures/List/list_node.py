def new_single_node(element):
    return {"info": element, "next": None}


def new_double_node(element):
    return {"info": element, "next": None, "prev": None}


def get_element(node):
    return node["info"]
