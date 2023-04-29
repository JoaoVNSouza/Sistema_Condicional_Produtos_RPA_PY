
# Sistema completo para gerenciamento de condicionais de peças em uma loja de vestuário com interface gráfica em Python.

Este é um sistema completo desenvolvido para digitalizar o processo de gerenciamento de condicionais em uma loja de vestuário, automatizando os principais processos que envolvem o sistema principal da loja.


## Instalação

1. Clone o repositório.
2. Execute o arquivo "condicional - GUI.pyw" para iniciar a aplicação.
3. Configure os diretórios dos arquivos com imagens, condicionais e também a lixeira.     Altere as variáveis path_img, path_lixeira e path_condicional no arquivo "condicional - GUI.pyw" para corresponder aos diretórios corretos em seu sistema.


## Créditos:

Este projeto utiliza as seguintes bibliotecas:

* os: manipulação de arquivos e diretórios.
* pyautogui: automação do mouse e teclado.
* pandas: manipulação de dados xlsx.
* clipboard: inserção de cópias na área de transferência.
* datetime: geração de data e hora.
* ctypes: pressionamento de teclas do teclado.
* tkinter: interface gráfica customizável com elementos de notificação.
* PIL: inserção de ícone nas janelas.
* openpyxl: criação, exclusão e manipulação de arquivos .xlsx.


## Uso/Exemplos

Com este sistema, é possível gerenciar condicionais criando um novo condicional com o nome do cliente e adicionando peças ao condicional, seja pela automação que busca informações do produto baseado no código de barras da etiqueta ou pela inserção manual das informações nos campos adequados. Também é possível remover produtos do condicional por meio da automação ou da tela exibida. Além disso, é possível lançar os produtos do condicional diretamente para o sistema da loja e gerenciar a lixeira de condicionais apagados, podendo restaurar ou remover permanentemente. Algumas funcionalidades adicionais incluem:

* Verificação de arquivos em diretório.
* Renomeio de arquivos .xlsx.
* Customização de cada informação manualmente antes de inserir.
* Tempo de gerenciamento reduzido para poucos minutos.
* Redução das falhas humanas.
* Otimização da gestão empresarial.


## Contribuindo

Contribuições são sempre bem-vindas! Para começar, consulte o arquivo contribuindo.md. Por favor, siga o código de conduta desse projeto.


## Licença

Este projeto está licenciado sob a licença MIT. Para mais informações, consulte o arquivo LICENSE.
[MIT](https://choosealicense.com/licenses/mit/)


## 💬 Contato
Eu sou um desenvolvedor em busca de uma carreira de sucesso! Entre em contato comigo no LinkedIn: 
https://www.linkedin.com/in/joaovitornsouza/.


## Screenshots

#### **Telas**: principal, adicionar peça, remover peça e lixeira.


<p align="center">
  <img src="https://github.com/JoaoVNSouza/Sistema_Condicional_Produtos_RPA_PY/blob/main/screenshots/tela_principal.png" alt="Image" width="650">
</p>


<div style="display: flex; justify-content: center; align-items: center;">
  <img src="https://github.com/JoaoVNSouza/Sistema_Condicional_Produtos_RPA_PY/blob/main/screenshots/criar_condicional.png" alt="Criar condicional" width=400>
  <img src="https://github.com/JoaoVNSouza/Sistema_Condicional_Produtos_RPA_PY/blob/main/screenshots/deletar_condicional.png" alt="Deletar condicional" width=350>
</div>


<p align="center">
  <img src="https://github.com/JoaoVNSouza/Sistema_Condicional_Produtos_RPA_PY/blob/main/screenshots/adicionar_produto.png" alt="Image" width="650">
</p>