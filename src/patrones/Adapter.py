# Crea un programa que conecte una interfaz de base de datos antigua 
# con una nueva interfaz de base de datos utilizando un adaptador.

#SOLUCION: Es necesario usar el patrón Adapter.

# Interfaz esperada por la nueva aplicación
class NewDatabaseInterface:
    def connect(self):
        raise NotImplementedError("Debe implementar el método connect()")

    def execute_query(self, query: str):
        raise NotImplementedError("Debe implementar el método execute_query()")
    

# Interfaz antigua (de un sistema legado)
class OldDatabase:
    def open_connection(self):
        print("Conexión abierta con base de datos antigua.")

    def run_sql(self, sql: str):
        print(f"Ejecutando en sistema antiguo: {sql}")


# Adaptador que permite usar OldDatabase como si fuera NewDatabaseInterface
# hereda de la nueva interfaz, porque es lo que queremos ofrecer, 
# pero se relaciona con la legacy, porque  al final interactuamos con ella (Slide 26)

# El adaptador no hereda de la clase original, sino que la contiene. En este caso, DatabaseAdapter 
# no hereda de OldDatabase, sino que tiene un atributo 
# self.old_db que es una instancia de OldDatabase. Por eso es un patron adapter de objeto.

# Si heredase, seria de clase, y aunque seria posible, heredar de una clase que es legacy, 
# podria no ser lo correcto (mejor desacoplarlo -> mejor flexibilidad y compatibilidad futura)-
class DatabaseAdapter(NewDatabaseInterface):
    def __init__(self, old_db: OldDatabase):
        self.old_db = old_db

    def connect(self):
        print("Adaptador traduce 'connect' a 'open_connection'")
        self.old_db.open_connection()

    def execute_query(self, query: str):
        print("Adaptador traduce 'execute_query' a 'run_sql'")
        self.old_db.run_sql(query)

# Cliente que espera una base de datos con la nueva interfaz
class App:
    def __init__(self, db: NewDatabaseInterface):
        self.db = db

    def run(self):
        self.db.connect()
        self.db.execute_query("SELECT * FROM usuarios")


# Simulación
if __name__ == "__main__":
    # Sistema legado que no queremos reescribir
    old_db = OldDatabase()

    # Lo adaptamos para que se comporte como la nueva interfaz
    adapted_db = DatabaseAdapter(old_db)

    # La aplicación trabaja con la nueva interfaz sin saber que usa una base de datos vieja
    app = App(adapted_db)
    app.run()


#Ejemplo adapter de clase (no recomendado pero posible)
"""
class DatabaseAdapter(OldDatabase, NewDatabaseInterface):
    def connect(self):
        print("Adaptador traduce 'connect' a 'open_connection'")
        self.open_connection()

    def execute_query(self, query: str):
        print("Adaptador traduce 'execute_query' a 'run_sql'")
        self.run_sql(query)

"""


#por que no el patron proxy?   Se usa cuando ya tienes compatibilidad de interfaces y solo quieres añadir lógica extra alrededor del objeto. No adapta nada, simplemente "vigila" o "controla" el acceso al objeto real.
