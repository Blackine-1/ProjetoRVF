import pygame
import os
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, TLARGURA, PERSONAGEM_SIZE

class quadrado2:
    class Projetil:
        def __init__(self, x, y, dano=25, vx=4, anim_speed=200):
            self.frames = [pygame.image.load(os.path.join('assets','kurtbullet.png')).convert_alpha()]
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(midleft=(x, y))
            self.vx = vx
            self.dano = dano
            self.ultimo_frame = pygame.time.get_ticks()
            self.anim_speed = anim_speed

        def update(self):
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_frame > self.anim_speed:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.image = self.frames[self.frame_index]
                self.ultimo_frame = agora
            self.rect.x += self.vx

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    def __init__(self, linha, coluna, hp=100):
        self.hp = hp
        self.linha = linha
        self.coluna = coluna

        # Frames idle
        self.frames_idle = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'kurt', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(4)]

        # Frames ataque
        attack_path = os.path.join('assets', 'kurtattack')
        if os.path.exists(attack_path):
            self.frames_attack = [pygame.transform.scale(
                pygame.image.load(os.path.join(attack_path, f'{i}.png')).convert_alpha(),
                PERSONAGEM_SIZE
            ) for i in range(3)]
        else:
            self.frames_attack = self.frames_idle

        self.atacando = False
        self.frame_index = 0
        self.image = self.frames_idle[0]
        self.rect = self.image.get_rect()

        self.ultimo_frame = pygame.time.get_ticks()
        self.anim_speed = 200

        self.projeteis = []
        self.cooldown = 1020
        self.ultimo_tiro = -self.cooldown
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
                    self.projeteis.append(self.Projetil(self.rect.right, self.rect.centery))
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

        # Verifica se há inimigos na linha ou boss cobrindo a linha
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
