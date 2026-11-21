"""Tela inicial e tela de game over.

Cada função desenha a sua tela, espera o jogador apertar uma tecla
e devolve o próximo estado do jogo (GAME ou QUIT, de config.py).
Código gerado com ajuda de IA (Claude) — ver README.
"""
import os

import pygame

from config import WIDTH, HEIGHT, FPS, PASTA, BRANCO, AMARELO, AZUL_ESCURO, GAME, QUIT

ARQUIVO_RECORDE = os.path.join(PASTA, 'recorde.txt')


def le_recorde():
    """Lê o recorde salvo no arquivo. Se ainda não existir, o recorde é 0."""
    try:
        with open(ARQUIVO_RECORDE) as arquivo:
            return int(arquivo.read())
    except (FileNotFoundError, ValueError):
        return 0


def salva_recorde(pontos):
    """Grava os pontos como novo recorde se forem maiores que o atual.

    Devolve True quando é um recorde novo.
    """
    if pontos > le_recorde():
        with open(ARQUIVO_RECORDE, 'w') as arquivo:
            arquivo.write(str(pontos))
        return True
    return False


def escreve(tela, texto, tamanho, cor, centro):
    """Escreve um texto centralizado no ponto `centro`."""
    fonte = pygame.font.Font(None, tamanho)
    superficie = fonte.render(texto, True, cor)
    tela.blit(superficie, superficie.get_rect(center=centro))


def espera_tecla(tela, desenha):
    """Loop genérico das telas paradas.

    Chama desenha() todo frame. ESC ou fechar a janela -> QUIT;
    qualquer outra tecla -> GAME.
    """
    relogio = pygame.time.Clock()
    while True:
        relogio.tick(FPS)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return QUIT
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_ESCAPE:
                    return QUIT
                return GAME
        desenha()
        pygame.display.flip()


def tela_inicial(tela, assets):
    """Mostra o título, os controles e o recorde até o jogador apertar uma tecla."""
    recorde = le_recorde()

    def desenha():
        tela.fill(AZUL_ESCURO)
        img = assets['jogador']
        tela.blit(img, img.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 60)))
        escreve(tela, 'ESQUADRÃO 1945', 56, AMARELO, (WIDTH // 2, HEIGHT // 3))
        escreve(tela, 'Setas ou WASD: mover', 28, BRANCO, (WIDTH // 2, HEIGHT // 2))
        escreve(tela, 'Espaço: atirar', 28, BRANCO, (WIDTH // 2, HEIGHT // 2 + 30))
        escreve(tela, 'Pegue o P para ganhar tiros e aviões de ala', 22, BRANCO, (WIDTH // 2, HEIGHT // 2 + 70))
        escreve(tela, f'Recorde: {recorde}', 30, AMARELO, (WIDTH // 2, HEIGHT // 2 + 120))
        # texto piscando a cada meio segundo
        if (pygame.time.get_ticks() // 500) % 2:
            escreve(tela, 'Aperte qualquer tecla para jogar', 26, BRANCO, (WIDTH // 2, HEIGHT - 80))

    return espera_tecla(tela, desenha)


def tela_game_over(tela, pontos):
    """Mostra a pontuação final e o recorde. Qualquer tecla joga de novo."""
    novo_recorde = salva_recorde(pontos)
    recorde = le_recorde()

    # evita que uma tecla que ainda estava apertada pule a tela na hora
    pygame.time.wait(500)
    pygame.event.clear()

    def desenha():
        tela.fill(AZUL_ESCURO)
        escreve(tela, 'GAME OVER', 64, AMARELO, (WIDTH // 2, HEIGHT // 3))
        escreve(tela, f'Pontos: {pontos}', 36, BRANCO, (WIDTH // 2, HEIGHT // 2))
        if novo_recorde:
            escreve(tela, 'NOVO RECORDE!', 32, AMARELO, (WIDTH // 2, HEIGHT // 2 + 45))
        else:
            escreve(tela, f'Recorde: {recorde}', 30, BRANCO, (WIDTH // 2, HEIGHT // 2 + 45))
        escreve(tela, 'Qualquer tecla: jogar de novo   ESC: sair', 24, BRANCO, (WIDTH // 2, HEIGHT - 80))

    return espera_tecla(tela, desenha)
