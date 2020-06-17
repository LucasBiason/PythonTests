from unittest.mock import patch
from python_duble.colecao.livros import consultar_livros

def  test_consultar_livros_001():
    ''' Retorna dados com formato string '''
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str
    
def  test_consultar_livros_002():
    ''' Chama preparar dados para requisição uma vez e com os mesmos
    parâmetrosde consultar livros '''
    ## Com isso consigo verificar se a função foi chamada uma vez 
    with patch('python_duble.colecao.livros.preparar_dados_para_requisicao') as duble:
        consultar_livros("Agatha Christie")
        duble.assert_called_once_with("Agatha Christie")