import pygame
import os
import config  # importa o módulo inteiro para evitar import circular

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
        self.image_original = pygame.image.load(os.path.join('assets', 'ozzy', '0.png'))
        self.image = None
        self.rect = None
        self.projeteis = []
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cooldown = 500
        self.atualizar_posicao()

    def atualizar_posicao(self):
        x = config.GRADE_X + self.coluna * config.TAMANHO_CELULA + 5
        y = config.GRADE_Y + self.linha * config.TAMANHO_CELULA + 5
        self.image = pygame.transform.scale(self.image_original, (config.TAMANHO_CELULA - 10, config.TAMANHO_CELULA - 10))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.atirar()
        for proj in self.projeteis:
            proj.update()

        largura_tela = config.screen.get_width()
        self.projeteis = [p for p in self.projeteis if p.rect.x < largura_tela]

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown:
            novo_proj = Projetil(self.rect.right, self.rect.centery)
            self.projeteis.append(novo_proj)
            self.ultimo_tiro = agora
