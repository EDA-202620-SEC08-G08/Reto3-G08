import time
import csv
import os
import math

from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mlp
from DataStructures.Tree import red_black_tree as rbt
from DataStructures.Priority_queue import priority_queue as pq

csv.field_size_limit(2147483647)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "Data", "Data")


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        # Todas las ventas en el orden en que aparecen en el archivo
        "sales": al.new_list(),
        # marca (minúscula) -> RBT {discount_percent -> lista de ventas}  (REQ 1)
        "brand_discount": mlp.new_map(20, 0.5),
        # RBT {customer_rating -> lista de ventas}  (REQ 2)
        "country_rating": mlp.new_map(40,0.5),
        # RBT {order_date "AAAA-MM-DD" -> lista de ventas}  (REQ 4, 5, 6)
        "dates": rbt.new_map(),
        # Venta con menor y mayor precio final (se calculan durante la carga)
        "min_sale": None,
        "max_sale": None,
    }
    return catalog


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga los datos del reto. Lee el archivo una sola vez.
    Retorna un diccionario con el resumen de la carga.
    """
    start = get_time()
    path = os.path.join(DATA_DIR, filename)

    with open(path, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            sale = format_sale(row)
            add_sale(catalog, sale)

    sales = catalog["sales"]
    total = al.size(sales)
    k = min(5, total)
    first = al.sub_list(sales, 0, k) if total > 0 else al.new_list()
    last = al.sub_list(sales, total - k, k) if total > 0 else al.new_list()

    end = get_time()
    return {
        "time": delta_time(start, end),
        "total": total,
        "min_sale": catalog["min_sale"],
        "max_sale": catalog["max_sale"],
        "first": first,
        "last": last,
    }


def format_sale(row):
    """
    Convierte a número los campos numéricos de un registro del CSV.
    """
    row["base_price_usd"] = float(row["base_price_usd"])
    row["discount_percent"] = float(row["discount_percent"])
    row["final_price_usd"] = float(row["final_price_usd"])
    row["units_sold"] = int(row["units_sold"])
    row["revenue_usd"] = float(row["revenue_usd"])
    row["customer_rating"] = float(row["customer_rating"])
    return row


def add_sale(catalog, sale):
    """
    Agrega una venta a todas las estructuras del catálogo.
    """
    al.add_last(catalog["sales"], sale)

    # Índice marca -> RBT por descuento
    brand_key = sale["brand"].strip().lower()
    tree = mlp.get(catalog["brand_discount"], brand_key)
    if tree is None:
        tree = rbt.new_map()
        mlp.put(catalog["brand_discount"], brand_key, tree)
    add_to_tree_list(tree, sale["discount_percent"], sale)
    
    # Índice por país -> RBT por calificación
    country_key = sale["country"].strip().lower()
    rating_tree = mlp.get(catalog["country_rating"], country_key)
    if rating_tree is None:
        rating_tree = rbt.new_map()
        mlp.put(catalog["country_rating"], country_key, rating_tree)
    add_to_tree_list(rating_tree, sale["customer_rating"], sale)

    # Índice por fecha
    add_to_tree_list(catalog["dates"], sale["order_date"], sale)

    # Menor precio final (empate -> la más reciente)
    current = catalog["min_sale"]
    if (current is None
            or sale["final_price_usd"] < current["final_price_usd"]
            or (sale["final_price_usd"] == current["final_price_usd"]
                and sale["order_date"] > current["order_date"])):
        catalog["min_sale"] = sale

    # Mayor precio final (empate -> la más antigua)
    current = catalog["max_sale"]
    if (current is None
            or sale["final_price_usd"] > current["final_price_usd"]
            or (sale["final_price_usd"] == current["final_price_usd"]
                and sale["order_date"] < current["order_date"])):
        catalog["max_sale"] = sale


def add_to_tree_list(tree, key, sale):
    """
    Agrega la venta a la lista asociada a 'key' en el árbol; la crea si no existe.
    """
    bucket = rbt.get(tree, key)
    if bucket is None:
        bucket = al.new_list()
        rbt.put(tree, key, bucket)
    al.add_last(bucket, sale)


def order_number(order_id):
    """
    Parte numérica del order_id (ej: 'ORD102308' -> 102308) para comparar ids.
    """
    digits = "".join(c for c in order_id if c.isdigit())
    return int(digits) if digits else 0


def get_sale_count(catalog):
    return al.size(catalog["sales"])


# Funciones de consulta sobre el catálogo


def sort_crit_req_1(sale1, sale2):
    """
    Ascendente por descuento; empate -> fecha más antigua primero;
    empate -> menor order_id.
    """
    if sale1["discount_percent"] != sale2["discount_percent"]:
        return sale1["discount_percent"] < sale2["discount_percent"]
    if sale1["order_date"] != sale2["order_date"]:
        return sale1["order_date"] < sale2["order_date"]
    return order_number(sale1["order_id"]) < order_number(sale2["order_id"])


def req_1(catalog, brand, discount_min, discount_max):
    """
    Retorna el resultado del requerimiento 1: órdenes de una marca con
    descuento dentro de [discount_min, discount_max].
    """
    start = get_time()
    result = al.new_list()
    total_cost = 0

    tree = mlp.get(catalog["brand_discount"], brand.strip().lower())
    if tree is not None and discount_min <= discount_max:
        # Rango en el RBT: listas de ventas con descuento en [min, max]
        buckets = rbt.values(tree, float(discount_min), float(discount_max))
        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)
            for j in range(al.size(bucket)):
                sale = al.get_element(bucket, j)
                al.add_last(result, sale)
                total_cost += sale["final_price_usd"]
        al.merge_sort(result, sort_crit_req_1)

    end = get_time()
    
    return {
        "time": delta_time(start, end),
        "total": al.size(result),
        "total_cost": total_cost,
        "orders": result,
    }

def sort_crit_req_2(sale1, sale2):
    """
    Descendente por calificación; empate -> fecha más reciente primero.
    """

    if sale1["customer_rating"] != sale2["customer_rating"]:
        return sale1["customer_rating"] > sale2["customer_rating"]

    return sale1["order_date"] > sale2["order_date"]


def req_2(catalog, country, rating_min, rating_max):
    """
    Retorna el resultado del requerimiento 2: órdenes de un país con
    calificación del cliente dentro de [rating_min, rating_max].
    """
    start = get_time()

    result = al.new_list()
    total_cost = 0.0

    tree = mlp.get(catalog["country_rating"], country.strip().lower())

    if tree is not None and rating_min <= rating_max:
        # Rango en el RBT: listas de ventas con calificación en [min,max]
        buckets = rbt.values(tree, float(rating_min), float(rating_max))
        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)
            
            for j in range(al.size(bucket)):
                sale = al.get_element(bucket, j)

                al.add_last(result, sale)
                total_cost += sale["final_price_usd"]

        al.merge_sort(result, sort_crit_req_2)

    end = get_time()

    return {
        "time": delta_time(start, end),
        "total": al.size(result),
        "total_cost": total_cost,
        "orders": result,
    }
    
def sort_crit_req_3(sale1, sale2):
    """
    Ascendente por precio final; empate -> fecha mas antigua primero;
    empate -> menor order_id.
     """
    if sale1["final_price_usd"] != sale2["final_price_usd"]:
         return sale1["final_price_usd"] < sale2["final_price_usd"]
    if sale1["order_date"] != sale2["order_date"]:
        return sale1["order_date"] < sale2["order_date"]
    return order_number(sale1["order_id"]) < order_number(sale2["order_id"])

def req_3(catalog, channel, category, price_min, price_max):
    """
    Retorna el resultado del requerimiento 3
    """
    start = get_time()
    result = al.new_list()
    total_cost = 0.0
 
    cc_key = channel_category_key(channel, category)
    tree = mlp.get(catalog["channel_category_price"], cc_key)
    if tree is not None and price_min <= price_max:
        buckets = rbt.values(tree, float(price_min), float(price_max))
        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)
            for j in range(al.size(bucket)):
                sale = al.get_element(bucket, j)
                al.add_last(result, sale)
                total_cost += sale["final_price_usd"]
        al.merge_sort(result, sort_crit_req_3)
 
    end = get_time()
 
    return {
        "time": delta_time(start, end),
        "total": al.size(result),
        "total_cost": total_cost,
        "orders": result,
    }
    
def sort_crit_req_4(parent, child):
    """
    Mayor número de órdenes primero.
    En empate, marca alfabéticamente ascendente.
    """
    p1 = parent["priority"]
    p2 = child["priority"]
 
    if p1[0] != p2[0]:
        return p1[0] > p2[0]
 
    return p1[1] <= p2[1]


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    start = get_time()
    income_key = income_level.strip().lower()
 

    brands = mlp.new_map(20, 0.5)
    if date_start <= date_end:
        buckets = rbt.values(catalog["dates"], date_start, date_end)
 
        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)
 
            for j in range(al.size(bucket)):
                sale = al.get_element(bucket, j)
 
                if sale["customer_income_level"].strip().lower() == income_key:
                    brand_name = sale["brand"]
                    stats = mlp.get(brands, brand_name)
 
                    if stats is None:
                        stats = {
                            "brand": brand_name,
                            "count": 0,
                            "price_sum": 0.0,
                            "revenue_sum": 0.0,
                            "max_revenue_sale": None
                        }
 
                        mlp.put(brands, brand_name, stats)
 
                    stats["count"] += 1
                    stats["price_sum"] += sale["final_price_usd"]
                    stats["revenue_sum"] += sale["revenue_usd"]
 
                    current = stats["max_revenue_sale"]
 
                    if (current is None or sale["revenue_usd"] > current["revenue_usd"]
                        or (sale["revenue_usd"] == current["revenue_usd"]
                            and sale["order_date"] > current["order_date"])):
 
                        stats["max_revenue_sale"] = sale
 
    heap = pq.new_heap(cmp_function=sort_crit_req_4)
 
    brand_names = mlp.key_set(brands)
 
    for i in range(al.size(brand_names)):
        name = al.get_element(brand_names, i)
        stats = mlp.get(brands, name)
 
        stats["price_avg"] = (stats["price_sum"] / stats["count"])
        stats["revenue_avg"] = (stats["revenue_sum"] / stats["count"])
        priority = (stats["count"], name)
        pq.insert(heap, priority, stats)
 
    result = al.new_list()
    while not pq.is_empty(heap) and al.size(result) < n:
        al.add_last(result, pq.remove(heap))
 
    end = get_time()
 
    return {
        "time": delta_time(start, end),
        "total_brands": al.size(result),
        "brands": result,
    }

def sort_crit_req_5(parent, child):
    """
    Mayor calificación promedio primero.
    En empate, marca alfabéticamente ascendente.
    """
    p1 = parent["priority"]
    p2 = child["priority"]

    if p1[0] != p2[0]:
        return p1[0] >= p2[0]

    return p1[1] <= p2[1]

def req_5(catalog, country, date_start, date_end, n):
    """
    Retorna el resultado del requerimiento 5: las N marcas con mejor
    calificación promedio en un país y un rango de fechas.
    """
    start = get_time()
    country_key = country.strip().lower()

    # 1. Filtrar las órdenes por fecha y país
    brands = mlp.new_map(20, 0.5)
    if date_start <= date_end:
        buckets = rbt.values(catalog["dates"], date_start, date_end)

        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)

            for j in range(al.size(bucket)):
                sale = al.get_element(bucket, j)

                if sale["country"].strip().lower() == country_key:
                    brand_name = sale["brand"]
                    stats = mlp.get(brands, brand_name)

                    if stats is None:
                        stats = {
                            "brand": brand_name,
                            "count": 0,
                            "rating_sum": 0.0,
                            "revenue_sum": 0.0,
                            "max_units_sale": None
                        }

                        mlp.put(brands, brand_name, stats)

                    stats["count"] += 1
                    stats["rating_sum"] += sale["customer_rating"]
                    stats["revenue_sum"] += sale["revenue_usd"]

                    # Mayor número de unidades; empate -> mayor order_id
                    current = stats["max_units_sale"]

                    if (current is None or sale["units_sold"] > current["units_sold"] 
                        or (sale["units_sold"] == current["units_sold"]
                            and sale["order_id"] > current["order_id"])):
                        
                        stats["max_units_sale"] = sale

    # 2. Promedios por marca y cola de prioridad
    heap = pq.new_heap(cmp_function=sort_crit_req_5)

    brand_names = mlp.key_set(brands)

    for i in range(al.size(brand_names)):
        name = al.get_element(brand_names, i)
        stats = mlp.get(brands, name)

        stats["rating_avg"] = (stats["rating_sum"] / stats["count"])
        stats["revenue_avg"] = (stats["revenue_sum"] / stats["count"])
        priority = (round(stats["rating_avg"], 6), name)
        pq.insert(heap, priority, stats)

    # 3. Extraer las N mejor calificadas 
    result = al.new_list()
    while not pq.is_empty(heap) and al.size(result) < n:
        al.add_last(result, pq.remove(heap))

    end = get_time()

    return {
        "time": delta_time(start, end),
        "total_brands": al.size(result),
        "brands": result,
    }


def req_6(catalog, date_start, date_end, price_min, price_max, n):
    """
    Retorna el resultado del requerimiento 6: las N marcas más consistentes
    (menor desviación estándar del discount_percent) para un rango de fechas
    y un rango de precios base.
    """
    start = get_time()

    # 1. Filtrar por fecha (RBT) y precio base; agrupar por marca
    brands = mlp.new_map(20, 0.5)
    if date_start <= date_end and price_min <= price_max:
        buckets = rbt.values(catalog["dates"], date_start, date_end)
        for i in range(al.size(buckets)):
            bucket = al.get_element(buckets, i)
            for j in range(al.size(bucket)):
                sale = al.get_element(bucket, j)
                if price_min <= sale["base_price_usd"] <= price_max:
                    brand_sales = mlp.get(brands, sale["brand"])
                    if brand_sales is None:
                        brand_sales = al.new_list()
                        mlp.put(brands, sale["brand"], brand_sales)
                    al.add_last(brand_sales, sale)

    # 2. Estadísticas por marca y cola de prioridad (min-heap)
    heap = pq.new_heap(True)
    brand_names = mlp.key_set(brands)
    total_brands = al.size(brand_names)
    for i in range(total_brands):
        name = al.get_element(brand_names, i)
        stats = brand_discount_stats(name, mlp.get(brands, name))
        # Menor desviación primero; empate -> menor promedio; luego nombre
        priority = (round(stats["std"], 9), round(stats["mean"], 9), name)
        pq.insert(heap, priority, stats)

    # 3. Extraer las N más consistentes
    result = al.new_list()
    while not pq.is_empty(heap) and al.size(result) < n:
        al.add_last(result, pq.remove(heap))

    end = get_time()
    return {
        "time": delta_time(start, end),
        "total_brands": total_brands,
        "brands": result,
    }


def brand_discount_stats(name, sales):
    """
    Calcula número de órdenes, promedio y desviación estándar poblacional
    del discount_percent, y la orden con descuento más cercano al promedio
    (empate -> menor order_id).
    """
    count = al.size(sales)
    total = 0.0
    for i in range(count):
        total += al.get_element(sales, i)["discount_percent"]
    mean = total / count

    squares = 0.0
    closest = None
    best_diff = None
    for i in range(count):
        sale = al.get_element(sales, i)
        x = sale["discount_percent"]
        squares += (x - mean) ** 2
        diff = abs(x - mean)
        if (closest is None
                or diff < best_diff - 1e-9
                or (abs(diff - best_diff) <= 1e-9
                    and order_number(sale["order_id"]) < order_number(closest["order_id"]))):
            closest = sale
            best_diff = diff
    std = math.sqrt(squares / count)

    return {
        "brand": name,
        "count": count,
        "mean": mean,
        "std": std,
        "closest": closest,
    }


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
