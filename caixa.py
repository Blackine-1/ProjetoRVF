import pygame
import os
from config import *

class Caixa:
    def __init__(self, linha, coluna, hp=3000, cooldown_energia=5000):
        self.linha = linha
        self.coluna = coluna
        self.hp = hp
        self.vivo = True

        # animação idle (pasta: assets/caixa)
        pasta_idle = os.path.join("assets", "caixa")
        self.frames_idle = [
            pygame.transform.scale(
                pygame.image.load(os.path.join(pasta_idle, img)).convert_alpha(),
                (TAMANHO_CELULA, TAMANHO_CELULA)
            )
            for img in sorted(os.listdir(pasta_idle)) if img.endswith(".png")
        ]

        # animação
        self.frame_index = 0
        self.image = self.frames_idle[0]
        self.anim_speed = 300
        self.ultimo_frame = pygame.time.get_ticks()

        # posição na grade
        self.rect = self.image.get_rect()
        self.rect.topleft = (
            GRADE_X + coluna * TAMANHO_CELULA,
            GRADE_Y + linha * TAMANHO_CELULA
        )

        # energia
        self.cooldown_energia = cooldown_energia
        self.ultimo_gerado = pygame.time.get_ticks()

    def animar(self):
        agora = pygame.time.get_ticks()

        # só anima o idle
        if agora - self.ultimo_frame >= self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames_idle)
            self.image = self.frames_idle[self.frame_index]
            self.ultimo_frame = agora

    def update(self, funkeiros, recursos):
        if self.hp <= 0:
            self.vivo = False
            return

        self.animar()

        # gera energia
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_gerado >= self.cooldown_energia:
            recursos[0] += 25
            self.ultimo_gerado = agora
            print("Caixa gerou energia! Total:", recursos[0])

    def draw(self, screen):
        if self.vivo:
            screen.blit(self.image, self.rect)
