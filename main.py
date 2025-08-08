import pygame
import os

pygame.init()
screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Rockeiros vs Funkeiros")

# Carrega a imagem do boneco
boneco_flat = pygame.image.load(os.path.join('assets', 'riven.png'))
boneco = pygame.transform.scale(boneco_flat, (60, 60))

# Dados da grade
LINHAS = 5
COLUNAS = 8
TAMANHO_CELULA = 70
GRADE_X = 50
GRADE_Y = 50

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Grade vazia (para futuras plantas)
grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]

# Desenha a grade
def desenhar_grade():
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = GRADE_X + coluna * TAMANHO_CELULA
            y = GRADE_Y + linha * TAMANHO_CELULA
            pygame.draw.rect(screen, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)

# Transforma posição do mouse em coordenadas da grade
def pegar_celula(pos):
    mx, my = pos
    col = (mx - GRADE_X) // TAMANHO_CELULA
    lin = (my - GRADE_Y) // TAMANHO_CELULA
    if 0 <= col < COLUNAS and 0 <= lin < LINHAS:
        return lin, col
    return None

# Desenha tudo
def draw():
    screen.fill(BRANCO)
    desenhar_grade()

    # Desenha bonecos plantados
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if grade[linha][coluna] == "boneco":
                x = GRADE_X + coluna * TAMANHO_CELULA + 5
                y = GRADE_Y + linha * TAMANHO_CELULA + 5
                screen.blit(boneco, (x, y))

    pygame.display.flip()

# Loop principal
def main():
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clique esquerdo
                    celula = pegar_celula(event.pos)
                    if celula:
                        lin, col = celula
                        # Só planta se a célula estiver vazia
                        if grade[lin][col] is None:
                            grade[lin][col] = "boneco"
                            print(f"Plantou na célula: linha {lin}, coluna {col}")

        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
