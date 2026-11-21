"""Esquadrão 1945 — arquivo principal. Rode com:  python jogo.py

Abre a janela, carrega imagens e sons e controla qual tela aparece
(máquina de estados: INIT -> GAME -> GAME_OVER -> GAME ... até QUIT).
Código gerado com ajuda de IA (Claude) — ver README.
"""
import os

import pygame

from config import WIDTH, HEIGHT, TITULO, IMG_DIR, INIT, GAME, GAME_OVER, QUIT


def prepara_assets():
    """Na primeira vez que o jogo roda, cria as imagens e os sons em assets/."""
    if not os.path.exists(os.path.join(IMG_DIR, 'jogador.png')):
        import gerar_assets
        gerar_assets.main()


def main():
    """Inicia o pygame e troca de tela de acordo com o estado."""
    prepara_assets()
    pygame.init()
    try:
        pygame.mixer.init()
    except pygame.error:
        pass  # computador sem som: o jogo roda mudo

    tela = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITULO)

    # só dá para carregar as imagens depois de abrir a janela (por causa do convert())
    from assets import load_assets, toca_musica
    from telas import tela_inicial, tela_game_over
    from tela_jogo import tela_jogo

    assets = load_assets()
    toca_musica()

    estado = INIT
    pontos = 0
    while estado != QUIT:
        if estado == INIT:
            estado = tela_inicial(tela, assets)
        elif estado == GAME:
            estado, pontos = tela_jogo(tela, assets)
        elif estado == GAME_OVER:
            estado = tela_game_over(tela, pontos)

    pygame.quit()


if __name__ == '__main__':
    main()
