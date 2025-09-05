import pygame
import sys
import os

from rockeiro import Rockeiro
from quadrado1 import Quadrado1
from Quadrado2 import quadrado2
from config import *

pygame.init()

# inicialização da tela
screen = pygame.display.set_mode((TLARGURA, TALTURA))
pygame.display.set_caption("Jogo de Rockeiro")

# fonte
fonte = pygame.font.SysFont(None, 30)

# --------------------------
# Função para carregar a seringa
def seringa():
    seringa_img = pygame.image.load(os.path.join('assets', 'seringa.png')).convert_alpha()
    seringa_img = pygame.transform.scale(seringa_img, (60, 60))  # menor tamanho
    seringa_caixa = seringa_img.get_rect(topleft=(1300, 10))  # canto superior direito
    return seringa_caixa, seringa_img

seringa_caixa, seringa_img = seringa()
# --------------------------

# cria grade
grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]

# lista de personagens disponíveis
personagens_disponiveis = {
    "rockeiro": Rockeiro,
    "Axelrose": Quadrado1,
    "quadrado2": quadrado2,
}

personagem_selecionado = "rockeiro"
pa_mode = False  # modo pá/remover

# botões para seleção
botoes = {
    "rockeiro": pygame.Rect(50, TALTURA - 90, 120, 50),
    "Axelrose": pygame.Rect(200, TALTURA - 90, 120, 50),
    "quadrado2": pygame.Rect(350, TALTURA - 90, 120, 50),
}

# -------------------------
def desenhar_botoes():
    for nome, rect in botoes.items():
        cor = (0, 255, 0) if nome == personagem_selecionado else (150, 150, 150)
        pygame.draw.rect(screen, cor, rect)
        texto = fonte.render(nome, True, (0, 0, 0))
        screen.blit(texto, (rect.x + 10, rect.y + 15))

def desenhar_grade():
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            x = GRADE_X + col * TAMANHO_CELULA
            y = GRADE_Y + lin * TAMANHO_CELULA
            pygame.draw.rect(screen, (200, 200, 200), (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)
            if grade[lin][col]:
                grade[lin][col].draw(screen)

def main():
    global personagem_selecionado, pa_mode
    clock = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos

                # clique nos botões
                for nome, rect in botoes.items():
                    if rect.collidepoint(x, y):
                        personagem_selecionado = nome
                        pa_mode = False  # cancela pá ao selecionar personagem
                        print(f"Selecionado: {nome}")

                # clique na seringa -> alterna modo pá
                if seringa_caixa.collidepoint(x, y):
                    pa_mode = not pa_mode
                    personagem_selecionado = None
                    print(f"Modo pá {'ativado' if pa_mode else 'desativado'}")

                # clique na grade
                col = (x - GRADE_X) // TAMANHO_CELULA
                lin = (y - GRADE_Y) // TAMANHO_CELULA
                if 0 <= lin < LINHAS and 0 <= col < COLUNAS:
                    if pa_mode:
                        if grade[lin][col]:
                            grade[lin][col] = None
                            print(f"Personagem removido em linha {lin}, coluna {col}")
                    else:
                        if grade[lin][col] is None and personagem_selecionado:
                            grade[lin][col] = personagens_disponiveis[personagem_selecionado](lin, col)

        # --- Desenho ---
        screen.fill((60, 60, 60))
        desenhar_grade()
        desenhar_botoes()

        # desenha a seringa
        screen.blit(seringa_img, seringa_caixa)

        # destaque se modo pá ativo
        if pa_mode:
            pygame.draw.rect(screen, (0, 255, 0), seringa_caixa, 3)

        # atualiza personagens
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if grade[lin][col]:
                    grade[lin][col].update()
                    grade[lin][col].draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()