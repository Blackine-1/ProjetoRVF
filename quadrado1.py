import pygame
import os
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, TLARGURA, PERSONAGEM_SIZE

class quadrado1:
    class Projetil:
        def __init__(self, x, y, dano=10, vx=6):
            # Carregar frames do projetil (não redimensiona)
            self.frames = [pygame.image.load(os.path.join('assets', 'axlattack', f'{i}.png')).convert_alpha() for i in range(2)]
            self.frame_index = 0
            self.image = self.frames[self.frame_index]
            self.rect = self.image.get_rect(midleft=(x, y))
            self.vx = vx
            self.dano = dano
            self.ultimo_frame = pygame.time.get_ticks()
            self.anim_speed = 150

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

        # Frames idle (aplicando resize)
        self.frames_idle = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'axlrose', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(1)]

        # Frames de ataque (aplicando resize)
        attack_path = os.path.join('assets', 'axlT')
        if os.path.exists(attack_path):
            self.frames_attack = [pygame.transform.scale(
                pygame.image.load(os.path.join(attack_path, f'{i}.png')).convert_alpha(),
                PERSONAGEM_SIZE
            ) for i in range(2)]
        else:
            self.frames_attack = self.frames_idle

        self.atacando = False
        self.frame_index = 0
        self.image = self.frames_idle[0]
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
        frames = self.frames_attack if self.atacando else self.frames_idle
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.image = frames[self.frame_index]
            self.ultimo_frame = agora

    def atirar(self, funkeiros):
        if not funkeiros:
            self.atacando = False
            return

        # Verifica inimigos na linha (funkeiros normais ou boss)
        tem_inimigo = any(
            (hasattr(f, "linha") and f.linha == self.linha) or  # inimigo normal
            (hasattr(f, "boss") and self.linha in getattr(f, "linhas_ocupadas", range(5)))  # boss
            for f in funkeiros
        )
        self.atacando = tem_inimigo

        if not tem_inimigo:
            return

        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown:
            self.projeteis.append(self.Projetil(self.rect.right, self.rect.centery))
            self.ultimo_tiro = agora

    def update(self, funkeiros=None):
        self.animar()
        self.atirar(funkeiros)
        for proj in self.projeteis:
            proj.update()
        screen = pygame.display.get_surface()
        largura = screen.get_width() if screen else TLARGURA
        self.projeteis = [p for p in self.projeteis if p.rect.x < largura]

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for proj in self.projeteis:
            proj.draw(surface)
