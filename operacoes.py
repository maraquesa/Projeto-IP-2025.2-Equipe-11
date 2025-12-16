import math
import random
import pygame



#os elementos a baixo são os elementos que podem ser mudado a qualquer momento, trocar eles não causará erros
x = 1500 # x e y são o tamanho da tela
y = 750
velocidade_padrao_perssonagens = 2
n_colecionaveis_principais = 2 # quantidade maxima de coletaveis principais que aparecerão na tela ao msm tempo
tempo_spawn_min_coletavel = 50 # o menor tempo em ticks para spawnar um coletavel secundario, 1 segundo possui 60 ticks
tempo_spawn_max_coletavel = 100 # maior tempo para spawnar um coletavel secundario
tempo_despawn_coletavel = 500 # tempo em ticks para deletar um coletavel secundario
tempo_para_prox = 0 #tempo inicial para proximo spawn de coletavel
itensidade_bonus_velocidade = 1.5 # a itenssidade do efeito de velocidade, 1 = 100%, 1.5 = 150% etc
lista_bonus_disponiveis = [('velocidade', 3, 10), ('bome', 1, 2)] #lista com todos os bonus possiveis e os pesos dele ser escolhido quando um coletavel secundario spawnar, cada elemento é uma tupla do tipo (elemento, peso, duração efeito em segundos)
velocidade_bomerangue = 5

posicao_jogadores = {
    1: pygame.Rect(0, 0, 0, 0),
    2: pygame.Rect(0, 0, 0, 0)
}

#não mudar esses elementos
pontuacao_1 = 0
pontuacao_2 = 0
lista_bonus_tipos = [elemento[0] for elemento in lista_bonus_disponiveis]
lista_bonus_pesos = [elemento[1] for elemento in lista_bonus_disponiveis]
lista_duracao = [elemento[2] * 60 for elemento in lista_bonus_disponiveis]

bonus = {1 : {}, 2 : {}}
for i, j in zip(lista_bonus_tipos, lista_duracao) :
    bonus[1][i] = {'atual' : 0, 'max' : j}
    bonus[2][i] = {'atual' : 0, 'max' : j}


#serve para calcular a velocidade quando se move tanto no y quanto no x, por exemplo ao apertar W e D ao mesmo tempo
def calcular_velocidade_diagonal(velocidade : int) -> float :
    return round(velocidade * math.sin(math.radians(45)), 4)

def achar_numero_tela() -> tuple[int,int] : #gera um numero dentro da tela

    return (random.randint(50, x - 50), random.randint(50, y - 50))

def colisao_personagem(area_de_colisao: pygame.Rect) -> int : # recebe o objeto deimitado por um retangulo (correspondente a sua area de ocupacao)
    # verifica a colisão usando o método colliderect (colisao entre retangulos)
    if posicao_jogadores[1].colliderect(area_de_colisao): # 1 se colidir com personagem 1
        return 1
    elif posicao_jogadores[2].colliderect(area_de_colisao): # 2 se colidir com personagem 2
        return 2
    return 0 # 0 caso colida com ninguem

def gerar_novo_coletavel() -> bool :
    global tempo_para_prox

    if tempo_para_prox == 0 :
        tempo_para_prox = random.randint(tempo_spawn_min_coletavel, tempo_spawn_max_coletavel)
        return True
    tempo_para_prox -= 1
    return False

def escolher_bonus() -> str :
    return random.choices(lista_bonus_tipos, lista_bonus_pesos)[0]
