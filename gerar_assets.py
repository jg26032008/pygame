# Gera as imagens e sons do jogo (não é preciso baixar nada).
# Rode uma vez:  python gerar_assets.py
# Os arquivos vão para assets/img e assets/snd.

import math
import os
import random
import struct
import wave

import pygame

PASTA = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(PASTA, 'assets', 'img')
SND = os.path.join(PASTA, 'assets', 'snd')
TAXA = 22050


# ------------------------------------------------------------------ imagens
def aviao(cor, cor_escura, tam=(64, 64), inimigo=False, bombardeiro=False):
    """Desenha um avião visto de cima. Inimigos apontam para baixo."""
    w, h = tam
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    cx = w // 2
    if bombardeiro:
        # asa larga, dois motores
        pygame.draw.polygon(s, cor_escura, [(2, h*0.42), (w-2, h*0.42), (w-8, h*0.58), (8, h*0.58)])
        pygame.draw.polygon(s, cor, [(4, h*0.44), (w-4, h*0.44), (w-10, h*0.55), (10, h*0.55)])
        for mx in (w*0.28, w*0.72):
            pygame.draw.ellipse(s, cor_escura, (mx-6, h*0.30, 12, 28))
            pygame.draw.circle(s, (40, 40, 40), (int(mx), int(h*0.30)), 5)
        pygame.draw.ellipse(s, cor, (cx-9, 4, 18, h-8))
        pygame.draw.polygon(s, cor_escura, [(cx-20, h-14), (cx+20, h-14), (cx+14, h-6), (cx-14, h-6)])
        pygame.draw.ellipse(s, (170, 220, 255), (cx-5, 10, 10, 14))
    else:
        pygame.draw.polygon(s, cor_escura, [(2, h*0.48), (w-2, h*0.48), (w-6, h*0.62), (6, h*0.62)])
        pygame.draw.polygon(s, cor, [(4, h*0.50), (w-4, h*0.50), (w-8, h*0.59), (8, h*0.59)])
        pygame.draw.ellipse(s, cor, (cx-7, 4, 14, h-8))
        pygame.draw.polygon(s, cor_escura, [(cx-15, h-12), (cx+15, h-12), (cx+11, h-5), (cx-11, h-5)])
        pygame.draw.ellipse(s, (170, 220, 255), (cx-4, h*0.30, 8, 12))
        pygame.draw.line(s, (40, 40, 40), (cx-10, 5), (cx+10, 5), 3)  # hélice
        if not inimigo:
            pygame.draw.circle(s, (255, 255, 255), (int(w*0.2), int(h*0.55)), 4)
            pygame.draw.circle(s, (200, 30, 30), (int(w*0.2), int(h*0.55)), 2)
            pygame.draw.circle(s, (255, 255, 255), (int(w*0.8), int(h*0.55)), 4)
            pygame.draw.circle(s, (200, 30, 30), (int(w*0.8), int(h*0.55)), 2)
        else:
            pygame.draw.circle(s, (220, 0, 0), (int(w*0.2), int(h*0.55)), 4)
            pygame.draw.circle(s, (220, 0, 0), (int(w*0.8), int(h*0.55)), 4)
    if inimigo:
        s = pygame.transform.flip(s, False, True)
    return s


def mar(w=480, h=600):
    s = pygame.Surface((w, h))
    s.fill((20, 90, 160))
    rnd = random.Random(7)
    for _ in range(260):  # ondas
        x, y = rnd.randint(0, w), rnd.randint(0, h)
        pygame.draw.line(s, (60, 130, 200), (x, y), (x + rnd.randint(6, 18), y), 2)
    for _ in range(3):  # ilhas
        r = rnd.randint(25, 45)
        x, y = rnd.randint(r+10, w-r-10), rnd.randint(r+10, h-r-10)
        pygame.draw.circle(s, (230, 210, 150), (x, y), r + 6)
        pygame.draw.circle(s, (40, 140, 60), (x, y), r)
        pygame.draw.circle(s, (30, 110, 45), (x - r//3, y - r//4), r//2)
    return s


def nuvem():
    s = pygame.Surface((140, 70), pygame.SRCALPHA)
    for (x, y, r) in [(35, 40, 25), (65, 30, 30), (100, 40, 25), (70, 48, 22)]:
        pygame.draw.circle(s, (255, 255, 255, 150), (x, y), r)
    return s


def explosao(n=9, tam=64):
    quadros = []
    for i in range(n):
        s = pygame.Surface((tam, tam), pygame.SRCALPHA)
        t = (i + 1) / n
        r = int(tam/2 * t)
        alpha = int(255 * (1 - t*0.8))
        pygame.draw.circle(s, (255, 120, 0, alpha), (tam//2, tam//2), r)
        pygame.draw.circle(s, (255, 230, 80, alpha), (tam//2, tam//2), int(r*0.6))
        if i > n//2:
            pygame.draw.circle(s, (90, 90, 90, alpha), (tam//2, tam//2), int(r*0.35))
        quadros.append(s)
    return quadros


def moeda(tam=22):
    s = pygame.Surface((tam, tam), pygame.SRCALPHA)
    pygame.draw.circle(s, (200, 150, 0), (tam//2, tam//2), tam//2)
    pygame.draw.circle(s, (255, 215, 0), (tam//2, tam//2), tam//2 - 3)
    f = pygame.font.SysFont(None, 20, bold=True)
    t = f.render('$', True, (180, 120, 0))
    s.blit(t, t.get_rect(center=(tam//2, tam//2 + 1)))
    return s


def powerup(tam=26):
    s = pygame.Surface((tam, tam), pygame.SRCALPHA)
    pygame.draw.rect(s, (30, 200, 80), (0, 0, tam, tam), border_radius=6)
    pygame.draw.rect(s, (255, 255, 255), (0, 0, tam, tam), 2, border_radius=6)
    f = pygame.font.SysFont(None, 26, bold=True)
    t = f.render('P', True, (255, 255, 255))
    s.blit(t, t.get_rect(center=(tam//2, tam//2 + 1)))
    return s


def tiro(cor, w=6, h=16):
    s = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(s, cor, (0, 0, w, h))
    pygame.draw.ellipse(s, (255, 255, 255), (w//4, 2, w//2, h//2))
    return s


def tiro_inimigo(r=5):
    s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
    pygame.draw.circle(s, (255, 60, 60), (r, r), r)
    pygame.draw.circle(s, (255, 200, 200), (r, r), r//2)
    return s


# ------------------------------------------------------------------ sons
def salvar_wav(nome, amostras, pasta=None):
    with wave.open(os.path.join(pasta or SND, nome), 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(TAXA)
        f.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, a)) * 30000)) for a in amostras))


def som_tiro():
    n = int(TAXA * 0.12)
    return [math.sin(2*math.pi*(900 - 5000*i/TAXA)*i/TAXA) * (1 - i/n) * 0.5 for i in range(n)]


def som_explosao():
    rnd = random.Random(1)
    n = int(TAXA * 0.6)
    out, v = [], 0.0
    for i in range(n):
        v = v*0.9 + rnd.uniform(-1, 1)*0.1  # ruído filtrado (grave)
        out.append(v * 4 * (1 - i/n)**2)
    return out


def som_moeda():
    out = []
    for freq, dur in ((988, 0.06), (1319, 0.12)):
        n = int(TAXA*dur)
        out += [0.4*math.copysign(1, math.sin(2*math.pi*freq*i/TAXA)) * (1 - i/n) for i in range(n)]
    return out


def musica():
    # loop simples de marcha (baixo + melodia), ~8 s
    notas = [220, 220, 262, 220, 294, 262, 247, 196,
             220, 220, 262, 330, 294, 262, 247, 220]
    out = []
    dur = 0.25
    for k in range(2):
        for j, f in enumerate(notas):
            n = int(TAXA*dur)
            baixo = notas[(j // 4) * 4] / 2
            for i in range(n):
                t = i / TAXA
                env = 1 - i/n
                a = 0.18*math.copysign(1, math.sin(2*math.pi*f*t))*env
                a += 0.15*math.sin(2*math.pi*baixo*t)
                if j % 2 == 0 and i < n*0.15:
                    a += random.uniform(-0.1, 0.1)  # caixa
                out.append(a)
    return out


def main():
    pygame.init()  # desenhar e salvar imagens não precisa abrir janela
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(SND, exist_ok=True)

    pygame.image.save(aviao((90, 140, 70), (50, 90, 40)), os.path.join(IMG, 'jogador.png'))
    pygame.image.save(aviao((150, 180, 210), (100, 120, 150), (40, 40)), os.path.join(IMG, 'ala.png'))
    pygame.image.save(aviao((200, 60, 50), (130, 30, 30), (48, 48), inimigo=True), os.path.join(IMG, 'inimigo.png'))
    pygame.image.save(aviao((110, 110, 120), (60, 60, 70), (110, 90), inimigo=True, bombardeiro=True), os.path.join(IMG, 'bombardeiro.png'))
    pygame.image.save(mar(), os.path.join(IMG, 'mar.png'))
    pygame.image.save(nuvem(), os.path.join(IMG, 'nuvem.png'))
    pygame.image.save(moeda(), os.path.join(IMG, 'moeda.png'))
    pygame.image.save(powerup(), os.path.join(IMG, 'powerup.png'))
    pygame.image.save(tiro((255, 230, 60)), os.path.join(IMG, 'tiro.png'))
    pygame.image.save(tiro_inimigo(), os.path.join(IMG, 'tiro_inimigo.png'))
    for i, q in enumerate(explosao()):
        pygame.image.save(q, os.path.join(IMG, f'explosao{i:02d}.png'))

    salvar_wav('tiro.wav', som_tiro())
    salvar_wav('explosao.wav', som_explosao())
    salvar_wav('moeda.wav', som_moeda())
    salvar_wav('musica.wav', musica())

    print('Assets gerados.')


if __name__ == '__main__':
    main()
