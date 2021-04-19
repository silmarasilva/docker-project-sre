import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response
from flask import flash, request
from flask_debug import Debug
from flask_basicauth import BasicAuth

basic_auth = auth

#Criando as Rotas API para relação JOIN Cliente e Endereço
# http://127.0.0.1:5000/clientes/enderecos/id
@app.route('/clientes/enderecos/<int:id>')
@basic_auth.required
def ligacao_cliente_enderecos(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT db_clientes.tbl_clientes.nome, db_clientes.tbl_enderecos.rua, db_clientes.tbl_enderecos.numero, db_clients.tbl_enderecos.bairro, db_clientes.tbl_enderecos.cidade, db_clientes.tbl_enderecos.estado, db_clientes.tbl_enderecos.cep FROM db_clientes.tbl_clientes JOIN db_clientes.tbl_enderecos ON db_clientes.tbl_clientes.id = db_clientes.tbl_enderecos.idCliente WHERE id = %s", id)
        userRow = cursor.fetchall()
        if not userRow:
            return Response('Usuário não cadastrado', status=404)
        response = jsonify(userRow)
        response.status_code = 200
        return response
    except Exception as error:
        print(error)
    finally:
        cursor.close() 
        conn.close()


@app.errorhandler(404)
@basic_auth.required
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    response = jsonify(message)
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()