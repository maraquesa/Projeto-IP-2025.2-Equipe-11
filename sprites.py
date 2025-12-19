import math
import pygame

from operacoes import *


class Jogador(pygame.sprite.Sprite):

    def __init__(self, velocidade: int, posicao_inicial: tuple[int, int], wasd: bool, skin: str):
        super().__init__()
        self.imagem = pygame.Surface((20, 20))  # mudar
        self.imagem.fill(skin)
        self.retangulo = self.imagem.get_rect(midbottom=(posicao_inicial[0], posicao_inicial[1]))
        self.velocidade = velocidade
        self.delay_x = 0
        self.delay_y = 0
        self.modo_movimento = wasd

        self.empurrao_vx = 0.0  # velocidade de repulsão no eixo X
        self.empurrao_vy = 0.0  # velocidade de repulsão no eixo Y
        self.empurrao_frames = 0 # contagem de frames do empurrão

        self.ultimo_y = 0
        self.ultimo_x = 0
        self.delay_bomerangue = 0
        self.delay_tele = 0

    def update(self, tela):
        tela.blit(self.imagem, self.retangulo)
        tecla = pygame.key.get_pressed()

        if self.delay_tele > 0 :
            self.delay_tele -= 1

        largura_tela = tela.get_width()
        altura_tela = tela.get_height()

        if self.modo_movimento:
            tecla_a = True if tecla[pygame.K_a] else False
            tecla_d = True if tecla[pygame.K_d] else False
            tecla_w = True if tecla[pygame.K_w] else False
            tecla_s = True if tecla[pygame.K_s] else False

            # ATUALIZA A POSIÇÃO GLOBAL DO JOGADOR 1 NAS OPERAÇÕES
            posicao_jogadores[1] = self.retangulo
            #aplicar bonus velocidade
            self.atualizar_bonus(1)

        else:
            tecla_a = True if tecla[pygame.K_LEFT] else False
            tecla_d = True if tecla[pygame.K_RIGHT] else False
            tecla_w = True if tecla[pygame.K_UP] else False
            tecla_s = True if tecla[pygame.K_DOWN] else False

            posicao_jogadores[2] = self.retangulo

            self.atualizar_bonus(2)

        if (self.empurrao_frames > 0):
            self.alterar_x(self.empurrao_vx) # aplica o empurrão no eixo x
            self.alterar_y(self.empurrao_vy) # aplica o empurrão no eixo y
            
            # diminui a velocidade do empurrão gradualmente para melhor efeito visual
            self.empurrao_vx *= 0.9  
            self.empurrao_vy *= 0.9
            
            self.empurrao_frames -= 1 # reduz o contador de frames do empurrão
        else: # empurrao acabou, zera as velocidades
            self.empurrao_vx = 0.0
            self.empurrao_vy = 0.0

        #resetar os movimentos passados
        self.ultimo_y = 0
        self.ultimo_x = 0

        # movimento
        if tecla_a:
            self.ultimo_x = -1
            if tecla_s or tecla_w:
                self.alterar_x(calcular_velocidade_diagonal(-self.velocidade))
            else:
                self.alterar_x(-self.velocidade)

        if tecla_d:
            self.ultimo_x = 1
            if tecla_s or tecla_w:
                self.alterar_x(calcular_velocidade_diagonal(self.velocidade))
            else:
                self.alterar_x(self.velocidade)

        if tecla_s:
            self.ultimo_y = 1
            if tecla_a or tecla_d:
                self.alterar_y(calcular_velocidade_diagonal(self.velocidade))
            else:
                self.alterar_y(self.velocidade)

        if tecla_w:
            self.ultimo_y = -1
            if tecla_a or tecla_d:
                self.alterar_y(calcular_velocidade_diagonal(-self.velocidade))
            else:
                self.alterar_y(-self.velocidade)
        
        # teletransporte quando sai da tela (wrap-around)
        if (self.retangulo.right < 0): # se sumir pela esquerda (canto direito desapareceu)
            self.retangulo.left = largura_tela # reaparece na direita (primeiro o canto esquerdo)
        elif (self.retangulo.left > largura_tela): # se sumir pela direita (canto esquerdo desapareceu)
            self.retangulo.right = 0 # reaparece na esquerda (primeiro o canto direito)
            
        if (self.retangulo.bottom < 0): # se sumir por cima (canto inferior desapareceu)
            self.retangulo.top = altura_tela # reaparece embaixo (primeiro o canto superior)
        elif (self.retangulo.top > altura_tela): # se sumir por baixo (canto superior desapareceu)
            self.retangulo.bottom = 0 # reaparece em cima (primeiro o canto inferior)



    '''funções que execultam o movimento, a maior parte é para resolver o proplema do objeto se mover mais rapido ou lento na diagonal,
        como o pygame não conssegue mover um objeto em numero decimais, o progama ele sempre arredondara o movimento para cima, toda vez que 
        o progama execultar um movimento que foi maior que o recebido, ele coloca uma "divida" no progama, e o perssonagem não conssiguira se 
        ate a divida ser paga, se o perssonagem tiver uma divida de movimento, ao invez do movimento ser usado para mover o perssonagem,
        o movimento sera utilizado para pagar a divida.'''

    def alterar_x(self, valor: float):
        if self.delay_x <= 0:
            self.retangulo.x += math.ceil(valor) if valor >= 0 else math.floor(valor)
            self.delay_x += abs(valor) - int(abs(valor))
        else:
            self.delay_x -= abs(valor)

    def alterar_y(self, valor: float):
        if self.delay_y <= 0:
            self.retangulo.y += math.ceil(valor) if valor >= 0 else math.floor(valor)
            self.delay_y += abs(valor) - int(abs(valor))
        else:
            self.delay_y -= abs(valor)


    def atualizar_bonus(self, jogador) :


        i = bonus[jogador]
        j = 'atual'
        if i['velocidade'][j] > 0 :
            i['velocidade'][j] -= 1
            self.velocidade = velocidade_padrao_perssonagens * itensidade_bonus_velocidade
        else :
            self.velocidade = velocidade_padrao_perssonagens

        #bomerangue
        tecla_r = True if pygame.key.get_pressed()[pygame.K_r] and jogador == 1 else False
        tecla_o = True if pygame.key.get_pressed()[pygame.K_o] and jogador == 2 else False
        if self.delay_bomerangue <= 0 :
            if i['bome'][j] > 0 and (tecla_r or tecla_o) and (abs(self.ultimo_x) > 0 or abs(self.ultimo_y) > 0) :
                print(self.ultimo_y)
                print('ok')
                bomerangues.add(Bomerangue((self.retangulo.x, self.retangulo.y), self.ultimo_x, self.ultimo_y, jogador))
                self.delay_bomerangue = 50
                i['bome'][j] -= 60

        else : self.delay_bomerangue -= 1

        


        if i['obsta'][j] > 0 :
            if jogador == 1:
                pontuacao_lista[1] = max(0, pontuacao_lista[1] - 1)
            elif jogador == 2:
                pontuacao_lista[2] = max(0, pontuacao_lista[2] - 1)
            i['obsta'][j] = 0


        #teletransporte
        tecla_t = True if pygame.key.get_pressed()[pygame.K_t] and jogador == 1 else False
        tecla_m = True if pygame.key.get_pressed()[pygame.K_m] and jogador == 2 else False
        if i['tele'][j] > 0 and (tecla_t or tecla_m) and (abs(self.ultimo_x) > 0 or abs(self.ultimo_y) > 0) and self.delay_tele <= 0 :
            self.velocidade = distancia_teleporte
            i['tele'][j] -= 60
            self.delay_tele = delay_entre_teletransportes


    def colidir_jogadores(self, todos_jogadores):
        for outro_jogador in todos_jogadores: 
            if (outro_jogador is not self): # colisao não é consigo mesmo
                if self.retangulo.colliderect(outro_jogador.retangulo): # caso ocorra colisão entre jogadores
                    dx = self.retangulo.centerx - outro_jogador.retangulo.centerx # vetor distancia x (diferença dos centros no eixo x)
                    dy = self.retangulo.centery - outro_jogador.retangulo.centery # vetor distancia y (diferença dos centros no eixo y)
                    
                    # distancia minima entre os centros sem se sobrepor(soma da metade da largura/altura)
                    # empurrao > 0 significa que teve empurrao
                    empurrao_x = (self.retangulo.width / 2) + (outro_jogador.retangulo.width / 2) - abs(dx) 
                    empurrao_y = (self.retangulo.height / 2) + (outro_jogador.retangulo.height / 2) - abs(dy)
                    
                    fator_empurrao = 3.0 # fator para aumentar a força do empurrao
                    frames_empurrao = 15 # duração do efeito de empurrão em frames
                    forca_min_empurrao = 5.0 # força minima do empurrao que seja perceptível visualmente

                    if (empurrao_x < empurrao_y): # mexe no eixo x (menor sobreposição)
                        # pra prevenir tremido, jogadores sao movidos metade do empurrao para fora da sobreposição
                        if (dx > 0): # jogador na direita
                            self.retangulo.x += empurrao_x / 2 #afasta para direita
                            outro_jogador.retangulo.x -= empurrao_x / 2 #afasta o outro jogador para esquerda
                        else: # jogador na esquerda
                            self.retangulo.x -= empurrao_x / 2 #afasta para esquerda
                            outro_jogador.retangulo.x += empurrao_x / 2 #afasta o outro jogador para direita
                            
                        forca_empurrao_x = max(empurrao_x * fator_empurrao, forca_min_empurrao) * (1 if (dx > 0) else -1) # para direita se dx>0, senao esquerda
                        
                        self.empurrao_vx = forca_empurrao_x
                        self.empurrao_frames = frames_empurrao
            
                        outro_jogador.empurrao_vx = -forca_empurrao_x # outro jogador é empurrado na direção oposta
                        outro_jogador.empurrao_frames = frames_empurrao
                        
                    else: # mexe no eixo y
                        if (dy > 0): # jogador emabixo
                            self.retangulo.y += empurrao_y / 2 #afasta para baixo
                            outro_jogador.retangulo.y -= empurrao_y / 2 # afasta o outro jogador para cima
                        else: # jogador em cima
                            self.retangulo.y -= empurrao_y / 2 # afasta para cima
                            outro_jogador.retangulo.y += empurrao_y / 2 # afasta o outro jogador para baixo

                        forca_empurrao_y = max(empurrao_y * fator_empurrao, forca_min_empurrao) * (1 if (dy > 0) else -1) # para baixo se dy>0, senao cima
                        
                        self.empurrao_vy = forca_empurrao_y
                        self.empurrao_frames = frames_empurrao
            
                        outro_jogador.empurrao_vy = -forca_empurrao_y # outro jogador é empurrado na direção oposta
                        outro_jogador.empurrao_frames = frames_empurrao




class Coletavel_generico(pygame.sprite.Sprite):

    def __init__(self, acao_na_coleta: str, aparencia: str, tempo_vida: int = None, bonus_tipo : str = None):
        super().__init__()

        self.imagem = pygame.Surface((10, 10))
        self.imagem.fill(aparencia)
        if acao_na_coleta != 'principal' : self.imagem.fill('Purple') if bonus_tipo == 'velocidade' else self.imagem.fill('Black') if bonus_tipo == 'bome' else self.imagem.fill('Red') if bonus_tipo == 'obsta' else self.imagem.fill('White')
        self.retangulo = self.imagem.get_rect(midbottom=achar_numero_tela())
        self.metodo = acao_na_coleta
        self.bonus = bonus_tipo
        if self.metodo == 'secundario': self.tempo_vida = tempo_vida

        if self.bonus == 'obsta' :
            self.direcao = 0
            self.delay_direcao = 100



    def update(self, tela):  # açao na coleta é do tipo função
        tela.blit(self.imagem, self.retangulo)

        if (colisao_personagem(self.retangulo) == 1):  # passa a area inteira do retangulo, nao apenas um ponto
            if (self.metodo == 'principal'):
                pontuacao_lista[1] += 1
                print(pontuacao_1)
                self.retangulo.x, self.retangulo.y = achar_numero_tela()[0], achar_numero_tela()[1]

            else :
                self.coleta_secundaria(1)

        elif (colisao_personagem(self.retangulo) == 2):
            if (self.metodo == 'principal'):
                pontuacao_lista[2] += 1
                self.retangulo.x, self.retangulo.y = achar_numero_tela()[0], achar_numero_tela()[1]
            else :
                self.coleta_secundaria(2)


        if self.metodo == 'secundario':
            if self.tempo_vida <= 0:
                self.kill()
            else:
                self.tempo_vida -= 1




        if self.bonus == 'obsta' : self.atualizar_movimento()




    def coleta_secundaria(self, jogador : int):
        bonus[jogador][self.bonus]['atual'] += bonus[jogador][self.bonus]['max']
        self.kill()

    def atualizar_movimento(self):
        if self.direcao == 0 : self.retangulo.x += velocidade_obstaculo
        if self.direcao == 1 : self.retangulo.y += velocidade_obstaculo
        if self.direcao == 2 : self.retangulo.x -= velocidade_obstaculo
        if self.direcao == 3 : self.retangulo.y -= velocidade_obstaculo

        if self.delay_direcao > 0 : self.delay_direcao -= 1
        else :
            self.direcao = (self.direcao + 1) % 4
            self.delay_direcao = 100




class Bomerangue(pygame.sprite.Sprite) :

    def __init__(self, localizacao : tuple[int,int],x : int,y : int, jogador : int):
        super().__init__()
        self.imagem = pygame.Surface((25,25))
        self.retangulo = self.imagem.get_rect(midbottom = localizacao)
        self.imagem.fill('Black')
        self.movimento_x = x
        self.movimento_y = y
        self.velocidade = velocidade_bomerangue
        if abs(self.movimento_x) > 0 and abs(self.movimento_y): self.velocidade = calcular_velocidade_diagonal(velocidade_bomerangue)
        print('bomerangue criado')
        self.jogador = jogador

        self.divida_x = 0
        self.divida_y = 0
        self.tempo_de_vida = 0

    def update(self,tela, *args, **kwargs):
        tela.blit(self.imagem, self.retangulo)
        if self.divida_x <= 0 :
            self.retangulo.x += math.ceil(self.movimento_x * self.velocidade) if self.movimento_x > 0 else math.floor(self.movimento_x * self.velocidade)
            self.divida_x += -abs(self.velocidade) + abs(math.ceil(self.velocidade))
        else :
            self.divida_x -= self.velocidade

        if self.divida_y <= 0 :
            self.retangulo.y += math.ceil(self.movimento_y * self.velocidade) if self.movimento_y > 0 else math.floor(self.movimento_y * self.velocidade)
            self.divida_y += -abs(self.velocidade) + abs(math.ceil(self.velocidade))
        else :
            self.divida_y -= self.velocidade


        if colisao_personagem(self.retangulo) == 1 and self.jogador == 2 :
            pontuacao_lista[1] = max(0, pontuacao_lista[1] - 1)
            self.kill()

        if colisao_personagem(self.retangulo) == 2 and self.jogador == 1 :
            pontuacao_lista[2] = max(0, pontuacao_lista[2] - 1)
            self.kill()


        if self.tempo_de_vida >= 200 : self.kill()
        else : self.tempo_de_vida += 1





jogador_1 = pygame.sprite.GroupSingle()
jogador_1.add(Jogador(velocidade_padrao_perssonagens, (200,200), True, 'Green'))
jogador_2 = pygame.sprite.GroupSingle()
jogador_2.add(Jogador(velocidade_padrao_perssonagens,(400,400), False, 'Yellow'))
bomerangues = pygame.sprite.Group()
