import pygame
from sys import exit
from sprites import *
from operacoes import *
from menu import tela_inicial, tela_vitoria, desenhar_texto

pygame.init()
#criar a tela
tela = pygame.display.set_mode((x, y))
pygame.display.set_caption("Cinbate")
clock = pygame.time.Clock()

#tela de fundo
background = pygame.Surface((x, y)) #mudar
background.fill((20, 20, 40))

def mostrar_interface():
    vermelho = (231, 25, 33)
    branco = (255, 255, 255)
    dourado = (255, 215, 0)

    margem_x = 20
    margem_y = 30
    espacamento_linhas = 25

    # HUD Jogador 1 na esquerda
    desenhar_texto("P1:", 35, vermelho, tela, margem_x + 15, margem_y)
    desenhar_texto(f"{pontuacao_lista[1]}", 35, dourado, tela, margem_x + 70, margem_y)
    bome_1 = bonus[1]['bome']['atual'] // 60
    tele_1 = bonus[1]['tele']['atual'] // 60
    desenhar_texto(f"boome: {bome_1} | teleporte: {tele_1}", 20, branco, tela, margem_x + 85, margem_y + espacamento_linhas)

    # HUD Jogador 2 na direita
    desenhar_texto("P2:", 35, vermelho, tela, x - margem_x - 85, margem_y)
    desenhar_texto(f"{pontuacao_lista[2]}", 35, dourado, tela, x - margem_x - 30, margem_y)
    bome_2 = bonus[2]['bome']['atual'] // 60
    tele_2 = bonus[2]['tele']['atual'] // 60
    desenhar_texto(f"boome: {bome_2} | teleporte: {tele_2}", 20, branco, tela, x - margem_x - 85, margem_y + espacamento_linhas)
   
programa_rodando = True
#inicio loop
while programa_rodando :
    escolha = tela_inicial()
    
    if escolha == "sair":
        programa_rodando = False
    
    if escolha == "start":
        # reinicia  jogo para uma nova partida
        pontuacao_lista[1] = 0
        pontuacao_lista[2] = 0
        coletaveis_principais = pygame.sprite.Group()
        for i in range(n_colecionaveis_principais): 
            coletaveis_principais.add(Coletavel_generico('principal', 'Gold'))
        coletaveis_secundarios = pygame.sprite.Group()
        bomerangues.empty() 
        todos_jogadores = pygame.sprite.Group(jogador_1.sprite, jogador_2.sprite)

        jogo_ativo = True
        while jogo_ativo :
            #eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jogo_ativo = False
                    programa_rodando = False

            if gerar_novo_coletavel() :
                coletaveis_secundarios.add(Coletavel_generico('secundario', 'Purple', tempo_despawn_coletavel, escolher_bonus()))

            tela.blit(background,(0,0))
            jogador_1.update(tela)
            jogador_2.update(tela)

            #colisao entre jogadores (empurrao)
            jogador_1.sprite.colidir_jogadores(todos_jogadores)

            coletaveis_principais.update(tela)
            coletaveis_secundarios.update(tela)
            bomerangues.update(tela)

            mostrar_interface()

            # verifica condição de vitória
            if (pontuacao_lista[1] >= pontuacao_maxima):
                jogo_ativo = False
                tela_vitoria(1)
            if (pontuacao_lista[2] >= pontuacao_maxima):
                jogo_ativo = False
                tela_vitoria(2)

            pygame.display.update()
            clock.tick(60)

pygame.quit()
exit()