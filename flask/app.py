from flask import Flask, render_template, request, redirect, url_for
from conexao import conecta_db
from categoria_bd import inserir_categoria
from cliente_bd import inserir_cliente, listar_clientes_bd
from usuario_bd import inserir_usuario_bd, listar_usuarios_bd, deletar_usuario_db

app = Flask(__name__)


@app.route("/home")
def home():
    return render_template("home.html")

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        # Valida campos obrigatórios; ajuste aqui para autenticar de verdade
        if not usuario or not senha:
            erro = "Preencha usuário e senha para entrar."
            return render_template("login.html", erro=erro)

        return redirect(url_for('home'))

    return render_template("login.html")

# Cliente
@app.route("/salvar-cliente", methods=["GET", "POST"])
def salvar_cliente():
    if request.method == "POST":
        nome = request.form.get("nome")
        celular = request.form.get("celular")
        email = request.form.get("email")
        cpf_cnpj = request.form.get("cpf_cnpj")

        if not nome:
            return "<h3> Por favor, preencha o nome</h3>"

        conexao = conecta_db()
        cursor = conexao.cursor()
        sql_insert = """
            INSERT INTO cliente (nome, celular, email, cpf_cnpj)
            VALUES (%s, %s, %s, %s)
        """
        dados = (nome, celular, email, cpf_cnpj)
        cursor.execute(sql_insert, dados)
        conexao.commit()

        return f"<h2> Cliente salvo com sucesso: {nome} </h2>"

    return render_template("cliente-form.html", titulo="Cadastrar Cliente")

@app.route("/listar-clientes", methods=["GET"])
def listar_clientes():
    conexao = conecta_db()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT id, nome, celular, email, cpf_cnpj FROM cliente ORDER BY id DESC"
    )
    clientes = cursor.fetchall()
    return render_template("cliente-list.html", clientes=clientes, titulo="Clientes")


@app.route("/usuario/novo", methods=["GET", "POST"])
def salvar_usuario():
    if request.method == "POST":
        login = request.form.get("login")
        senha = request.form.get("senha")

        if not login or not senha:
            return "<h3> Por favor, preencha todos os campos</h3>"

        conexao = conecta_db()
        inserir_usuario_bd(conexao, login, senha, 'S')
        return f"<h2> Usuário Salvo com Sucesso:  {login} </h2>"
    
    return render_template("usuario-form.html", titulo="Cadastrar Usuário")

@app.route("/listar-usuarios", methods=["GET"])
def listar_usuarios():
    conexao = conecta_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, login, admin FROM usuario")
    usuarios = cursor.fetchall()
    return render_template("usuario-list.html", usuarios=usuarios)


@app.route("/usuario/<int:id>/deletar", methods=["POST"])
def usuarios_excluir(id):
    conexao = conecta_db()
    deletar_usuario_db(conexao, id)
    return redirect(url_for('listar_usuarios'))




# Categoria
@app.route("/salvar-categoria", methods=["GET", "POST"])
def salvar_categoria():
    if request.method == "POST":
        nome = request.form.get("nome")
        if not nome:
            return "<h3> Por favor, preencha todos os campos</h3"

        conexao = conecta_db()
        inserir_categoria(conexao, nome)

        return f"<h2> Categoria Salva com Sucesso:  {nome} </h2>"
    return render_template("categoria-form.html", titulo="Cadastrar Categoria")


@app.route("/deletar-categoria", methods=["POST", "GET"])
def deletar_categoria():
    if request.method == "POST":
        id_categoria = request.form["id"]

        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM categoria WHERE id = %s", (id_categoria,))

        conexao.commit()

        return "Categoria excluída com sucesso!"
    return render_template("categoria-delete.html")


@app.route("/listar-categoria", methods=["GET"])
def categoria_listar():
    cursor = conecta_db().cursor()
    cursor.execute("SELECT id, nome FROM categoria")
    registros = cursor.fetchall()

    resultado = "<h2>Registros da tabela categoria:</h2><ul>"
    for registro in registros:
        resultado += f"<li>ID: {registro[0]}, Nome: {registro[1]}</li>"
    resultado += "</ul>"

    return render_template("categoria-list.html", categorias=registros, titulo="Categorias")


# Produto
@app.route("/listar-produtos", methods=["GET"])
def listar_produtos():
    cursor = conecta_db().cursor()
    cursor.execute("SELECT id, nome, valor_venda, estoque, categoria_id FROM produto")
    registros = cursor.fetchall()

    resultado = "<h2>Registros da tabela produto:</h2><ul>"
    for registro in registros:
        resultado += f"<li>ID: {registro[0]}, Nome: {registro[1]}, Preço: {registro[2]}, Estoque: {registro[3]}, CategoriaID: {registro[4]}</li>"
    resultado += "</ul>"

    return render_template("produtos-list.html", produtos=registros)


@app.route("/salvar-produto", methods=["GET", "POST"])
def salvar_produto():
    if request.method == "POST":
        nome = request.form.get("nome")
        valor_venda = request.form.get("valor_venda")
        estoque = request.form.get("estoque")
        categoria_id = request.form.get("categoria_id")

        if not nome or not valor_venda or not estoque or not categoria_id:
            return "<h3> Por favor, preencha todos os campos</h3>"

        conexao = conecta_db()
        cursor = conexao.cursor()
        sql_insert = "INSERT INTO produto (nome, valor_venda, estoque, categoria_id) VALUES (%s, %s, %s, %s)"
        dados = (nome, valor_venda, estoque, categoria_id)
        cursor.execute(sql_insert, dados)
        conexao.commit()

        return f"<h2> Produto Salvo com Sucesso:  {nome} </h2>"

    conexao = conecta_db()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM categoria")
    categorias = cursor.fetchall()

    return render_template(
        "produto-form.html", categorias=categorias, titulo="Cadastrar Produto"
    )


@app.route("/deletar-produto", methods=["POST", "GET"])
def deletar_produto():
    if request.method == "POST":
        id_produto = request.form["id"]

        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produto WHERE id = %s", (id_produto))

        conexao.commit()

        return "Produto excluído com sucesso!"
    return render_template("produto-delete.html")


@app.route("/categorias/<int:id>/editar", methods=["GET", "POST"])
def categorias_editar():
    return redirect(url_for("categoria_listar"))


if __name__ == "__main__":
    app.run(debug=True)