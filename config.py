import pygame

# Configurações da tela
Tlargura = 1366
Taltura = 768

pygame.init()
screen = pygame.display.set_mode((Tlargura, Taltura))
pygame.display.set_caption("Rockeiros vs Funkeiros")

FPS = 60
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Grade
LINHAS = 5
COLUNAS = 8
TAMANHO_CELULA = 70
GRADE_X = 50
GRADE_Y = 50
