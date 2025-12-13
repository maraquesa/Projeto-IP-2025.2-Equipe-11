import math
import random
import pygame

x = 1500 # x e y são o tamanho da tela
y = 750
pontuacao_1 = 0
pontuacao_2 = 0
n_colecionaveis_principais = 2 # quantidade maxima de coletaveis principais que aparecerão na tela ao msm tempo
tempo_spawn_min_coletavel = 50
tempo_spawn_max_coletavel = 100
tempo_despawn_coletavel = 500 # tempo em ticks para deletar um coletavel secundario
tempo_para_prox = 0 #tempo inicial para proximo spawn de coletavel

posicao_jogadores = {
    1: pygame.Rect(0, 0, 0, 0),
    2: pygame.Rect(0, 0, 0, 0)
}

#serve para calcular a velocidade quando se move tanto no y quanto no x, por exemplo ao apertar W e D ao mesmo tempo
def calcular_velocidade_diagonal(velocidade : int) -> float :
    return round(velocidade * math.sin(math.radians(45)), 4)

def achar_numero_tela() -> tuple[int,int] : #gera um numero dentro da tela

    return (random.randint(50, x - 50), random.randint(50, y - 50))

def colisao_jogador(localizacao_chek : tuple[int,int]) -> int : #1 se colidir com jogador 1 e 2 se coledir com jogador 2, 0 caso com ninguem
    # Verifica colisão usando o método collidepoint do Pygame
    if posicao_jogadores[1].collidepoint(localizacao_chek):
        return 1
    elif posicao_jogadores[2].collidepoint(localizacao_chek):
        return 2
    return 0

def gerar_novo_coletavel() -> bool :
    global tempo_para_prox

    if tempo_para_prox == 0 :
        tempo_para_prox = random.randint(tempo_spawn_min_coletavel, tempo_spawn_max_coletavel)
        return True
    tempo_para_prox -= 1
    return False
