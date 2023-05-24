from modules_definitions import *
from functions_pag import *
from functions_janela import *


class App(tk.Tk): # Classe das telas.
    def __init__(self): # Tela principal.
        super().__init__()

        geometria_tela(self, 700, 580, 50)                  # Dimensão e posição.
        self.title('Sistema de Condicional')            # Define o título.
        self.iconbitmap(f'{path_img}/janela_icon.ico')  # Define o ícone.
        self.configure(bg=COR_FUNDO2)                    # Define a cor de fundo.
        
        espaco_vazio = tk.Frame(self, height=20, bg=COR_FUNDO2)
        espaco_vazio.pack()  # Espaço vazio na self.
        
        label_condExistentes = tk.Label(self, font=FONTE_TITULO, bg=COR_FUNDO2, text="Condicionais existentes")
        label_condExistentes.pack() # Label texto.

        frame_lista_arquivos = tk.Frame(self, bg=COR_FUNDO2)
        frame_lista_arquivos.pack(pady=5)

        lista_arquivos = tk.Listbox(frame_lista_arquivos, width=50, height=12, bg=COR_FUNDO, font=FONTE_GERAL)
        lista_arquivos.pack(side='left', fill='both', expand=True) # Lista de arquivos.

        # Scrollbar para a lista de arquivos.
        scrollbar = ttk.Scrollbar(frame_lista_arquivos, orient='vertical', command=lista_arquivos.yview)
        scrollbar.pack(side='right', fill='y')
        lista_arquivos.config(yscrollcommand=scrollbar.set)

        atualiza_lista_arquivos(lista_arquivos)

        lista_arquivos.focus_set() # Para selecionar o primeiro elemento da lista.

        # Label para espaço vazio.
        espaco_vazio2 = tk.Frame(self, height=20, bg=COR_FUNDO2)
        espaco_vazio2.pack()

        # Botões da Primeira fileira.
        frame_botoes = tk.Frame(self, bg=COR_FUNDO2)
        frame_botoes.pack(pady=10) # Frame de botões 1.

        btn_criarCond = tk.Button(frame_botoes, text='Criar condicional', command=lambda: criar_condicional(lista_arquivos), bg=COR_BOTAO_FUNDO,
                                fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
        btn_criarCond.bind('<Enter>', on_enter)
        btn_criarCond.bind('<Leave>', on_leave)
        btn_criarCond.pack(side='left', padx=12)

        btn_mostrarCond = tk.Button(frame_botoes, text='Mostrar condicional', command=lambda: mostrar_condicional(lista_arquivos), bg=COR_BOTAO_FUNDO,
                                    fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
        btn_mostrarCond.bind('<Enter>', on_enter)
        btn_mostrarCond.bind('<Leave>', on_leave)
        btn_mostrarCond.pack(side='left', padx=12)
        self.bind('<Return>', lambda event: btn_mostrarCond.invoke())

        btn_delCond = tk.Button(frame_botoes, text='Deletar condicional', command=lambda: deletar_condicional(lista_arquivos), bg=COR_BOTAO_FUNDO,
                                fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
        btn_delCond.bind('<Enter>', on_enter)
        btn_delCond.bind('<Leave>', on_leave)
        btn_delCond.pack(side='left', padx=12)

        # Botões da Segunda fileira.
        frame_botoes2 = tk.Frame(self, bg=COR_FUNDO2)
        frame_botoes2.pack(pady=10) # Frame de botões 2.

        btn_addProd = tk.Button(frame_botoes2, text='Adicionar peça', command=lambda: self.tela_adicionar(lista_arquivos.get(tk.ACTIVE)), bg=COR_BOTAO_FUNDO,
                                fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
        btn_addProd.bind('<Enter>', on_enter)
        btn_addProd.bind('<Leave>', on_leave)
        btn_addProd.pack(side='left', padx=12)

        btn_delProd = tk.Button(frame_botoes2, text='Remover peça', command=lambda: self.tela_remover(lista_arquivos.get(tk.ACTIVE)), bg=COR_BOTAO_FUNDO,
                                fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
        btn_delProd.bind('<Enter>', on_enter)
        btn_delProd.bind('<Leave>', on_leave)
        btn_delProd.pack(side='left', padx=12)

        btn_closeCond = tk.Button(frame_botoes2, text='Lançar no sistema', command=lambda: fechar_condicional(lista_arquivos.get(tk.ACTIVE), self), bg=COR_BOTAO_FUNDO_ESPECIAL,
                                fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
        btn_closeCond.bind('<Enter>', on_enter)
        btn_closeCond.bind('<Leave>', on_leave2)
        btn_closeCond.pack(side='left', padx=12)

        # Botões da Terceira fileira.
        # Adicionar botão com ícone de lixeira.
        imagem = Image.open(f'{path_img}/lixeira.png')
        imagem = imagem.resize((60, 60))          # Redimensionar a imagem se necessário.
        icone = ImageTk.PhotoImage(imagem)

        # ATENÇÃO NO QUE ESTÁ PASSANDO PARA tela_lixeira
        btn_lixeira = tk.Button(self, image=icone, command=lambda: self.tela_lixeira(lista_arquivos), bg=COR_BOTAO_FUNDO,
                                fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
        btn_lixeira.bind('<Enter>', on_enter)
        btn_lixeira.bind('<Leave>', on_leave)
        btn_lixeira.image = icone  # salvar uma referência à imagem para evitar o Garbage Collector
        btn_lixeira.pack(pady=20) 


    def tela_remover(self, arquivo): # Tela "Remover Produto"

        # Ler o arquivo df.
        arquivo = f'{arquivo}.xlsx' # Nome do arquivo com .xlsx       
        df = pd.read_excel(arquivo, index_col=0, dtype={'Código': str, 'Referência': str, 'Descrição': str, 'Marca': str, 'Preço': str, 'Desconto': float, 'Status': str})

        if not len(df) > 0: # Verifica se o condicional está vazio.
            messagebox.showwarning('AVISO', 'O condicional está vazio!')
            return
        
        # Criar self.
        window_remover = tk.Toplevel(self)
        #window_remover.geometry('610x430+330+120')
        geometria_tela(window_remover, 600, 500, 35) 
        window_remover.title('Remover produto')
        window_remover.iconbitmap(f'{path_img}/janela_icon.ico')
        window_remover.configure(bg=COR_FUNDO2)

        df_gatos = df.loc[df['Marca'] == 'GA']              # Filtrar apenas produtos 'GA'.
        colunas = ['Referência', 'Descrição', 'Preço', 'Desconto', 'Status'] # Lista de colunas a serem exibidas no Treeview.
        df_gatos = df_gatos[colunas]                        # Seleciona apenas as colunas importantes.
        df_gatos['Desconto'] = df_gatos['Desconto'] * 100   # Muda a porcentagem corretamente.

        # Espaço vazio.
        espaco_vazio = tk.Frame(window_remover, height=1, bg=COR_FUNDO2)
        espaco_vazio.grid(row=0, column=0, padx=1, pady=5, sticky=tk.W)

        # Código.
        label_codigo = tk.Label(window_remover, text='Escanear o código \nde barras do produto', font=FONTE_GERAL, bg=COR_FUNDO2)
        label_codigo.grid(row=1, column=1, padx=30, pady=5, sticky=tk.W)

        entry_codigo = tk.Entry(window_remover, width=40)
        entry_codigo.grid(row=1, column=2)
        entry_codigo.focus_set()

        # Espaço vazio.
        espaco_vazio = tk.Frame(window_remover, height=1, bg=COR_FUNDO2)
        espaco_vazio.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

        # Texto GATOS & ATOS.
        label_gatos = tk.Label(window_remover, text='GATOS ', font=FONTE_TITULO, bg=COR_FUNDO2)
        label_gatos.grid(row=3, column=1, pady=10, sticky=tk.E)

        label_atos = tk.Label(window_remover, text='& ATOS', font=FONTE_TITULO, bg=COR_FUNDO2)
        label_atos.grid(row=3, column=2, pady=10, sticky=tk.W)

        # Criar o Treeview para exibir a lista de produtos.
        lista_produtos = ttk.Treeview(window_remover, columns=colunas, show='headings')
        lista_produtos.grid(row=4, column=1, columnspan=2, padx=25, pady=5, sticky=tk.NSEW)

        # Definir o tamanho das colunas e alinhamento.
        for col in colunas:
            lista_produtos.heading(col, text=col, anchor='center')
            if col == 'Descrição':
                lista_produtos.column(col, width=250, anchor='center')
            elif col == 'Desconto' or col == 'Status':
                lista_produtos.column(col, width=60, anchor='center')
            else:
                lista_produtos.column(col, width=80, anchor='center')

        # Adicionar os produtos ao Treeview.
        for index, row in df_gatos.iterrows():
            lista_produtos.insert('', 'end', text=index, values=row[colunas].tolist())

        # Espaço vazio.
        espaco_vazio = tk.Frame(window_remover, height=1, bg=COR_FUNDO2)
        espaco_vazio.grid(row=5, column=1, padx=10, pady=1, sticky=tk.W)

        # Botão remover e cancelar.
        # Botões botões.
        frame_botoes = tk.Frame(window_remover, bg=COR_FUNDO2)
        frame_botoes.grid(row=6, columnspan=3, padx=90, pady=30) # Frame de botões.

        btn_remover = tk.Button(frame_botoes, text='Remover', width=10, command=lambda: remover_produto(arquivo, entry_codigo, window_remover), bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE, padx=10, pady=5, bd=0, font=FONTE_BTN)
        btn_remover.bind('<Enter>', on_enter)
        btn_remover.bind('<Leave>', on_leave)
        btn_remover.pack(side='left', padx=45)
        window_remover.bind('<Return>', lambda event: btn_remover.invoke())

        btn_cancelar = tk.Button(frame_botoes, text='Cancelar', width=10, command=window_remover.destroy, bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE, padx=10, pady=5, bd=0, font=FONTE_BTN)
        btn_cancelar.bind('<Enter>', on_enter)
        btn_cancelar.bind('<Leave>', on_leave)
        btn_cancelar.pack(side='left', padx=45)
        window_remover.bind('<Escape>', lambda event: btn_cancelar.invoke())

        def editar_celula(event) -> None: # Função para editar o valor da célula.
            item = lista_produtos.selection()[0]             # Obter item selecionado.
            coluna = lista_produtos.identify_column(event.x) # Obter coluna clicada.

            if coluna == '#5': # Define a coluna.
                coluna = 'Status'

                # Obter valor da célula.
                valor = lista_produtos.item(item, 'values')[colunas.index(coluna)]

                # Criar menu de opções.
                menu_opcoes = tk.Menu(window_remover, tearoff=0)
                menu_opcoes.add_command(label='ON', command=lambda: atualizar_valor(item, coluna, 'ON'))
                menu_opcoes.add_command(label='OFF', command=lambda: atualizar_valor(item, coluna, 'OFF'))

                # Mostrar menu de opções.
                menu_opcoes.post(event.x_root, event.y_root)

        def atualizar_valor(item, coluna : str, valor : str) -> None: # Função para atualizar o valor na coluna status.
            lista_produtos.set(item, coluna, valor)

            # Atualizar dataframe
            referencia = lista_produtos.item(item, 'text')
            df_gatos.loc[referencia, coluna] = valor
            df.loc[referencia, coluna] = valor

            save_dataframe_to_excel(df, arquivo)

        # Adicionar evento de duplo clique na coluna 'Status'
        lista_produtos.bind('<Double-Button-1>', editar_celula)


    def tela_adicionar(self, arquivo): # Tela "Adicionar Produto"
        
        largura_entry = 40

        # Nova tela adicionar produtos.
        window_adicionar = tk.Toplevel(self)
        #window_adicionar.geometry('590x400+330+150')
        geometria_tela(window_adicionar, 600, 500, 35) 
        window_adicionar.title('Adicionar Produto')
        window_adicionar.iconbitmap(f'{path_img}/janela_icon.ico')
        window_adicionar.configure(bg=COR_FUNDO2)

        # Espaço vazio.
        espaco_vazio = tk.Frame(window_adicionar, width=5, height=5, bg=COR_FUNDO2)
        espaco_vazio.grid(row=0, column=0, sticky=tk.W)

        # Texto ESCANEAR CÓDIGO.
        label_escanear = tk.Label(window_adicionar, text='ESCANEAR', font=FONTE_TITULO, bg=COR_FUNDO2)
        label_escanear.grid(row=1, column=1, pady=10, sticky=tk.E)

        label_cd = tk.Label(window_adicionar, text=' CÓDIGO', font=FONTE_TITULO, bg=COR_FUNDO2)
        label_cd.grid(row=1, column=2, pady=10, sticky=tk.W)

        # Código.
        label_codigo = tk.Label(window_adicionar, text='Código de barras:', font=FONTE_GERAL, bg=COR_FUNDO2)
        label_codigo.grid(row=2, column=1, sticky=tk.E)

        entry_codigo = tk.Entry(window_adicionar, width=largura_entry)
        entry_codigo.grid(row=2, column=2)
        entry_codigo.focus_set()

        # Desconto.
        label_desconto = tk.Label(window_adicionar, text='Desconto', font=FONTE_GERAL, bg=COR_FUNDO2)
        label_desconto.grid(row=3, column=1, padx=35, pady=10, sticky=tk.E)

        entry_desconto = tk.Entry(window_adicionar, width=largura_entry)
        entry_desconto.grid(row=3, column=2)
        entry_desconto.insert(0, '0')  # definir valor padrão como 0

        # Espaço vazio.
        espaco_vazio = tk.Frame(window_adicionar, height=35, bg=COR_FUNDO2)
        espaco_vazio.grid(row=4, column=1, sticky=tk.W)

        # Texto GATOS & ATOS.
        label_gatos = tk.Label(window_adicionar, text='GATOS', font=FONTE_TITULO, bg=COR_FUNDO2)
        label_gatos.grid(row=5, column=1, pady=2, sticky=tk.E)

        label_atos = tk.Label(window_adicionar, text='& ATOS', font=FONTE_TITULO, bg=COR_FUNDO2)
        label_atos.grid(row=5, column=2, pady=2, sticky=tk.W)
        
        # Referência
        label_referencia = tk.Label(window_adicionar, text='Referência',font=FONTE_GERAL, bg=COR_FUNDO2)
        label_referencia.grid(row=6, column=1, padx=20, pady=10, sticky=tk.E)

        entry_referencia = tk.Entry(window_adicionar, width=largura_entry)
        entry_referencia.grid(row=6, column=2)

        # Descrição.
        label_descricao = tk.Label(window_adicionar, text='Descrição', font=FONTE_GERAL, bg=COR_FUNDO2)
        label_descricao.grid(row=7, column=1, padx=20, pady=10, sticky=tk.E)

        entry_descricao = tk.Entry(window_adicionar, width=largura_entry)
        entry_descricao.grid(row=7, column=2)

        # Preço.
        label_preco = tk.Label(window_adicionar, text='Preço', font=FONTE_GERAL, bg=COR_FUNDO2)
        label_preco.grid(row=8, column=1, padx=38, pady=10, sticky=tk.E)

        entry_preco = tk.Entry(window_adicionar, width=largura_entry)
        entry_preco.grid(row=8, column=2)

        # Desconto GA.
        label_desconto_ga = tk.Label(window_adicionar, text='Desconto', font=FONTE_GERAL, bg=COR_FUNDO2)
        label_desconto_ga.grid(row=9, column=1, padx=20, pady=10, sticky=tk.E)

        entry_desconto_ga = tk.Entry(window_adicionar, width=largura_entry)
        entry_desconto_ga.grid(row=9, column=2)
        entry_desconto_ga.insert(0, '0')  # definir valor padrão como 0

        # Botões botões.
        frame_botoes = tk.Frame(window_adicionar, bg=COR_FUNDO2)
        frame_botoes.grid(row=10, columnspan=3, padx=90, pady=20) # Frame de botões.

        btn_adicionar = tk.Button(frame_botoes, text='Adicionar', width=8, command=lambda: adicionar_produto(arquivo, entry_codigo, entry_desconto, entry_referencia, entry_descricao, entry_preco, entry_desconto_ga, window_adicionar), bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE, padx=10, pady=5, bd=0, font=FONTE_BTN)
        btn_adicionar.bind('<Enter>', on_enter)
        btn_adicionar.bind('<Leave>', on_leave)
        #btn_adicionar.bind('<Button-1>', lambda event: btn_adicionar.invoke())
        btn_adicionar.pack(side='left', padx=45)
        window_adicionar.bind('<Return>', lambda event: btn_adicionar.invoke())

        btn_cancelar = tk.Button(frame_botoes, text='Cancelar', width=8, command=window_adicionar.destroy, bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE, padx=10, pady=5, bd=0, font=FONTE_BTN)
        btn_cancelar.bind('<Enter>', on_enter)
        btn_cancelar.bind('<Leave>', on_leave)
        btn_cancelar.pack(side='left', padx=45)
        window_adicionar.bind('<Escape>', lambda event: btn_cancelar.invoke())

        #window_adicionar.transient(self)
        #window_adicionar.grab_set()
        #self.wait_window(window_adicionar)


    def tela_lixeira(self, lista_arquivos): # Tela "Lixeira"
        try:

            # Lista os arquivos por data.
            arquivos = sorted([arquivo for arquivo in os.listdir(f'{path_lixeira}.') if arquivo.endswith('.xlsx')])
            
            if len(arquivos) > 0: # Se a lixeira não estiver vazia.
            
                # Cria uma nova self topLevel.
                window_lixeira = tk.Toplevel(self)
                #window_lixeira.geometry('800x500+300+120')
                geometria_tela(window_lixeira, 600, 570, 35)
                window_lixeira.title('Condicionais Apagados')
                window_lixeira.iconbitmap(f'{path_img}/janela_icon.ico')
                window_lixeira.configure(bg=COR_FUNDO2)

                # Espaço vazio.
                espaco_vazio = tk.Frame(window_lixeira, height=40, bg=COR_FUNDO2)
                espaco_vazio.pack()

                # Texto cond. apagados.
                label_condApagados = tk.Label(window_lixeira, text='Condicionais apagados', font=FONTE_TITULO, bg=COR_FUNDO2)
                label_condApagados.pack()

                # Frame para lista de arquivos.
                frame_lista_arquivos = tk.Frame(window_lixeira, bg=COR_FUNDO2)
                frame_lista_arquivos.pack(pady=5)

                lista_arquivos_apagados = tk.Listbox(frame_lista_arquivos, width=50, height=12, bg=COR_FUNDO, font=FONTE_GERAL)
                lista_arquivos_apagados.pack(side='left', fill='both', expand=True) # Lista de arquivos apagados.

                # Scrollbar para a lista de arquivos.
                scrollbar = ttk.Scrollbar(frame_lista_arquivos, orient='vertical', command=lista_arquivos_apagados.yview)
                scrollbar.pack(side='right', fill='y')
                lista_arquivos_apagados.config(yscrollcommand=scrollbar.set)

                atualiza_lista_arquivos(lista_arquivos_apagados, 'lixeira')

                lista_arquivos_apagados.focus_set() # Para selecionar o primeiro elemento da lista.

                # Espaço vazio.
                espaco_vazio = tk.Frame(window_lixeira, height=40, bg=COR_FUNDO2)
                espaco_vazio.pack()
                
                # Frame para os botões "Restaurar" e "apagar"
                frame_botoes = tk.Frame(window_lixeira, bg=COR_FUNDO2)
                frame_botoes.pack(pady=5) # Frame de botões.

                # Botão para restaurar condicional.
                btn_restaurar = tk.Button(frame_botoes, text='Restaurar', width=12, command=lambda : restaurar_condicional(lista_arquivos, lista_arquivos_apagados.get(tk.ACTIVE), window_lixeira), bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
                btn_restaurar.bind('<Enter>', on_enter)
                btn_restaurar.bind('<Leave>', on_leave)
                btn_restaurar.pack(side='left', padx=10)
                btn_restaurar.bind('<Button-1>', lambda event: btn_restaurar.invoke())
                window_lixeira.bind('<Return>', lambda event: btn_restaurar.invoke())

                # Botão para apagar um único condicional.
                btn_deletar = tk.Button(frame_botoes, text='Apagar', width = 12, command=lambda : apagar_condicional(lista_arquivos, lista_arquivos_apagados.get(tk.ACTIVE), window_lixeira), bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
                btn_deletar.bind('<Enter>', on_enter)
                btn_deletar.bind('<Leave>', on_leave)
                btn_deletar.pack(side='left', padx=10)

                # Botão cancelar e voltar para tela anterior.
                btn_cancelar = tk.Button(frame_botoes, text='Voltar', width=12, command=window_lixeira.destroy, bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE, padx=10, pady=5, bd=0, font=FONTE_BTN)
                btn_cancelar.bind('<Enter>', on_enter)
                btn_cancelar.bind('<Leave>', on_leave)
                btn_cancelar.pack(side='left', padx=10)
                window_lixeira.bind('<Escape>', lambda event: btn_cancelar.invoke())

                # Frame2 para o botão "limpar lixeira"
                frame_botoes2 = tk.Frame(window_lixeira, bg=COR_FUNDO2)
                frame_botoes2.pack(pady=25) # Frame de botões.

                # Botão para limpar a lixeira.
                btn_limpar = tk.Button(frame_botoes2, text='Limpar Lixeira', width=17, command=lambda : limpar_lixeira(window_lixeira), bg=COR_BOTAO_FUNDO_ESPECIAL,fg=COR_BOTAO_FONTE, font=FONTE_BTN, padx=10, pady=5, bd=0)
                btn_limpar.bind('<Enter>', on_enter)
                btn_limpar.bind('<Leave>', on_leave2)
                btn_limpar.pack(side='left', padx=150)

            else:
                messagebox.showwarning('AVISO', 'A lixeira está vazia!')
        except:
            messagebox.showerror('ERROR', 'ERRO NO SISTEMA, CONTATE O SUPORTE!')


if __name__ == "__main__":
    app = App()
    app.mainloop()