# Importar los modulos necesarios
'''
    estas líneas de código importan los módulos necesarios para trabajar con Flask y SQLAlchemy, 
    lo que permite desarrollar aplicaciones web y realizar operaciones con bases de datos de manera eficiente y sencilla
'''
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError # modulos para validacion
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity # modulos para autentication

# Configurar la aplicacion flask y la conexion a la base de datos
'''
    estas líneas de código establecen la configuración de la aplicación Flask, 
    incluyendo la URI de la base de datos, y crean una instancia de SQLAlchemy vinculada a la aplicación. 
    Esto permite la conexión y la interacción con la base de datos MySQL en la aplicación Flask.
'''
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/contacts'
app.config['JWT_SECRET_KEY'] = 'mi_clave_secreta' # Reemplaza esto con una clave segura y secreta en producción
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Crear modelo de base de datos
'''
 la clase Contact representa una tabla en la base de datos con columnas para id, name, email y phone. 
 El método serialize() se utiliza para convertir un objeto Contact en un formato serializable. 
 Esto permite el almacenamiento y recuperación de datos de la tabla Contact en la base de datos utilizando SQLAlchemy.
'''
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }
    
class User(db.Model):
    """
    Representa la tabla de usuarios en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)


# Crea las tablas en la base de datos
'''
  with app.app_context(): se utiliza para crear un contexto de aplicación Flask en el cual se ejecutan ciertas operaciones, 
  como db.create_all(), que requieren acceder a la configuración y a otros componentes específicos de la aplicación Flask. 
  Esto garantiza que estas operaciones se realicen correctamente dentro del contexto de la aplicación.
'''
with app.app_context():
    db.create_all()

# Manejadores de errores
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({'error': 'No se encontró el recurso solicitado'}), 404

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500

@app.errorhandler(Exception)
def unhandled_exception(error):
    return jsonify({'error': 'Ocurrió un error no controlado'}), 500

# clase para la validacion
class ContactSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)

# Definir las rutas de la API endpoints
@app.route('/contacts', methods = ['GET'])
@jwt_required()
def get_contacts():
    #current_user_id = current_user.id('id')
    contacts = Contact.query.all() # obtiene todos los registros en la tabla
    '''se utiliza una comprensión de lista para iterar sobre la lista de objetos Contact 
    y llamar al método serialize() en cada objeto. Esto convierte cada objeto Contact 
    en un diccionario utilizando el método serialize() definido en la clase Contact.
    '''
    return jsonify({'contacts': [contact.serialize() for contact in contacts]})


@app.route('/contacts', methods = ['POST'])
def create_contact():
    contact_schema = ContactSchema()
    print('contact_schema', contact_schema)
    # obtener los datos json
    data = request.get_json() # Flask lo parsea y devuelve un diccionario
    print('data',data)
    try:
        result = contact_schema.load(data) # validacion
        print('\nresult', result)
    except ValidationError as errors:
        return jsonify({'errors': errors.messages}), 400

    print('data',data)
    print('result', result)
    # Los datos son válidos, realiza las operaciones necesarias
    # Se obtiene los datos de data y se crea un nuevo objeto 'Contact'
    contact = Contact(name=data['name'], email=data['email'], phone=data['phone'])
    print('contact')
    # Prepara el objeto para ser guardado en la db
    db.session.add(contact)

    # Confirmar los cambios y persistir el nuevo contacto
    db.session.commit()

    # La respuesta también incluye un código de estado HTTP 201,
    #  que indica que la solicitud ha tenido éxito y se ha creado un nuevo recurso.
    return jsonify({'message':'Contacto creado con exito', 'contact': contact.serialize()}), 201

@app.route('/contacts/<int:id>', methods = ['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id) # busca un registro en la tabla segun id
    return jsonify(contact.serialize())

@app.route('/contacts/<int:id>', methods = ['PUT'])
def edit_contact(id):
    # Obtiene el objeto contact o se genera un http 404
    contact = Contact.query.get_or_404(id)
    data = request.get_json()

    if 'name' in data:
        contact.name = data['name']
    if 'email' in data:
        contact.email = data['email']
    if 'phone' in data:
        contact.phone = data['phone']

    db.session.commit()

    return jsonify({'message':'Contacto actualizado con exito', 'contact': contact.serialize()})

@app.route('/contacts/<int:id>', methods = ['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message':'Contacto eliminado con exito'})

# Implementar una función para verificar las credenciales de usuario
"""
Decorador que permite personalizar cómo se identifica
 al usuario dentro del token JWT.
 """
@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    función para obtener el nombre de usuario del usuario y
      establecerlo como la identidad del token JWT.
    """
    return user.username

@app.route('/login', methods=['POST'])
def login():
    """
    Aqui es donde se eviaran sus credenciales.
    """
    username = request.json.get('username', None) # obtiene el valor de la clave 'username', sino None
    password = request.json.get('password', None)

    # consulta la base de datos para encontrar un usuario.
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        # Si el usuario existe y las credenciales son validas
        # creamos un token de acceso JWT
        """
        se llamara automaticamente a la funcion del decorador @jwt.user_identity_loader
        para obtener la identidad del usuario y se incluira en el token.
        """
        access_token = create_access_token(identity=user) 
        return jsonify(access_token=access_token), 200
    
    return jsonify({"msg": "Credenciales invalidas"}), 401

# Ruta para el registro de nuevos usuarios
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Verificar si el usuario ya esta registrado
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({'message': 'El usuario ya existe'}), 400
    
    # Crear un nuevo usuario
    new_user = User(username=data['username'], password=data['password'])

    # Agregar el nuevo usuario a la base de datos
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registro exitoso'}), 201

if __name__ == '__main__':
    app.run(debug=True)