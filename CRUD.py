import json, os, pymysql, psycopg2, getpass


# Archivo donde se almacenarán los datos JSON
FILE_NAME = "data.json"
# Archivo donde se almacenarán las credenciales de la Base de Datos
CREDENCIALES_FILE = "credenciales.json"

# Clase Padre para todas las Bases de Datos
class BaseDeDatos:
    def crear(self, producto="", precio=0.0):
        raise NotImplementedError

    def leer(self):
        raise NotImplementedError

    def actualizar(self, index, nuevo_producto=None, nuevo_precio=None):
        raise NotImplementedError

    def eliminar(self, index):
        raise NotImplementedError

# Clase Hijo para la Base de Datos MySQL
class BaseDeDatosMySQL(BaseDeDatos):
    def __init__(self, host, user, password, database):
        # Conectar sin especificar la base de datos para verificar y crearla si no existe
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        self.connection.commit()
        self.connection.close()

        # Conectar a la base de datos específica
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INT AUTO_INCREMENT PRIMARY KEY,
                producto VARCHAR(255),
                precio FLOAT
            )
        """)
        self.connection.commit()

    # Crea el Producto en la Base de Datos
    def crear(self, producto="", precio=0.0):
        self.cursor.execute(
            "INSERT INTO productos (producto, precio) VALUES (%s, %s)", (producto, precio))
        self.connection.commit()
        print(f"'{producto}' con precio {precio} ha sido creado.")

    # Lee el Producto en la Base de Datos
    def leer(self):
        self.cursor.execute("SELECT id, producto, precio FROM productos")
        results = self.cursor.fetchall()
        if not results:
            print("No hay datos para mostrar.")
        else:
            for row in results:
                print(f"{row[0]}. Producto: {row[1]}, Precio: {row[2]}")

    # Actualiza el Producto en la Base de Datos
    def actualizar(self, index, nuevo_producto=None, nuevo_precio=None):
        if nuevo_producto is not None and nuevo_precio is not None:
            self.cursor.execute(
                "UPDATE productos SET producto=%s, precio=%s WHERE id=%s", (nuevo_producto, nuevo_precio, index))
        elif nuevo_producto is not None:
            self.cursor.execute(
                "UPDATE productos SET producto=%s WHERE id=%s", (nuevo_producto, index))
        elif nuevo_precio is not None:
            self.cursor.execute(
                "UPDATE productos SET precio=%s WHERE id=%s", (nuevo_precio, index))
        self.connection.commit()
        print(f"Elemento {index} ha sido actualizado.")

    # Elimina el Producto en la Base de Datos
    def eliminar(self, index):
        self.cursor.execute("DELETE FROM productos WHERE id=%s", (index,))
        self.connection.commit()
        print(f"Elemento {index} ha sido eliminado.")

# Clase Hijo para la Base de Datos PostgreSQL
class BaseDeDatosPostgreSQL(BaseDeDatos):
    def __init__(self, host, user, password, database):
        # Conectar sin especificar la base de datos para verificar y crearla si no existe
        self.connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            dbname=database
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                producto VARCHAR(255),
                precio FLOAT
            )
        """)
        self.connection.commit()

    # Crea el Producto en la Base de Datos
    def crear(self, producto="", precio=0.0):
        self.cursor.execute(
            "INSERT INTO productos (producto, precio) VALUES (%s, %s)", (producto, precio))
        self.connection.commit()
        print(f"'{producto}' con precio {precio} ha sido creado.")

    # Lee el Producto en la Base de Datos
    def leer(self):
        self.cursor.execute("SELECT id, producto, precio FROM productos")
        results = self.cursor.fetchall()
        if not results:
            print("No hay datos para mostrar.")
        else:
            for row in results:
                print(f"{row[0]}. Producto: {row[1]}, Precio: {row[2]}")

    # Actualiza el Producto en la Base de Datos
    def actualizar(self, index, nuevo_producto=None, nuevo_precio=None):
        if nuevo_producto is not None and nuevo_precio is None:
            self.cursor.execute(
                "UPDATE productos SET producto=%s, precio=%s WHERE id=%s", (nuevo_producto, nuevo_precio, index))
        elif nuevo_producto is None:
            self.cursor.execute(
                "UPDATE productos SET producto=%s WHERE id=%s", (nuevo_producto, index))
        elif nuevo_precio is None:
            self.cursor.execute(
                "UPDATE productos SET precio=%s WHERE id=%s", (nuevo_precio, index))
        self.connection.commit()
        print(f"Elemento {index} ha sido actualizado.")

    # Elimina el Producto en la Base de Datos
    def eliminar(self, index):
        self.cursor.execute("DELETE FROM productos WHERE id=%s", (index,))
        self.connection.commit()
        print(f"Elemento {index} ha sido eliminado.")

class CLI:
    def __init__(self):
        self.db = None
        self.ejecutando = True

    # Función para mostrar la Ayuda al Usuario
    def mostrar_ayuda(self):
        print("""
                Comandos:
                crear [producto] [precio]         - Crea un nuevo item (producto y precio opcionales).
                leer                              - Muestra todos los items.
                actualizar <n> [nuevo_producto] [nuevo_precio] - Actualiza el item en la posición n (producto y/o precio opcionales).
                eliminar <n>                      - Elimina el item en la posición n.
                cambiar_db                        - Cambia la base de datos actual.
                ayuda                             - Muestra este mensaje de ayuda.
                salir                             - Sale del programa.
            """)

    # Función para cargar las credenciales de la Base de Datos
    def cargar_credenciales(self):
        if os.path.exists(CREDENCIALES_FILE):
            with open(CREDENCIALES_FILE, 'r') as file:
                credenciales = json.load(file)
            return credenciales
        else:
            return {}

    # Función para guardar las credenciales de la Base de Datos
    def guardar_credenciales(self, credenciales):
        with open(CREDENCIALES_FILE, 'w') as file:
            json.dump(credenciales, file)

    # Función para Verifica si las credenciales son correctas y desea cargarla
    def cargar_db(self):
        credenciales = self.cargar_credenciales()
        if credenciales:
            print("Cargando credenciales guardadas...")
            print(credenciales)
            confirmar = input(
                "¿Desea utilizar estas credenciales? (s/n): ").lower()
            if confirmar == 's':
                self.inicializar_db(credenciales)
                return
        self.inicializar_db()

    # Función para seleccionar la Base de Datos que desea utilizar
    def inicializar_db(self, credenciales=None):
        print("Seleccione el tipo de base de datos:")
        print("1. MySQL")
        print("2. PostgreSQL")

        if not credenciales:
            opcion = input("Ingrese el número de la opción deseada: ")
        else:
            opcion = credenciales.get('db_type', None)

        if opcion == "1":
            if not credenciales:
                host = input("Ingrese el host de MySQL: ")
                user = input("Ingrese el usuario de MySQL: ")
                password = getpass.getpass("Ingrese la contraseña de MySQL: ")
                database = input("Ingrese el nombre de la base de datos: ")
            else:
                host = credenciales.get('host', None)
                user = credenciales.get('user', None)
                password = credenciales.get('password', None)
                database = credenciales.get('database', None)
            self.db = BaseDeDatosMySQL(host, user, password, database)
        elif opcion == "2":
            if not credenciales:
                host = input("Ingrese el host de PostgreSQL: ")
                user = input("Ingrese el usuario de PostgreSQL: ")
                password = getpass.getpass("Ingrese la contraseña de PostgreSQL: ")
                database = input("Ingrese el nombre de la base de datos: ")
            else:
                host = credenciales.get('host', None)
                user = credenciales.get('user', None)
                password = credenciales.get('password', None)
                database = credenciales.get('database', None)
            self.db = BaseDeDatosPostgreSQL(host, user, password, database)
        else:
            print("Opción no válida.")
            self.inicializar_db()

        if not credenciales:
            credenciales = {
                'db_type': opcion,
                'host': host,
                'username': user if opcion == "2" else None,
                'password': password if opcion == "2" else None,
                'database': database
            }
            self.guardar_credenciales(credenciales)

    # Función que se encarga de procesar cada comando
    def procesar_comando(self, comando):
        partes = comando.split()
        if not partes:
            return

        comando_principal = partes[0]

        if comando_principal == "crear":
            producto = partes[1] if len(partes) > 1 else ""
            precio = float(partes[2]) if len(partes) > 2 else 0.0
            self.db.crear(producto, precio)

        elif comando_principal == "leer":
            self.db.leer()

        elif comando_principal == "actualizar":
            if len(partes) < 2:
                print("Uso: actualizar <n> [nuevo_producto] [nuevo_precio]")
                return
            index = int(partes[1]) - 1
            nuevo_producto = partes[2] if len(partes) > 2 else None
            nuevo_precio = float(partes[3]) if len(partes) > 3 else None
            self.db.actualizar(index, nuevo_producto, nuevo_precio)

        elif comando_principal == "eliminar":
            if len(partes) < 2:
                print("Uso: eliminar <n>")
                return
            index = int(partes[1]) - 1
            self.db.eliminar(index)

        elif comando_principal == "cambiar_db":
            self.cargar_db()

        elif comando_principal == "ayuda":
            self.mostrar_ayuda()

        elif comando_principal == "salir":
            self.ejecutando = False

        else:
            print(f"Comando no reconocido: {comando_principal}. Escriba 'ayuda' para ver la lista de comandos.")

    # Función que se encarga de iniciar el proyecto
    def main(self):
        self.cargar_db()
        self.mostrar_ayuda()
        while self.ejecutando:
            comando = input("Ingrese un comando: ")
            self.procesar_comando(comando)


if __name__ == "__main__":
    CLI().main()
