# core/projetil_base.py
import pygame

class ProjetilBase:
    def __init__(self, x, y, vx, dano, frames, anim_speed=150):
        self.rect = frames[0].get_rect(center=(x, y))
        self.vx = vx
        self.dano = dano
        self.frames = frames
        self.anim_speed = anim_speed
        self.frame_index = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.image = self.frames[self.frame_index]
        self.vivo = True

    def update(self, lista_inimigos=None):
        # Movimento horizontal
        self.rect.x += self.vx

        # Verifica colisão com inimigos, se passado
        if lista_inimigos:
            for inimigo in lista_inimigos:
                if inimigo.vivo and self.rect.colliderect(inimigo.rect):
                    inimigo.hp -= self.dano
                    self.vivo = False
                    break

        # Animação
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.ultimo_frame = agora

    def draw(self, surface):
        surface.blit(self.image, self.rect)
