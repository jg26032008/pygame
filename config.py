# Configurações gerais do jogo
import os

PASTA = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(PASTA, 'assets', 'img')
SND_DIR = os.path.join(PASTA, 'assets', 'snd')

WIDTH = 480
HEIGHT = 600
FPS = 60
TITULO = 'Esquadrão 1945 — Jogo do André'

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AMARELO = (255, 220, 0)
VERMELHO = (220, 40, 40)
AZUL_ESCURO = (10, 40, 90)

# Jogador
PLAYER_SPEED = 5
SHOOT_TICKS = 250          # tempo mínimo entre tiros (ms)
VIDAS_INICIAIS = 3
VIDA_EXTRA_A_CADA = 1000   # pontos
INVENCIVEL_MS = 2000       # tempo piscando depois de renascer

# Pontos
PONTOS_INIMIGO = 100
PONTOS_BOMBARDEIRO = 500
PONTOS_MOEDA = 50
PONTOS_POR_FASE = 2000     # a cada X pontos o jogo passa de fase

# Estados das telas
INIT = 0
GAME = 1
GAME_OVER = 2
QUIT = 3
