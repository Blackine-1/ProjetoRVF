import pygame, os
from config import PERSONAGEM_SIZE
from core.base_atirador import AtiradorBase

class RockeiroAxl(AtiradorBase):
    def __init__(self, linha, coluna):
        idle = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'axlrose', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(1)]

        attack = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'axlT', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(2)]

        proj_frames = [pygame.image.load(os.path.join('assets', 'axlattack', f'{i}.png')).convert_alpha()
                       for i in range(2)]

        proj_config = {
            "frames": proj_frames,
            "dano": 10,
            "vx": 6,
            "anim_speed": 150
        }

        super().__init__(linha, coluna, hp=100,
                         idle_frames=idle, attack_frames=attack,
                         cooldown=500, anim_speed=200,
                         proj_config=proj_config)
