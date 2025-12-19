import pygame
import sys
import webbrowser
from operacoes import x, y  # Importamos as dimensões definidas nas configurações

def desenhar_texto(texto, tamanho, cor, superficie, x_centro, y_centro):
    """Função auxiliar para desenhar texto centralizado"""
    fonte = pygame.font.Font("fonts/VT323-Regular.ttf", tamanho)
    obj_texto = fonte.render(texto, True, cor)
    rect_texto = obj_texto.get_rect(center=(x_centro, y_centro))
    superficie.blit(obj_texto, rect_texto)

def tela_inicial():
    # Pega a referência da tela que já foi criada no main.py
    tela = pygame.display.get_surface()

    # Logo do CIn
    logo_cin = pygame.image.load("assets/logo_cin.png")
    logo_cin = pygame.transform.scale(logo_cin, (150, 70))
    rect_logo = logo_cin.get_rect(bottomleft=(20, y - 20))

    # Cores
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA_CLARO = (200, 200, 200)
    CINZA_ESCURO = (100, 100, 100)
    AZUL_FUNDO = (30, 30, 100) # Um azul escuro para diferenciar do jogo
    VERMELHO = (231, 25, 33)

    # Definição dos Botões (Centralizados)
    largura_botao = 300
    altura_botao = 80
    centro_x = x / 2

    rect_jogar = pygame.Rect(0, 0, largura_botao, altura_botao)
    rect_jogar.center = (centro_x, y / 2 - 80) # Botão JOGAR
    
    rect_sobre = pygame.Rect(0, 0, largura_botao, altura_botao)
    rect_sobre.center = (centro_x, y / 2 + 40) # Botão SOBRE
    
    rect_sair = pygame.Rect(0, 0, largura_botao, altura_botao)
    rect_sair.center = (centro_x, y / 2 + 160) # Botão SAIR

    fonte_titulo = pygame.font.Font("fonts/VT323-Regular.ttf", 120)
    largura_cin = fonte_titulo.size("Cin")[0]
    largura_bate = fonte_titulo.size("bate")[0]
    largura_total = largura_cin + largura_bate

    inicio_x = (x / 2) - (largura_total / 2)

    centro_cin = inicio_x + (largura_cin / 2)
    centro_bate = inicio_x + largura_cin + (largura_bate / 2)

    rodando_menu = True
    escolha = "sair"

    while rodando_menu:
        pos_mouse = pygame.mouse.get_pos()

        # 1. Processamento de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Botão esquerdo
                    if rect_jogar.collidepoint(pos_mouse):
                        rodando_menu = False
                        escolha = "start" 
                    
                    if rect_sobre.collidepoint(pos_mouse):
                        webbrowser.open("https://github.com/seu-repositorio")
                    
                    if rect_sair.collidepoint(pos_mouse):
                        rodando_menu = False
                        escolha = "sair"

        # 2. Atualizações Visuais
        tela.fill(AZUL_FUNDO)

        # Desenhar Logo
        tela.blit(logo_cin, rect_logo)

        # Título do Jogo
        desenhar_texto("Cin", 120, VERMELHO, tela, centro_cin, 150)
        desenhar_texto("bate", 120, BRANCO, tela, centro_bate, 150)

        # --- Desenhar Botão JOGAR ---
        cor_jogar = CINZA_ESCURO if rect_jogar.collidepoint(pos_mouse) else CINZA_CLARO
        pygame.draw.rect(tela, cor_jogar, rect_jogar, border_radius=10)
        pygame.draw.rect(tela, PRETO, rect_jogar, 3, border_radius=10) # Borda
        desenhar_texto("JOGAR", 50, PRETO, tela, rect_jogar.centerx, rect_jogar.centery)

        # --- Desenhar Botão SOBRE ---
        cor_sobre = CINZA_ESCURO if rect_sobre.collidepoint(pos_mouse) else CINZA_CLARO
        pygame.draw.rect(tela, cor_sobre, rect_sobre, border_radius=10)
        pygame.draw.rect(tela, PRETO, rect_sobre, 3, border_radius=10) # Borda
        desenhar_texto("SOBRE", 50, PRETO, tela, rect_sobre.centerx, rect_sobre.centery)

        # --- Desenhar Botão SAIR ---
        cor_sair = CINZA_ESCURO if rect_sair.collidepoint(pos_mouse) else CINZA_CLARO
        pygame.draw.rect(tela, cor_sair, rect_sair, border_radius=10)
        pygame.draw.rect(tela, PRETO, rect_sair, 3, border_radius=10) # Borda
        desenhar_texto("SAIR", 50, PRETO, tela, rect_sair.centerx, rect_sair.centery)

        # Atualiza a tela
        pygame.display.flip()
    return escolha # Retorna a string que o main.py espera

def tela_vitoria(vencedor):
    tela = pygame.display.get_surface()
    BRANCO = (255, 255, 255)
    
    if (vencedor == 1):
        nome_vencedor = "Márcio Cornélio"
        cor_venc = (100, 255, 100) # Verde
    elif vencedor == 2:
        nome_vencedor = "Ricardo Massa"
        cor_venc = (255, 255, 100) # Amarelo
    
    exibindo = True
    while exibindo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                exibindo = False # fecha o jogo

        tela.fill((0, 0, 0))
        desenhar_texto("VITÓRIA!", 80, BRANCO, tela, x/2, y/2 - 150)
        desenhar_texto(f"{nome_vencedor} VENCEU!", 110, cor_venc, tela, x/2, y/2)
        desenhar_texto("CLIQUE PARA FINALIZAR", 50, BRANCO, tela, x/2, y/2 + 100)
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()