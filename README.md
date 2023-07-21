# mi-api-rest
# Mi API REST

Mi API REST, un proyecto desarrollado con Flask que proporciona una API para administrar contactos. Esta API permite realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) en una base de datos de contactos.

## Funcionalidades

- Registro de nuevos usuarios.
- Autenticación de usuarios con JWT (JSON Web Tokens).
- Creación, lectura, actualización y eliminación de contactos.
- Validación de datos de entrada en las solicitudes a la API.
- Protección de rutas mediante JWT para acceso a recursos protegidos.

## Configuración

Antes de ejecutar la API, asegúrate de tener instaladas las dependencias necesarias. Puedes instalarlas utilizando el archivo `requirements.txt` con el siguiente comando:

Para convertir esta descripción a lenguaje markdown, puedes usar el siguiente código:


# Endpoints

## Obtener todos los contactos
- URL: `/contacts`
- Método HTTP: `GET`
- Descripción: Retorna todos los contactos almacenados en la base de datos.
- Respuesta Exitosa:
  - Código: `200`
  - Contenido: 
  ```json
  { "contacts": [ {"id": 1, "name": "Juan Pérez", "email": "juan@example.com", "phone": "1234567890"}, {"id": 2, "name": "María López", "email": "maria@example.com", "phone": "9876543210"} ] }
  ```

## Crear un nuevo contacto
- URL: `/contacts`
- Método HTTP: `POST`
- Descripción: Crea un nuevo contacto en la base de datos.
- Cuerpo de la Solicitud:
  - Formato: `JSON`
  - Campos obligatorios: `name`, `email`, `phone`
  - Ejemplo: 
  ```json
  {"name": "Carlos Gómez", "email": "carlos@example.com", "phone": "5678901234"}
  ```
- Respuesta Exitosa:
  - Código: `201`
  - Contenido: 
  ```json
  { "message": "Contacto creado con éxito", "contact": {"id": 3, "name": "Carlos Gómez", "email": "carlos@example.com", "phone": "5678901234"} }
  ```

## Obtener un contacto por ID
- URL: `/contacts/{id}`
- Método HTTP: `GET`
- Descripción: Retorna un contacto específico por su ID.
- Parámetros de la URL:
  - Reemplaza `{id}` con el ID numérico del contacto deseado.
- Respuesta Exitosa:
  - Código: `200`
  - Contenido: 
  ```json
  {"id": 1, "name": "Juan Pérez", "email": "juan@example.com", "phone": "1234567890"}
  ```

## Actualizar un contacto
- URL: `/contacts/{id}`
- Método HTTP: `PUT`
- Descripción: Actualiza los datos de un contacto existente.
- Parámetros de la URL:
  - Reemplaza `{id}` con el ID numérico del contacto a actualizar.
- Cuerpo de la Solicitud:
  - Formato: `JSON`
  - Campos permitidos: `name`, `email`, `phone`
  - Ejemplo: 
  ```json
  {"name": "Juan Pérez Gómez"}
  ```
- Respuesta Exitosa:
  - Código: `200`
  - Contenido: 
  ```json
   { "message": "Contacto actualizado con éxito", "contact": {"id": 1, "name": "Juan Pérez Gómez", "email": "juan@example.com", "phone": "1234567890"} }
   ```

## Eliminar un contacto
- URL: `/contacts/{id}`
- Método HTTP: `DELETE`
- Descripción: Elimina un contacto existente de la base de datos.
- Parámetros de la URL:
  - Reemplaza `{id}` con el ID numérico del contacto a eliminar.
- Respuesta Exitosa:
  - Código: `200`
  - Contenido: 
   ```json
   {"message": "Contacto eliminado con éxito"}
   ```

# Autenticación

Para acceder a los endpoints protegidos, se debe incluir un token de acceso JWT válido en la cabecera de la solicitud (`Authorization: Bearer <TOKEN>`).

# Ejecución Local

1. Clona el repositorio desde GitHub: `git clone https://github.com/tuusuario/tu-api-rest.git`
2. Instala las dependencias requeridas: `pip install -r requirements.txt`
3. Configura la base de datos MySQL en el archivo app.py.
4. Ejecuta la aplicación localmente: `python app.py`
```

Espero que te sea útil. 😊
