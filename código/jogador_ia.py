# -*- coding: utf-8 -*-
from random import randint
from jogador import Jogador
from tabuleiro import Tabuleiro

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)

    def getJogada(self) -> (int, int):
        import random
        tab = self.matriz
        tipo = self.tipo
        oponente = 1 if tipo == 2 else 2

        def checar_linha_para_vencer(jogador):
            for i in range(3):
                linha = [tab[i][j] for j in range(3)]
                if linha.count(jogador) == 2 and linha.count(Tabuleiro.DESCONHECIDO) == 1:
                    return (i, linha.index(Tabuleiro.DESCONHECIDO))
            return None

        def checar_coluna_para_vencer(jogador):
            for j in range(3):
                coluna = [tab[i][j] for i in range(3)]
                if coluna.count(jogador) == 2 and coluna.count(Tabuleiro.DESCONHECIDO) == 1:
                    return (coluna.index(Tabuleiro.DESCONHECIDO), j)
            return None

        def checar_diagonal_para_vencer(jogador):
            diag1 = [tab[i][i] for i in range(3)]
            if diag1.count(jogador) == 2 and diag1.count(Tabuleiro.DESCONHECIDO) == 1:
                i = diag1.index(Tabuleiro.DESCONHECIDO)
                return (i, i)
            diag2 = [tab[i][2 - i] for i in range(3)]
            if diag2.count(jogador) == 2 and diag2.count(Tabuleiro.DESCONHECIDO) == 1:
                i = diag2.index(Tabuleiro.DESCONHECIDO)
                return (i, 2 - i)
            return None

        def jogadas_duplas(jogador):
            for l in range(3):
                for c in range(3):
                    if tab[l][c] == Tabuleiro.DESCONHECIDO:
                        tab[l][c] = jogador
                        cont = 0
                        if checar_linha_para_vencer(jogador): cont += 1
                        if checar_coluna_para_vencer(jogador): cont += 1
                        if checar_diagonal_para_vencer(jogador): cont += 1
                        tab[l][c] = Tabuleiro.DESCONHECIDO
                        if cont >= 2:
                            return (l, c)
            return None

        def centro_livre():
            if tab[1][1] == Tabuleiro.DESCONHECIDO:
                return (1, 1)
            return None

        def canto_oposto():
            cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
            for (l, c) in cantos:
                if tab[l][c] == oponente:
                    oposto = (2 - l, 2 - c)
                    if tab[oposto[0]][oposto[1]] == Tabuleiro.DESCONHECIDO:
                        return oposto
            return None

        def canto_vazio():
            for (l, c) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
                if tab[l][c] == Tabuleiro.DESCONHECIDO:
                    return (l, c)
            return None

        def aleatoria():
            livres = [(l, c) for l in range(3) for c in range(3) if tab[l][c] == Tabuleiro.DESCONHECIDO]
            return random.choice(livres) if livres else None

        # Aplicar regras em ordem R1 a R6
        for func in [
            lambda: checar_linha_para_vencer(tipo) or checar_linha_para_vencer(oponente) or
                    checar_coluna_para_vencer(tipo) or checar_coluna_para_vencer(oponente) or
                    checar_diagonal_para_vencer(tipo) or checar_diagonal_para_vencer(oponente),
            lambda: jogadas_duplas(tipo),
            centro_livre,
            canto_oposto,
            canto_vazio,
            aleatoria
        ]:
            jogada = func()
            if jogada:
                return jogada

        return None
