import pygame
import os
import random
from config import TLARGURA, LINHAS, TAMANHO_CELULA, GRADE_Y
from funkeiro import Funkeiro
from config import *

class Boss:
    def __init__(self, hp=1500, dano=50, linhas=5, tamanho_celula=TAMANHO_CELULA):
        self.hp = hp
        self.max_hp = hp
        self.dano = dano
        self.vivo = True
        self.boss = True
        self.linhas_ocupadas = list(range(linhas))

        self.tamanho_celula = tamanho_celula
        self.largura = 100
        self.altura = 500
        self.rect = pygame.Rect(TLARGURA - 150, GRADE_Y, self.largura, self.altura)

        # Controle de spawn de minions
        self.next_spawn_threshold = self.max_hp - (self.max_hp * 0.1)

        # Controle da música do boss
        self.musica_tocando = False

        # --- Animação ---
        self.frames = []
        for i in range(8):
            img = pygame.image.load(os.path.join("assets", "boss", f"{i}.png")).convert_alpha()
            img = pygame.transform.scale(img, (self.largura, self.altura))
            self.frames.append(img)
        self.frame_index = 0
        self.anim_speed = 150
        self.last_update = pygame.time.get_ticks()
        self.image = self.frames[self.frame_index]

    def update(self, grade, lista_inimigos):
        if not self.vivo:
            return

        # Inicia música do boss se ainda não estiver tocando
        if not self.musica_tocando:
            pygame.mixer.music.stop()  # cancela qualquer música
            pygame.mixer.music.load(os.path.join("assets", "music", "bossbattle.mp3"))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)  # loop infinito
            self.musica_tocando = True

        # Animação
        agora = pygame.time.get_ticks()
        if agora - self.last_update > self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = agora

        # Spawn de zumbis com mais variedade
        if self.hp <= self.next_spawn_threshold and self.hp > 0:
            qtd = random.randint(3, 6)  # quantidade variável
            for _ in range(qtd):
                linha = random.choice(self.linhas_ocupadas)
                vida_ratio = self.hp / self.max_hp

                # Stats base
                if vida_ratio > 0.7:
                    hp, dano, velocidade = 80, 10, 1.2
                elif vida_ratio > 0.4:
                    hp, dano, velocidade = 150, 18, 1.5
                else:
                    hp, dano, velocidade = 250, 30, 1.8

                # Chance de zumbi rápido
                if random.random() < 0.3:
                    hp = max(10, hp // 2)
                    velocidade *= 1.5

                zumbi = Funkeiro(
                    linha=linha,
                    hp=hp,
                    velocidade=velocidade,
                    dano=dano
                )
                zumbi.rect.x = self.rect.x - random.randint(50, 120)
                lista_inimigos.append(zumbi)

            self.next_spawn_threshold -= self.max_hp * 0.1  # diminui threshold para próximo spawn

        # Verifica morte do boss
        if self.hp <= 0:
            self.vivo = False
            self.musica_tocando = False  # permite tocar outra música após a morte

    def spawn_zumbis(self, lista_inimigos):
        qtd = random.randint(3, 5)
        for _ in range(qtd):
            linha = random.choice(self.linhas_ocupadas)
            vida_ratio = self.hp / self.max_hp

            if vida_ratio > 0.6:
                hp, dano, velocidade = 80, 10, 1.2
            elif vida_ratio > 0.3:
                hp, dano, velocidade = 150, 18, 1.5
            else:
                hp, dano, velocidade = 250, 30, 1.8

            zumbi = Funkeiro(
                linha=linha,
                hp=hp,
                velocidade=velocidade,
                dano=dano
            )
            zumbi.rect.x = self.rect.x - random.randint(50, 120)
            lista_inimigos.append(zumbi)

    def draw(self, screen):
        if not self.vivo:
            return

        screen.blit(self.image, self.rect)

        # Barra de vida acima do boss
        barra_largura = self.rect.width
        barra_altura = 10
        vida_ratio = self.hp / self.max_hp
        vida_largura = int(barra_largura * vida_ratio)
        barra_vida_rect = pygame.Rect(self.rect.x, self.rect.y - 15, vida_largura, barra_altura)
        pygame.draw.rect(screen, (0, 255, 0), barra_vida_rect)
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x, self.rect.y - 15, barra_largura, barra_altura), 2)
