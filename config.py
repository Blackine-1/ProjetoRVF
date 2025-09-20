# config.py
# Apenas constantes de configuração, sem inicializar o pygame nem criar a tela aqui.

import pygame
import os
TLARGURA = 1366
TALTURA = 768

FPS = 100
volume = 0.01


# Grade
LINHAS = 5
COLUNAS = 12
TAMANHO_CELULA = 100
PERSONAGEM_SIZE = (TAMANHO_CELULA, TAMANHO_CELULA)
PROJ_SIZE = (int(TAMANHO_CELULA * 0.3), int(TAMANHO_CELULA * 0.3)) 
GRADE_X = 100
GRADE_Y = 200


# Cores (opcional)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# tela
screen = pygame.display.set_mode((TLARGURA, TALTURA))
pygame.display.set_caption("Jogo de Rockeiro")


# --- Carrega mapa ---
mapa_img = pygame.image.load(os.path.join('assets', 'mapa', 'mapa.jfif')).convert()
mapa_img = pygame.transform.scale(mapa_img, (TLARGURA, TALTURA))  # ajusta à tela

def desenhar_mapa():
    """Desenha o mapa como fundo da tela."""
    screen.blit(mapa_img, (0, 0))