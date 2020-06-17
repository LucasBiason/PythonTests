import pytest
from urllib.error import HTTPError
from unittest.mock import patch, mock_open, Mock
from unittest import skip

from python_duble.colecao.livros import consultar_livros, executar_requisicao

@skip("Vale quando consultar_livros estiver completo")
def  test_consultar_livros_001():
    ''' Retorna dados com formato string '''
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str
    
@skip("")
def  test_consultar_livros_002():
    ''' Chama preparar dados para requisição uma vez e com os mesmos
    parâmetrosde consultar livros '''
    ## Com isso consigo verificar se a função foi chamada uma vez 
    with patch('python_duble.colecao.livros.preparar_dados_para_requisicao') as duble:
        consultar_livros("Agatha Christie")
        duble.assert_called_once_with("Agatha Christie")

@skip("")
def test_consultar_livros_003():
    ''' Chama obter url usando como parametro o retorno de preparar 
    dados para requisicao'''
    with patch("python_duble.colecao.livros.preparar_dados_para_requisicao") as duble_preparar:
        dados = {"author": "Agatha Christie"}
        duble_preparar.return_value = dados
        with patch("python_duble.colecao.livros.obter_url") as duble_obter_url:
            consultar_livros("Agatha Christie")
            duble_obter_url.assert_called_once_with("https://buscador", dados)

@skip("")
def test_consultar_livros_004():
    ''' Chama executar reuisição usando retorno do obter_url'''
    with patch("python_duble.colecao.livros.obter_url") as duble_obter_url:
        duble_obter_url.return_value = "https://buscador"
        with patch("python_duble.colecao.livros.executar_requisicao") as duble_executar_requisicao:
            consultar_livros("Agatha Christie")
            duble_executar_requisicao.assert_called_once_with("https://buscador")

class StubHTTPResponse:
    def read(self):
        return b""

    def __enter__(self):
        return self

    def __exit__(self, param1, param2, param3):
        pass
    
def stub_de_urlopen(url, timeout):
    return StubHTTPResponse()

def  test_consultar_livros_005():
    ''' Executar Requisição retorna tipo string '''
    with patch("python_duble.colecao.livros.urlopen", stub_de_urlopen):
        print(stub_de_urlopen)
        resultado = executar_requisicao("https://buscarlivros?autor=Jk+Rowlings")
        assert type(resultado) == str