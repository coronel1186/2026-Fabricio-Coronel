class Usuario:
    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        """
        Inicializa un objeto de tipo Usuario realizando validaciones estrictas.
        
        :raises ValueError: Si alguno de los campos de texto está vacío.
        """
        if not identificacion or not identificacion.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        if not correo or not correo.strip():
            raise ValueError("El correo del usuario no puede estar vacío.")

        self._identificacion: str = identificacion.strip()
        self._nombre: str = nombre.strip()
        self._correo: str = correo.strip()

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El nombre no puede modificarse a un valor vacío.")
        self._nombre = valor.strip()

    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not valor or not valor.strip():
            raise ValueError("El correo no puede modificarse a un valor vacío.")
        self._correo = valor.strip()

    def mostrar_informacion(self) -> str:
        """
        Retorna la representación legible de la información de este usuario.
        """