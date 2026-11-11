from DataStructures.Priority_queue import pq_entry as pqe
from DataStructures.List import array_list as al


def default_compare_higher_value(father_node, child_node):
    """
    Max-heap: el padre está bien ubicado si su prioridad es >= a la del hijo.
    """
    return pqe.get_priority(father_node) >= pqe.get_priority(child_node)


def default_compare_lower_value(father_node, child_node):
    """
    Min-heap: el padre está bien ubicado si su prioridad es <= a la del hijo.
    """
    return pqe.get_priority(father_node) <= pqe.get_priority(child_node)


def new_heap(is_min_pq=True, cmp_function=None):
    """
    Crea una cola de prioridad orientada a menor (is_min_pq=True) o a mayor.
    Si se pasa cmp_function(padre, hijo) -> bool, se usa en lugar de la
    comparación por defecto. La posición 0 del arreglo no se usa.
    """
    heap = {
        "elements": al.new_list(),
        "size": 0,
        "cmp_function": None,
    }
    if cmp_function is not None:
        heap["cmp_function"] = cmp_function
    elif is_min_pq:
        heap["cmp_function"] = default_compare_lower_value
    else:
        heap["cmp_function"] = default_compare_higher_value

    al.add_last(heap["elements"], None)
    return heap


def size(my_heap):
    return my_heap["size"]


def is_empty(my_heap):
    return size(my_heap) == 0


def priority(my_heap, parent, child):
    cmp = my_heap["cmp_function"]
    return cmp(parent, child)


def exchange(my_heap, i, j):
    al.exchange(my_heap["elements"], i, j)


def swim(my_heap, pos):
    while pos > 1:
        parent_pos = pos // 2
        parent = al.get_element(my_heap["elements"], parent_pos)
        child = al.get_element(my_heap["elements"], pos)
        if priority(my_heap, parent, child):
            break
        exchange(my_heap, parent_pos, pos)
        pos = parent_pos


def sink(my_heap, pos):
    n = my_heap["size"]
    elements = my_heap["elements"]
    while 2 * pos <= n:
        child_pos = 2 * pos
        if child_pos < n:
            left = al.get_element(elements, child_pos)
            right = al.get_element(elements, child_pos + 1)
            if not priority(my_heap, left, right):
                child_pos += 1
        parent = al.get_element(elements, pos)
        child = al.get_element(elements, child_pos)
        if priority(my_heap, parent, child):
            break
        exchange(my_heap, pos, child_pos)
        pos = child_pos


def insert(my_heap, priority_value, value):
    entry = pqe.new_pq_entry(priority_value, value)
    al.add_last(my_heap["elements"], entry)
    my_heap["size"] += 1
    swim(my_heap, my_heap["size"])
    return my_heap


def get_first_priority(my_heap):
    """
    Retorna (sin eliminar) el valor del elemento con mayor prioridad.
    """
    if is_empty(my_heap):
        return None
    return pqe.get_value(al.get_element(my_heap["elements"], 1))


def remove(my_heap):
    """
    Elimina y retorna el valor del elemento con mayor prioridad.
    """
    if is_empty(my_heap):
        return None
    elements = my_heap["elements"]
    first = al.get_element(elements, 1)
    exchange(my_heap, 1, my_heap["size"])
    al.remove_last(elements)
    my_heap["size"] -= 1
    sink(my_heap, 1)
    return pqe.get_value(first)
