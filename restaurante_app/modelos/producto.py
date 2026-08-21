class Producto:
    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float) -> None:
        """
        Inicializa un objeto de tipo Producto realizando validaciones estrictas.
        
        :raises ValueError: Si los campos de texto están vacíos o el precio es negativo.
        """
        if not codigo or not codigo.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not categoria or not categoria.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        if precio < 0:
            raise ValueError("El precio del producto no puede ser un valor negativo.")

        self._codigo: str = codigo.strip()
        self._nombre: str = nombre.strip()
        self._categoria: str = categoria.strip()
        self._precio: float = precio

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede modificarse a un valor vacío.")
        self._nombre = valor.strip()

    @property
    def categoria(self) -> str:
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("La categoría no puede modificarse a un valor vacío.")
        self._categoria = valor.strip()

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        if valor < 0:
            raise ValueError("El precio no puede modificarse a un valor negativo.")
        self._precio = valor

    def to_dict(self) -> dict:
        """
        Convierte la información del objeto Producto a un diccionario para poder guardarla en JSON.
        """
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "categoria": self._categoria,
            "precio": self._precio
        }

    @classmethod
    def from_dict(cls, datos: dict) -> "Producto":
        """
        Reconstruye una instancia de Producto a partir de un diccionario de datos.
        
        :raises KeyError: Si falta alguna clave esperada en el diccionario.
        :raises ValueError: Si los valores de las claves son inválidos.
        """
        try:
            return cls(
                codigo=datos["codigo"],
                nombre=datos["nombre"],
                categoria=datos["categoria"],
                precio=float(datos["precio"])
            )
        except KeyError as e:
            raise KeyError(f"Falta el campo obligatorio {e} en los datos del producto.")
        except ValueError as e:
            raise ValueError(f"Formato de datos incorrecto en el diccionario del producto: {e}")

    def mostrar_informacion(self) -> str:
        """
        Retorna la representación legible de la información de este producto.
        """
        return f"[{self._codigo}] {self._nombre} ({self._categoria}) - ${self._precio:.2f}"
       