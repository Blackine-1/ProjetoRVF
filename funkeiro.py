import pygame
import os
from config import GRADE_X, GRADE_Y, TAMANHO_CELULA, COLUNAS, PERSONAGEM_SIZE

class Funkeiro:
    def __init__(self, linha, hp=50, velocidade=10, dano=10):
        self.linha = linha
        self.hp = hp
        self.velocidade = velocidade
        self.dano = dano
        self.vivo = True

        # Posição inicial (entra pelo lado direito da tela)
        x = GRADE_X + (COLUNAS - 1) * TAMANHO_CELULA + 5
        y = GRADE_Y + linha * TAMANHO_CELULA - 3

        # Frames de andar e atacar (aplicando resize)
        self.frames_andar = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "mcb", f"{i}.png")).convert_alpha(),
                PERSONAGEM_SIZE
            ) for i in range(3)
        ]
        self.frames_atacar = [
            pygame.transform.scale(
                pygame.image.load(os.path.join("assets", "mcbattack", f"{i}.png")).convert_alpha(),
                PERSONAGEM_SIZE
            ) for i in range(4)
        ]

        # Controle de animação
        self.anim_speed = 150  # tempo entre frames (ms)
        self.ultimo_frame = pygame.time.get_ticks()
        self.frame_index = 0
        self.image = self.frames_andar[self.frame_index]

        # Rect do personagem
        self.rect = self.image.get_rect(topleft=(x, y))

        # Ataque
        self.atacando = False
        self.cooldown_ataque = 500
        self.ultimo_ataque = 0

    def animar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_frame > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % (len(self.frames_atacar) if self.atacando else len(self.frames_andar))
            self.image = (self.frames_atacar if self.atacando else self.frames_andar)[self.frame_index]
            self.ultimo_frame = agora

    def update(self, grade):
        self.animar()

        # Se já está atacando, não se move
        if self.atacando:
            agora = pygame.time.get_ticks()
            if agora - self.ultimo_ataque >= self.cooldown_ataque:
                col = (self.rect.x - 5 - GRADE_X) // TAMANHO_CELULA
                if 0 <= col < COLUNAS and grade[self.linha][col]:
                    grade[self.linha][col].hp -= self.dano
                    print(f"Funkeiro atacou {grade[self.linha][col]} - HP: {grade[self.linha][col].hp}")
                    if grade[self.linha][col].hp <= 0:
                        grade[self.linha][col] = None
                        self.atacando = False
                else:
                    self.atacando = False
                self.ultimo_ataque = agora
            return

        # Se não está atacando, anda
        self.rect.x -= self.velocidade

        # Verifica colisão com defensor
        col = (self.rect.x - 5 - GRADE_X) // TAMANHO_CELULA
        if 0 <= col < COLUNAS and grade[self.linha][col]:
            self.atacando = True
            self.frame_index = 0  # reinicia animação de ataque

        # Saiu da tela
        if self.rect.right < 0:
            self.vivo = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
