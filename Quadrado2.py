import pygame
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, screen

class quadrado2:
    class Projetil:
        def __init__(self, x, y, vx=8):
            self.image = pygame.Surface((20, 20))
            self.image.fill((0, 0, 100))
            self.rect = self.image.get_rect(midleft=(x, y))
            self.vx = vx

        def update(self):
            self.rect.x += self.vx

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.image = pygame.Surface((TAMANHO_CELULA - 15, TAMANHO_CELULA - 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.projeteis = []
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cooldown = 400
        self.atualizar_posicao(GRADE_X, GRADE_Y, TAMANHO_CELULA)

    def atualizar_posicao(self, grade_x, grade_y, tamanho_celula):
        x = grade_x + self.coluna * tamanho_celula + 5
        y = grade_y + self.linha * tamanho_celula + 5
        self.rect.topleft = (x, y)

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown:
            self.projeteis.append(self.Projetil(self.rect.right, self.rect.centery))
            self.ultimo_tiro = agora

    def update(self):
        self.atirar()
        for proj in self.projeteis:
            proj.update()
        self.projeteis = [p for p in self.projeteis if p.rect.x < screen.get_width()]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for proj in self.projeteis:
            proj.draw(surface)
