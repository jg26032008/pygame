"""Classes dos objetos do jogo (sprites).

Cada classe herda de pygame.sprite.Sprite e tem um método update(),
chamado uma vez por frame pelo grupo onde o sprite está.
Código gerado com ajuda de IA (Claude) — ver README.
"""
import math
import random

import pygame

from config import WIDTH, HEIGHT, PLAYER_SPEED, SHOOT_TICKS, INVENCIVEL_MS


class Fundo:
    """Fundo que rola para baixo sem parar, dando a sensação de voo."""

    def __init__(self, imagem, velocidade=2):
        self.imagem = pygame.transform.scale(imagem, (WIDTH, HEIGHT))
        self.velocidade = velocidade
        self.y = 0

    def update(self):
        """Desce a imagem e volta ao topo quando ela sai inteira da tela."""
        self.y = (self.y + self.velocidade) % HEIGHT

    def draw(self, tela):
        """Desenha duas cópias, uma em cima da outra, para não aparecer buraco."""
        tela.blit(self.imagem, (0, self.y))
        tela.blit(self.imagem, (0, self.y - HEIGHT))


class Tiro(pygame.sprite.Sprite):
    """Tiro em linha reta. vx e vy dizem a direção e a velocidade."""

    def __init__(self, imagem, x, y, vx, vy):
        super().__init__()
        self.image = imagem
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(x, y))
        # posição em float para tiros em diagonal não perderem precisão
        self.x = float(x)
        self.y = float(y)
        self.vx = vx
        self.vy = vy

    def update(self):
        """Move o tiro e apaga quando ele sai da tela."""
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (round(self.x), round(self.y))
        if not pygame.Rect(0, 0, WIDTH, HEIGHT).colliderect(self.rect):
            self.kill()


class Jogador(pygame.sprite.Sprite):
    """Avião do jogador: anda com setas/WASD e atira com espaço.

    nivel_tiro: 1 = tiro simples, 2 = duplo, 3 = triplo (com power-up).
    """

    def __init__(self, assets, grupo_tiros, todos):
        super().__init__()
        self.assets = assets
        self.image = assets['jogador']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.grupo_tiros = grupo_tiros
        self.todos = todos
        self.nivel_tiro = 1
        self.ultimo_tiro = 0
        self.invencivel_ate = 0
        self.renasce()

    def renasce(self):
        """Volta para o centro de baixo e fica invencível por um tempo."""
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.invencivel_ate = pygame.time.get_ticks() + INVENCIVEL_MS

    def invencivel(self):
        """True enquanto o jogador ainda está piscando depois de renascer."""
        return pygame.time.get_ticks() < self.invencivel_ate

    def update(self):
        """Lê o teclado, move o avião sem sair da tela e faz ele piscar."""
        teclas = pygame.key.get_pressed()
        dx = (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) - (teclas[pygame.K_LEFT] or teclas[pygame.K_a])
        dy = (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) - (teclas[pygame.K_UP] or teclas[pygame.K_w])
        self.rect.x += dx * PLAYER_SPEED
        self.rect.y += dy * PLAYER_SPEED
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

        # pisca: some a cada 100 ms enquanto estiver invencível
        if self.invencivel() and (pygame.time.get_ticks() // 100) % 2:
            self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        else:
            self.image = self.assets['jogador']

    def atira(self):
        """Cria os tiros de acordo com o nível, respeitando SHOOT_TICKS."""
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro < SHOOT_TICKS:
            return
        self.ultimo_tiro = agora

        x, y = self.rect.centerx, self.rect.top
        if self.nivel_tiro == 1:
            saidas = [(x, 0)]
        elif self.nivel_tiro == 2:
            saidas = [(x - 10, 0), (x + 10, 0)]
        else:
            saidas = [(x - 12, -2), (x, 0), (x + 12, 2)]  # o 2º valor abre o leque

        for sx, vx in saidas:
            tiro = Tiro(self.assets['tiro'], sx, y, vx, -10)
            self.grupo_tiros.add(tiro)
            self.todos.add(tiro)
        self.assets['som_tiro'].play()


class Ala(pygame.sprite.Sprite):
    """Avião de ala: segue o jogador ao lado dele e atira junto.

    lado = -1 fica à esquerda, lado = 1 fica à direita.
    """

    def __init__(self, assets, jogador, lado, grupo_tiros, todos):
        super().__init__()
        self.assets = assets
        self.image = assets['ala']
        self.rect = self.image.get_rect()
        self.jogador = jogador
        self.lado = lado
        self.grupo_tiros = grupo_tiros
        self.todos = todos
        self.ultimo_tiro = 0

    def update(self):
        """Acompanha o jogador, mantendo uma distância fixa para o lado."""
        self.rect.centerx = self.jogador.rect.centerx + self.lado * 45
        self.rect.centery = self.jogador.rect.centery + 15

    def atira(self):
        """Atira um tiro simples, com o mesmo intervalo do jogador."""
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro < SHOOT_TICKS:
            return
        self.ultimo_tiro = agora
        tiro = Tiro(self.assets['tiro'], self.rect.centerx, self.rect.top, 0, -10)
        self.grupo_tiros.add(tiro)
        self.todos.add(tiro)


class Inimigo(pygame.sprite.Sprite):
    """Caça inimigo que desce com posição e velocidade aleatórias.

    A velocidade máxima aumenta com a fase.
    """

    def __init__(self, assets, fase):
        super().__init__()
        self.image = assets['inimigo']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.fase = fase
        self.sorteia()

    def sorteia(self):
        """Coloca o caça acima da tela com posição e velocidade aleatórias."""
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randint(-200, 0)
        self.vx = random.randint(-2, 2)
        self.vy = random.randint(2, 4 + self.fase)

    def update(self):
        """Desce; se sair da tela, volta lá em cima com novos valores."""
        self.rect.x += self.vx
        self.rect.y += self.vy
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.sorteia()


class Bombardeiro(pygame.sprite.Sprite):
    """Avião grande e lento, com barra de vida, que atira mirando no jogador."""

    def __init__(self, assets, jogador, grupo_tiros_inimigos, todos, fase):
        super().__init__()
        self.assets = assets
        self.image = assets['bombardeiro']
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(self.rect.width // 2, WIDTH - self.rect.width // 2)
        self.rect.bottom = 0
        self.jogador = jogador
        self.grupo_tiros = grupo_tiros_inimigos
        self.todos = todos
        self.vida_max = 8 + 2 * fase
        self.vida = self.vida_max
        self.intervalo_tiro = max(600, 1500 - 150 * fase)  # atira mais rápido nas fases altas
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):
        """Desce até 1/4 da tela, fica lá atirando e some se sair da tela."""
        if self.rect.top < HEIGHT // 4:
            self.rect.y += 1

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro > self.intervalo_tiro:
            self.ultimo_tiro = agora
            self.atira_no_jogador()

    def atira_no_jogador(self):
        """Calcula a direção até o jogador e solta um tiro nessa direção."""
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.bottom
        dist = math.hypot(dx, dy) or 1  # "or 1" evita dividir por zero
        vel = 5
        tiro = Tiro(self.assets['tiro_inimigo'], self.rect.centerx, self.rect.bottom,
                    dx / dist * vel, dy / dist * vel)
        self.grupo_tiros.add(tiro)
        self.todos.add(tiro)

    def leva_dano(self):
        """Tira 1 de vida. Devolve True se o bombardeiro foi destruído."""
        self.vida -= 1
        return self.vida <= 0

    def desenha_barra(self, tela):
        """Desenha a barra de vida (vermelha por baixo, verde por cima)."""
        largura = self.rect.width
        x, y = self.rect.left, self.rect.top - 8
        pygame.draw.rect(tela, (200, 0, 0), (x, y, largura, 5))
        pygame.draw.rect(tela, (0, 200, 0), (x, y, largura * self.vida // self.vida_max, 5))


class Item(pygame.sprite.Sprite):
    """Coisa que desce devagar para o jogador pegar: moeda ou power-up.

    tipo é 'moeda' ou 'powerup' (também é a chave da imagem nos assets).
    """

    def __init__(self, assets, tipo, centro):
        super().__init__()
        self.tipo = tipo
        self.image = assets[tipo]
        self.rect = self.image.get_rect(center=centro)

    def update(self):
        """Desce 2 pixels por frame e some quando sai da tela."""
        self.rect.y += 2
        if self.rect.top > HEIGHT:
            self.kill()


class Explosao(pygame.sprite.Sprite):
    """Animação de explosão: troca de quadro a cada 50 ms e depois some."""

    def __init__(self, assets, centro):
        super().__init__()
        self.quadros = assets['explosao']
        self.quadro = 0
        self.image = self.quadros[0]
        self.rect = self.image.get_rect(center=centro)
        self.ultimo = pygame.time.get_ticks()
        self.duracao_quadro = 50

    def update(self):
        """Avança a animação; no último quadro o sprite é removido."""
        agora = pygame.time.get_ticks()
        if agora - self.ultimo > self.duracao_quadro:
            self.ultimo = agora
            self.quadro += 1
            if self.quadro == len(self.quadros):
                self.kill()
                return
            centro = self.rect.center
            self.image = self.quadros[self.quadro]
            self.rect = self.image.get_rect(center=centro)
