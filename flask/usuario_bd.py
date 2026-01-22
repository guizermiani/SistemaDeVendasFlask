from conexao import conecta_db
import bcrypt
from flask_jwt_extended import create_access_token

def login_bd(conexao, login, senha) -> str:
    cursor = conexao.cursor()
    cursor.execute("SELECT id, login, senha FROM usuario WHERE login = %s", (login,))
    registro = cursor.fetchone()

    if registro: # Verificando se o usuario foi encontrado
        senha_verificar = senha.encode("utf-8")

        senha_bd = registro[2]

        if isinstance(senha_bd, str):
            senha_bd_bytes = senha_bd.encode("utf-8")
        else:
            senha_bd_bytes = senha_bd
            
        if bcrypt.checkpw(senha_verificar, senha_bd_bytes):
             return "OK"
        else:
             return "Senha inválida."
         
    else:
        return "Usuário não encontrado."


def listar_usuarios_bd(conexao):
    cursor = conexao.cursor()
    sql_listar = """ select id, login, from  usuario 
                     order by id asc    
                 """

    # Execução do select xno banco de dados
    cursor.execute(sql_listar)
    # recuperar todos registros
    registros = cursor.fetchall()
    usuarios = []
    for registro in registros:
        usuario = {
            "id": registro[0],
             "nome": registro[1]
        }
        usuarios.append(usuario)
    return usuarios




def consultar_usuario_por_id(conexao):
    id = input("Digite o ID: ")
    cursor = conexao.cursor()
    cursor.execute("select id,login,admin from usuario where id = " + id)
    registro = cursor.fetchone()

    if registro is None:
        print("Usuário não encontrado:")
    else:
        print(f"| ID        ..: {registro[0]} ")
        print(f"| Login       : {registro[1]} ")
        print(f"| Admin       : {registro[2]} ")

def inserir_usuario_bd(conexao, login,senha,admin):
    print("Inserindo o Usuário ..: ")
    cursor = conexao.cursor()

    senha = senha.encode("utf-8")
    print("Senha : ",  senha)
    salt = bcrypt.gensalt() #Gera um salt aleatorio
    hash_senha = bcrypt.hashpw(senha, salt)
    print("Hash Senha ", hash_senha)

    sql_insert = "insert into usuario (login,senha,admin) values ( %s, %s,%s )"
    dados = (login,hash_senha,admin)
    cursor.execute(sql_insert, dados)
    conexao.commit()

    

def atualizar_usuario(conexao):
    print("Alterando dados dos Usuario")
    cursor = conexao.cursor()

    id    = input("Digite o ID : ")
    login = input("Login :")
    senha = input("Senha :")
    admin = input("Admin :")

    sql_update = "update usuario set login = %s, senha = %s, admin = %s where id = %s"
    dados = (login,senha,admin,id)

    cursor.execute(sql_update,dados)
    conexao.commit()

def deletar_usuario_db(conexao, id):
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuario WHERE id = %s", (id,))
    conexao.commit()
