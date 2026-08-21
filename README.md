# Restaurante App - Sistema de Gestión de Restaurante (Semana 10)

Este proyecto consiste en un sistema de consola modular en Python diseñado para administrar los productos y usuarios de un restaurante. Aplica principios de **Responsabilidad Única (SRP)** para separar la representación de los datos, la persistencia en disco y la lógica de interacción con el usuario.

---

## Características Principales

1. **Persistencia Física de Datos (Módulo JSON)**  
   * Los productos se guardan físicamente en un archivo `productos.json` dentro de la carpeta `datos/`.
   * Al iniciar la aplicación, se leen los datos persistidos y se reconstruyen como instancias de la clase `Producto` en memoria.
   * La persistencia es automática y se actualiza inmediatamente después de registrar, actualizar o eliminar un producto con éxito.

2. **Control Preventivo de Excepciones**  
   * **`FileNotFoundError`**: Si el archivo de almacenamiento no existe en la primera ejecución, el programa inicia de forma controlada con una lista vacía de productos.
   * **`json.JSONDecodeError`**: Evita la caída del sistema si el archivo JSON externo se encuentra corrupto o tiene un formato no válido.
   * **`PermissionError`**: Atrapa los errores del sistema operativo si no se poseen los permisos de lectura o escritura requeridos para el archivo.
   * **`KeyError`**: Detecta de forma selectiva si un registro del archivo JSON carece de alguna clave obligatoria, omitiendo dicho elemento corrupto y permitiendo la carga del resto de los datos sanos.
   * **`ValueError`**: Gestiona las validaciones de negocio en los modelos (como evitar precios negativos) y previene cierres si el usuario ingresa tipos de datos incorrectos por consola.

3. **Uso Justificado de Estructuras de Datos**  
   * **Listas (`list`)**: Colecciones dinámicas y mutables idóneas para almacenar y modificar la colección de productos y usuarios en memoria.
   * **Tuplas (`tuple`)**: Secuencias ordenadas e inmutables utilizadas para definir de forma fija y constante las opciones del menú de consola.
   * **Diccionarios (`dict`)**: Estructuras clave-valor empleadas para relacionar pedidos activos e implementar un mapeo directo de acciones desde el menú.
   * **Conjuntos (`set`)**: Colecciones mutables de elementos únicos utilizadas para filtrar y extraer de manera limpia todas las categorías existentes sin duplicaciones.

4. **Encapsulamiento y Diseño de Dominio (POO)**  
   * La clase `Producto` protege sus atributos internos mediante propiedades `@property` de solo lectura para el código único y setters controlados con validaciones estrictas para el precio, nombre y categoría.

---

## Estructura Completa del Proyecto

El sistema mantiene una arquitectura estrictamente modular y organizada por paquetes físicos:

```text
restaurante_app/
│
├── datos/
│   └── productos.json            # Archivo físico para persistir los datos de productos
│
├── modelos/
│   ├── __init__.py               # Archivo vacío que define el paquete de modelos
│   ├── producto.py               # Clase entidad de Producto y sus validaciones internas
│   └── usuario.py                # Clase entidad de Usuario (registro temporal en memoria)
│
├── servicios/
│   ├── __init__.py               # Archivo vacío que define el paquete de servicios
│   ├── archivo_servicio.py       # Encargado exclusivo de la persistencia de productos (lectura/escritura)
│   └── restaurante.py            # Servicio central que administra las colecciones y lógica de negocio
│
├── main.py                       # Punto de entrada; maneja el menú de consola y captura de datos
└── README.md                     # Documentación técnica del proyecto
```
