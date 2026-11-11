from DataStructures.List import array_list as al

def new_list():
    new_list ={
    "elements": [],
    "size":0,
    }
    
    return new_list

def add_first(my_list, element):
    my_list["elements"].insert(0, element)
    my_list["size"] += 1
    return my_list

def add_last(my_list, element):
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list

def size(my_list):

    return my_list["size"]

def first_element(my_list):
    if my_list["size"] == 0:
        raise Exception("IndexError: list index out of range")

    return my_list["elements"][0]

def is_empty(my_list):
    return my_list["size"] == 0

def last_element(my_list):
    if my_list["size"] == 0:
        raise Exception("IndexError: list index out of range")
    
    return my_list["elements"][-1]

def get_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception("IndexError: list index out of range")

    return my_list["elements"][pos]

def is_present(my_list, element, cmp_function):
    size = my_list["size"]
    if size > 0:
        keyexist = False
        for keypos in range(0, size):
            info = my_list["elements"][keypos]
            if cmp_function(element, info) == 0:
                keyexist = True
                break
        if keyexist:
            return keypos
    return -1

def delete_element(my_list, pos):
    if pos < 0 or pos >= my_list["size"]:
        raise Exception("IndexError: list index out of range")
    else:
        my_list["elements"].pop(pos)
        my_list["size"] -= 1
        return my_list

def remove_first(my_list):
    if my_list["size"] == 0:
        if my_list["size"] == 0:
            raise Exception("IndexError: list index out of range")
    else:
        element = my_list["elements"].pop(0)
        my_list["size"] -= 1
        return element

def remove_last(my_list):
    if my_list["size"] == 0:
        if my_list["size"] == 0:
            raise Exception("IndexError: list index out of range")
    else:
        element = my_list["elements"].pop()
        my_list["size"] -= 1
        return element

def insert_element(my_list, pos, element):
    if pos < 0 or pos > my_list["size"]:
        raise Exception("IndexError: list index out of range")
    else:
        my_list["elements"].insert(pos, element)
        my_list["size"] += 1
        return my_list

def change_info(my_list, pos, new_element):
    if pos < 0 or pos >= my_list["size"]:
         raise Exception("IndexError: list index out of range")
        
    else:
        my_list["elements"][pos] = new_element
        return my_list
    
def exchange(my_list, pos1, pos2):
    if pos1 < 0 or pos1 >= my_list["size"] or pos2 < 0 or pos2 >= my_list["size"]:
         raise Exception("IndexError: list index out of range")
    else:
        my_list["elements"][pos1], my_list["elements"][pos2] = my_list["elements"][pos2], my_list["elements"][pos1]
        return my_list

def sub_list(my_list, pos, size):
    if pos < 0 or pos >= my_list["size"] or size < 0 or pos + size > my_list["size"]:
         raise Exception("IndexError: list index out of range")
    else:
        sub_list = {
            "elements": my_list["elements"][pos:pos + size],
            "size": size
        }
        return sub_list
    
def default_sort_criteria (element1, element2):
    
    is_sorted = False
    
    if element1 < element2:
        is_sorted = True
    return is_sorted

def selection_sort(my_list,sort_crit):
    n=my_list["size"]
    for i in range(n):
        min_index=i
        for j in range(i+1, n):
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

