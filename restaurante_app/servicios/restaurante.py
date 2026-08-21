from typing import List, Optional, Set
from modelos.producto import Producto
from modelos.usuario import Usuario

class Restaurante:
    def __init__(self, productos_iniciales: List[Producto]) -> None:
        """
        Inicializa el servicio Restaurante con productos persistidos.
        """
        self._productos: List[Producto] = productos_iniciales
        self._usuarios: List[Usuario] = []

    # --- Operaciones de Productos (CRUD) ---
    def registrar_producto(self, producto: Producto) -> bool:
        """
        Registra un producto en la colección asegurando que no existan códigos duplicados.
        
        :return: True si se registró con éxito, False si el código ya existe.
        """
        if self.buscar_producto(producto.codigo) is not None:
            return False
    def nombre(self) -> str:
        self._productos.append
        return True

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código (sin importar espacios en blanco).
        """
        codigo_limpio = codigo.strip()
        for producto in self._productos:
            if producto.codigo == codigo_limpio:
                return producto
        return None

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nueva_categoria: str, nuevo_precio: float) -> bool:
        """
        Actualiza los atributos de un producto existente. Las validaciones ocurren dentro del modelo.
        
        :return: True si se actualizó con éxito, False si el producto no existe.
        :raises ValueError: Si los nuevos valores ingresados no pasan las validaciones.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        
        # Validar preventivamente creando una instancia temporal
        # Esto asegura que si hay un error de validación, no se altere a medias el objeto original
        validador = Producto(codigo, nuevo_nombre, nueva_categoria, nuevo_precio)
        
        producto.nombre = validador.nombre
        producto.categoria = validador.categoria
        producto.precio = validador.precio
        return True

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto de la colección por su código.
        
        :return: True si se eliminó con éxito, False si el producto no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            return False
        self._productos.remove(producto)
        return True

    def listar_productos(self) -> List[Producto]:
        """
        Retorna una copia superficial de la lista de productos por motivos de seguridad y encapsulación.
        """
        return self._productos.copy()

    # --- Operaciones de Categorías (set) ---
    def obtener_categorias_unicas(self) -> Set[str]:
        """
        Utiliza un conjunto (set) para garantizar que las categorías se obtengan sin duplicados.
        """
        return {p.categoria for p in self._productos}

    # --- Operaciones de Usuarios ---
    def registrar_usuario(self, usuario: Usuario) -> bool:
        """
        Registra un usuario en la colección asegurando que no existan identificaciones duplicadas.
        
        :return: True si se registró con éxito, False si la identificación ya existe.
        """
        for u in self._usuarios:
            if u.identificacion == usuario.identificacion:
                return False
        self._usuarios.append(usuario)
        return True

    def listar_usuarios(self) -> List[Usuario]:
        """
        Retorna una copia de la lista de usuarios.
        """
        return self._usuarios.copy()
