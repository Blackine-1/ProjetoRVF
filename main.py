from common import *

clock = pygame.time.Clock()
grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]

def atualizar_grade_para_tela():
    global TAMANHO_CELULA, GRADE_X, GRADE_Y
    largura_tela, altura_tela = screen.get_size()

    largura_grade = largura_tela
    altura_grade = altura_tela

    TAMANHO_CELULA = int(min(largura_grade / COLUNAS, altura_grade / LINHAS))

    largura_total = TAMANHO_CELULA * COLUNAS
    altura_total = TAMANHO_CELULA * LINHAS
    GRADE_X = (largura_tela - largura_total) // 2
    GRADE_Y = (altura_tela - altura_total) // 2

def desenhar_grade():
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = GRADE_X + coluna * TAMANHO_CELULA
            y = GRADE_Y + linha * TAMANHO_CELULA
            pygame.draw.rect(screen, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)

def pegar_celula(pos):
    mx, my = pos
    col = (mx - GRADE_X) // TAMANHO_CELULA
    lin = (my - GRADE_Y) // TAMANHO_CELULA
    if 0 <= col < COLUNAS and 0 <= lin < LINHAS:
        return lin, col
    return None

def draw():
    screen.fill(BRANCO)
    desenhar_grade()

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            celula = grade[linha][coluna]
            if isinstance(celula, Rockeiro):
                celula.draw(screen)

    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            celula = grade[linha][coluna]
            if isinstance(celula, Rockeiro):
                for proj in celula.projeteis:
                    proj.draw(screen)

    pygame.display.flip()

def main():
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                celula = pegar_celula(event.pos)
                if celula:
                    lin, col = celula
                    if grade[lin][col] is None:
                        grade[lin][col] = Rockeiro(lin, col)
                        print(f"Plantou na célula: linha {lin}, coluna {col}")

        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                celula = grade[linha][coluna]
                if isinstance(celula, Rockeiro):
                    celula.update()

        draw()

    pygame.quit()

if __name__ == "__main__":
    main()
