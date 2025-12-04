from flask import Flask, render_template, request, redirect, url_for
from conexao import conecta_db
from categoria_bd import inserir_categoria
from cliente_bd import inserir_cliente, listar_clientes_bd

app = Flask(__name__)

@app.route('/')
def home():
    nome = "Guilherme Zermiani"
    return render_template("index.html", nome=nome)

#Cliente
@app.route('/cliente', methods=['GET', 'POST'])
def salvar_cliente():
     if request.method == 'POST':
        nome = request.form.get('nome')
        celular = request.form.get('celular')
        email = request.form.get('email')
        cpf_cnpj = request.form.get('cpf_cnpj')
        
        if not nome:
            return "<h3> Por favor, preencha todos os campos</h3"
        
        conexao = conecta_db()
        inserir_cliente(conexao,nome, celular, email, cpf_cnpj)

        return f"<h2> Cliente Salvo com Sucesso:  {nome} </h2>"
     return render_template("cliente-form.html")
 
@app.route("/listar-clientes", methods=["GET"])
def listar_clientes():
    conexao = conecta_db()
    clientes = listar_clientes_bd(conexao)
    return render_template("cliente-listar.html", clientes=clientes)

#Categoria
@app.route("/salvar-categoria", methods=['GET','POST'])
def salvar_categoria():
    if request.method == 'POST':
        nome = request.form.get('nome')
        if not nome:
            return "<h3> Por favor, preencha todos os campos</h3"
        
        conexao = conecta_db()
        inserir_categoria(conexao,nome)

        return f"<h2> Categoria Salva com Sucesso:  {nome} </h2>"
    return render_template("categoria-form.html")

@app.route("/deletar-categoria", methods=["POST", "GET"])
def deletar_categoria():
    if request.method == "POST":
        id_categoria = request.form['id']
        
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
    
    return render_template("categoria-list.html", categorias=registros)

#Produto
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

@app.route("/salvar-produto", methods=['GET','POST'])
def salvar_produto():
    if request.method == 'POST':
        nome = request.form.get('nome')
        valor_venda = request.form.get('valor_venda')
        estoque = request.form.get('estoque')
        categoria_id = request.form.get('categoria_id')
        
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

    return render_template("produto-form.html", categorias=categorias, titulo="Cadastrar Produto")


@app.route('/deletar-produto', methods=['POST', 'GET'])
def deletar_produto():
    if request.method == "POST":
        id_produto = request.form['id']
        
        conexao = conecta_db()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produto WHERE id = %s", (id_produto))
        
        conexao.commit()
        
        return "Produto excluído com sucesso!"
    return render_template("produto-delete.html")

@app.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
def categorias_editar():
    return redirect(url_for('categoria_listar'))

if __name__ == '__main__':
    app.run(debug=True)