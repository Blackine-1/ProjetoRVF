import pygame
import os
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, screen

class Projetil:
    def __init__(self, x, y, vx=4):
        self.image = pygame.image.load(os.path.join('assets', 'morcego', '0.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 20))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.vx = vx

    def update(self):
        self.rect.x += self.vx

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Rockeiro:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.frames = [
            pygame.image.load(os.path.join('assets', 'ozzy', '0.png')).convert_alpha(),
            pygame.image.load(os.path.join('assets', 'ozzy', '1.png')).convert_alpha(),
            pygame.image.load(os.path.join('assets', 'ozzy', '2.png')).convert_alpha(),
            pygame.image.load(os.path.join('assets', 'ozzy', '3.png')).convert_alpha(),
            pygame.image.load(os.path.join('assets', 'ozzy', '4.png')).convert_alpha(),
            pygame.image.load(os.path.join('assets', 'ozzy', '5.png')).convert_alpha(),
            pygame.image.load(os.path.join('assets', 'ozzy', '6.png')).convert_alpha(),
        ]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.ultimo_frame = pygame.time.get_ticks()
        self.anim_speed = 200
        self.projeteis = []
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cooldown = 500
        self.atualizar_posicao(GRADE_X, GRADE_Y, TAMANHO_CELULA)

    def atualizar_posicao(self, grade_x, grade_y, tamanho_celula):
        x = grade_x + self.coluna * tamanho_celula + 5
        y = grade_y + self.linha * tamanho_celula + 5
        self.rect.topleft = (x, y)

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.ultimo_frame = agora

    def update(self):
        self.animar()
        self.atirar()
        for proj in self.projeteis:
            proj.update()
        largura_tela = screen.get_width()
        self.projeteis = [p for p in self.projeteis if p.rect.x < largura_tela]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for proj in self.projeteis:
            proj.draw(surface)

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown:
            novo_proj = Projetil(self.rect.right, self.rect.centery)
            self.projeteis.append(novo_proj)
            self.ultimo_tiro = agora
