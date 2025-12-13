import pygame
from sys import exit
from sprites import *
from operacoes import *

pygame.init()
#criar a tela
tela = pygame.display.set_mode((x, y))

clock = pygame.time.Clock()
#tela de fundo
background = pygame.Surface((x, y)) #mudar
background.fill('Blue')


jogador_1 = pygame.sprite.GroupSingle()
jogador_1.add(Jogador(2, (200,200), True, 'Green'))
jogador_2 = pygame.sprite.GroupSingle()
jogador_2.add(Jogador(2,(400,400), False, 'Yellow'))

coletaveis_principais = pygame.sprite.Group()
for i in range(n_colecionaveis_principais) : coletaveis_principais.add(Coletavel_generico('principal', 'Gold'))
coletaveis_secundarios = pygame.sprite.Group()


#inicio loop
while True :


    #eventos
    for evento in pygame.event.get() :

        #finalizar progama
        if evento.type == pygame.QUIT :
            pygame.quit()
            exit()

    if gerar_novo_coletavel() :
        coletaveis_secundarios.add(Coletavel_generico('secundario', 'Purple', tempo_despawn_coletavel))

    pygame.display.update()
    tela.blit(background,(0,0))
    jogador_1.update(tela)
    jogador_2.update(tela)
    coletaveis_principais.update(tela)
    coletaveis_secundarios.update(tela)
    clock.tick(60)
