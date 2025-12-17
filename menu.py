import pygame
import sys
from operacoes import x, y  # Importamos as dimensões definidas nas configurações

def desenhar_texto(texto, fonte, cor, superficie, x_centro, y_centro):
    """Função auxiliar para desenhar texto centralizado"""
    obj_texto = fonte.render(texto, True, cor)
    rect_texto = obj_texto.get_rect(center=(x_centro, y_centro))
    superficie.blit(obj_texto, rect_texto)

def tela_inicial():
    # Pega a referência da tela que já foi criada no main.py
    tela = pygame.display.get_surface()
    
    # Se por acaso a tela não tiver sido criada (teste isolado), cria uma
    if tela is None:
        tela = pygame.display.set_mode((x, y))

    # Cores
    BRANCO = (255, 255, 255)
    PRETO = (0, 0, 0)
    CINZA_CLARO = (200, 200, 200)
    CINZA_ESCURO = (100, 100, 100)
    AZUL_FUNDO = (30, 30, 100) # Um azul escuro para diferenciar do jogo

    # Fontes
    fonte_titulo = pygame.font.SysFont("arial", 80, bold=True)
    fonte_botao = pygame.font.SysFont("arial", 40)

    # Definição dos Botões (Centralizados)
    largura_botao = 300
    altura_botao = 80
    centro_x = x / 2
    
    rect_jogar = pygame.Rect(0, 0, largura_botao, altura_botao)
    rect_jogar.center = (centro_x, y / 2) # Meio da tela
    
    rect_sair = pygame.Rect(0, 0, largura_botao, altura_botao)
    rect_sair.center = (centro_x, (y / 2) + 120) # Um pouco abaixo

    rodando_menu = True
    
    while rodando_menu:
        # 1. Processamento de Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Clique do mouse
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Botão esquerdo
                    pos_mouse = pygame.mouse.get_pos()
                    
                    if rect_jogar.collidepoint(pos_mouse):
                        return "start" # Retorna a string que o main.py espera
                    
                    if rect_sair.collidepoint(pos_mouse):
                        pygame.quit()
                        sys.exit()

        # 2. Atualizações Visuais
        tela.fill(AZUL_FUNDO)
        
        pos_mouse = pygame.mouse.get_pos()

        # Título do Jogo
        desenhar_texto("NOME DO JOGO", fonte_titulo, BRANCO, tela, centro_x, 150)

        # --- Desenhar Botão JOGAR ---
        cor_jogar = CINZA_ESCURO if rect_jogar.collidepoint(pos_mouse) else CINZA_CLARO
        pygame.draw.rect(tela, cor_jogar, rect_jogar, border_radius=10)
        pygame.draw.rect(tela, PRETO, rect_jogar, 3, border_radius=10) # Borda
        desenhar_texto("JOGAR", fonte_botao, PRETO, tela, rect_jogar.centerx, rect_jogar.centery)

        # --- Desenhar Botão SAIR ---
        cor_sair = CINZA_ESCURO if rect_sair.collidepoint(pos_mouse) else CINZA_CLARO
        pygame.draw.rect(tela, cor_sair, rect_sair, border_radius=10)
        pygame.draw.rect(tela, PRETO, rect_sair, 3, border_radius=10) # Borda
        desenhar_texto("SAIR", fonte_botao, PRETO, tela, rect_sair.centerx, rect_sair.centery)

        # Atualiza a tela
        pygame.display.flip()