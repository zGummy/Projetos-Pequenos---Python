import sqlite3

#Senha mestre
SENHA_MESTRE = "Senha123"

senha = input("Insira sua senha mestre: ")
if senha != SENHA_MESTRE:
	print("Senha inválida! Encerrando ...")
	exit()

conn = sqlite3.connect('banco.db')

cursor = conn.cursor()

#Cria a tabela vazia (inicializa)
cursor.execute('''
CREATE TABLE IF NOT EXISTS  users(
  service TEXT NOT NULL,
  username TEXT NOT NULL,
  password TEXT NOT NULL
);
''')


def menu():
	print("_____________MENU_____________")
	print("* i: Inserir nova senha      *")
	print("* l: Listar serviços salvos  *")
	print("* r: Recuperar uma senha     *")
	print("* s: Sair                    *")
	print("______________________________")
	print("")


def get_password(service):
	cursor.execute(f'''
    SELECT username, password FROM users
      WHERE service = '{service}'  
  ''')

	if cursor.rowcount == 0:
		print(
		    "Serviço não cadastrado (use a opção Listar para ver todos os serviços"
		)
	else:
		for user in cursor.fetchall():
			print(user)


def insert_password(service, username, password):
	cursor.execute(f'''
  INSERT INTO users (service,username,password)
  VALUES ('{service}','{username}','{password}')
  ''')
	conn.commit()


def show_services():
	cursor.execute('''
    SELECT service FROM users;
  ''')
	for services in cursor.fetchall():
		print(services)


while True:
	menu()
	op = input("O que deseja fazer ?")
	if op not in ['l', 'i', 'r', 's']:
		print("Opção inválida!")
		continue

	if (op == "s"):
		break

	if (op == "i"):
		service = input("Qual o nome do serviço?")
		username = input("Qual o nome do usuário ?")
		password = input("Qual é a senha?")
		insert_password(service, username, password)

	if (op == "l"):
		show_services()

	if (op == "r"):
		service = input("Qual o serviço que você quer a senha ?")
		get_password(service)

conn.close()
