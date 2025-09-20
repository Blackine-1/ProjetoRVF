import pygame, os
from config import PERSONAGEM_SIZE, PROJ_SIZE
from core.base_atirador import AtiradorBase

class RockeiroOzzy(AtiradorBase):
    def __init__(self, linha, coluna):
        idle = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'ozzy', f'{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(7)]

        attack = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'ozzyattack', f'atk{i}.png')).convert_alpha(),
            PERSONAGEM_SIZE
        ) for i in range(14)]

        proj_frames = [pygame.image.load(os.path.join('assets', 'morcego', f'{i}.png')).convert_alpha()
                       for i in range(5)]

        proj_config = {
            "frames": proj_frames,
            "dano": 10,
            "vx": 8,
            "anim_speed": 150,
            "size": PROJ_SIZE
        }

        super().__init__(linha, coluna, hp=100,
                         idle_frames=idle, attack_frames=attack,
                         cooldown=500, anim_speed=100,
                         proj_config=proj_config,
                         dispara_no_meio=True)
