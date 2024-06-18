# Base de Datos Abstracción en Python

Este proyecto proporciona una abstracción de base de datos en Python que permite realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en diferentes tipos de bases de datos: JSON, MySQL, PostgreSQL y MongoDB.

## Estructura del Proyecto

El proyecto está organizado en varias clases, cada una de las cuales maneja una base de datos específica:

1. **BaseDeDatos**: Clase base abstracta que define la interfaz para las operaciones CRUD.
3. **BaseDeDatosMySQL**: Implementación de `BaseDeDatos` para manejar datos almacenados en una base de datos MySQL.
4. **BaseDeDatosPostgreSQL**: Implementación de `BaseDeDatos` para manejar datos almacenados en una base de datos PostgreSQL.

## Requisitos

Para ejecutar este proyecto, necesitas tener instaladas las siguientes bibliotecas de Python:

- `pymysql`
- `psycopg2`

Puedes instalarlas usando pip:

```sh
pip install pymysql psycopg2
```

## Uso

### Inicialización

Cada clase de base de datos tiene su propio método de inicialización. Aquí hay ejemplos de cómo inicializar cada una:

#### MySQL

```python
db_mysql = BaseDeDatosMySQL(host="localhost", user="usuario", password="contraseña", database="mi_base_de_datos")
```

#### PostgreSQL

```python
db_postgresql = BaseDeDatosPostgreSQL(host="localhost", user="usuario", password="contraseña", database="mi_base_de_datos")
```

### Operaciones CRUD

Una vez que has inicializado la base de datos, puedes realizar operaciones CRUD.

#### Crear

```python
db.crear(producto="Producto1", precio=10.0)
```

#### Leer

```python
db.leer()
```

#### Actualizar

```python
db.actualizar(index=1, nuevo_producto="Producto Actualizado", nuevo_precio=20.0)
```

#### Eliminar

```python
db.eliminar(index=1)
```

### Ejemplo Completo

Aquí hay un ejemplo completo de cómo usar la clase `BaseDeDatosMySQL`:

```python
from MiBaseDeDatos import BaseDeDatosMySQL

# Inicializar la base de datos JMySQL
db = MiBaseDeDatos(host='localhost', user='usuario', password='contraseña', database='nombre_basedatos')

# Crear un nuevo producto
db.crear(producto='Producto A', precio=10.0)

# Leer todos los productos
db.leer()

# Actualizar el primer producto
db.actualizar(index=0, nuevo_producto="Producto Actualizado", nuevo_precio=20.0)

# Eliminar el primer producto
db.eliminar(index=0)
```

## Contribuciones

Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.