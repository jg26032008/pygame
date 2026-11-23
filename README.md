# pygame

## Esquadrão 1945

Jogo de aviões em pygame, no estilo do 1945 Air Force

## Como rodar
```
pip install pygame-ce
python jogo.py
```
Na primeira vez o jogo cria sozinho as imagens e sons em `assets/`.

**Por que `pygame-ce`?** O `pygame` normal não instala no Python 3.14 (o erro é
`Failed to build 'pygame'`). O `pygame-ce` é a versão mantida pela comunidade,
funciona do Python 3.10 ao 3.14 e é usado no código do mesmo jeito (`import pygame`).
Em versões mais antigas do Python, `pip install pygame` também funciona.
Se já tiver o `pygame` instalado, desinstale antes (`pip uninstall pygame`) para não dar conflito.

Se o terminal disser que `pip` ou `python` não é reconhecido (comum com Anaconda no Windows),
use o caminho completo do Python:
```
& "$HOME\anaconda3\python.exe" -m pip install pygame-ce
& "$HOME\anaconda3\python.exe" jogo.py
```

## Controles
- Setas ou WASD: mover
- Espaço: atirar
- ESC: sair

## Regras
- Derrube caças (100 pts) e bombardeiros (500 pts)
- Moedas valem 50 pts
- Power-up P: tiro duplo, depois triplo + 2 aviões de ala
- Vida extra a cada 1000 pontos, nova fase a cada 2000
