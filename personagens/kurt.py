import pygame, os
from config import PERSONAGEM_SIZE
from core.base_atirador import AtiradorBase

class RockeiroKurt(AtiradorBase):
    def __init__(self, linha, coluna):
        idle = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'kurt', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(4)]

        attack = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'kurtattack', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(3)]

        proj_frames = [pygame.image.load(os.path.join('assets', 'kurtbullet.png')).convert_alpha()]

        proj_config = {
            "frames": proj_frames,
            "dano": 25,
            "vx": 6,
            "anim_speed": 200
        }

        super().__init__(linha, coluna, hp=100,
                         idle_frames=idle, attack_frames=attack,
                         cooldown=800, anim_speed=200,
                         proj_config=proj_config,
                         dispara_no_meio=True)
