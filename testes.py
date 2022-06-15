import pygame
import time
import math
from funções import tamanho_imagens
from carro import Carro

grama = tamanho_imagens(pygame.image.load('FOTOS/grama.jpg'), 2.5)
pista = tamanho_imagens(pygame.image.load('FOTOS/pista.png'), 0.9)
borda = tamanho_imagens(pygame.image.load('FOTOS/bordaDaPista.png'), 0.9)
chegada = pygame.image.load('FOTOS/chegada.png')
carroVerde = pygame.image.load('FOTOS/carroVerde.png')
carroRoxo = pygame.image.load('FOTOS/carroRoxo.png')

width, height = pista.get_width(), pista.get_height()
janela = pygame.display.set_mode((width, height))
pygame.display.set_caption('Top Carros!!')
fps = 60
run = True
relogio = pygame.time.Clock()
imagens = [(grama, (0,0)), (pista, (0,0))]
def desenho(janela, imagens, jogadorVerde):
    for imagem, pos in imagens:
        janela.blit(imagem, pos)
    jogadorVerde.desenho(janela)
    pygame.display.update()
class PlayerVerde(Carro):
    img = carroVerde
jogadorVerde = PlayerVerde(4, 2)

while run:
    relogio.tick(fps)
    desenho(janela, imagens, jogadorVerde)
    janela.blit(grama, (0,0))
    janela.blit(pista, (0,0))
    janela.blit(chegada, (0,0))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break      
pygame.quit()


import pygame


def tamanho_imagens(imagem, fator):
    tamanho = round(imagem.get_width() * fator), round(imagem.get_height() * fator)
    return pygame.transform.scale(imagem, tamanho)


def rotate_center(janela, imagem, top_esquerda, angulo):
    rotacao_imagem = pygame.transform.rotate(imagem, angulo)
    nova_reta = rotacao_imagem.get_rect(
        center=imagem.get_rect(topleft=top_esquerda).center)
    janela.blit(rotacao_imagem, nova_reta.topleft)



    import pygame
from funções import rotate_center

class Carro:
    def __init__(self, velocidadeMax, velocidadeRot):
        self.img = self.img
        self.velocidadeMax = velocidadeMax
        self.velocidade = 0
        self.velocidadeRot = velocidadeRot
        self.angulo = 0

    def rotacao(self, esquerda=False, direita=False):
        if esquerda:
            self.angulo += self.velocidadeRot
        elif direita:
            self.angulo -= self.velocidadeRot

    def posicao(self, janela):
        rotate_center(janela, self.img)