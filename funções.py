import pygame


def tamanho_imagem(imagem, factor):
    tamanho = round(imagem.get_width() * factor), round(imagem.get_height() * factor)
    return pygame.transform.scale(imagem, tamanho)


def rotate_center(janela, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    nova_reta = rotated_image.get_rect(
        center=image.get_rect(topleft=top_left).center)
    janela.blit(rotated_image, nova_reta.topleft)


def text_center(janela, fonte, text):
    render = fonte.render(text, 1, (200, 200, 200))
    janela.blit(render, (janela.get_width()/2 - render.get_width() /
                      2, janela.get_height()/2 - render.get_height()/2))