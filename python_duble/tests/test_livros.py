import pytest
from urllib.error import HTTPError
from unittest.mock import patch, mock_open, Mock, MagicMock
from unittest import skip

from python_duble.colecao.livros import consultar_livros, executar_requisicao,\
    escrever_em_arquivo, mandar_email

URL_BUSCADOR ="https://buscador"
PATH_BASE = 'python_duble.colecao.livros.'

#### Stbs, Dummys, ...

class StubHTTPResponse:
    def read(self):
        return b""

    def __enter__(self):
        return self

    def __exit__(self, param1, param2, param3):
        pass
    
    
def stub_de_urlopen(url, timeout):
    return StubHTTPResponse()


class Dummy:
    pass


def stub_de_urlopen_que_levanta_excecao_http_error(url, timeout):
    fp = mock_open
    fp.close = Dummy
    raise HTTPError(Dummy(), Dummy(), "mensagem de erro", Dummy(), fp)


class DubleLogging:
    def __init__(self):
        self._mensagens = []

    @property
    def mensagens(self):
        return self._mensagens

    def exception(self, mensagem):
        self._mensagens.append(mensagem)

def duble_makedirs(diretorio):
    raise OSError("Não foi possível criar diretório %s" % diretorio)

class SpyFP:
    def __init__(self):
        pass
    
    def __enter__(self):
        return self

    def write(self, conteudo):
        self._conteudo = conteudo

    def __exit__(self, *args):
        pass
    

#### Tests
    
@patch(PATH_BASE+"urlopen", return_value=StubHTTPResponse())
def  test_consultar_livros_001(stub_urlopen):
    ''' Retorna dados com formato string '''
    resultado = consultar_livros("Agatha Christie")
    assert type(resultado) == str


@patch(PATH_BASE+"urlopen", return_value=StubHTTPResponse())
def  test_consultar_livros_002(stub_urlopen):
    ''' Chama preparar dados para requisição uma vez e com os mesmos
    parâmetrosde consultar livros '''
    ## Com isso consigo verificar se a função foi chamada uma vez 
    with patch(PATH_BASE+'preparar_dados_para_requisicao') as stub:
        consultar_livros("Agatha Christie")
        stub.assert_called_once_with("Agatha Christie")


@patch(PATH_BASE+"urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_003(stub_urlopen):
    ''' Chama obter url usando como parametro o retorno de preparar 
    dados para requisicao'''
    with patch(PATH_BASE+"preparar_dados_para_requisicao") as spy_preparar:
        dados = {"author": "Agatha Christie"}
        spy_preparar.return_value = dados
        with patch(PATH_BASE+"obter_url") as stub_obter_url:
            consultar_livros("Agatha Christie")
            stub_obter_url.assert_called_once_with(URL_BUSCADOR, dados)


@patch(PATH_BASE+"urlopen", return_value=StubHTTPResponse())
def test_consultar_livros_004(stub_urlopen):
    ''' Chama executar reuisição usando retorno do obter_url'''
    with patch(PATH_BASE+"obter_url") as stub_obter_url:
        stub_obter_url.return_value = URL_BUSCADOR
        with patch(PATH_BASE+"executar_requisicao") as spy_executar_requisicao:
            consultar_livros("Agatha Christie")
            spy_executar_requisicao.assert_called_once_with(URL_BUSCADOR)


@skip("")
def  test_consultar_livros_005():
    ''' Executar Requisição retorna tipo string (criando o stub por funcao) '''
    with patch(PATH_BASE+"urlopen", stub_de_urlopen):
        print(stub_de_urlopen)
        resultado = executar_requisicao("https://buscarlivros?autor=Jk+Rowlings")
        assert type(resultado) == str


@skip("")
def  test_consultar_livros_006():
    ''' Executar Requisição retorna tipo string (criando o stub diretamente)'''
    with patch(PATH_BASE+"urlopen")  as stub_de_urlopen:
        stub_de_urlopen.return_value = StubHTTPResponse()
        resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str
        

@skip("")
def  test_consultar_livros_007():
    ''' Executar Requisição retorna tipo string 
    (criando o stub com return_value nopatch)'''
    with patch(PATH_BASE+"urlopen", 
               return_value=StubHTTPResponse()):
        resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
        assert type(resultado) == str


@skip("")
@patch(PATH_BASE+"urlopen", return_value=StubHTTPResponse())
def  test_consultar_livros_008(stub_de_urlopen):
    ''' Executar Requisição retorna tipo string 
    (criando o stub com decorator)'''
    resultado = executar_requisicao("https://buscarlivros?author=Jk+Rowlings")
    assert type(resultado) == str
    

@skip("")
def test_consultar_livros_009():
    ''' Levantar excecao do tipo http error '''
    with patch(PATH_BASE+"urlopen", 
               stub_de_urlopen_que_levanta_excecao_http_error):
        with pytest.raises(HTTPError) as excecao:
            executar_requisicao("http://")
        assert "mensagem de erro" in str(excecao.value)


@skip("")
@patch(PATH_BASE+"urlopen")
def test_consultar_livros_010(stub_de_urlopen):
    ''' Levantar excecao do tipo http error '''
    fp = mock_open
    fp.close = Mock()
    stub_de_urlopen.side_effect = HTTPError(
        Mock(), Mock(), "mensagem de erro", Mock(), fp
    )
    with pytest.raises(HTTPError) as excecao:
        executar_requisicao("http://")
        assert "mensagem de erro" in str(excecao.value)
        

@skip("")
def test_consultar_livros_011(caplog):
    ''' Loga excecao '''
    with patch(PATH_BASE+"urlopen",
                stub_de_urlopen_que_levanta_excecao_http_error):
        resultado = executar_requisicao("http://")
        mensagem_de_erro = "mensagem de erro"
        assert len(caplog.records) == 1
        for registro in caplog.records:
            assert mensagem_de_erro in registro.message


@patch(PATH_BASE+"urlopen")
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
        

def test_consultar_livros_013():
    ''' Escrever em arquivo registra excecao que nao foi possivel criar diretorio '''
    arquivo = "tmp/arquivo.json"
    conteudo = "dados de livros"
    duble_logging = DubleLogging()
    with patch(PATH_BASE+"os.makedirs", duble_makedirs):
        with patch(PATH_BASE+"logging", duble_logging):
            escrever_em_arquivo(arquivo, conteudo)
            assert "Não foi possível criar diretório tmp" in duble_logging.mensagens


@patch(PATH_BASE+"os.makedirs")
@patch(PATH_BASE+"logging.exception")
@patch(PATH_BASE+"open", side_effect=OSError())
def test_consultar_livros_014(stub_open, spy_exception, stub_makedirs):
    ''' Escrever em arquivo registra excecao que nao foi possivel criar diretorio '''
    arq = "/bla/arquivo.json"
    escrever_em_arquivo(arq, "dados de livros")
    spy_exception.assert_called_once_with("Não foi possível criar arquivo %s" % arq)


@patch(PATH_BASE+"open")
def test_consultar_livros_015(stub_open):
    ''' Escrever em arquivo chama write'''
    arquivo = "tmp/arquivo.json"
    conteudo = "dados de livros"
    
    spy_fp = SpyFP()
    stub_open.return_value = spy_fp
    escrever_em_arquivo(arquivo, conteudo)
    assert spy_fp._conteudo == conteudo

@patch(PATH_BASE+"open")
def test_consultar_livros_016(stub_open):
    ''' Escrever em arquivo chama write'''
    arquivo = "tmp/arquivo.json"
    conteudo = "dados de livros"
    
    spy_de_fp = MagicMock()
    spy_de_fp.__enter__.return_value = spy_de_fp
    spy_de_fp.__exit__.return_value = None
    stub_open.return_value = spy_de_fp
    escrever_em_arquivo(arquivo, conteudo)
    spy_de_fp.write.assert_called_once_with(conteudo)


def test_mandar_email():
    with patch("smtplib.SMTP") as mock_smtp:
        m = mock_smtp("localhost")
        mandar_email("from", "to", "bla bla bla")
        m.sendmail.assert_called_once_with("from", "to", "bla bla bla")