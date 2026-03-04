#1. Implementa un sistema que permita tener una única instancia de la clase ConexionBD que da acceso a una determinada base de datos. 

# SOLUCION: Requiere del patrón Singleton

class ConexionBD:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __init__(self, nombre_bd):
        # Esta clase solo debe ser instanciada una vez
        if ConexionBD._instance is not None:
            raise Exception("¡Esta clase es un Singleton! Utilice 'get_instance()' para obtener la instancia.")
        
        # Inicialización de la conexión a la base de datos con el nombre proporcionado
        self.nombre_bd = nombre_bd
        print(f"Conexión establecida a la base de datos: {self.nombre_bd}")

    @classmethod
    def get_instance(cls, nombre_bd):
        # Método de clase para obtener la instancia única de la clase ConexionBD
        if cls._instance is None:
            cls._instance = cls(nombre_bd)
        return cls._instance

# Ejemplo de uso del Singleton
def main():
    # Intentar crear una instancia directamente causará un error
    # conexion = ConexionBD("MiBaseDeDatos")  # Esto lanzará una excepción

    # Obtener la instancia única usando el método get_instance
    instancia1 = ConexionBD.get_instance("MiBaseDeDatos")
    instancia2 = ConexionBD.get_instance("OtraBaseDeDatos")

    # Ambas variables hacen referencia a la misma instancia
    print(instancia1 is instancia2)  # True, son la misma instancia

if __name__ == "__main__":
    main()