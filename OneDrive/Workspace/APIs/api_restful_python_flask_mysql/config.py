# Objeto de conexão para encontrar o servidor, sql logon e efetivar a conexão
from app import app
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth

app.config['BASIC_AUTH_USERNAME'] = 'seu user'
app.config['BASIC_AUTH_PASSWORD'] = 'sua senha'

auth = BasicAuth(app)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sua senha do mysql' #insira a sua senha do DB
app.config['MYSQL_DATABASE_DB'] = 'db_clientes' #insira o nome do seu DB
app.config['MYSQL_DATABASE_DB'] = 'db_produtos' #insira o nome do seu DB
app.config['MYSQL_DATABASE_DB'] = 'db_vendas' #insira o nome do seu DB
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


