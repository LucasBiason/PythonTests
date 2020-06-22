
import logging
import os
import smtplib

from urllib.request import urlopen
from urllib.error import HTTPError


def consultar_livros(autor):
    dados = preparar_dados_para_requisicao(autor)
    url = obter_url("https://buscador", dados)
    ret = executar_requisicao(url)
    return ret

def preparar_dados_para_requisicao(autor):
    pass
    
def obter_url(url, dados):
    pass

def executar_requisicao(url):
    try:
        with urlopen(url, timeout=10) as resposta:
            resultado = resposta.read().decode("utf-8")
    except HTTPError as e:
        logging.exception("Ao acessar '%s': %s" % (url, e))
    else:
        return resultado
    

def escrever_em_arquivo(arquivo, conteudo):
    diretorio = os.path.dirname(arquivo)
    try:
        os.makedirs(diretorio)
    except OSError as e:
        logging.exception("Não foi possível criar diretório %s" % diretorio)

    try:
        with open(arquivo, "a") as fp:
            fp.write(conteudo)
    except OSError as e:
        logging.exception("Não foi possível criar arquivo %s" % arquivo)
        

def mandar_email(fromaddr, toaddrs, msg):
    server = smtplib.SMTP('localhost')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()