import pymysql
from app import app
from config import mysql, auth
from flask import jsonify, Response, flash, request
from flask_debug import Debug
from mysql.connector import Error
from flask_basicauth import BasicAuth

basic_auth = auth

#Criando a Tabela enderecos
def create_table():
	conn = mysql.connect()
	cursor = conn.cursor(pymysql.cursors.DictCursor)
	cursor.execute("CREATE TABLE IF NOT EXISTS db_clientes.tbl_enderecos (idCliente INTEGER NOT NULL,idEndereco INT NOT NULL AUTO_INCREMENT, rua VARCHAR(100) NOT NULL, numero INT NOT NULL, bairro VARCHAR(60) NOT NULL, cidade VARCHAR(60) NOT NULL, estado VARCHAR(60) NOT NULL, cep VARCHAR(20) NOT NULL, PRIMARY KEY(idEndereco), FOREIGN KEY(idCliente) REFERENCES tbl_clientes(id))")

#Criando as Rotas API's para a Tabela Endereço
# Para fazer um POST o idEndreço e o IdCliente deve ser passdo no body/raw da API manualmente
@app.route('/enderecos', methods = ['POST'])
@basic_auth.required
def add_endereco():
	try:
		_json = request.get_json(force = True)
		_idCliente = _json['idCliente']
		_idEndereco = _json['idEndereco']
		_rua = _json['rua']
		_numero = _json['numero']
		_bairro = _json['bairro']
		_cidade = _json['cidade']
		_estado = _json['estado']
		_cep = _json['cep']		
		if _rua and _numero and _bairro and _cidade and _estado and _cep and _idEndereco and request.method == 'POST':			
			sqlQuery = "INSERT INTO tbl_enderecos(idCliente, rua, numero, bairro, cidade, estado, cep, idEndereco) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
			bindData = (_idCliente, _rua, _numero, _bairro, _cidade, _estado, _cep, _idEndereco)
			conn = mysql.connect()
			cursor = conn.cursor(pymysql.cursors.DictCursor)
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			respone = jsonify('Cliente cadastrado com sucesso!')
			respone.status_code = 200
			return respone
		else:
			return not_found()
	except Exception as e:
		print(e)

#Buscando todos os endereços cadastrados (GET)
@app.route('/enderecos', methods = ['GET'])
@basic_auth.required
def enderecos():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT idCliente, rua, numero, bairro, cidade, estado, cep, idEndereco FROM tbl_enderecos")
		empRows = cursor.fetchall()
		respone = jsonify(empRows)
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

#Buscando um endereços cadastrados por meio de um ID (GET)
@app.route('/enderecos/<int:idEndereco>', methods =['GET'])
@basic_auth.required
def endereco_cliente(idEndereco):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT idCliente, rua, numero, bairro, cidade, estado, cep, idEndereco FROM tbl_enderecos WHERE idEndereco = {}".format(idEndereco))
		empRow = cursor.fetchone
		if not userRow:
			return Response('Usuário não cadastrado', status=404)
		respone = jsonify(empRow)
		respone.status_code = 200
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

# Alterando um endereço cadastrado (PUT)
@app.route('/enderecos', methods=['PUT'])
@basic_auth.required
def update_endereco():
	try:
		_json = request.get_json(force = True)
		_idCliente = _json['idCliente']
		_idEndereco = _json['idEndereco']
		_rua = _json['rua']
		_numero = _json['numero']
		_bairro = _json['bairro']
		_cidade = _json['cidade']
		_estado = _json['estado']
		_cep = _json['cep']		
		if _rua and _numero and _bairro and _cidade and _estado and _cep and _idCliente and _idEndereco and request.method == 'PUT':
			sqlQuery = "UPDATE tbl_enderecos SET rua=%s, numero=%s, bairro=%s, cidade=%s, estado=%s, cep=%s, idCliente=%s WHERE idEndereco=%s"
			bindData = (_rua, _numero, _bairro, _cidade, _estado, _cep, _idCliente, _idEndereco)
			print("oi")
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sqlQuery, bindData)
			conn.commit()
			response = jsonify('Dados alterados com sucesso!')
			response.status_code = 200
			return response
		else:
			return not_found()

	except Exception as error:
		print(error)
	finally:
		cursor.close()
		conn.close()

# Deletando algum ID endereço cadastrado (DELETE) 
@app.route('/enderecos/<int:idEndereco>', methods=['DELETE'])
@basic_auth.required
def delete_endereco(idEndereco):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tbl_enderecos WHERE idEndereco =%s", (id))
		conn.commit()
		respone = jsonify('Cliente deletado com sucesso!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
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
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.debug = True
    create_table()
    app.run()