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
tempo_desde_inicio = 0

mapa = pygame.image.load("assets/piso_mapa.png").convert() #caminho do asset do mapa    
background = pygame.transform.scale(mapa, (x, y)) #redmensiona


def mostrar_interface():
    preto = (0, 0, 0)
    branco = (255, 255, 255)
    dourado = (212, 175, 55)
    vermelho = (231, 25, 33)

    cor_painel = (255, 255, 255)  
    opacidade = 180              
    largura_p, altura_p = 220, 75
    margem_x = 20
    margem_y = 30

    painel_p1 = pygame.Surface((largura_p, altura_p))
    painel_p1.set_alpha(opacidade)
    painel_p1.fill(cor_painel)
    tela.blit(painel_p1, (margem_x, margem_y - 10))
    
    desenhar_texto("P1:", 35, vermelho, tela, margem_x + 35, margem_y + 10)
    desenhar_texto(f"{pontuacao_lista[1]}", 35, dourado, tela, margem_x + 90, margem_y + 10)
    
    bome_1 = bonus[1]['bome']['atual'] // 60
    tele_1 = bonus[1]['tele']['atual'] // 60
    desenhar_texto(f"boome: {bome_1} | teleporte: {tele_1}", 20, preto, tela, margem_x + 110, margem_y + 45)

    painel_p2 = pygame.Surface((largura_p, altura_p))
    painel_p2.set_alpha(opacidade)
    painel_p2.fill(cor_painel)
    pos_x_p2 = x - margem_x - largura_p
    tela.blit(painel_p2, (pos_x_p2, margem_y - 10))
    
    desenhar_texto("P2:", 35, vermelho, tela, pos_x_p2 + 35, margem_y + 10)
    desenhar_texto(f"{pontuacao_lista[2]}", 35, dourado, tela, pos_x_p2 + 90, margem_y + 10)
    
    bome_2 = bonus[2]['bome']['atual'] // 60
    tele_2 = bonus[2]['tele']['atual'] // 60
    desenhar_texto(f"boome: {bome_2} | teleporte: {tele_2}", 20, preto, tela, pos_x_p2 + 110, margem_y + 45)
   
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
            tempo_desde_inicio += 1
            print(proximo_obstaculo)
            #eventos
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    jogo_ativo = False
                    programa_rodando = False

            if gerar_novo_coletavel() :
                coletaveis_secundarios.add(Coletavel_generico('secundario', 'Purple', tempo_despawn_coletavel, escolher_bonus()))

            if proximo_obstaculo <= 0 :
                coletaveis_secundarios.add(Coletavel_generico('secundario', 'Purple', tempo_despawn_coletavel, escolher_bonus()))
                proximo_obstaculo = escalacao_dificuldade
            else : proximo_obstaculo -= min([escalacao_maxima, tempo_desde_inicio])

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