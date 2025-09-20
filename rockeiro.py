import pygame
import os
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, TLARGURA, PERSONAGEM_SIZE, PROJ_SIZE

class Projetil:
    def __init__(self, x, y, dano=10, vx=8, size=PROJ_SIZE, anim_speed=150):
        self.frames = [pygame.image.load(os.path.join('assets', 'morcego', f'{i}.png')).convert_alpha() for i in range(5)]
        if size:
            self.frames = [pygame.transform.scale(frame, size) for frame in self.frames]

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midleft=(x, y))
        self.vx = vx
        self.dano = dano
        self.anim_speed = anim_speed
        self.ultimo_frame = pygame.time.get_ticks()

    def update(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.ultimo_frame = agora
        self.rect.x += self.vx

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Rockeiro:
    def __init__(self, linha, coluna, hp=100, proj_size=PROJ_SIZE):
        self.hp = hp
        self.linha = linha
        self.coluna = coluna
        self.proj_size = proj_size

        # Frames do personagem com resize
        self.frames_idle = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'ozzy', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(7)]

        self.frames_attack = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'ozzyattack', f'atk{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(14)]

        self.frame_index = 0
        self.image = self.frames_idle[0]
        self.rect = self.image.get_rect()

        self.anim_speed = 100
        self.ultimo_frame = pygame.time.get_ticks()

        self.projeteis = []
        self.cooldown = 500
        self.ultimo_tiro = -self.cooldown
        self.atacando = False
        self.tiro_disparado = False

        self.atualizar_posicao(GRADE_X, GRADE_Y, TAMANHO_CELULA)

    def atualizar_posicao(self, grade_x, grade_y, tamanho_celula):
        x = grade_x + self.coluna * tamanho_celula + 5
        y = grade_y + self.linha * tamanho_celula + 5
        self.rect.topleft = (x, y)

    def animar(self):
        frames = self.frames_attack if self.atacando else self.frames_idle
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_frame > self.anim_speed:
            self.frame_index += 1

            if self.atacando:
                meio = len(frames) // 2
                if self.frame_index == meio and not self.tiro_disparado:
                    self.projeteis.append(Projetil(self.rect.right, self.rect.centery, dano=10, size=self.proj_size))
                    self.ultimo_tiro = agora
                    self.tiro_disparado = True

                if self.frame_index >= len(frames):
                    self.frame_index = 0
                    self.atacando = False
                    self.tiro_disparado = False

            if not self.atacando and self.frame_index >= len(frames):
                self.frame_index = 0

            self.image = frames[self.frame_index]
            self.ultimo_frame = agora

    def atirar(self, funkeiros):
        if not funkeiros:
            self.atacando = False
            self.tiro_disparado = False
            return

        # Verifica inimigos normais ou Boss na linha
        tem_inimigo = any(
            (hasattr(f, "linha") and f.linha == self.linha) or
            (hasattr(f, "boss") and self.linha in getattr(f, "linhas_ocupadas", range(5)))
            for f in funkeiros
        )

        agora = pygame.time.get_ticks()
        if tem_inimigo and (agora - self.ultimo_tiro >= self.cooldown) and not self.atacando:
            self.atacando = True
            self.frame_index = 0
            self.tiro_disparado = False

    def update(self, funkeiros=None):
        self.atirar(funkeiros)
        self.animar()
        for proj in self.projeteis:
            proj.update()
        screen = pygame.display.get_surface()
        largura = screen.get_width() if screen else TLARGURA
        self.projeteis = [p for p in self.projeteis if p.rect.x < largura]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for proj in self.projeteis:
            proj.draw(surface)
