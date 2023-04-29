from modules_definitions import *


# Função para alterar a geometria da janela.
def geometria_tela(janela: tk, width_janela: int, height_janela: int, desl_y: int) -> None:
    """
        Função para definir a geometria da janela, tamanho e posição.

        Parâmetros:
        janela: janela a ser redimensionada.
        width: largura da janela.
        height: altura da janela.
        desl_y: deslocamento em y.

        Retorno:
        Nenhum.
    """

    width_tela = janela.winfo_screenwidth()
    height_tela = janela.winfo_screenheight()
    x = (width_tela // 2) - (width_janela // 2)
    y = (height_tela // 2) - (height_janela // 2) - desl_y   # deslocamenteo em y.

    janela.geometry('{}x{}+{}+{}'.format(width_janela, height_janela, x, y))


# Função a ser executada quando o mouse entrar na área dos botões.
def on_enter(event) -> None:
    """
        Muda a cor dos botões comum ao passar o mouse.

        Parâmetros:
        event: evento do mouse.

        Retorno:
        Nenhum.
    """

    event.widget.config(bg='#42e54c', fg='#000000',
                        relief=tk.SUNKEN, font=FONTE_BTN)


# Função a ser executada quando o mouse sair da área dos botões.
def on_leave(event) -> None:
    """
        Volta a cor do botões comum ao original.

        Parâmetros:
        event: evento do mouse.

        Retorno:
        Nenhum.
    """

    event.widget.config(bg=COR_BOTAO_FUNDO, fg=COR_BOTAO_FONTE,
                        relief=tk.FLAT, font=FONTE_BTN)


# Função a ser executada quando o mouse sair da área dos botões especiais.
def on_leave2(event) -> None:
    """
        Volta a cor do botões ESPECIAIS ao original.

        Parâmetros:
        event: evento do mouse.

        Retorno:
        Nenhum.
    """

    event.widget.config(bg=COR_BOTAO_FUNDO_ESPECIAL, fg=COR_BOTAO_FONTE,
                        relief=tk.FLAT, font=FONTE_BTN)
