"""Tela da partida: loop principal do jogo, colisões, pontos, vidas e fases.

Código gerado com ajuda de IA (Claude) — ver README.
"""
import random

import pygame

from config import (WIDTH, HEIGHT, FPS, BRANCO, AMARELO, VIDAS_INICIAIS,
                    VIDA_EXTRA_A_CADA, PONTOS_INIMIGO, PONTOS_BOMBARDEIRO,
                    PONTOS_MOEDA, PONTOS_POR_FASE, GAME_OVER, QUIT)
from sprites import Fundo, Jogador, Ala, Inimigo, Bombardeiro, Item, Explosao

# Estados internos da partida
JOGANDO = 0
EXPLODINDO = 1   # o jogador foi atingido e a explosão está rolando
ACABOU = 2

CHANCE_MOEDA = 0.3       # chance de um caça derrubado soltar moeda
CHANCE_POWERUP = 0.08    # chance de soltar power-up P
INIMIGOS_POR_FASE = 2    # caças a mais a cada fase


class Partida:
    """Guarda tudo de uma partida e tem um método para cada etapa do frame."""

    def __init__(self, tela, assets):
        self.tela = tela
        self.assets = assets
        self.fundo = Fundo(assets['mar'])

        # grupos de sprites
        self.todos = pygame.sprite.Group()
        self.tiros = pygame.sprite.Group()
        self.tiros_inimigos = pygame.sprite.Group()
        self.inimigos = pygame.sprite.Group()
        self.bombardeiros = pygame.sprite.Group()
        self.itens = pygame.sprite.Group()
        self.alas = pygame.sprite.Group()

        self.jogador = Jogador(assets, self.tiros, self.todos)
        self.todos.add(self.jogador)

        self.pontos = 0
        self.vidas = VIDAS_INICIAIS
        self.proxima_vida_extra = VIDA_EXTRA_A_CADA
        self.fase = 1
        self.estado = JOGANDO
        self.fim_explosao = 0
        self.proximo_bombardeiro = pygame.time.get_ticks() + 8000
        self.mostra_fase_ate = pygame.time.get_ticks() + 2000

        self.cria_inimigos(5)

    # ---------- criação ----------

    def cria_inimigos(self, quantidade):
        """Adiciona caças na tela."""
        for _ in range(quantidade):
            inimigo = Inimigo(self.assets, self.fase)
            self.inimigos.add(inimigo)
            self.todos.add(inimigo)

    def cria_bombardeiro(self):
        """Cria um bombardeiro de tempos em tempos (mais seguido nas fases altas)."""
        agora = pygame.time.get_ticks()
        if agora > self.proximo_bombardeiro and not self.bombardeiros:
            bomb = Bombardeiro(self.assets, self.jogador, self.tiros_inimigos, self.todos, self.fase)
            self.bombardeiros.add(bomb)
            self.todos.add(bomb)
            self.proximo_bombardeiro = agora + max(6000, 15000 - 1500 * self.fase)

    def solta_item(self, centro):
        """Sorteia se o inimigo derrubado solta moeda, power-up ou nada."""
        sorteio = random.random()
        if sorteio < CHANCE_POWERUP:
            tipo = 'powerup'
        elif sorteio < CHANCE_POWERUP + CHANCE_MOEDA:
            tipo = 'moeda'
        else:
            return
        item = Item(self.assets, tipo, centro)
        self.itens.add(item)
        self.todos.add(item)

    def explode(self, centro):
        """Mostra a animação de explosão e toca o som."""
        self.todos.add(Explosao(self.assets, centro))
        self.assets['som_explosao'].play()

    # ---------- eventos e regras ----------

    def trata_eventos(self):
        """Fechar a janela ou ESC encerra; espaço segurado faz atirar."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return QUIT
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return QUIT
        if self.estado == JOGANDO and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.jogador.atira()
            for ala in self.alas:
                ala.atira()
        return None

    def soma_pontos(self, valor):
        """Soma pontos, dá vida extra e passa de fase quando chega no limite."""
        self.pontos += valor
        if self.pontos >= self.proxima_vida_extra:
            self.vidas += 1
            self.proxima_vida_extra += VIDA_EXTRA_A_CADA
        nova_fase = self.pontos // PONTOS_POR_FASE + 1
        if nova_fase > self.fase:
            self.fase = nova_fase
            self.cria_inimigos(INIMIGOS_POR_FASE)
            self.mostra_fase_ate = pygame.time.get_ticks() + 2000

    def pega_powerup(self):
        """Cada P melhora o tiro: duplo -> triplo -> 2 aviões de ala."""
        self.assets['som_moeda'].play()  # não existe som próprio de power-up
        if self.jogador.nivel_tiro < 3:
            self.jogador.nivel_tiro += 1
        elif not self.alas:
            for lado in (-1, 1):
                ala = Ala(self.assets, self.jogador, lado, self.tiros, self.todos)
                self.alas.add(ala)
                self.todos.add(ala)
        else:
            self.soma_pontos(PONTOS_MOEDA)  # já tem tudo: vira pontos

    def colisoes(self):
        """Confere todas as colisões do frame."""
        # tiros do jogador x caças: os dois somem
        acertos = pygame.sprite.groupcollide(self.inimigos, self.tiros, True, True,
                                             pygame.sprite.collide_mask)
        for inimigo in acertos:
            self.explode(inimigo.rect.center)
            self.solta_item(inimigo.rect.center)
            self.soma_pontos(PONTOS_INIMIGO)
            self.cria_inimigos(1)  # sempre repõe o caça derrubado

        # tiros do jogador x bombardeiro: tira vida até destruir
        acertos = pygame.sprite.groupcollide(self.bombardeiros, self.tiros, False, True,
                                             pygame.sprite.collide_mask)
        for bomb, tiros in acertos.items():
            for _ in tiros:
                if bomb.leva_dano():
                    self.explode(bomb.rect.center)
                    item = Item(self.assets, 'powerup', bomb.rect.center)  # sempre dá P
                    self.itens.add(item)
                    self.todos.add(item)
                    self.soma_pontos(PONTOS_BOMBARDEIRO)
                    bomb.kill()
                    break

        # jogador x itens
        for item in pygame.sprite.spritecollide(self.jogador, self.itens, True):
            if item.tipo == 'moeda':
                self.assets['som_moeda'].play()
                self.soma_pontos(PONTOS_MOEDA)
            else:
                self.pega_powerup()

        # jogador x inimigos e tiros inimigos (só se não estiver invencível)
        if self.jogador.invencivel():
            return
        bateu = (pygame.sprite.spritecollide(self.jogador, self.inimigos, True, pygame.sprite.collide_mask)
                 or pygame.sprite.spritecollide(self.jogador, self.tiros_inimigos, True, pygame.sprite.collide_mask)
                 or pygame.sprite.spritecollide(self.jogador, self.bombardeiros, False, pygame.sprite.collide_mask))
        if bateu:
            self.jogador_morre()

    def jogador_morre(self):
        """Perde uma vida, o power-up e os aviões de ala; espera a explosão."""
        self.explode(self.jogador.rect.center)
        self.jogador.kill()
        for ala in self.alas:
            ala.kill()
        self.jogador.nivel_tiro = 1
        self.vidas -= 1
        self.estado = EXPLODINDO
        self.fim_explosao = pygame.time.get_ticks() + 1200

    def depois_da_explosao(self):
        """Quando a explosão acaba: renasce ou termina a partida."""
        if pygame.time.get_ticks() < self.fim_explosao:
            return
        if self.vidas <= 0:
            self.estado = ACABOU
        else:
            self.jogador.renasce()
            self.todos.add(self.jogador)
            self.estado = JOGANDO
        # caças que estavam em cima do jogador não podem matar de novo na hora
        if len(self.inimigos) < 5:
            self.cria_inimigos(5 - len(self.inimigos))

    # ---------- desenho ----------

    def desenha_hud(self):
        """Pontos, fase e vidas (mininaves) no topo da tela."""
        fonte = pygame.font.Font(None, 30)
        self.tela.blit(fonte.render(f'{self.pontos:06d}', True, AMARELO), (10, 10))
        self.tela.blit(fonte.render(f'Fase {self.fase}', True, BRANCO), (WIDTH // 2 - 35, 10))
        mini = self.assets['vida']
        for i in range(self.vidas):
            self.tela.blit(mini, (WIDTH - 28 - i * 24, 10))

        if pygame.time.get_ticks() < self.mostra_fase_ate:
            grande = pygame.font.Font(None, 60)
            texto = grande.render(f'FASE {self.fase}', True, AMARELO)
            self.tela.blit(texto, texto.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

    def desenha(self):
        """Desenha fundo, sprites, barras de vida e HUD."""
        self.fundo.draw(self.tela)
        self.todos.draw(self.tela)
        for bomb in self.bombardeiros:
            bomb.desenha_barra(self.tela)
        self.desenha_hud()
        pygame.display.flip()


def tela_jogo(tela, assets):
    """Roda uma partida inteira.

    Devolve (próximo estado, pontos): GAME_OVER quando as vidas acabam
    ou QUIT se o jogador fechar a janela.
    """
    relogio = pygame.time.Clock()
    partida = Partida(tela, assets)

    while partida.estado != ACABOU:
        relogio.tick(FPS)
        if partida.trata_eventos() == QUIT:
            return QUIT, partida.pontos

        partida.fundo.update()
        partida.todos.update()
        if partida.estado == JOGANDO:
            partida.cria_bombardeiro()
            partida.colisoes()
        else:
            partida.depois_da_explosao()
        partida.desenha()

    return GAME_OVER, partida.pontos
