import unittest
from unittest import TestCase
from .dominio import Usuario, Lance, Leilao


class TestAvaliador(TestCase):
    
    def setUp(self):
        self.gui  = Usuario('Gui')
        self.yuri = Usuario('Yuri')
        self.vini = Usuario('Vinicius')
        self.lance_do_gui = Lance(self.gui, 150.0)
        self.lance_do_yuri = Lance(self.yuri, 100.0)
        self.lance_do_vini = Lance(self.vini, 200.0)
        self.leilao = Leilao('Celular')
        
    def criar_lance(self, nome, valor):
        user = Usuario(nome)
        lance= Lance(user, valor)
        self.leilao.novo_lance(lance)
    
    def avaliar(self, menor_valor, maior_valor):
        print(f'O menor lance foi de {self.leilao.menor_lance} e o maior lance foi de {self.leilao.maior_lance}')
        self.assertEqual(self.leilao.menor_lance, menor_valor)
        self.assertEqual(self.leilao.maior_lance, maior_valor)

    def test_case001(self):
        self.criar_lance('Gui', 150.0)
        self.criar_lance('Yuri', 100.0)
        self.avaliar(100.0 , 150.0)

    def test_case002(self):
        self.criar_lance('Vinicius', 200.0)
        self.criar_lance('Gui', 150.0)
        self.criar_lance('Yuri', 100.0)
        self.avaliar(100.0 , 200.0)

#if __name__ == '__main__':
#    unittest.main()
