# personagens/ozzy.py
import pygame, os
from core.base_atirador import AtiradorBase
from core.projetil import ProjetilBase
from config import PERSONAGEM_SIZE, PROJ_SIZE

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

        proj_frames = [pygame.transform.scale(
            pygame.image.load(os.path.join('assets', 'morcego', f'{i}.png')).convert_alpha(),
            PROJ_SIZE
        ) for i in range(5)]

        proj_config = {
            "frames": proj_frames,
            "dano": 20,        # um pouco mais forte
            "vx": 7,           # tiro mais lento que antes
            "anim_speed": 150
        }

        # Ativando tiro duplo
        self.tiros_duplos = True

        super().__init__(linha, coluna, hp=120,
                         idle_frames=idle, attack_frames=attack,
                         cooldown=700, anim_speed=100,
                         proj_config=proj_config,
                         dispara_no_meio=True)

    def criar_projetil(self, x=None, y=None):
        # Usa o centro do personagem se x ou y não forem passados
        x = x or self.rect.right
        y = y or self.rect.centery

        proj1 = ProjetilBase(x, y - 5,
                             self.proj_config["vx"],
                             self.proj_config["dano"],
                             self.proj_config["frames"],
                             self.proj_config["anim_speed"])
        if getattr(self, "tiros_duplos", False):
            proj2 = ProjetilBase(x, y + 5,
                                 self.proj_config["vx"],
                                 self.proj_config["dano"],
                                 self.proj_config["frames"],
                                 self.proj_config["anim_speed"])
            return [proj1, proj2]

        return [proj1]
