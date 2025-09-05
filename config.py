import pygame

# Configurações da tela
TLARGURA = 1366
TALTURA = 768

pygame.init()
screen = pygame.display.set_mode((TLARGURA, TALTURA))
pygame.display.set_caption("Rockeiros vs Funkeiros")

FPS = 60
clock = pygame.time.Clock()

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Grade
LINHAS = 5
COLUNAS = 12
TAMANHO_CELULA = 80
GRADE_X = 50
GRADE_Y = 50
OFFSET_X = -150
OFFSET_Y = 150
