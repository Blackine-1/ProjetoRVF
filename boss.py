import pygame
from config import TLARGURA, LINHAS, TAMANHO_CELULA, GRADE_Y

class Boss:
    def __init__(self, hp=1500, velocidade=0.6, dano=50, linhas=5, tamanho_celula=TAMANHO_CELULA):
        self.hp = hp
        self.max_hp = hp
        self.velocidade = velocidade
        self.dano = dano
        self.vivo = True
        self.boss = True  # identifica como boss
        self.linhas_ocupadas = list(range(linhas))  # todas as linhas da grade

        self.tamanho_celula = tamanho_celula
        self.largura = tamanho_celula
        self.altura = tamanho_celula * linhas

        # Começa visível à direita da tela
        self.rect = pygame.Rect(TLARGURA - 150, GRADE_Y, self.largura, self.altura)

    def update(self, grade):
        if not self.vivo:
            return

        # Move para a esquerda
        self.rect.x -= self.velocidade

        # Dano às plantas em todas as linhas que ele atravessa
        for lin in range(len(grade)):
            for col in range(len(grade[0])):
                celula_x = 100 + col * self.tamanho_celula
                celula_y = GRADE_Y + lin * self.tamanho_celula
                celula_rect = pygame.Rect(celula_x, celula_y, self.tamanho_celula, self.tamanho_celula)
                if self.rect.colliderect(celula_rect) and grade[lin][col]:
                    grade[lin][col].hp -= self.dano * 0.05

    def draw(self, screen):
        if not self.vivo:
            return

        # Corpo do boss (retângulo vermelho)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

        # Barra de vida
        barra_largura = self.rect.width
        barra_altura = 10
        vida_ratio = self.hp / self.max_hp
        vida_largura = int(barra_largura * vida_ratio)
        barra_vida_rect = pygame.Rect(self.rect.x, self.rect.y - 15, vida_largura, barra_altura)
        pygame.draw.rect(screen, (0, 255, 0), barra_vida_rect)  # barra verde
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x, self.rect.y - 15, barra_largura, barra_altura), 2)  # contorno
