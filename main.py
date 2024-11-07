from flask import Flask, render_template, request, redirect, url_for, flash
import fdb
# importando banco de dados

app = Flask(__name__)
app.config['SECRET_KEY'] = 'maju_2024_alalala'
# chave secreta

host = 'localhost'
database = r'C:\Users\Aluno\Downloads\BANCO_07\BANCO.FDB'
user = 'sysdba'
password = 'sysdba'

con = fdb.connect(host=host, database=database, user=user, password=password)

class livro:
    def __init__(self, id_livro, titulo, autor, ano_publicacao):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.ano_publicacao = ano_publicacao

@app.route('/')
def index():
    cursor = con.cursor()
    cursor.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livros")
    livros = cursor.fetchall()
    cursor.close()
    return render_template('livros.html', livros=livros)

@app.route('/novo')
def novo():
    return render_template('adicionar.html', titulo='Novo livro')
@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    # criando o cursor
    cursor = con.cursor()

    try:
        # verificando se o livro já existe
        cursor.execute("SELECT 1 FROM livros WHERE titulo = ?", (titulo,))
        if cursor.fetchone(): # se já existir um registro
            flash('Erro: Livro já cadastrado.', 'error')
            return redirect(url_for('novo'))

        # Inserir o novo livro (sem capturar o ID)
        cursor.execute("INSERT INTO livros (titulo, autor, ano_publicacao) VALUES (?, ?, ?)", (titulo, autor, ano_publicacao))
        con.commit()

    finally:
        cursor.close() # fechando o cursor manualmente
    flash('Livro cadastrado com sucesso!', 'sucess')
    return redirect(url_for('index'))

@app.route('/atualizar')
def atualizar():
    return render_template('editar.html', titulo='Editar Livro')

@app.route('/editar/<int:id>', methods=['GET', 'POST']) # selecionando o livro pelo ID
def editar(id):
    cursor = con.cursor() # 'abrindo' cursor
    cursor.execute("SELECT id_livro, titulo, autor, ano_publicacao FROM livros WHERE ID_LIVRO= ?", (id,))
    livro = cursor.fetchone()

    if not livro:
        cursor.close() # fechando cursor caso o livro não exista
        flash('Livro não encontrado! ):', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        titulo = request.form['titulo']
        autor = request.form['autor']
        ano_publicacao = request.form['ano_publicacao']

        cursor.execute("UPDATE livros SET titulo = ?, autor = ?, ano_publicacao = ? WHERE id_livro = ?", (titulo, autor, ano_publicacao, id))

        con.commit()
        cursor.close() # fecha o cursor caso o método seja POST
        flash('Livro atualizado com sucesso! (;', 'sucess')
        return redirect(url_for('index'))

    cursor.close()
    return render_template('editar.html', livro=livro, titulo='Editar Livro')

@app.route('/deletar/<int:id>', methods=['POST'])
def deletar(id):

    cursor = con.cursor()

    try:
        cursor.execute("DELETE FROM livros WHERE id_livro = ?", (id,))
        con.commit()
        flash('Livro excluído com sucesso!', 'sucess')
    except Exeception as e:
        con.rollback()
        flash('Erro ao excluir o livro. ):', 'error')
    finally:
        cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
