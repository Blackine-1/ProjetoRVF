import pygame

class ProjetilBase:
    def __init__(self, x, y, frames, dano=10, vx=6, anim_speed=150, size=None):
        if size:
            frames = [pygame.transform.scale(f, size) for f in frames]
        self.frames = frames
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
