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

@skip("")
def  test_consultar_livros_005():
    ''' Executar Requisição retorna tipo string (criando o duble por funcao) '''
    with patch("python_duble.colecao.livros.urlopen", stub_de_urlopen):
        print(stub_de_urlopen)
        resultado = executar_requisicao("https://buscarlivros?autor=Jk+Rowlings")
        assert type(resultado) == str

@skip("")
def  test_consultar_livros_006():
    ''' Executar Requisição retorna tipo string (criando o duble diretamente)'''
    with patch("python_duble.colecao.livros.urlopen")  as duble_de_urlopen:
        duble_de_urlopen.return_value = StubHTTPResponse()
        resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str
        
@skip("")
def  test_consultar_livros_007():
    ''' Executar Requisição retorna tipo string 
    (criando o duble com return_value nopatch)'''
    with patch("python_duble.colecao.livros.urlopen", 
               return_value=StubHTTPResponse()):
        resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str
    

@skip("")
@patch("python_duble.colecao.livros.urlopen", return_value=StubHTTPResponse())
def  test_consultar_livros_008(duble_de_urlopen):
    ''' Executar Requisição retorna tipo string 
    (criando o duble com decorator)'''
    resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
    assert type(resultado) == str
    

class Dummy:
    pass

def stub_de_urlopen_que_levanta_excecao_http_error(url, timeout):
    fp = mock_open
    fp.close = Dummy
    raise HTTPError(Dummy(), Dummy(), "mensagem de erro", Dummy(), fp)
    
@skip("")
def test_consultar_livros_009():
    ''' Levantar excecao do tipo http error '''
    with patch("python_duble.colecao.livros.urlopen", 
               stub_de_urlopen_que_levanta_excecao_http_error):
        with pytest.raises(HTTPError) as excecao:
            executar_requisicao("http://")
        assert "mensagem de erro" in str(excecao.value)
            

@skip("")
@patch("python_duble.colecao.livros.urlopen")
def test_consultar_livros_010(duble_de_urlopen):
    ''' Levantar excecao do tipo http error '''
    fp = mock_open
    fp.close = Mock()
    duble_de_urlopen.side_effect = HTTPError(
        Mock(), Mock(), "mensagem de erro", Mock(), fp
    )
    with pytest.raises(HTTPError) as excecao:
        executar_requisicao("http://")
        assert "mensagem de erro" in str(excecao.value)
        

def test_consultar_livros_011(caplog):
    ''' Loga excecao '''
    with patch("python_duble.colecao.livros.urlopen",
                stub_de_urlopen_que_levanta_excecao_http_error):
        resultado = executar_requisicao("http://")
        mensagem_de_erro = "mensagem de erro"
        assert len(caplog.records) == 1
        for registro in caplog.records:
            assert mensagem_de_erro in registro.message


@patch("python_duble.colecao.livros.urlopen")
def test_consultar_livros_012(stub_urlopen, caplog):
    fp = mock_open
    fp.close = Mock()
    stub_urlopen.side_effect = HTTPError(
        Mock(), Mock(), "mensagem de erro", Mock(), fp
    )
    executar_requisicao("http://")
    assert len(caplog.records) == 1
    for registro in caplog.records:
        assert "mensagem de erro" in registro.message