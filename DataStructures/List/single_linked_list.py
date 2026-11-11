from DataStructures.List.list_node import new_single_node


def new_list():
    new_list ={
    "first": None,
    "last": None,
    "size": 0,
    }
    return new_list  

def add_first(my_list, element):
    node = new_single_node(element)
    if my_list["first"] is None:
        my_list["first"] = node
        my_list["last"] = node
    else:
        node["next"] = my_list["first"]
        my_list["first"] = node
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    node = new_single_node(element)
    if my_list["first"] is None:
        my_list["first"] = node
        my_list["last"] = node
    else:
        my_list["last"]["next"] = node
        my_list["last"] = node
    my_list["size"] += 1
    return my_list
def size(my_list):

    return my_list["size"]

def first_element(my_list):
    if my_list["size"] == 0:
        raise Exception('IndexError: list index out of range')
        
    return my_list["first"]["info"]

def get_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception("IndexError: list index out of range")
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    return node["info"]
def is_present(my_list,element,cmp_funcion):
    is_in_array = False
    temp=my_list["first"]
    count=0
    while temp is not None and not is_in_array:
        if cmp_funcion(element,temp["info"])==0:
            is_in_array=True
        else:
            temp=temp["next"]
            count+=1
    if not is_in_array:
        count=-1
    return count
def is_empty(my_list):
    return my_list["size"] == 0
def last_element(my_list):
    if my_list == 0:
        raise Exception('IndexError: list index out of range')
    return my_list["last"]["info"]
def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception("IndexError: list index out of range")
    
    if pos == 0:
        my_list["first"] = my_list["first"]["next"]
        
        if my_list["size"] == 1:
            my_list["last"] = None
    else:
        searchpos = 0
        node = my_list["first"]
        while searchpos < pos - 1:
            node = node["next"]
            searchpos += 1
            
        if node["next"] == my_list["last"]:
            my_list["last"] = node
            
        node["next"] = node["next"]["next"]
    my_list["size"] -= 1
    return my_list
def remove_first(my_list):
    if my_list["first"] is None:
        raise Exception("IndexError: list index out of range")

    element = my_list["first"]["info"]
    my_list["first"] = my_list["first"]["next"]
    my_list["size"] -= 1

    if my_list["first"] is None:
        my_list["last"] = None

    return element
def remove_last(my_list):
    if my_list["first"] is None:
        raise Exception("IndexError: list index out of range")

    element = my_list["last"]["info"]

    if my_list["first"] == my_list["last"]:
        my_list["first"] = None
        my_list["last"] = None

    else:
        node = my_list["first"]

        while node["next"] != my_list["last"]:
            node = node["next"]

        node["next"] = None
        my_list["last"] = node

    my_list["size"] -= 1

    return element
def insert_element(my_list, element, pos):
    if pos < 0 or pos > my_list["size"]:
        raise Exception("IndexError: list index out of range")

    node = new_single_node(element)

    if pos == 0:
        node["next"] = my_list["first"]
        my_list["first"] = node

        if my_list["last"] is None:
            my_list["last"] = node

    elif pos == my_list["size"]:
        my_list["last"]["next"] = node
        my_list["last"] = node

    else:
        searchpos = 0
        current_node = my_list["first"]

        while searchpos < pos - 1:
            current_node = current_node["next"]
            searchpos += 1

        node["next"] = current_node["next"]
        current_node["next"] = node

    my_list["size"] += 1

    return my_list
    

def change_info(my_list, pos, new_element):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception("IndexError: list index out of range")

    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    node["info"] = new_element
    return my_list
def exchange(my_list, pos1, pos2):
    if pos1 < 0 or pos1 >= my_list["size"] or pos2 < 0 or pos2 >= my_list["size"]:
        raise Exception("IndexError: list index out of range")

    if pos1 == pos2:
        return my_list
    searchpos1 = 0
    searchpos2 = 0
    node1 = my_list["first"]
    node2 = my_list["first"]
    while searchpos1 < pos1:
        node1 = node1["next"]
        searchpos1 += 1
    while searchpos2 < pos2:
        node2 = node2["next"]
        searchpos2 += 1
    temp_info = node1["info"]
    node1["info"] = node2["info"]
    node2["info"] = temp_info
    return my_list
def sub_list(my_list, pos, size):
    if pos < 0 or pos >= my_list["size"] or size < 0 or pos + size > my_list["size"]:
        raise Exception("IndexError: list index out of range")
    sub_list = new_list()
    searchpos = 0
    node = my_list["first"]
    while searchpos < pos:
        node = node["next"]
        searchpos += 1
    count = 0
    while count < size:
        add_last(sub_list, node["info"])
        node = node["next"]
        searchpos += 1
        count += 1
    return sub_list

def default_sort_criteria (element1, element2):
    
    is_sorted = False
    
    if element1 < element2:
        is_sorted = True
    return is_sorted

def selection_sort(my_list, sort_crit):
    n = my_list["size"]

    for i in range(n):
        min_index = i

        for j in range(i + 1, n):
            element_j = get_element(my_list, j)
            element_min = get_element(my_list, min_index)

            if sort_crit(element_j, element_min):
                min_index = j

        element_i = get_element(my_list, i)
        element_min = get_element(my_list, min_index)

        change_info(my_list, i, element_min)
        change_info(my_list, min_index, element_i)

    return my_list

def insertion_sort(my_list, sort_crit):
    n = my_list["size"]

    for i in range(1, n):
        element = get_element(my_list, i)
        j = i - 1

        while j >= 0 and sort_crit(element, get_element(my_list, j)):
            previous = get_element(my_list, j)
            change_info(my_list, j + 1, previous)
            j = j - 1

        change_info(my_list, j + 1, element)

    return my_list

def shell_sort(my_list, sort_crit):
    n = my_list["size"]
    h = n // 2

    while h > 0:

        for i in range(h, n):
            element = get_element(my_list, i)
            j = i

            while j >= h and sort_crit(element, get_element(my_list, j - h)):
                previous = get_element(my_list, j - h)
                change_info(my_list, j, previous)
                j = j - h

            change_info(my_list, j, element)

        h = h // 2

    return my_list

def merge_sort(my_list, sort_crit):
    n = my_list["size"]

    if n > 1:
        mid = n // 2
        left = new_list()
        right = new_list()

        for i in range(0, mid):
            add_last(left, get_element(my_list, i))

        for i in range(mid, n):
            add_last(right, get_element(my_list, i))

        merge_sort(left, sort_crit)
        merge_sort(right, sort_crit)

        i = 0
        j = 0
        k = 0
        n_left = left["size"]
        n_right = right["size"]

        while i < n_left and j < n_right:
            element_left = get_element(left, i)
            element_right = get_element(right, j)

            if sort_crit(element_left, element_right):
                change_info(my_list, k, element_left)
                i += 1
            else:
                change_info(my_list, k, element_right)
                j += 1
            k += 1

        while i < n_left:
            change_info(my_list, k, get_element(left, i))
            i += 1
            k += 1

        while j < n_right:
            change_info(my_list, k, get_element(right, j))
            j += 1
            k += 1

    return my_list

#single linked list 

def quick_sort(my_list, sort_crit):

    def sort_range(low, high):
        if low < high:
            pivot = get_element(my_list, high)
            i = low - 1

            for j in range(low, high):
                element_j = get_element(my_list, j)
                if sort_crit(element_j, pivot):
                    i += 1
                    exchange(my_list, i, j)

            exchange(my_list, i + 1, high)
            pivot_pos = i + 1

            sort_range(low, pivot_pos - 1)
            sort_range(pivot_pos + 1, high)

    sort_range(0, my_list["size"] - 1)
    return my_list
