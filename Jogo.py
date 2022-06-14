import pygame
import time
import math
from funções import tamanho_imagens, desenho

grama = tamanho_imagens(pygame.image.load('imagens/grama.jpg'), 2.5)
pista = tamanho_imagens(pygame.image.load('imagens/pista.png'), 0.9)
borda = tamanho_imagens(pygame.image.load('imagens/bordaDaPista.png'), 0.9)
chegada = pygame.image.load('imagens/chegada.png')
carroVerde = pygame.image.load('imagens/carroVerde.png')
carroRoxo = pygame.image.load('imagens/carroRoxo.png')

width, height = pista.get_width(), pista.get_height()
janela = pygame.display.set_mode((width, height))
pygame.display.set_caption('Top Carros!!')
fps = 60
run = True
relogio = pygame.time.Clock()
imagens = [(grama, (0,0)), (pista, (0,0))]
while run:
    relogio.tick(fps)
    desenho(janela, imagens)
    janela.blit(grama, (0,0))
    janela.blit(pista, (0,0))
    janela.blit(chegada, (0,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break      
pygame.quit()