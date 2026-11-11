from DataStructures.List import array_list as al
from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_entry as me
import random 

def new_map(num_elements,load_factor,prime=109345121):
    capacity = mf.next_prime(int(num_elements/load_factor))
    
    table= al.new_list()
    for i in range(capacity):
        al.add_last(table,me.new_map_entry(None,None))
        
    my_table = {
        "prime": prime,
        "type": "PROBING",
        "capacity": capacity,
        "scale":random.randint(1,prime-1),
        "shift":random.randint(0,prime-1),
        "table": table,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0
        }
    return my_table

def is_available(table, pos):
    entry = al.get_element(table, pos)
    return me.get_key(entry) is None or me.get_key(entry) == "__EMPTY__"

def default_compare(key, entry):
    entry_key = me.get_key(entry)
    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    return -1

def find_slot(my_map, key, hash_value):
   first_avail = None
   found = False
   ocupied = False
   while not found:
      if is_available(my_map["table"], hash_value):
            if first_avail is None:
               first_avail = hash_value
            entry = al.get_element(my_map["table"], hash_value)
            if me.get_key(entry) is None:
               found = True
      elif default_compare(key, al.get_element(my_map["table"], hash_value)) == 0:
            first_avail = hash_value
            found = True
            ocupied = True
      hash_value = (hash_value + 1) % my_map["capacity"]
   return ocupied, first_avail

def put(my_map, key, value):
    hash_value = mf.hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, hash_value)
    entry = al.get_element(my_map["table"], pos)

    if ocupied:
        me.set_value(entry, value)
    else:
        me.set_key(entry, key)
        me.set_value(entry, value)
        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        if my_map["current_factor"] > my_map["limit_factor"]:
            rehash(my_map)
    return my_map

def rehash(my_map):
    new_table=new_map(2 * (my_map["capacity"]),1,my_map["prime"])
    new_table["limit_factor"] = my_map["limit_factor"]
    
    old=my_map["table"]
    for i in range(al.size(old)):
        entry=al.get_element(old,i)
        k = me.get_key(entry)
        if k is not None and k != "__EMPTY__":
            put(new_table, k, me.get_value(entry))
    my_map.update(new_table)
    return my_map

def contains(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, hash_value)
    return ocupied

def get(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, hash_value)
    if ocupied:
        entry = al.get_element(my_map["table"], pos)
        return me.get_value(entry)
    return None

def remove(my_map, key):
    hash_value = mf.hash_value(my_map, key)
    ocupied, pos = find_slot(my_map, key, hash_value)
    if ocupied:
        entry = al.get_element(my_map["table"], pos)
        value = me.get_value(entry)
        me.set_key(entry, "__EMPTY__")
        me.set_value(entry, "__EMPTY__")
        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]
        return value

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    if my_map["size"] == 0:
        return True
    return False

def key_set(my_map):
    keys = al.new_list()
    for i in range(al.size(my_map["table"])):
        entry = al.get_element(my_map["table"], i)
        k = me.get_key(entry)
        if k is not None and k != "__EMPTY__":
            al.add_last(keys, k)
    return keys

def value_set(my_map):
    values = al.new_list()
    for i in range(al.size(my_map["table"])):
        entry = al.get_element(my_map["table"], i)
        k = me.get_key(entry)
        if k is not None and k != "__EMPTY__":
            al.add_last(values, me.get_value(entry))
    return values