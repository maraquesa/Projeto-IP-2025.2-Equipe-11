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



    def update(self, tela):
        tela.blit(self.imagem, self.retangulo)
        tecla = pygame.key.get_pressed()


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

        # movimento
        if tecla_a:
            if tecla_s or tecla_w:
                self.alterar_x(calcular_velocidade_diagonal(-self.velocidade))
            else:
                self.alterar_x(-self.velocidade)

        if tecla_d:
            if tecla_s or tecla_w:
                self.alterar_x(calcular_velocidade_diagonal(self.velocidade))
            else:
                self.alterar_x(self.velocidade)

        if tecla_s:
            if tecla_a or tecla_d:
                self.alterar_y(calcular_velocidade_diagonal(self.velocidade))
            else:
                self.alterar_y(self.velocidade)

        if tecla_w:
            if tecla_a or tecla_d:
                self.alterar_y(calcular_velocidade_diagonal(-self.velocidade))
            else:
                self.alterar_y(-self.velocidade)

        self.retangulo.clamp_ip(tela.get_rect())  # impede o jogador de sair da tela



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





class Coletavel_generico(pygame.sprite.Sprite):

    def __init__(self, acao_na_coleta: str, aparencia: str, tempo_vida: int = None, bonus_tipo : str = None):
        super().__init__()

        global pontuacao_1, pontuacao_2
        self.imagem = pygame.Surface((10, 10))
        self.imagem.fill(aparencia)
        self.retangulo = self.imagem.get_rect(midbottom=achar_numero_tela())
        self.metodo = acao_na_coleta
        self.bonus = bonus_tipo
        if self.metodo == 'secundario': self.tempo_vida = tempo_vida



    def update(self, tela):  # açao na coleta é do tipo função
        tela.blit(self.imagem, self.retangulo)

        if (colisao_personagem(self.retangulo) == 1):  # passa a area inteira do retangulo, nao apenas um ponto
            if (self.metodo == 'principal'):
                global pontuacao_1
                pontuacao_1 += 1
                self.retangulo.x, self.retangulo.y = achar_numero_tela()[0], achar_numero_tela()[1]

            else :
                self.coleta_secundaria(1)

        elif (colisao_personagem(self.retangulo) == 2):
            if (self.metodo == 'principal'):
                global pontuacao_2
                pontuacao_2 += 1
                self.retangulo.x, self.retangulo.y = achar_numero_tela()[0], achar_numero_tela()[1]
            else :
                self.coleta_secundaria(2)


        if self.metodo == 'secundario':
            if self.tempo_vida <= 0:
                self.kill()
            else:
                self.tempo_vida -= 1



    def coleta_secundaria(self, jogador : int):
        if self.bonus == 'velocidade' : bonus[jogador][self.bonus]['atual'] = bonus[jogador][self.bonus]['max']
        self.kill()



jogador_1 = pygame.sprite.GroupSingle()
jogador_1.add(Jogador(velocidade_padrao_perssonagens, (200,200), True, 'Green'))
jogador_2 = pygame.sprite.GroupSingle()
jogador_2.add(Jogador(velocidade_padrao_perssonagens,(400,400), False, 'Yellow'))
