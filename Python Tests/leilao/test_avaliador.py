import unittest
from unittest import TestCase
from .dominio import Usuario, Lance, Leilao, Avaliador


class TestAvaliador(TestCase):
    
    def setUp(self):
        self.gui  = Usuario('Gui')
        self.yuri = Usuario('Yuri')
        self.vini = Usuario('Vinicius')
        self.lance_do_gui = Lance(self.gui, 150.0)
        self.lance_do_yuri = Lance(self.yuri, 100.0)
        self.lance_do_vini = Lance(self.vini, 200.0)
        self.leilao = Leilao('Celular')
    
    def avaliar(self, menor_valor, maior_valor):
        avaliador = Avaliador()
        avaliador.avalia(self.leilao)
        print(f'O menor lance foi de {avaliador.menor_lance} e o maior lance foi de {avaliador.maior_lance}')
        self.assertEqual(avaliador.menor_lance, menor_valor)
        self.assertEqual(avaliador.maior_lance, maior_valor)

    def test_case001(self):
        self.leilao.lances.append(self.lance_do_gui)
        self.leilao.lances.append(self.lance_do_yuri)
        self.avaliar(self.lance_do_yuri.valor,   self.lance_do_gui .valor)

    def test_case002(self):
        self.leilao.lances.append(self.lance_do_gui)
        self.leilao.lances.append(self.lance_do_vini)
        self.leilao.lances.append(self.lance_do_yuri)
        self.avaliar(self.lance_do_yuri.valor, self.lance_do_vini.valor)

#if __name__ == '__main__':
#    unittest.main()
