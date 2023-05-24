# Bibliotecas utilizadas.
import os
import pyautogui as pag
import pandas as pd
import clipboard as clip
from datetime import datetime
import ctypes
from tkinter import simpledialog, messagebox, ttk
import tkinter as tk
from PIL import Image, ImageTk

# Bibliotecas para o Excel.
import openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Border, Side, Font, Alignment, numbers
from openpyxl.utils.dataframe import dataframe_to_rows

# Constantes.
COR_FUNDO = '#ffffff'
COR_FUNDO2 = "#E0E0E0"
COR_BOTAO_FUNDO = '#314cf7'
COR_BOTAO_FUNDO_ESPECIAL = '#c25456'
COR_BOTAO_FONTE = '#ffffff'
COR_FONTE = '#000000'
FONTE_GERAL = ('Arial', 14)
FONTE_TITULO = ('Arial', 14, 'bold')
FONTE_BTN = ('Arial', 12)

# Definições
# Tempo de Pausa na automação.
pag.PAUSE = 0.2
# Interrompe automação pag.
pag.FAILSAFE = True
# Endereço imagens.
path_img = r'C:\Sistemas\Condicionais\img'
# Endereço condicionais apagados.
path_lixeira = r'C:\Sistemas\Condicionais\lixeira'
# Endereço condicionais.
path_condicional = r'C:\Sistemas\Condicionais\arquivos_condicionais'
# Pasta padrão.
os.chdir(path_condicional)
# Data atual.
atual = datetime.now()
