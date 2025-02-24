import os
from producto import Producto

class Inventario:
    def __init__(self, archivo_inventario="inventario.txt"):
        self.productos = []
        self.archivo_inventario = archivo_inventario
        self.cargar_inventario()

    def cargar_inventario(self):
        try:
            if os.path.exists(self.archivo_inventario):
                with open(self.archivo_inventario, "r") as archivo:
                    for linea in archivo:
                        id_producto, nombre, cantidad, precio = linea.strip().split(",")
                        producto = Producto(int(id_producto), nombre, int(cantidad), float(precio))
                        self.productos.append(producto)
                print("Inventario cargado desde el archivo.")
            else:
                print("El archivo de inventario no existe. Se creará uno nuevo.")
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.archivo_inventario}.")
        except PermissionError:
            print(f"Error: No tienes permisos para leer {self.archivo_inventario}.")
        except Exception as e:
            print(f"Error inesperado al cargar el inventario: {e}")

    def guardar_inventario(self):
        try:
            with open(self.archivo_inventario, "w") as archivo:
                for producto in self.productos:
                    archivo.write(f"{producto.get_id()},{producto.get_nombre()},{producto.get_cantidad()},{producto.get_precio()}\n")
            print("Inventario guardado en el archivo.")
        except PermissionError:
            print(f"Error: No tienes permisos para escribir en {self.archivo_inventario}.")
        except Exception as e:
            print(f"Error inesperado al guardar el inventario: {e}")

    def agregar_producto(self, producto):
        if self.buscar_producto_por_id(producto.get_id()) is None:
            self.productos.append(producto)
            self.guardar_inventario()
            print(f"Producto '{producto.get_nombre()}' agregado al inventario y guardado en el archivo.")
        else:
            print(f"Error: Ya existe un producto con el ID {producto.get_id()}.")

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto_por_id(id_producto)
        if producto:
            self.productos.remove(producto)
            self.guardar_inventario()
            print(f"Producto '{producto.get_nombre()}' eliminado del inventario y guardado en el archivo.")
        else:
            print(f"Error: No se encontró ningún producto con el ID {id_producto}.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        producto = self.buscar_producto_por_id(id_producto)
        if producto:
            if cantidad is not None:
                producto.set_cantidad(cantidad)
            if precio is not None:
                producto.set_precio(precio)
            self.guardar_inventario()
            print(f"Producto '{producto.get_nombre()}' actualizado y guardado en el archivo.")
        else:
            print(f"Error: No se encontró ningún producto con el ID {id_producto}.")

    def buscar_producto_por_nombre(self, nombre):
        resultados = []
        for producto in self.productos:
            if nombre.lower() in producto.get_nombre().lower():
                resultados.append(producto)
        return resultados

    def buscar_producto_por_id(self, id_producto):
        for producto in self.productos:
            if producto.get_id() == id_producto:
                return producto
        return None

    def mostrar_inventario(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            print("Inventario:")
            for producto in self.productos:
                print(producto)


from inventario import Inventario
from producto import Producto


def main():
    inventario = Inventario()

    while True:
        print("\n--- Menú ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar inventario")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        try:
            if opcion == '1':
                id_producto = int(input("ID del producto: "))
                nombre = input("Nombre del producto: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                producto = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(producto)
            elif opcion == '2':
                id_producto = int(input("ID del producto a eliminar: "))
                inventario.eliminar_producto(id_producto)
            elif opcion == '3':
                id_producto = int(input("ID del producto a actualizar: "))
                cantidad = input("Nueva cantidad (dejar en blanco para no cambiar): ")
                precio = input("Nuevo precio (dejar en blanco para no cambiar): ")
                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None
                inventario.actualizar_producto(id_producto, cantidad, precio)
            elif opcion == '4':
                nombre = input("Nombre a buscar: ")
                resultados = inventario.buscar_producto_por_nombre(nombre)
                if resultados:
                    print("Resultados de la búsqueda:")
                    for producto in resultados:
                        print(producto)
                else:
                    print("No se encontraron productos con ese nombre.")
            elif opcion == '5':
                inventario.mostrar_inventario()
            elif opcion == '6':
                break
            else:
                print("Opción no válida. Inténtalo de nuevo.")
        except ValueError:
            print("Error: Debes ingresar valores numéricos para ID, cantidad y precio.")


if __name__ == "__main__":
    main()