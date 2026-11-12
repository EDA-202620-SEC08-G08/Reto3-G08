import sys
from datetime import datetime

import App.logic as logic
from DataStructures.List import array_list as al

try:
    from tabulate import tabulate
except ImportError:  # Respaldo si tabulate no está instalado
    tabulate = None

default_limit = 1000
sys.setrecursionlimit(default_limit * 10)

DATA_FILES = {
    "1": "global_sports_footwear_sales-small.csv",
    "2": "global_sports_footwear_sales-medium.csv",
    "3": "global_sports_footwear_sales-large.csv",
}


def new_logic():
    """
        Se crea una instancia del controlador
    """
    return logic.new_logic()


def print_menu():
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")


# ---------------------------------------------------------------------------
# Utilidades de impresión
# ---------------------------------------------------------------------------

def fmt(value):
    if isinstance(value, float):
        return f"{value:,.2f}"
    return value


def print_table(rows, headers):
    """
    Imprime una tabla (lista de listas de Python) con tabulate o, si no está
    disponible, con un formato de columnas simple.
    """
    rows = [[fmt(v) for v in r] for r in rows]
    if tabulate is not None:
        print(tabulate(rows, headers=headers, tablefmt="grid"))
        return
    widths = [len(str(h)) for h in headers]
    for r in rows:
        for i, v in enumerate(r):
            widths[i] = max(widths[i], len(str(v)))
    sep = "+" + "+".join("-" * (w + 2) for w in widths) + "+"
    print(sep)
    print("| " + " | ".join(str(h).ljust(w) for h, w in zip(headers, widths)) + " |")
    print(sep.replace("-", "="))
    for r in rows:
        print("| " + " | ".join(str(v).ljust(w) for v, w in zip(r, widths)) + " |")
        print(sep)


def sales_to_rows(sales, fields):
    """
    Convierte un array_list de ventas a filas; si tiene más de 10 elementos
    solo toma los 5 primeros y los 5 últimos.
    """
    n = al.size(sales)
    if n > 10:
        positions = list(range(5)) + list(range(n - 5, n))
    else:
        positions = list(range(n))
    rows = []
    for pos in positions:
        sale = al.get_element(sales, pos)
        rows.append([sale[f] for f in fields])
    return rows


def read_float(message):
    while True:
        try:
            return float(input(message).strip().replace(",", "."))
        except ValueError:
            print("Valor inválido, ingrese un número.")


def read_int(message):
    while True:
        try:
            return int(input(message).strip())
        except ValueError:
            print("Valor inválido, ingrese un número entero.")


def read_date(message):
    while True:
        text = input(message).strip()
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Fecha inválida, use el formato AAAA-MM-DD.")


def is_loaded(control):
    if logic.get_sale_count(control) == 0:
        print("\nPrimero debe cargar la información (opción 0).\n")
        return False
    return True


# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------

def load_data(control):
    """
    Carga los datos
    """
    print("\nArchivos disponibles:")
    print("1- small")
    print("2- medium")
    print("3- large")
    option = input("Seleccione el tamaño del archivo: ").strip()
    filename = DATA_FILES.get(option)
    if filename is None:
        print("Opción incorrecta\n")
        return control

    # Se crea un catálogo nuevo para no mezclar cargas anteriores
    control.clear()
    control.update(logic.new_logic())
    result = logic.load_data(control, filename)

    print(f"\nArchivo cargado: {filename}")
    print(f"Tiempo de carga: {result['time']:.2f} milisegundos")
    print(f"Total de ventas cargadas: {result['total']}")

    if result["total"] == 0:
        print("\nNo se encontraron ventas en el archivo\n")
        return control

    price_fields = [
        ("order_id", "order_id"),
        ("brand", "Marca"),
        ("model_name", "Modelo"),
        ("category", "Categoría"),
        ("final_price_usd", "Precio final (USD)"),
        ("country", "País"),
    ]
    print("\nVENTA CON MENOR PRECIO FINAL")
    print_sale(result["min_sale"], price_fields)

    print("\nVENTA CON MAYOR PRECIO FINAL")
    print_sale(result["max_sale"], price_fields)

    fields = [
        ("order_id", "order_id"),
        ("order_date", "Fecha de la orden"),
        ("brand", "Marca"),
        ("model_name", "Modelo"),
        ("category", "Categoría"),
        ("final_price_usd", "Precio final (USD)"),
        ("units_sold", "Unidades vendidas"),
        ("revenue_usd", "Ingreso generado (USD)"),
        ("country", "País"),
        ("sales_channel", "Canal de venta"),
    ]
    print("\nPRIMERAS CINCO VENTAS")
    for i in range(al.size(result["first"])):
        print(f"\nVenta {i + 1}")
        print_sale(al.get_element(result["first"], i), fields)

    print("\nÚLTIMAS CINCO VENTAS")
    for i in range(al.size(result["last"])):
        print(f"\nVenta {i + 1}")
        print_sale(al.get_element(result["last"], i), fields)
    print()
    return control


def print_first_last(sales, fields):
    """
    Imprime las ventas de la lista; si hay más de 10, solo las 5 primeras
    y las 5 últimas.
    """
    n = al.size(sales)
    if n > 10:
        print("\nSe muestran las 5 primeras y las 5 últimas órdenes")
        positions = list(range(5)) + list(range(n - 5, n))
    else:
        positions = list(range(n))
    for pos in positions:
        print(f"\nOrden {pos + 1}")
        print_sale(al.get_element(sales, pos), fields)


def print_sale(sale, fields):
    """
    Imprime una venta en formato 'Campo: valor', un campo por línea.
    """
    for key, label in fields:
        value = sale[key]
        if isinstance(value, float):
            value = f"{value:.2f}"
        print(f"{label}: {value}")


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    sales = control["sales"]
    for i in range(al.size(sales)):
        sale = al.get_element(sales, i)
        if sale["order_id"] == id:
            print_table([[k, v] for k, v in sale.items()], ["Campo", "Valor"])
            return
    print(f"No se encontró la orden {id}")


# ---------------------------------------------------------------------------
# Requerimientos
# ---------------------------------------------------------------------------

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    if not is_loaded(control):
        return
    brand = input("Nombre de la marca: ").strip()
    d_min = read_float("Porcentaje de descuento mínimo: ")
    d_max = read_float("Porcentaje de descuento máximo: ")

    result = logic.req_1(control, brand, d_min, d_max)

    print(f"\nREQUERIMIENTO 1: {brand} con descuento entre {d_min} y {d_max}")
    print(f"Tiempo de ejecución: {result['time']:.2f} milisegundos")
    print(f"Total de órdenes que cumplen el filtro: {result['total']}")
    print(f"Costo total final (USD): {result['total_cost']:.2f}")

    if result["total"] == 0:
        print("\nNo se encontraron órdenes con esos criterios.\n")
        return

    fields = [
        ("order_id", "order_id"),
        ("order_date", "Fecha de la orden"),
        ("brand", "Marca"),
        ("model_name", "Modelo"),
        ("category", "Categoría"),
        ("country", "País"),
        ("sales_channel", "Canal de venta"),
        ("discount_percent", "Descuento (%)"),
        ("final_price_usd", "Precio final (USD)"),
    ]
    print_first_last(result["orders"], fields)
    print()


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    if not is_loaded(control):
        return

    country = input("Nombre del país: ").strip()
    rating_min = read_float("Calificación mínima: ")
    rating_max = read_float("Calificación máxima: ")

    result = logic.req_2(
        control,
        country,
        rating_min,
        rating_max
    )

    print("\nREQUERIMIENTO 2")
    print(f"Tiempo de ejecución: {result['time']:.2f} milisegundos")
    print(f"Total de órdenes que cumplen el filtro: {result['total']}")
    print(f"Costo total final (USD): {result['total_cost']:.2f}")

    if result["total"] == 0:
        print("\nNo se encontraron órdenes.\n")
        return

    fields = [
        ("order_id", "Identificador de la orden"),
        ("order_date", "Fecha de la orden"),
        ("brand", "Marca"),
        ("model_name", "Modelo"),
        ("country", "País"),
        ("sales_channel", "Canal de venta"),
        ("customer_rating", "Calificación del cliente"),
        ("final_price_usd", "Precio final (USD)"),
        ("revenue_usd", "Ingresos totales"),
    ]

    print_first_last(result["orders"], fields)
    print()


def print_req_3(control):
    """
        Funcion que imprime la solucion del Requerimiento 3 en consola
    """
    if not is_loaded(control):
        return
    channel = input("Canal de venta (Online / Retail Store): ").strip()
    category = input("Categoria del producto: ").strip()
    p_min = read_float("Precio final minimo (USD): ")
    p_max = read_float("Precio final maximo (USD): ")
 
    result = logic.req_3(control, channel, category, p_min, p_max)
 
    print(f"\nREQUERIMIENTO 3: canal {channel}, categoria {category}, "
          f"precio final entre {p_min} y {p_max}")
    print(f"Tiempo de ejecucion: {result['time']:.2f} milisegundos")
    print(f"Total de ordenes que cumplen el filtro: {result['total']}")
    print(f"Costo total final (USD): {result['total_cost']:.2f}")
 
    if result["total"] == 0:
        print("\nNo se encontraron ordenes con esos criterios.\n")
        return
 
    fields = [
        ("order_id", "order_id"),
        ("order_date", "Fecha de la orden"),
        ("brand", "Marca"),
        ("model_name", "Modelo"),
        ("category", "Categoria"),
        ("sales_channel", "Canal de venta"),
        ("country", "Pais"),
        ("final_price_usd", "Precio final (USD)"),
        ("units_sold", "Unidades vendidas"),
    ]
    print_first_last(result["orders"], fields)
    print()


def print_req_4(control):
    """
        Funcion que imprime la solucion del Requerimiento 4 en consola
    """
    if not is_loaded(control):
        return
 
    date_start = read_date("Fecha inicial (AAAA-MM-DD): ")
    date_end = read_date("Fecha final (AAAA-MM-DD): ")
    income_level = input("Nivel de ingresos del cliente (Low / Medium / High): ").strip()
    n = read_int("Cantidad N de marcas: ")
 
    result = logic.req_4(control, date_start, date_end, income_level, n)
 
    print(f"\nREQUERIMIENTO 4: fechas entre {date_start} y {date_end}, "
          f"nivel de ingresos {income_level}, N = {n}")
    print(f"Tiempo de ejecucion: {result['time']:.2f} milisegundos")
    print(f"Número de marcas consideradas: {result['total_brands']}")
 
    if result["total_brands"] == 0:
        print("\nNo se encontraron marcas.\n")
        return
 
    for i in range(al.size(result["brands"])):
        brand = al.get_element(result["brands"], i)
        sale = brand["max_revenue_sale"]
 
        print(f"\nMARCA {i + 1}")
        print(f"Nombre de la marca: {brand['brand']}")
        print(f"Total de ordenes: {brand['count']}")
        print(f"Precio final promedio (USD): {brand['price_avg']:.2f}")
        print(f"Ingreso generado promedio (USD): {brand['revenue_avg']:.2f}")
 
        print("\nOrden con mayor ingreso generado:")
        print(f"Identificador: {sale['order_id']}")
        print(f"Fecha: {sale['order_date']}")
        print(f"Marca y modelo: {sale['brand']} - {sale['model_name']}")
        print(f"Pais: {sale['country']}")
        print(f"Canal de venta: {sale['sales_channel']}")
        print(f"Precio final (USD): {sale['final_price_usd']:.2f}")
        print(f"Ingreso generado (USD): {sale['revenue_usd']:.2f}")
 
    print()


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    if not is_loaded(control):
        return

    country = input("Nombre del país: ").strip()
    date_start = read_date("Fecha inicial (AAAA-MM-DD): ")
    date_end = read_date("Fecha final (AAAA-MM-DD): ")
    n = read_int("Cantidad N de marcas: ")

    result = logic.req_5(control, country, date_start, date_end, n)

    print("\nREQUERIMIENTO 5")
    print(f"Tiempo de ejecución: {result['time']:.2f} milisegundos")
    print(f"Número de marcas consideradas: {result['total_brands']}")

    if result["total_brands"] == 0:
        print("\nNo se encontraron marcas.\n")
        return

    for i in range(al.size(result["brands"])):
        brand = al.get_element(result["brands"], i)
        sale = brand["max_units_sale"]

        print(f"\nMARCA {i + 1}")
        print(f"Nombre de la marca: {brand['brand']}")
        print(f"Total de órdenes: {brand['count']}")
        print(f"Calificación promedio: {brand['rating_avg']:.4f}")
        print(f"Ingreso generado promedio (USD): {brand['revenue_avg']:.2f}")

        print("\nOrden con mayor número de unidades vendidas:")
        print(f"Identificador: {sale['order_id']}")
        print(f"Fecha: {sale['order_date']}")
        print(f"Marca: {sale['brand']}")
        print(f"Modelo: {sale['model_name']}")
        print(f"País: {sale['country']}")
        print(f"Canal de venta: {sale['sales_channel']}")
        print(f"Unidades vendidas: {sale['units_sold']}")
        print(f"Calificación del cliente: {sale['customer_rating']:.2f}")

    print()


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    if not is_loaded(control):
        return
    date_start = read_date("Fecha inicial (AAAA-MM-DD): ")
    date_end = read_date("Fecha final (AAAA-MM-DD): ")
    p_min = read_float("Precio base mínimo (USD): ")
    p_max = read_float("Precio base máximo (USD): ")
    n = read_int("Cantidad N de marcas a mostrar: ")

    result = logic.req_6(control, date_start, date_end, p_min, p_max, n)

    print(f"\nREQUERIMIENTO 6: fechas entre {date_start} y {date_end}, "
          f"precio base entre {p_min} y {p_max}, N = {n}")
    print(f"Tiempo de ejecución: {result['time']:.2f} milisegundos")
    print(f"Total de marcas resultado del filtro: {result['total_brands']}")

    if al.size(result["brands"]) == 0:
        print("\nNo se encontraron órdenes con esos criterios.\n")
        return

    print(f"\nLAS {al.size(result['brands'])} MARCAS MÁS CONSISTENTES")
    for i in range(al.size(result["brands"])):
        b = al.get_element(result["brands"], i)
        c = b["closest"]
        print(f"\nMarca {i + 1}")
        print(f"Nombre de la marca: {b['brand']}")
        print(f"Órdenes analizadas: {b['count']}")
        print(f"Descuento promedio (%): {b['mean']:.2f}")
        print(f"Consistencia (desviación estándar, pp): {b['std']:.2f}")
        print("Orden con descuento más cercano al promedio:")
        print(f"  order_id: {c['order_id']}")
        print(f"  Fecha de la orden: {c['order_date']}")
        print(f"  Marca y modelo: {c['brand']} - {c['model_name']}")
        print(f"  País y canal de venta: {c['country']} - {c['sales_channel']}")
        print(f"  Descuento (%): {c['discount_percent']:.2f}")
    print()


# Se crea la lógica asociado a la vista
control = new_logic()

# main del ejercicio
def main():
    """
    Menu principal
    """
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n').strip()
        if not inputs.isdigit():
            print("Opción errónea, vuelva a elegir.\n")
            continue
        option = int(inputs)
        if option == 0:
            print("Cargando información de los archivos ....\n")
            load_data(control)
        elif option == 1:
            print_req_1(control)

        elif option == 2:
            print_req_2(control)

        elif option == 3:
            print_req_3(control)

        elif option == 4:
            print_req_4(control)

        elif option == 5:
            print_req_5(control)

        elif option == 6:
            print_req_6(control)

        elif option == 7:
            working = False
            print("\nGracias por utilizar el programa")
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
