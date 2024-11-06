import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

'''
Esse arquivo deve conter 
todas as funções relacionadas à 
manipulação direta do banco de dados
'''
#--Funcao para criar o banco e as tabelas
def criar_banco():
    #Conectando ao banco de dados
    conexao = sqlite3.connect('biblioteca.db')
    #Criando um cursor(Cursos é a ponte entre o codigo e o banco de dados)
    #Logo qualquer comando direcionado ao BD é feito pelo cursos
    cursor = conexao.cursor()

    #Criando as tabelas dentro do BD
    # Criar a tabela de livros
    cursor.execute('''CREATE TABLE IF NOT EXISTS livros (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   titulo TEXT NOT NULL,
                   disponivel INTEGER NOT NULL DEFAULT 1
                   )''')
    # Criar tabela de usuários
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         nome TEXT NOT NULL,
                         email TEXT NOT NULL
                      )''')
    # Criando a tabela de empréstimos
    cursor.execute('''CREATE TABLE IF NOT EXISTS emprestimos (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         usuario_id INTEGER NOT NULL,
                         livro_id INTEGER NOT NULL,
                         status TEXT DEFAULT 'ativo',
                         data_emprestimo TEXT NOT NULL,
                         FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                         FOREIGN KEY(livro_id) REFERENCES livros(id)
                      )''')
    # Criando a tabela de historico
    cursor.execute('''CREATE TABLE IF NOT EXISTS historico (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         usuario_id INTEGER NOT NULL,
                         nome_usuario TEXT NOT NULL,
                         livro_id INTEGER NOT NULL,
                         titulo_livro TEXT NOT NULL,
                         data_acao TEXT NOT NULL,
                         acao TEXT NOT NULL,
                         FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                         FOREIGN KEY(livro_id) REFERENCES livros(id)
                      )''')
    #Fazendo commit das alterações e fechando a conexao
    conexao.commit()
    conexao.close()

#--Funcao para adicionar usuario
def adicionar_usuario(nome, email):
    #Verificando se os campos estao preenchidos
    if nome and email:
        conexao = sqlite3.connect('biblioteca.db')
        cursor = conexao.cursor()

        #Se os campos estiverem preenchidos os usuarios serao adicionados
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (?, ?)", (nome, email))
        conexao.commit()
        conexao.close()

        #Definindo alertas de insercao
        messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso!")
        return True # Retorna True se o usuário foi adicionado

    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
        return False  # Retorna False se houve erro

# Função para listar usuários do banco de dados
def listar_usuarios_banco():
    # Conectando ao BD
    conexao = sqlite3.connect('biblioteca.db')
    cursor = conexao.cursor()

    # Fazendo a consulta no BD
    cursor.execute("SELECT id, nome, email FROM usuarios ORDER BY nome ASC")
    usuarios = cursor.fetchall()  # Pegando os resultados

    conexao.close()  # Fechando a conexão
    return usuarios  # Retornando os resultados

#--Funcao para adicionar livros    
def adicionar_livros(titulo):
    #If else para ver como estao os campos
    if titulo:
        #Conectando ao BD
        conexao = sqlite3.connect('biblioteca.db')
        cursor = conexao.cursor()

        #Inserindo o livro no BD
        cursor.execute("INSERT INTO livros (titulo) VALUES (?)", (titulo,))
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", "Livro adicionado com sucesso!")
        return True  # Retorna True se o livro foi adicionado
    else:
        messagebox.showwarning("Erro", "O campo título é obrigatório!")
        return False  # Retorna False se houve erro

#--Funcao para listar livros ja inseridos
def listar_livros_banco():
    #Conectando ao BD
    conexao = sqlite3.connect('biblioteca.db')
    cursor = conexao.cursor()

    #Fazendo busca no BD
    cursor.execute("SELECT id, titulo, disponivel FROM livros ORDER BY titulo")
    #Pegando os resultados da busca
    livros = cursor.fetchall()

    conexao.close()
    return livros

#--Funcao para registrar emprestimo de livro
def registrar_emprestimo(usuario_id, livro_id):
    #If else para verificar os campos
    if usuario_id and livro_id:
        conexao = sqlite3.connect('biblioteca.db')
        cursor = conexao.cursor()


        # Verificar se o usuario existe e obter seu nome
        cursor.execute("SELECT id, nome FROM usuarios WHERE id = ?", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            conexao.close()
            messagebox.showwarning("Erro", "Usuário não encontrado!")
            return False  # Retorna False se o usuário não existe
        
        usuario_id, nome_usuario = usuario  # Desempacotar o resultado
        

        # Verificar se o livro existe e está disponível para empréstimo
        cursor.execute("SELECT id, titulo, disponivel FROM livros WHERE id = ?", (livro_id,))
        livro = cursor.fetchone()
        

        if not livro or livro[2] != 1:  # livro[2] é o status de disponibilidade que sera (1 ou 2)
            conexao.close()
            messagebox.showwarning("Erro", "O livro não está disponível ou não existe!")
            return False

        livro_id, titulo_livro, _ = livro  # Desempacotar o resultado

        data_emprestimo = datetime.now().strftime("%d/%m/%Y")

        # Registrar o empréstimo
        cursor.execute("INSERT INTO emprestimos (usuario_id, livro_id, data_emprestimo) VALUES (?, ?, ?)", 
                       (usuario_id, livro_id, data_emprestimo))

        # Atualizar o status do livro para "não disponível" (0)
        cursor.execute("UPDATE livros SET disponivel = 0 WHERE id = ?", (livro_id,))

        
        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", "Empréstimo registrado com sucesso!")
        return True
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
        return False
    
# Função para registrar devolução de livro
def registrar_devolucao(livro_id, usuario_id):
    #If Else para verificar se os campos estao preenchidos
    if livro_id and usuario_id:
        conexao = sqlite3.connect("biblioteca.db")
        cursor = conexao.cursor()

        # Verifica se o empréstimo existe e está ativo
        cursor.execute("""
            SELECT emprestimos.id, usuarios.nome, livros.titulo 
            FROM emprestimos 
            JOIN usuarios ON emprestimos.usuario_id = usuarios.id 
            JOIN livros ON emprestimos.livro_id = livros.id 
            WHERE emprestimos.livro_id = ? AND emprestimos.usuario_id = ? AND emprestimos.status = 'ativo'
        """, (livro_id, usuario_id))
        

        emprestimo = cursor.fetchone()#Aki pegamos todo o resultado da consulta acima

        if not emprestimo:#If para verificar se a consulta troxe algum emprestimo valido
            conexao.close()
            messagebox.showwarning("Erro", "Este livro não foi emprestado para este usuário ou já foi devolvido.")
            return False 
        #Continuando, se a consulta do emprestimo trouxer um resultado valido ele continua a logica

        # Atualizar o status para "devolvido"
        cursor.execute("UPDATE emprestimos SET status = 'devolvido' WHERE livro_id = ? AND usuario_id = ?", (livro_id, usuario_id))
        
        # Alterar o status do livro para disponível
        cursor.execute("UPDATE livros SET disponivel = 1 WHERE id = ?", (livro_id,))

        conexao.commit()
        conexao.close()

        messagebox.showinfo("Sucesso", "Livro devolvido com sucesso!")
        return True
    else:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
        return False
 
#--Funcao para registrar cada acao num historico
def registrar_acao_historico(usuario_id, nome_usuario, livro_id, titulo_livro, data_acao, acao):
    # Conectando ao BD
    conexao = sqlite3.connect('biblioteca.db')
    cursor = conexao.cursor()

    #Inserindo a acao no historico
    cursor.execute("INSERT INTO historico (usuario_id, nome_usuario, livro_id, titulo_livro, data_acao, acao) VALUES (?, ?, ?, ?, ?, ?)", 
                   (usuario_id, nome_usuario, livro_id, titulo_livro, data_acao, acao))

    conexao.commit()
    conexao.close()

# Função para listar os filtrando por dat
def filtro_busca_historico(mes, ano):
    # Mapeamento de meses em texto para números
    meses_map = {
        "Janeiro": "01", "Fevereiro": "02", "Março": "03", "Abril": "04",
        "Maio": "05", "Junho": "06", "Julho": "07", "Agosto": "08",
        "Setembro": "09", "Outubro": "10", "Novembro": "11", "Dezembro": "12"
    }

    # Obter o número do mês a partir do nome
    mes_numerico = meses_map.get(mes, None)
    if not mes_numerico:
        return []  # Retorna uma lista vazia se o mês não for encontrado

    # Criar o padrão para o LIKE: "%mm/yyyy"
    padrao_data = f"%/{mes_numerico}/{ano}"

    conexao = sqlite3.connect('biblioteca.db')
    cursor = conexao.cursor()

    # Atualizar a consulta para usar o filtro LIKE para o mês e ano
    cursor.execute('''
        SELECT historico.usuario_id, usuarios.nome, historico.livro_id, livros.titulo, historico.data_acao, historico.acao
        FROM historico
        JOIN usuarios ON historico.usuario_id = usuarios.id
        JOIN livros ON historico.livro_id = livros.id
        WHERE historico.data_acao LIKE ?
        ORDER BY historico.data_acao DESC
    ''', (padrao_data,))

    historico = cursor.fetchall()
    conexao.close()

    return historico

# Função para listar os emprestimos ainda ativos
def listar_emprestimos_ativos():
    #Conexao com o banco
    conexao1 = sqlite3.connect('biblioteca.db')
    cursor1 = conexao1.cursor()

    # Consulta que retorna apenas os empréstimos com status ativo
    cursor1.execute("""
        SELECT emprestimos.id, usuarios.id AS usuario_id, usuarios.nome, livros.id AS livro_id, livros.titulo, emprestimos.data_emprestimo 
    FROM emprestimos 
    JOIN usuarios ON emprestimos.usuario_id = usuarios.id 
    JOIN livros ON emprestimos.livro_id = livros.id 
    WHERE emprestimos.status = 'ativo'
    """)


    registros = cursor1.fetchall()
    conexao1.close()
    return registros

# Funcao para obter o nome do usuario
def obter_nome_usuario_por_id(usuario_id):
    conexao = sqlite3.connect('biblioteca.db')
    cursor = conexao.cursor()
    
    cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario_id,))
    busca_usuario = cursor.fetchone()
    
    # Verificar se o usuário foi encontrado
    if not busca_usuario:
        conexao.close()
        return False  # Retorna False se o usuário não existe
    
    # Extrair o nome e fechar a conexão
    nome_usuario = busca_usuario[0]
    conexao.close()
    return nome_usuario

# Funcao para obter o titulo do livro
def obter_titulo_livro_por_id(livro_id):
    conexao = sqlite3.connect('biblioteca.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT titulo FROM livros WHERE id = ?", (livro_id,))
    busca_livro = cursor.fetchone()

    # Verificar se o livro foi encontrado
    if not busca_livro:
        conexao.close()
        return False  # Retorna False se o usuário não existe
    
    # Extrair o titulo e fechar a conexão
    titulo_livro = busca_livro[0]
    conexao.close()
    return titulo_livro


