# core/base_atirador.py
import pygame
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, TLARGURA
from core.projetil import ProjetilBase

class AtiradorBase:
    def __init__(self, linha, coluna, hp, idle_frames, attack_frames,
                 cooldown=500, anim_speed=200, proj_config=None,
                 dispara_no_meio=False, tiros_duplos=False):
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
        self.tiros_duplos = tiros_duplos
        self.proj_config = proj_config or {}

        self.atualizar_posicao(GRADE_X, GRADE_Y, TAMANHO_CELULA)

    def atualizar_posicao(self, grade_x, grade_y, tamanho_celula):
        x = grade_x + self.coluna * tamanho_celula + 5
        y = grade_y + self.linha * tamanho_celula + 5
        self.rect.topleft = (x, y)

    def criar_projetil(self, x=None, y=None):
        # x e y podem ser passados ou usa o centro do personagem
        x = x or self.rect.right
        y = y or self.rect.centery
        proj = ProjetilBase(x, y,
                            self.proj_config.get("vx", 10),
                            self.proj_config.get("dano", 10),
                            self.proj_config.get("frames", []),
                            self.proj_config.get("anim_speed", 100))
        if self.tiros_duplos:
            proj1 = ProjetilBase(x, y - 5,
                                 self.proj_config.get("vx", 10),
                                 self.proj_config.get("dano", 10),
                                 self.proj_config.get("frames", []),
                                 self.proj_config.get("anim_speed", 100))
            proj2 = ProjetilBase(x, y + 5,
                                 self.proj_config.get("vx", 10),
                                 self.proj_config.get("dano", 10),
                                 self.proj_config.get("frames", []),
                                 self.proj_config.get("anim_speed", 100))
            return [proj1, proj2]
        return [proj]

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
                    novos_proj = self.criar_projetil()
                    self.projeteis.extend(novos_proj)
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
