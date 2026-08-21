import json
import os
from typing import List
from modelos.producto import Producto

class ArchivoServicio:
    def __init__(self, ruta_archivo: str = "datos/productos.json") -> None:
        """
        Inicializa el servicio de manejo de archivos persistentes.
        """
        self._ruta: str = ruta_archivo

    def guardar_productos(self, productos: List[Producto]) -> None:
        """
        Guarda la lista de objetos Producto en el archivo JSON.
        Crea el directorio 'datos' automáticamente si no existe.
        
        :raises PermissionError: Si el sistema operativo deniega los permisos de escritura.
        """
        try:
            # Crear directorio si no existe
            directorio = os.path.dirname(self._ruta)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio, exist_ok=True)

            # Convertir objetos a diccionarios
            datos = [p.to_dict() for p in productos]
            
            with open(self._ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=4, ensure_ascii=False)
        except PermissionError:
            print(f"\n[Error de Permisos] No se poseen los permisos necesarios para escribir en: {self._ruta}")
        except Exception as e:
            print(f"\n[Error Inesperado] No se pudo guardar la colección de productos: {e}")

    def cargar_productos(self) -> List[Producto]:
        """
        Carga la colección de productos desde el archivo JSON y reconstruye los objetos Producto.
        Controla de forma específica las excepciones requeridas.
        
        :return: Lista de objetos Producto recuperados.
        """
        if not os.path.exists(self._ruta):
            print(f"\n[Carga] El archivo '{self._ruta}' no existe aún. Iniciando con colección vacía.")
            return []

        productos: List[Producto] = []
        try:
            with open(self._ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                
                if not isinstance(datos, list):
                    print("\n[Formato Inválido] El archivo JSON no contiene una lista de productos.")
                    return []

                for indice, item in enumerate(datos):
                    try:
                        # Reconstrucción del objeto Producto
                        producto = Producto.from_dict(item)
                        productos.append(producto)
                    except KeyError as ke:
                        # KeyError específico: un registro carece de claves esperadas
                        print(f"\n[Inconsistencia] Registro #{indice+1} omitido: {ke}")
                    except ValueError as ve:
                        # ValueError específico: un registro posee valores defectuosos
                        print(f"\n[Inconsistencia] Registro #{indice+1} contiene datos inválidos: {ve}")
                    except Exception as e:
                        print(f"\n[Inconsistencia] Registro #{indice+1} no se pudo procesar debido a un error: {e}")

        except FileNotFoundError:
            # Aunque se validó con exists(), controlamos FileNotFoundError por seguridad
            print(f"\n[Aviso] No se encontró el archivo '{self._ruta}'. Iniciando colección vacía.")
            return []
        except json.JSONDecodeError:
            # JSONDecodeError: El formato interno del archivo no es JSON válido
            print(f"\n[Error Crítico] El archivo '{self._ruta}' no posee un formato JSON válido.")
            print("El sistema iniciará con una colección vacía para proteger la ejecución.")
            return []
        except PermissionError:
            # PermissionError: Sin permisos para leer el archivo
            print(f"\n[Error de Permisos] No se tienen permisos de lectura para el archivo: {self._ruta}")
            return []
        except Exception as e:
            print(f"\n[Error Inesperado] No se pudo cargar el archivo debido a un fallo crítico: {e}")
            return []

        return productos
