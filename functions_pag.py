from modules_definitions import *

def VerificaTelaInicial() -> None: # Verifica se o Retaguarda está na tela inicial.
    """
        Verifica se o sistema RETAGUARDA está na tela inicial, caso contrário tenta voltar para ela.

        Parameters:
            None
        
        Returns:
            None
    """

    disable_caps_lock() # Desativar caps_lock.

    # Abrir sistema.
    pag.click(x=161, y=739)
    pag.click(x=161, y=640)

    # Lista todas as imagens da pasta.
    imagens = os.listdir(f'{path_img}')
    imagens_retaguarda = list(filter(lambda img: img.startswith('retaguarda'), imagens))
    
    try: # Se estiver na tela de vendas.
        pag.click(pag.center(pag.locateOnScreen(
            f'{path_img}/venda.png', grayscale=True, confidence=0.9)))
    except:
        try: # Se estiver nas outras telas. 
            for item in imagens_retaguarda:
                if (pag.locateOnScreen(f'{path_img}/{item}', grayscale=True, confidence=0.9)):
                    pag.press('esc')
                    break
        except:
            pass


def criar_condicional(lista_arquivos : list) -> None: # Função para criar um novo condicional.
    """
        Criar um arquivo .xlsx vazio, renomeado com o nome do cliente e data atual.

        Parameters:
            lista_arquivos: lista de arquivos.
        
        Returns:
            None
    """

    nome_cliente = simpledialog.askstring("Nome do Cliente", "\nDigite o nome do cliente para criar um novo condicional:\n")

    if nome_cliente:
        planilha = Workbook()                                           # Cria uma nova planilha vazia.
        arquivo = f'{nome_cliente} - {atual.strftime("%d_%m_%Y")}.xlsx' # Define o nome + a data atual.

        novo_arquivo = arquivo
        if os.path.exists(arquivo):                  # Verifica se o arquivo já existe no condicional.
            nome, data = arquivo.split(' - ')
            i = 1
            while True: # Adiciona um número no final do nome até não existir um igual.
                novo_arquivo = f'{nome} ({i}) - {data}' 
                if not os.path.exists(novo_arquivo):
                    break
                i += 1

        planilha.save(novo_arquivo)                                     # Salva o arquivo Excel.
        atualiza_lista_arquivos(lista_arquivos)                         # Atualiza os arquivos.


def mostrar_condicional(lista_arquivos : list) -> None: # Função que abre o arquivo excel.
    """
        Abre o arquivo excel.

        Parameters:
            lista_arquivos: lista de arquivos.
        
        Returns:
            None
    """
    
    arquivo = f'{lista_arquivos.get(tk.ACTIVE)}.xlsx'
    condicional_df = pd.read_excel(arquivo) # df do arquivo selecionado.

    if len(condicional_df) > 0:
        os.startfile(arquivo)
    else:
        messagebox.showwarning('AVISO', 'O condicional está vazio!')


def deletar_condicional(lista_arquivos : list) -> None: # Função para deletar o condicional.
    """
        Deleta o arquivo excel.

        Parameters:
            lista_arquivos: lista de arquivos.
        
        Returns:
            None
    """
    
    arquivo = f'{lista_arquivos.get(tk.ACTIVE)}.xlsx'
    space = ' ' * (42 - len(arquivo)) 
    if messagebox.askyesno('Deletar o condicional', '\nTem certeza que deseja deletar o condicional? \n\n{}{}\n'.format(space, arquivo[:-5].upper())):

        novo_arquivo = arquivo
        if os.path.exists(f'{path_lixeira}/{arquivo}'): # Verifica se o arquivo já existe na lixeira.
            nome, data = arquivo.split(' - ')
            i = 1
            while True: # Adiciona um número no final do nome até não existir um igual.
                novo_arquivo = f'{nome} ({i}) - {data}' 
                if not os.path.exists(f'{path_lixeira}/{novo_arquivo}'):
                    break
                i += 1
        
        os.rename(arquivo, f'{path_lixeira}/{novo_arquivo}') # Move o arquivo para pasta Lixeira.
        atualiza_lista_arquivos(lista_arquivos)              # Atualiza os arquivos.


def dados_produto(codigo : str) -> None: # Função para pegar os dados dentro do sistema da loja.
    """
        Automação para pegar as informações do produto no RETAGUARDA.

        Parameters:
            codigo: código do produto.
        
        Returns:
            referencia: referência do produto.
            descricao: descrição do produto.
            marca: marca do produto.
            preco: preço do produto.
            status: status do produto.
    """

    # Mudar opção de busca para código.
    pag.press('f4')         # Consultar produtos.
    pag.click(x=55, y=86)   # Apertar no menu.
    pag.write('Codigo')     # Digita Codigo.    
    pag.press('enter')  

    # Abrir opção de editar o produto daquele código.
    pag.write(codigo)
    pag.press('enter')
    pag.press('f2')

    # Se o código do produto for inválido.
    if pag.locateOnScreen(f'{path_img}/f2.png', grayscale=True, confidence=0.9):
        return

    # Pegar referência.
    pag.click(x=739, y=275, clicks=2)
    pag.hotkey('ctrl', 'c')
    referencia = clip.paste()

    # Pegar descrição.
    pag.press('tab')
    pag.hotkey('ctrl', 'c')
    descricao = clip.paste()

    # Pegar marca.
    pag.press('tab')
    pag.hotkey('ctrl', 'c')
    marca = clip.paste()

    # Pegar preco.
    pag.click(x=995, y=546, clicks=2)
    pag.hotkey('ctrl', 'c')
    preco = clip.paste()

    # Status.
    status = 'ON'

    # Fechar programa.
    pag.click(x=996, y=630)
    pag.press('esc')

    return referencia, descricao, marca, preco, status


def save_dataframe_to_excel(df, filename : str) -> None: # Converte o dataframe em excel mantendo as formatações.
    """
        Converte o dataframe em excel mantendo as formatações.

        Parameters:
            df: dataframe.
            filename: nome do arquivo.
        
        Returns:
            None
    """

    # Cria planilha.
    planilha = Workbook()
    aba_ativa = planilha.active

    # Converte o dataframe em excel.
    for row in dataframe_to_rows(df, index=True, header=True):
        aba_ativa.append([''] + row) # adiciona célula vazia na primeira coluna
    aba_ativa.delete_cols(idx=1)  # exclui coluna original 'A'

    # Define o estilo da borda.
    thin_border = Border(left=Side(style='thin'),
                         right=Side(style='thin'),
                         top=Side(style='thin'),
                         bottom=Side(style='thin'))

    # Define o estilo da fonte em negrito.
    bold_font = Font(bold=True)

    # Define o estilo da fonte em negrito para a primeira linha.
    for row in aba_ativa.iter_rows(min_row=1, max_row=1):
        for cell in row:
            cell.font = bold_font

    # Define negrito na primeira coluna.
    for cell in aba_ativa['A']:
        cell.font = bold_font

    # Define o alinhamento central.
    center_alignment = Alignment(horizontal='center', vertical='center')

    # Define as bordas para todas as células, exceto a segunda linha
    for row in aba_ativa.iter_rows():
        for cell in row:
            cell.border = thin_border
            cell.alignment = center_alignment

    # Deleta a segunda linha
    aba_ativa.delete_rows(idx=2)

    # Define o formato de número como "texto" para a coluna C em todas as linhas
    for row in aba_ativa.iter_rows():
        row[2].number_format = numbers.FORMAT_TEXT

    # Define o formato de número como "texto" para a coluna C em todas as linhas
    for row in aba_ativa.iter_rows():
        row[6].number_format = numbers.FORMAT_PERCENTAGE

    # Save the planilha
    planilha.save(filename)


def adicionar_produto(arquivo : str, codigo : str, desconto : float, referencia : str, descricao : str, preco : str, desconto_ga : float, window_adicionar : tk) -> None: # Adiciona o produto no condicional.
    """
        Adiciona o produto no condicional.

        Parameters:
            arquivo: nome do condicional selecionado sem o .xlxs.
            codigo: código do produto.
            referencia: referência do produto.
            descricao: descrição do produto.
            preco: preço do produto.
            desconto: desconto do produto.
            window_adicionar: janela de adicionar produto.
        
        Returns:
            None
    """
    
    #if True:
    try:
        window_adicionar.destroy()  # Fecha a janela após apertar no btn adicionar.

        arquivo = f'{arquivo}.xlsx' # Adiciona '.xlsx' no nome do arquivo.

        # Ler o condicional existente.
        df = pd.read_excel(arquivo, index_col=0, dtype={'Código': str, 'Referência': str, 'Descrição': str, 'Marca': str, 'Preço': str, 'Desconto': float, 'Status': str})
    
        if codigo: # Adiciona pelo código de barras.
            try:
                codigo = codigo[7:12] # Formata o código de barras para o código cadastrado no RETAGUARDA.

                if len(df) > 0 and codigo in df['Código'].dropna().tolist():
                    messagebox.showwarning('AVISO', 'Esse produto já está inserido no condicional!')
                    return

                # Abre o sitema, desativa caps lock e deixa na tela principal.
                VerificaTelaInicial()

                # Pegar os dados do produto.
                try:
                    referencia, descricao, marca, preco, status = dados_produto(codigo)
                except:
                    messagebox.showerror('ERROR', 'FALHA AO TENTAR PEGAR AS INFORMAÇÕES\n DO PRODUTO NO SISTEMA RETAGUARDA.') 
                    return

                # Adiciona uma nova linha no df.
                nova_linha = {'Código': codigo, 'Referência': referencia, 'Descrição': descricao,
                              'Marca': marca, 'Preço': preco, 'Desconto': desconto/100, 'Status': status}                
                df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                df.index += 1 # Altera o índice.

                save_dataframe_to_excel(df, arquivo) # Converte o df para um arquivo excel mantendo a formatação.
                
                messagebox.showinfo('SUCESSO', 'Item adicionado ao condicional.')

            except:
                messagebox.showerror('ERROR', 'ERRO NO PROGRAMA CONTATE O SUPORTE.')      
                    
        else: # Adiciona pelo GA.
            if referencia and descricao and preco:
                #if True:
                try:
                    # Adiciona uma nova linha no df.
                    nova_linha = {'Código': '', 'Referência': referencia.upper(), 'Descrição': descricao.upper(), 'Marca': 'GA', 'Preço': preco, 'Desconto': desconto_ga/100, 'Status': 'ON'}
                    df = pd.concat([df, pd.DataFrame(nova_linha, index=[0])], ignore_index=True)
                    df.index += 1

                    save_dataframe_to_excel(df, arquivo)

                    messagebox.showinfo('SUCESSO', 'Item adicionado ao condicional.')
                except:
                    messagebox.showerror('ERROR', 'ERRO NO PROGRAMA CONTATE O SUPORTE.')
    except:
        messagebox.showerror('ERROR', 'ERRO NO PROGRAMA CONTATE O SUPORTE.')


def remover_produto(arquivo : str, codigo : str, window_remover : tk) -> None: # Função para remover o produto do condicional.
    """
        Remove o produto do condicional.

        Parameters:
            arquivo: nome do condicional selecionado sem o .xlxs.
            codigo: código do produto.
            nova_janela: janela de remover produto.
        
        Returns:
            None
    """
    
    # Fecha a janela após apertar no btn remover o produto.
    window_remover.destroy()

    if codigo:
        try:
            codigo = codigo[7:12]                # Formata o código.
            wb = openpyxl.load_workbook(arquivo) # Carrega a planilha.
            ws = wb.active                       # Define a aba ativada.
            codigo_encontrado = False            # Variável para verificar se o código foi encontrado.

            rst = True                           # Variável para verificar se o produto já tinha sido removido.
            for row in ws.iter_rows(min_row=2):
                if str(row[1].value) == codigo:
                    if row[7].value == 'OFF':
                        rst = False
                        break # Testar
                    for cell in row:
                        if cell.column != 1 and cell.column != ws.max_column:
                            cell.font = Font(strikethrough=True) # tacha a fonte da célula
                        elif cell.column == ws.max_column and cell.value == "ON": 
                            cell.value = "OFF" # substitui o valor "ON" por "OFF"
                    codigo_encontrado = True  # código encontrado

            if codigo_encontrado:  # se o código foi encontrado, salva e mostra mensagem de sucesso
                wb.save(arquivo)  # Salva a planilha atualizada.
                if rst:
                    messagebox.showinfo('SUCESSO', 'Produto removido com sucesso.')
                else:
                    messagebox.showinfo('AVISO', 'Produto já tinha sido removido anteriormente.')

            else:  # se o código não foi encontrado, mostra mensagem de falha.
                messagebox.showerror('FALHA', 'Código do produto não encontrado.')
        except:
            messagebox.showerror('ERROR', 'ERRO NO PROGRAMA CONTATE O SUPORTE.')


def fechar_condicional(arquivo : str, self : tk) -> None: # Função para Fechar o condicional.
    """
        Fecha o condicional no sistema RETAGUARDA.

        Parameters:
            arquivo: nome do condicional selecionado sem o .xlxs..
            self: tela principal.

        Returns:
            None
    """

    arquivo = f'{arquivo}.xlsx'         # Nome do arquivo com .xlsx
    space = ' ' * (52 - len(arquivo))   # Espaço vazio para melhorar a visualização.

    # Ler o condicional existente.
    df = pd.read_excel(arquivo, index_col=0, dtype={'Código': str, 'Referência': str, 'Descrição': str, 'Marca': str, 'Preço': str, 'Desconto': float, 'Status': str})

    if len(df) > 0:  # Verifica se condicional está vazio.

        # Seleciona apenas as linhas com status ON.
        df = df[(df["Status"] == "ON")]

        if len(df) > 0:  # Se tiver produtos com status 'ON'.
            if messagebox.askyesno('Fechar condicional', '\nTem certeza que deseja lançar o condicional no sistema? \n\n{}{}\n'.format(space, arquivo[:-5].upper())):     
                
                try:
                    # Abre o sitema, desativa caps lock e deixa na tela principal.
                    VerificaTelaInicial()

                    # Lista contendo todos os códigos exceto "ga".
                    codigo_list = df['Código'].dropna().tolist()

                    # Verifica se tem produtos 'GA' no condicional.
                    ga_on = ((df['Marca'] == 'GA') & (df['Status'] == 'ON')).sum() > 0

                    if len(codigo_list) > 0: # Se existir produtos 'ON' com código.
                        pag.press('f5') # Abre o ORÇAMENTO.

                        if ga_on: # Faz ORÇAMENTO se tiver ga 'ON'.
                            pag.click(x=833, y=154)

                        for cod in codigo_list:  # Lança cada peça no RETAGUARDA.
                            pag.write(str(int(cod)))
                            for _ in range(4):
                                pag.press('enter')

                    if ga_on: # AVISO falta os prod ga.
                        self.iconify()
                        messagebox.showinfo('AVISO', 'Existe produtos ga para cadastrar e adicionar ao lançamento!')
                    else:
                        self.iconify()
                        messagebox.showinfo('AVISO', 'Todas as peças do condicional foram lançadas! Agora feche a nota.')
                        
                except:
                    messagebox.showerror('ERROR', 'ERRO NO PROGRAMA CONTATE O SUPORTE.')
        else:
            messagebox.showinfo('AVISO', 'Não tem peças para lançar\n\nO condicional foi devolvido por completo!')
    else:
        messagebox.showwarning('AVISO', 'O condicional está vazio!')


def disable_caps_lock() -> None: # Função para desativar o caps lock.
    """
        Desativa o caps lock.

        :param: None

        :return: None
    """

    if ctypes.windll.user32.GetKeyState(0x14) & 0xffff != 0: # Verifica o estado da tecla caps lock.
        pag.press('capslock')                                # Desativa a tecla caps lock.


def restaurar_condicional(lista_arquivos : list, arquivo : str, window_lixeira : tk) -> None: # Função para restaurar o condicional apagado.
    """
        Restaura um condicional apagado.

        Parameters:
            lista_arquivos: lista com todos os arquivos do condicional.
            arquivo: nome do arquivo selecionado sem o .xlxs da lixeira.
            window_lixeira: janela da lixeira.

        Returns:
            None
    """
    
    try:
        arquivo_selecionado = f'{arquivo}.xlsx' # Pega o nome do arquivo selecionado.
        
        novo_arquivo = arquivo_selecionado
        if os.path.exists(novo_arquivo): # Verifica se o arquivo já existe no condicional.
            nome, data = arquivo_selecionado.split(' - ')
            i = 1
            while True: # Adiciona um número no final do nome até não existir um igual.
                novo_arquivo = f'{nome} ({i}) - {data}' 
                if not os.path.exists(novo_arquivo):
                    break
                i += 1

        # Restaura o arquivo.
        caminho_origem = f'{path_lixeira}/{arquivo_selecionado}'
        caminho_destino = f'{path_condicional}/{novo_arquivo}'
        os.rename(caminho_origem, caminho_destino)

        atualiza_lista_arquivos(lista_arquivos)    # Atualiza os arquivos.
        window_lixeira.destroy()                   # Fecha a janela.
        messagebox.showinfo('Restaurado da lixeira', 'O condicional foi restaurado com sucesso!')
    except:
        messagebox.showerror('ERROR', 'NÃO FOI POSSÍVEL RESTAURAR O CONDICIONAL!')
            

def apagar_condicional(lista_arquivos : list, arquivo : str, window_lixeira : tk) -> None: # Função para remover um condicional da lixeira.
    """
        Apaga um condicional da lixeira.

        Parameters:
            lista_arquivos: lista com todos os arquivos do condicional.
            arquivo: nome do arquivo selecionado sem o .xlxs da lixeira.
            window_lixeira: janela da lixeira.

        Returns:
            None
    """
   
    try:
            arquivo_selecionado = f'{arquivo}.xlsx' # Pega o nome do arquivo selecionado.

            os.remove(f'{path_lixeira}/{arquivo_selecionado}')  # Remove cada arquivo da pasta da lixeira.
            
            window_lixeira.destroy()
            
            messagebox.showinfo('Removido da lixeira', 'Condicional removido da lixeira')
    except:
        messagebox.showerror('ERROR', 'NÃO FOI POSSÍVEL APAGAR TODOS OS CONDICIONAIS')


def limpar_lixeira(window_lixeira : tk) -> None: # Função para limpar a lixeira de condicionais.
    """
        Apaga todos os condicionais antigos.

        Parameters:
            window_lixeira: janela da lixeira.
        
        Returns:
            None
    """
   
    try:
        rst = messagebox.askyesno('APAGAR TUDO', 'Tem certeza que deseja apagar todos os condicionais antigos?', parent=window_lixeira)
        
        if rst: # Deletar todos os condidicionais antigos.
            
            # Pega a lista de arquivos apagados.
            arquivos_apagados = [arquivo for arquivo in os.listdir(f'{path_lixeira}.') if arquivo.endswith('.xlsx')]
            
            # Remove cada arquivo da pasta de backup.
            for arquivo in arquivos_apagados:
                os.remove(f'{path_lixeira}/{arquivo}')
            
            window_lixeira.destroy()
            
            messagebox.showinfo('Lixeira limpa', 'Todos os condicionais antigos foram removidos com sucesso!')
    except:
        messagebox.showerror('ERROR', 'NÃO FOI POSSÍVEL APAGAR TODOS OS CONDICIONAIS')


def atualiza_lista_arquivos(lista_arquivos : list, endereco : str = '') -> None: # Função para atualizar a lista de arquivos.
    """
        Atualiza a lista de arquivos existentes na janela.

        Parameters:
            lista_arquivos: Lista de arquivos existentes na janela.

        Returns: 
            None
    """

    def extrair_data(arquivo):
            data_str = arquivo.split(' - ')[-1].replace('.xlsx', '')
            return datetime.strptime(data_str, '%d_%m_%Y')
    
    if endereco != 'lixeira':
        arquivos = sorted([arquivo for arquivo in os.listdir('.') if arquivo.endswith('.xlsx')],
                key=extrair_data) # Lista os arquivos do condicional por data.
    else:
        arquivos = sorted([arquivo for arquivo in os.listdir(f'{path_lixeira}.') if arquivo.endswith('.xlsx')],
                key=extrair_data) # Lista os arquivos da lixeira por data.
    
    lista_arquivos.delete(0, tk.END) # Limpa a lista atual.

    # Adiciona os arquivos ordenados na lista.
    [lista_arquivos.insert(tk.END, arquivo.split('.')[0]) for arquivo in arquivos]


