import pygame
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, TLARGURA
from core.projetil import ProjetilBase

class AtiradorBase:
    def __init__(self, linha, coluna, hp, idle_frames, attack_frames,
                 cooldown=500, anim_speed=200, proj_config=None,
                 dispara_no_meio=False):
        self.hp = hp
        self.linha = linha
        self.coluna = coluna

        self.frames_idle = idle_frames
        self.frames_attack = attack_frames if attack_frames else idle_frames

        self.frame_index = 0
        self.image = self.frames_idle[0]
        self.rect = self.image.get_rect()

        self.anim_speed = anim_speed
        self.ultimo_frame = pygame.time.get_ticks()

        self.projeteis = []
        self.cooldown = cooldown
        self.ultimo_tiro = -cooldown

        self.atacando = False
        self.tiro_disparado = False
        self.dispara_no_meio = dispara_no_meio
        self.proj_config = proj_config or {}

        self.atualizar_posicao(GRADE_X, GRADE_Y, TAMANHO_CELULA)

    def atualizar_posicao(self, grade_x, grade_y, tamanho_celula):
        x = grade_x + self.coluna * tamanho_celula + 5
        y = grade_y + self.linha * tamanho_celula + 5
        self.rect.topleft = (x, y)

    def criar_projetil(self):
        return ProjetilBase(self.rect.right, self.rect.centery, **self.proj_config)

    def animar(self):
        frames = self.frames_attack if self.atacando else self.frames_idle
        agora = pygame.time.get_ticks()

        if agora - self.ultimo_frame > self.anim_speed:
            self.frame_index += 1

            if self.atacando:
                meio = len(frames) // 2
                deve_disparar = (not self.dispara_no_meio) or \
                                (self.frame_index == meio and not self.tiro_disparado)

                if deve_disparar:
                    self.projeteis.append(self.criar_projetil())
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
