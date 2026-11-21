# Carrega todas as imagens, sons e fontes em um dicionário
import os
import pygame
from config import IMG_DIR, SND_DIR


class SomMudo:
    """Usado se o computador não tiver saída de áudio."""
    def play(self, *args, **kwargs):
        pass

    def set_volume(self, *args):
        pass


def carrega_imagem(nome, tamanho=None):
    img = pygame.image.load(os.path.join(IMG_DIR, nome)).convert_alpha()
    if tamanho:
        img = pygame.transform.scale(img, tamanho)
    return img


def carrega_som(nome, volume=0.5):
    try:
        som = pygame.mixer.Sound(os.path.join(SND_DIR, nome))
        som.set_volume(volume)
        return som
    except pygame.error:
        return SomMudo()


def load_assets():
    assets = {}
    assets['mar'] = pygame.image.load(os.path.join(IMG_DIR, 'mar.png')).convert()
    assets['nuvem'] = carrega_imagem('nuvem.png')
    assets['jogador'] = carrega_imagem('jogador.png')
    assets['ala'] = carrega_imagem('ala.png')
    assets['inimigo'] = carrega_imagem('inimigo.png')
    assets['bombardeiro'] = carrega_imagem('bombardeiro.png')
    assets['tiro'] = carrega_imagem('tiro.png')
    assets['tiro_inimigo'] = carrega_imagem('tiro_inimigo.png')
    assets['moeda'] = carrega_imagem('moeda.png')
    assets['powerup'] = carrega_imagem('powerup.png')
    assets['explosao'] = [carrega_imagem(f'explosao{i:02d}.png') for i in range(9)]
    assets['explosao_grande'] = [pygame.transform.scale(q, (120, 120)) for q in assets['explosao']]
    assets['vida'] = carrega_imagem('jogador.png', (24, 24))

    assets['fonte_placar'] = pygame.font.SysFont('arial', 26, bold=True)
    assets['fonte_titulo'] = pygame.font.SysFont('arial', 44, bold=True)
    assets['fonte_texto'] = pygame.font.SysFont('arial', 20)

    assets['som_tiro'] = carrega_som('tiro.wav', 0.25)
    assets['som_explosao'] = carrega_som('explosao.wav', 0.6)
    assets['som_moeda'] = carrega_som('moeda.wav', 0.4)
    return assets


def toca_musica():
    try:
        pygame.mixer.music.load(os.path.join(SND_DIR, 'musica.wav'))
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(loops=-1)
    except pygame.error:
        pass
