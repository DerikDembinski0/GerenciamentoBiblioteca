import tkinter as tk
from tkinter import messagebox
import ponte
from ponte import (
    criar_banco, 
    adicionar_usuario_interface, 
    listar_usuarios, 
    adicionar_livros_interface, 
    listar_livros, 
    registrar_emprestimo_interface, 
    registrar_devolucao_interface,
    exibir_emprestimos_ativos_interface,
    listar_emprestimos_ativos,
    filtro_busca_historico_interface
)


# Criar a interface gráfica principal
root = tk.Tk()
root.title("Gerenciamento de Biblioteca")
root.geometry("1100x600")


# Criar banco de dados
criar_banco()




# Interface para adicionar usuários
#Um LabelFrame é basicamente um contêiner que pode agrupar
# widgets (como Entry, Button, etc.) e tem um título na borda.
aba_add_usuario = tk.LabelFrame(root, text="Adicionar Usuario", padx=10, pady=10)
aba_add_usuario.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
#Inserindo container com lugar para add o nome do usuario
tk.Label(aba_add_usuario, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(aba_add_usuario)
entry_nome.grid(row=0, column=1)
#Inserindo container com lugar para add o email do usuario
tk.Label(aba_add_usuario, text="Email:").grid(row=1, column=0)
entry_email = tk.Entry(aba_add_usuario)
entry_email.grid(row=1, column=1)
#Inserindo botao para confirmar a insercao do usuario
btn_add_user = tk.Button(aba_add_usuario, text="Adicionar Usuario", command=lambda: adicionar_usuario_interface(entry_nome, entry_email, listbox_usuarios))
btn_add_user.grid(row=2, columnspan=2, pady=10)
#Lambda é uma funcao intermediaria sem valor real
#Nesse caso temos a necessidade de usala pois sem ela a funcao adicionar_usuario seria executada assim que for lida
#Porem como temos o Lambda intermediando ela so sera executada quando o botao e apertado

#Interface para listar usuários
#Inserindo aba onde vao aparecer a lista de usuarios
aba_listar_user = tk.LabelFrame(root, text="Lista de Usuarios", padx=10, pady=10)
aba_listar_user.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
listbox_usuarios = tk.Listbox(aba_listar_user, width=80, height=10)
listbox_usuarios.pack()
listar_usuarios(listbox_usuarios)  # Carregar usuários ao iniciar


#Interface para adicionar livros
#Um LabelFrame é basicamente um contêiner que pode agrupar
# widgets (como Entry, Button, etc.) e tem um título na borda.
aba_add_livro = tk.LabelFrame(root, text="Adicionar Livro", padx=10, pady=10)
aba_add_livro.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
#Inserindo container com lugar para add o titulo do livro
tk.Label(aba_add_livro, text="Titulo:").grid(row=0, column=0)
entry_titulo = tk.Entry(aba_add_livro)
entry_titulo.grid(row=0, column=1)
#Inserindo botao para confirmar a adicao do livro
btn_add_livro = tk.Button(aba_add_livro, text="Adicionar Livro", command=lambda:adicionar_livros_interface(entry_titulo, listbox_livros))
btn_add_livro.grid(row=2, columnspan=2, pady=10)

# Interface para listar livros aba onde aparecerao os livros ja registrados
aba_listar_livro = tk.LabelFrame(root, text="Lista de Livros", padx=10, pady=10)
aba_listar_livro.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
listbox_livros = tk.Listbox(aba_listar_livro, width=80, height=10)
listbox_livros.pack()
listar_livros(listbox_livros)  # Carregar livros ao iniciar



#Interface para registrar empréstimos
aba_registrar_emprestimo = tk.LabelFrame(root, text="Registrar Emprestimo", padx=10, pady=10)
aba_registrar_emprestimo.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
#Inserir campo para o ID do usuário
tk.Label(aba_registrar_emprestimo, text="ID Do Usuario:").grid(row=0, column=0, sticky="e")
entry_usuario_id_emprestimo = tk.Entry(aba_registrar_emprestimo)
entry_usuario_id_emprestimo.grid(row=0, column=1)
#Inserir campo para o ID do livro
tk.Label(aba_registrar_emprestimo, text="ID do Livro:").grid(row=1, column=0, sticky="e")
entry_livro_id = tk.Entry(aba_registrar_emprestimo)
entry_livro_id.grid(row=1, column=1)
#Inserindo botao de registrar emprestimo
btn_registrar_emprestimo = tk.Button(aba_registrar_emprestimo, text="Registrar Emprestimo", command=lambda:registrar_emprestimo_interface(
    entry_usuario_id_emprestimo, entry_livro_id, listbox_livros,listbox_historico))
btn_registrar_emprestimo.grid(row=2, columnspan=2, pady=10)



# Interface para registrar devoluções
aba_registrar_devolucao = tk.LabelFrame(root, text="Registrar Devolucao", padx=10, pady=10)
aba_registrar_devolucao.grid(row=0, column=3, columnspan=2, padx=10, pady=10, sticky="nsew")
#Inserindo container para inserir o id do livro
tk.Label(aba_registrar_devolucao, text="ID Do livros:").grid(row=1, column=0)
entry_livro_id_devolucao = tk.Entry(aba_registrar_devolucao)
entry_livro_id_devolucao.grid(row=0, column=1)
#Inserir campo para o ID do usuário
tk.Label(aba_registrar_devolucao, text="ID Do Usuario:").grid(row=0, column=0)
entry_usuario_id = tk.Entry(aba_registrar_devolucao)
entry_usuario_id.grid(row=1, column=1)
#Inserindo botao para realizar a devolucao
btn_registrar_devolucao = tk.Button(aba_registrar_devolucao, text="Devolver Livro", command=lambda: registrar_devolucao_interface(
    entry_livro_id_devolucao, entry_usuario_id, listbox_livros, listbox_historico))
btn_registrar_devolucao.grid(row=2, columnspan=2, pady=10)




# Criar a interface da aba de Emprestimos Em Andamento
aba_historico = tk.LabelFrame(root, text="Emprestimos Em Andamento", padx=10, pady=10)
aba_historico.grid(row=1, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")
# Criar Listbox para exibir o histórico de Emprestimos Em Andamento
listbox_historico = tk.Listbox(aba_historico, width=80, height=10)
listbox_historico.pack()
exibir_emprestimos_ativos_interface(listbox_historico)  # Carregar historico ao iniciar



# Criar a interface da aba listar historico por data
historico_data = tk.LabelFrame(root, text="Historico Da Biblioteca", padx=10, pady=10)
historico_data.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="nsew")
#Criando a lista onde vai aparece o historico do mes desejado
data_historico_listbox = tk.Listbox(historico_data, width=80, height=10)
data_historico_listbox.pack()


# Botão para buscar empréstimos
btn_buscar_emprestimos = tk.Button(historico_data, text="Buscar Historico", command=lambda: filtro_busca_historico_interface(data_historico_listbox))
btn_buscar_emprestimos.pack(pady=5)
























# Iniciar o loop principal da interface
root.mainloop()


