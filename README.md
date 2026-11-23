# pygame

## Esquadrão 1945

Jogo de aviões em pygame, no estilo do 1945 Air Force

## Integrantes
- João Guilherme Farah
- Andre Conrado Pucci

## Vídeo
https://youtube.com/shorts/suQM5oyzfmM

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

## Uso de IA generativa

O código deste projeto foi praticamente todo (cerca de 90%) gerado com o
Claude (Anthropic), conforme permitido no enunciado.

- Arquivos de João (`sprites.py`, `telas.py`, `tela_jogo.py`, `jogo.py`):
  gerados pelo Claude a partir das regras do jogo definidas pelo grupo.
- Arquivos de Andre (`config.py`, `gerar_assets.py`, `assets.py`):
  gerados pelo Claude a partir do handout de pygame da disciplina e do
  jogo 1945 Air Force, usado como inspiração.
- As imagens e os sons são criados pelo `gerar_assets.py`, sem material
  de terceiros.

O grupo escolheu o tema e as regras, dividiu as partes entre os dois,
testou o jogo e revisou o código para entender cada arquivo.

Conversa com a IA (Andre): https://claude.ai/share/3b194557-1571-4eaa-a216-292389df3983
