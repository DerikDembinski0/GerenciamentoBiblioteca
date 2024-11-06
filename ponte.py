import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import gerenciador_bd

from gerenciador_bd import (
    criar_banco,
    adicionar_usuario,
    listar_usuarios_banco,
    adicionar_livros,
    listar_livros_banco,
    registrar_emprestimo,
    registrar_devolucao,
    filtro_busca_historico,
    listar_emprestimos_ativos
)


'''
Esse arquivo servirá como uma interface entre a lógica do banco de dados e a interface gráfica
As funções que manipulam a interface (como adicionar/remover/atualizar dados) serão definidas aqui
'''





## Função para listar usuários na interface
#Essa função deve chamar listar_usuarios_banco() de gerenciador_bd.py, atualizar o listbox e limpar o conteúdo anterior
def listar_usuarios(listbox_usuarios):
    #Limpa o listbox antes de atualizar
    listbox_usuarios.delete(0, tk.END)  

    # Chama a função do db_manager para obter os usuários
    usuarios = listar_usuarios_banco()

     # Adicionar usuários ao listbox
    for usuario in usuarios:
        listbox_usuarios.insert(tk.END, f"ID: {usuario[0]} | Nome: {usuario[1]} | Email: {usuario[2]}")


#Agora uma funcao para listar os livros
# Essa função deve chamar listar_livros() de gerenciador_bd.py, atualizar o listbox de livros e limpar o conteúdo anterior
def listar_livros(listbox_livros):
    # Limpar o listbox
    listbox_livros.delete(0, tk.END)

    # Obter livros do banco de dados
    livros = listar_livros_banco()

    # Adicionar livros ao listbox
    for livro in livros:
        status = "" if livro[2] == 1 else " | ⚠️ Indisponível"
        listbox_livros.insert(tk.END, f"ID: {livro[0]} | Titulo: {livro[1]}{status}")
    
    

# Função para adicionar usuário pela interface
def adicionar_usuario_interface(entry_nome, entry_email, listbox_usuarios):
    nome = entry_nome.get()
    email = entry_email.get()

    # Chamar a função para adicionar o usuário no banco de dados
    if adicionar_usuario(nome, email):
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        listar_usuarios(listbox_usuarios)  # Atualizar a lista de usuários


# Função para adicionar livro pela interface
def adicionar_livros_interface(entry_titulo, listbox_livros):
    titulo = entry_titulo.get()

    # Chamar a função para adicionar o livro no banco de dados
    if adicionar_livros(titulo):
        entry_titulo.delete(0, tk.END)
        listar_livros(listbox_livros)  # Atualizar a lista de livros


# Função para registrar empréstimo pela interface
def registrar_emprestimo_interface(entry_usuario_id_emprestimo, entry_livro_id, listbox_livros, listbox_historico):
    usuario_id = entry_usuario_id_emprestimo.get()
    livro_id = entry_livro_id.get()

    # Verificar se os IDs estão preenchidos
    if not usuario_id or not livro_id:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
        return
    
    # Obter nome do usuário e título do livro a partir do banco de dados
    nome_usuario = gerenciador_bd.obter_nome_usuario_por_id(usuario_id)
    titulo_livro = gerenciador_bd.obter_titulo_livro_por_id(livro_id)

    # Consultando se o nome esta no BD
    if not nome_usuario:
        messagebox.showwarning("Erro", "Usuário não encontrado!")
        return

    # Consultando se o livro esta no BD
    if not titulo_livro:
        messagebox.showwarning("Erro", "Livro não encontrado!")
        return

    # Chamar a função para registrar o empréstimo no banco de dados
    if registrar_emprestimo(usuario_id, livro_id):
        # Registrar a ação no histórico após o sucesso do registro do empréstimo
        data_emprestimo = datetime.now().strftime("%d/%m/%Y")
        gerenciador_bd.registrar_acao_historico(usuario_id, nome_usuario, livro_id, titulo_livro, data_emprestimo, 'Empréstimo')

        # Limpar entradas e atualizar listas
        entry_usuario_id_emprestimo.delete(0, tk.END)
        entry_livro_id.delete(0, tk.END)
        listar_livros(listbox_livros)  # Atualizar a lista de livros
        exibir_emprestimos_ativos_interface(listbox_historico)  # Atualiza o histórico
    else:
        messagebox.showwarning("Erro", "Não foi possível registrar o empréstimo.")

# Função para registrar devolução pela interface
def registrar_devolucao_interface(entry_livro_id_devolucao, entry_usuario_id, listbox_livros, listbox_historico):
    # Obtenha o ID do livro e o ID do usuário a partir dos campos de entrada
    livro_id = entry_livro_id_devolucao.get()
    usuario_id = entry_usuario_id.get()  # Aqui você obtém o valor do Entry

    # Verificar se os IDs estão preenchidos
    if not usuario_id or not livro_id:
        messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
        return
    
    # Obter título do livro a partir do banco de dados
    nome_usuariozz = gerenciador_bd.obter_nome_usuario_por_id(usuario_id)
    titulo_livro = gerenciador_bd.obter_titulo_livro_por_id(livro_id)


    # Verificar se o usuário e o livro existem
    if not nome_usuariozz:
        messagebox.showwarning("Erro", "Usuário não encontrado!")
        return
    if not titulo_livro:
        messagebox.showwarning("Erro", "Livro não encontrado!")
        return

    # Registrar a devolução e verificar se foi bem-sucedida
    if gerenciador_bd.registrar_devolucao(usuario_id, livro_id):
        # Atualizar a lista de livros
        listar_livros(listbox_livros)
        exibir_emprestimos_ativos_interface(listbox_historico)  # Atualiza o histórico

        # Registrando ação no histórico
        data_devolucao = datetime.now().strftime("%d/%m/%Y")
        gerenciador_bd.registrar_acao_historico(usuario_id, nome_usuariozz, livro_id, titulo_livro, data_devolucao, 'Devolução')
    else:
        messagebox.showwarning("Erro", "Não foi possível registrar a devolução.")

# Funcao para obter o historio de acoes
def exibir_emprestimos_ativos_interface(listbox_historico):
    # Limpar o Listbox de histórico
    listbox_historico.delete(0, tk.END)

    # Obter o histórico do gerenciador
    registros = gerenciador_bd.listar_emprestimos_ativos()

    # Insere os registros de empréstimos em andamento
    for registro in registros:
        emprestimo_id = registro[0]
        usuario_id = registro[1]
        usuario_nome = registro[2]
        livro_id = registro[3]
        livro_titulo = registro[4]
        data_emprestimo = registro[5]
        listbox_historico.insert(tk.END, f"Aluno: {usuario_nome} - ID: {usuario_id} |  Livro: {livro_titulo} - ID:{livro_id} - (Empréstimo em: {data_emprestimo})")

# Função para abrir a janela de filtro de busca
def filtro_busca_historico_interface(data_historico_listbox):
    # Criar uma nova janela para o filtro de busca
    janela_filtro = tk.Toplevel()
    janela_filtro.title("Filtro de Busca")

    # Obter o ano atual
    ano_atual = datetime.now().year

    # Criar lista de opções de meses
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]
    mes_atual = meses[datetime.now().month - 1]  # Mês atual em formato de texto

    # Dropdown para selecionar o mês
    label_mes = tk.Label(janela_filtro, text="Mês:")
    label_mes.pack()
    dropdown_mes = tk.StringVar(value=mes_atual)
    menu_mes = tk.OptionMenu(janela_filtro, dropdown_mes, *meses)
    menu_mes.pack()

    # Dropdown para selecionar o ano
    label_ano = tk.Label(janela_filtro, text="Ano:")
    label_ano.pack()
    dropdown_ano = tk.StringVar(value=ano_atual)
    menu_ano = tk.OptionMenu(janela_filtro, dropdown_ano, *range(ano_atual - 2, ano_atual + 1))
    menu_ano.pack()

    # Botão para confirmar a busca
    btn_busca = tk.Button(
        janela_filtro, 
        text="Busca", 
        command=lambda: buscar_historico(dropdown_mes.get(), dropdown_ano.get(), janela_filtro, data_historico_listbox)
    )
    btn_busca.pack(pady=10)

# Função para retornar os resultados da busca no histórico
def buscar_historico(mes, ano, janela, data_historico_listbox):
    # Fechar a janela de filtro após a busca
    janela.destroy()

    # Limpar o listbox antes de inserir novos dados
    data_historico_listbox.delete(0, tk.END)

    # Adicionar o título ao listbox
    data_historico_listbox.insert(tk.END, f"Mostrando Histórico de {mes} - {ano}")

    # Obter dados filtrados do banco de dados 
    registros = filtro_busca_historico(mes, ano)

    # Adicionar registros ao listbox
    # Inserir os registros de histórico formatados no Listbox
    for registro in registros:
        usuario_id = registro[0]
        usuario_nome = registro[1]
        livro_id = registro[2]
        livro_titulo = registro[3]
        data_emprestimo = registro[4]  # data_acao do histórico
        acao = registro[5]  # Tipo de ação: 'Empréstimo' ou 'Devolução'
        
        # Inserir no Listbox com a formatação desejada
        data_historico_listbox.insert(
            tk.END,
            f"Aluno: {usuario_nome} - ID: {usuario_id} | Livro: {livro_titulo} - ID: {livro_id} - ({acao} em: {data_emprestimo})"
        )