from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante
from servicios.archivo_servicio import ArchivoServicio

# TUPLA: Estructura inmutable para representar las opciones estables del menú principal.
OPCIONES_MENU = (
    ("1", "Registrar producto"),
    ("2", "Buscar producto"),
    ("3", "Actualizar producto"),
    ("4", "Eliminar producto"),
    ("5", "Listar productos"),
    ("6", "Registrar usuario"),
    ("7", "Listar usuarios"),
    ("8", "Mostrar categorías"),
    ("9", "Salir"),
)

def mostrar_encabezado() -> None:
    """
    Imprime en pantalla la interfaz visual del menú principal.
    """
    print("\n" + "=" * 40)
    print("        SISTEMA DE RESTAURANTE")
    print("=" * 40)
    for indice, (num, desc) in enumerate(OPCIONES_MENU):
        # Insertar separadores visuales para que se adapte al diseño solicitado
        if num == "6" or num == "8":
            print("-" * 40)
        print(f"{num}. {desc}")
    print("=" * 40)

def registrar_producto_consola(servicio: Restaurante, archivo_srv: ArchivoServicio) -> None:
    print("\n--- [1] REGISTRAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto: ")
    nombre = input("Ingrese el nombre del producto: ")
    categoria = input("Ingrese la categoría del producto: ")
    
    try:
        precio_raw = input("Ingrese el precio del producto: ")
        precio = float(precio_raw)
    except ValueError:
        raise ValueError("El precio debe ser un número decimal o entero válido.")

    # Crea el objeto Producto (lanzará ValueError si las validaciones del modelo no se cumplen)
    nuevo_producto = Producto(codigo, nombre, categoria, precio)
    
    if servicio.registrar_producto(nuevo_producto):
        # Persistencia automática inmediata tras registrar
        archivo_srv.guardar_productos(servicio.listar_productos())
        print("\n✓ ¡Éxito! Producto registrado y guardado de manera persistente.")
    else:
        print("\n⚠ Error: Ya existe un producto registrado con ese código.")

def buscar_producto_consola(servicio: Restaurante) -> None:
    print("\n--- [2] BUSCAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto a buscar: ")
    producto = servicio.buscar_producto(codigo)
    
    if producto:
        print(f"\nResultado de búsqueda:\n  {producto.mostrar_informacion()}")
    else:
        print("\n⚠ Producto no encontrado.")

def actualizar_producto_consola(servicio: Restaurante, archivo_srv: ArchivoServicio) -> None:
    print("\n--- [3] ACTUALIZAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto que desea actualizar: ")
    producto_existente = servicio.buscar_producto(codigo)
    
    if not producto_existente:
        print("\n⚠ No se encontró ningún producto con el código proporcionado.")
        return

    print(f"Producto actual: {producto_existente.mostrar_informacion()}")
    nuevo_nombre = input("Ingrese el nuevo nombre: ")
    nueva_categoria = input("Ingrese la nueva categoría: ")
    
    try:
        precio_raw = input("Ingrese el nuevo precio: ")
        nuevo_precio = float(precio_raw)
    except ValueError:
        raise ValueError("El precio debe ser un número decimal o entero válido.")

    # El servicio valida e intenta actualizar
    if servicio.actualizar_producto(codigo, nuevo_nombre, nueva_categoria, nuevo_precio):
        # Sincronización con el archivo JSON
        archivo_srv.guardar_productos(servicio.listar_productos())
        print("\n✓ ¡Éxito! Producto actualizado y sincronizado en productos.json.")
    else:
        print("\n⚠ No se pudo actualizar el producto.")

def eliminar_producto_consola(servicio: Restaurante, archivo_srv: ArchivoServicio) -> None:
    print("\n--- [4] ELIMINAR PRODUCTO ---")
    codigo = input("Ingrese el código del producto a eliminar: ")
    
    if servicio.eliminar_producto(codigo):
        # Sincronización inmediata con el archivo JSON
        archivo_srv.guardar_productos(servicio.listar_productos())
        print("\n✓ ¡Éxito! Producto eliminado de la base de datos.")
    else:
        print("\n⚠ No se encontró ningún producto con el código proporcionado.")

def listar_productos_consola(servicio: Restaurante) -> None:
    print("\n--- [5] LISTADO DE PRODUCTOS ---")
    productos = servicio.listar_productos()
    
    if not productos:
        print("No hay productos registrados en el sistema.")
    else:
        for p in productos:
            print(f"- {p.mostrar_informacion()}")

def registrar_usuario_consola(servicio: Restaurante) -> None:
    print("\n--- [6] REGISTRAR USUARIO ---")
    identificacion = input("Ingrese la identificación única: ")
    nombre = input("Ingrese el nombre del usuario: ")
    correo = input("Ingrese el correo electrónico: ")
    
    # Crea el objeto Usuario (lanzará ValueError si las validaciones del modelo fallan)
    nuevo_usuario = Usuario(identificacion, nombre, correo)
    
    if servicio.registrar_usuario(nuevo_usuario):
        print("\n✓ ¡Éxito! Usuario registrado en memoria.")
    else:
        print("\n⚠ Error: Ya existe un usuario registrado con esa identificación.")

def listar_usuarios_consola(servicio: Restaurante) -> None:
    print("\n--- [7] LISTADO DE USUARIOS (EN MEMORIA) ---")
    usuarios = servicio.listar_usuarios()
    
    if not usuarios:
        print("No hay usuarios registrados en memoria para esta sesión.")
    else:
        for u in usuarios:
            print(f"- {u.mostrar_informacion()}")

def mostrar_categorias_consola(servicio: Restaurante) -> None:
    print("\n--- [8] CATEGORÍAS DISPONIBLES ---")
    # El método obtener_categorias_unicas() devuelve un set, garantizando unicidad
    categorias = servicio.obtener_categorias_unicas()
    
    if not categorias:
        print("No hay categorías disponibles en este momento.")
    else:
        print("Categorías registradas (sin repetir):")
        for cat in sorted(categorias):
            print(f"  * {cat}")

def main() -> None:
    # 1. Instanciación del helper para persistencia
    archivo_srv = ArchivoServicio()
    
    # 2. Carga inicial desde JSON al arrancar
    productos_cargados = archivo_srv.cargar_productos()
    
    # 3. Inicialización del servicio restaurante con la lista de productos reconstruidos
    servicio = Restaurante(productos_cargados)

    # 4. Bucle principal de ejecución
    while True:
        mostrar_encabezado()
        opcion = input("Seleccione una opción (1-9): ").strip()

        if opcion == "9":
            print("\nGuardando sesión y cerrando sistema restaurante_app... ¡Hasta pronto!")
            break

        try:
            if opcion == "1":
                registrar_producto_consola(servicio, archivo_srv)
            elif opcion == "2":
                buscar_producto_consola(servicio)
            elif opcion == "3":
                actualizar_producto_consola(servicio, archivo_srv)
            elif opcion == "4":
                eliminar_producto_consola(servicio, archivo_srv)
            elif opcion == "5":
                listar_productos_consola(servicio)
            elif opcion == "6":
                registrar_usuario_consola(servicio)
            elif opcion == "7":
                listar_usuarios_consola(servicio)
            elif opcion == "8":
                mostrar_categorias_consola(servicio)
            else:
                print("\n⚠ Opción inválida. Por favor, seleccione un número entre 1 y 9.")
        except ValueError as ve:
            # Control específico de ValueError para impedir detenciones abruptas por datos inválidos
            print(f"\n⚠ Error de Validación: {ve}")
        except Exception as e:
            # Captura cualquier error inesperado para evitar que el programa se cuelgue
            print(f"\n⚠ Ocurrió un error inesperado en la interacción: {e}")

if __name__ == "__main__":
    main()