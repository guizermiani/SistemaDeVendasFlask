from conexao import conecta_db
import bcrypt

def login_bd(conexao, login,senha) -> bool:
    cursor = conexao.cursor()
    cursor.execute(" select id,login,senha from usuario"+
                   " where login = '" + login+ "'", '"' + senha+ "'")
    registro = cursor.fetchone()

    if  registro:
        return True
    else:
        return False


def listar_usuarios_bd(conexao):
    cursor = conexao.cursor()
    sql_listar = """ select id, login, admin  from  usuario 
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

def deletar_usuario(conexao):
    print("Deletando Usuario")
    cursor = conexao.cursor()
    id   = input("Digite o ID : ")
    sql_delete = "delete from usuario where id = "+ id
    cursor.execute(sql_delete)
    conexao.commit()