import pygame
import time
import math
from funções import tamanho_imagem, rotate_center, text_center
pygame.font.init()

grama = tamanho_imagem(pygame.image.load("FOTOS/grama.jpg"), 2.5)
pista = tamanho_imagem(pygame.image.load("FOTOS/pista.png"), 0.9)

borda = tamanho_imagem(pygame.image.load("FOTOS/borda.png"), 0.9)
borda_MASK = pygame.mask.from_surface(borda)

chegada = pygame.image.load("FOTOS/chegada.png")
chegada_MASK = pygame.mask.from_surface(chegada)
chegada_posicao = (130, 250)

carroVerde = tamanho_imagem(pygame.image.load("FOTOS/carroVerde.png"), 0.55)
carroRoxo = tamanho_imagem(pygame.image.load("FOTOS/carroRoxo.png"), 0.55)

WIDTH, HEIGHT = pista.get_width(), pista.get_height()
janela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top Carros!")

fonte = pygame.font.SysFont("times new roman", 44)

FPS = 60
caminho = [(175, 119), (110, 70), (56, 133), (70, 481), (318, 731), (404, 680), (418, 521), (507, 475), (600, 551), (613, 715), (736, 713),
        (734, 399), (611, 357), (409, 343), (433, 257), (697, 258), (738, 123), (581, 71), (303, 78), (275, 377), (176, 388), (178, 260)]


class GameInfo:
    LEVELS = 10

    def __init__(self, level=1):
        self.level = level
        self.inicio = False
        self.level_tempo_inicial = 0

    def prox_level(self):
        self.level += 1
        self.inicio = False

    def reset(self):
        self.level = 1
        self.inicio = False
        self.level_tempo_inicial = 0

    def game_chegada(self):
        return self.level > self.LEVELS

    def inicio_level(self):
        self.inicio = True
        self.level_tempo_inicial = time.time()

    def tempo_level(self):
        if not self.inicio:
            return 0
        return round(time.time() - self.level_tempo_inicial)


class Carro:
    def __init__(self, max_vel, rotacao_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotacao_vel = rotacao_vel
        self.angulo = 0
        self.x, self.y = self.inicio_POS
        self.aceleracao = 0.1

    def rotate(self, left=False, right=False):
        if left:
            self.angulo += self.rotacao_vel
        elif right:
            self.angulo -= self.rotacao_vel

    def desenho(self, janela):
        rotate_center(janela, self.img, (self.x, self.y), self.angulo)

    def mover_frente(self):
        self.vel = min(self.vel + self.aceleracao, self.max_vel)
        self.move()

    def mover_tras(self):
        self.vel = max(self.vel - self.aceleracao, -self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angulo)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def collide(self, mask, x=0, y=0):
        carro_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(carro_mask, offset)
        return poi

    def reset(self):
        self.x, self.y = self.inicio_POS
        self.angulo = 0
        self.vel = 0


class PlayerCar(Carro):
    IMG = carroVerde
    inicio_POS = (180, 200)

    def reduce_speed(self):
        self.vel = max(self.vel - self.aceleracao / 2, 0)
        self.move()

    def bounce(self):
        self.vel = -self.vel
        self.move()


class ComputerCar(Carro):
    IMG = carroRoxo
    inicio_POS = (150, 200)

    def __init__(self, max_vel, rotacao_vel, caminho=[]):
        super().__init__(max_vel, rotacao_vel)
        self.caminho = caminho
        self.ponto_atual = 0
        self.vel = max_vel

    def desenho_ponto(self, janela):
        for point in self.caminho:
            pygame.draw.circle(janela, (255, 0, 0), point, 5)

    def desenho(self, janela):
        super().desenho(janela)

    def calcular_angulo(self):
        ponto_x, ponto_y = self.caminho[self.ponto_atual]
        x_diferenca = ponto_x - self.x
        y_diferenca = ponto_y - self.y

        if y_diferenca == 0:
            angulo_desejado = math.pi / 2
        else:
            angulo_desejado = math.atan(x_diferenca / y_diferenca)

        if ponto_y > self.y:
            angulo_desejado += math.pi

        diferenca_angulo = self.angulo - math.degrees(angulo_desejado)
        if diferenca_angulo >= 180:
            diferenca_angulo -= 360

        if diferenca_angulo > 0:
            self.angulo -= min(self.rotacao_vel, abs(diferenca_angulo))
        else:
            self.angulo += min(self.rotacao_vel, abs(diferenca_angulo))

    def update_caminho_ponto(self):
        ponto = self.caminho[self.ponto_atual]
        rect = pygame.Rect(
            self.x, self.y, self.img.get_width(), self.img.get_height())
        if rect.collidepoint(*ponto):
            self.ponto_atual += 1

    def move(self):
        if self.ponto_atual >= len(self.caminho):
            return

        self.calcular_angulo()
        self.update_caminho_ponto()
        super().move()

    def prox_level(self, level):
        self.reset()
        self.vel = self.max_vel + (level - 1) * 0.2
        self.ponto_atual = 0


def desenho(janela, images, player_car, computer_car, game_info):
    for img, pos in images:
        janela.blit(img, pos)

    level_text = fonte.render(
        f"Level {game_info.level}", 1, (255, 255, 255))
    janela.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))

    time_text = fonte.render(
        f"Time: {game_info.tempo_level()}s", 1, (255, 255, 255))
    janela.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))

    vel_text = fonte.render(
        f"Vel: {round(player_car.vel, 1)}px/s", 1, (255, 255, 255))
    janela.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))

    player_car.desenho(janela)
    computer_car.desenho(janela)
    pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    movimento = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        movimento = True
        player_car.mover_frente()
    if keys[pygame.K_s]:
        movimento = True
        player_car.mover_tras()

    if not movimento:
        player_car.reduce_speed()


def controle_collision(player_car, computer_car, game_info):
    if player_car.collide(borda_MASK) != None:
        player_car.bounce()

    computer_chegada_poi_collide = computer_car.collide(
        chegada_MASK, *chegada_posicao)
    if computer_chegada_poi_collide != None:
        text_center(janela, fonte, "Você perdeu!")
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()

    player_chegada_poi_collide = player_car.collide(
        chegada_MASK, *chegada_posicao)
    if player_chegada_poi_collide != None:
        if player_chegada_poi_collide[1] == 0:
            player_car.bounce()
        else:
            game_info.prox_level()
            player_car.reset()
            computer_car.prox_level(game_info.level)


run = True
clock = pygame.time.Clock()
images = [(grama, (0, 0)), (pista, (0, 0)),
          (chegada, chegada_posicao), (borda, (0, 0))]
player_car = PlayerCar(3, 4)
computer_car = ComputerCar(2, 4, caminho)
game_info = GameInfo()

while run:
    clock.tick(FPS)

    desenho(janela, images, player_car, computer_car, game_info)

    while not game_info.inicio:
        text_center(
            janela, fonte, f"precione qualquer tecla para iniciar {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.inicio_level()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    computer_car.move()

    controle_collision(player_car, computer_car, game_info)

    if game_info.game_chegada():
        text_center(janela, fonte, "Você venceu!")
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()
        computer_car.reset()


pygame.quit()