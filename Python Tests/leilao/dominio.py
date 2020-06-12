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
        self.maior_lance = None
        self.menor_lance = None

    @property
    def lances(self):
        return self.__lances[:]
    
    def novo_lance(self,lance):
        self.__lances.append(lance)
        
       if self.maior_lance is None:
            self.maior_lance = lance.valor
        elif lance.valor > self.maior_lance:
            self.maior_lance = lance.valor
       
       if self.menor_lance is None:
            self.menor_lance = lance.valor
        elif lance.valor < self.menor_lance:
            self.menor_lance = lance.valor
    
    @property
    def first_value(self):
        if not self.__lances:
            return 0
        return self.__lances[0].valor
