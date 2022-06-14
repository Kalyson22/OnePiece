import pygame

def tamanho_imagens(imagem, fator):
    tamanho = round(imagem.get_width() * fator), round(imagem.get_height() * fator)
    return pygame.transform.scale(imagem, tamanho)

def desenho(janela, imagens):
    for imagem, pos in imagens:
        janela.blit(imagem, pos)