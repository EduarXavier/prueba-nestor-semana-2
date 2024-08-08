from flask import Flask, request, jsonify
import json

app = Flask(__name__)

def cargar_datos():
    try:
        with open('usuarios.json', 'r') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def guardar_datos(datos):
    with open('usuarios.json', 'w') as archivo:
        json.dump(datos, archivo, indent=4)

@app.route('/insertar', methods=['POST'])
def insertar_usuario():
    datos_usuario = request.json
    if 'id' not in datos_usuario:
        return jsonify({'error': 'El ID es requerido'}), 400

    datos = cargar_datos()
    datos[datos_usuario['id']] = datos_usuario
    guardar_datos(datos)

    return jsonify(datos_usuario), 201

@app.route('/eliminar/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    datos = cargar_datos()
    if id in datos:
        del datos[id]
        guardar_datos(datos)
        return jsonify({'success': f'Usuario {id} eliminado correctamente'}), 200
    else:
        return jsonify({'error': 'Usuario no encontrado'}), 404

@app.route('/listar', methods=['GET'])
def listar_usuarios():
    datos = cargar_datos()
    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)
