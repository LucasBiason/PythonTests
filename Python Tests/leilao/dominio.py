import sys

class Usuario:

    def __init__(self, nome):
        self.__nome = nome

    @property
    def nome(self):
        return self.__nome


class Lance:

    def __init__(self, usuario, valor):
        self.usuario = usuario
        self.valor = valor


class Leilao:

    def __init__(self, descricao):
        self.descricao = descricao
        self.__lances = []

    @property
    def lances(self):
        return self.__lances

class Avaliador:
    
    def __init__(self):
        self.maior_lance = 0.0
        self.menor_lance = 0.0
    
    def avalia(self, leilao: Leilao):
        self.maior_lance = leilao.lances[0].valor
        self.menor_lance = leilao.lances[0].valor
        
        for lance in leilao.lances:
            if lance.valor > self.maior_lance:
                self.maior_lance = lance.valor
            if lance.valor < self.menor_lance:
                self.menor_lance = lance.valor
                
        