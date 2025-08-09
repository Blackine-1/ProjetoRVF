import pygame
import os

# Inicialização
pygame.init()
screen = pygame.display.set_mode((700, 500), pygame.RESIZABLE)
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Rockeiros vs Funkeiros")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Configuração da grade
LINHAS = 5
COLUNAS = 8

# Variáveis que mudam com o tamanho da tela
TAMANHO_CELULA = 70
GRADE_X = 50
GRADE_Y = 50

def atualizar_grade_para_tela():
    global TAMANHO_CELULA, GRADE_X, GRADE_Y
    largura_tela, altura_tela = screen.get_size()

    # 60% da largura/altura disponível
    largura_grade = largura_tela * 0.6
    altura_grade = altura_tela * 0.6

    # Calcula tamanho de célula baseado no menor espaço disponível
    TAMANHO_CELULA = int(min(largura_grade / COLUNAS, altura_grade / LINHAS))

    # Centraliza a grade
    largura_total = TAMANHO_CELULA * COLUNAS
    altura_total = TAMANHO_CELULA * LINHAS
    GRADE_X = (largura_tela - largura_total) // 2
    GRADE_Y = (altura_tela - altura_total) // 2

# Classe Projetil
class Projetil:
    def __init__(self, x, y, vx=4):
        self.image = pygame.Surface((10, 5))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.vx = vx

    def update(self):
        self.rect.x += self.vx

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Classe Rockeiro
class Rockeiro:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        imagem_original = pygame.image.load(os.path.join('assets', 'riven.png'))
        self.image_original = imagem_original
        self.image = None
        self.rect = None
        self.projeteis = []
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cooldown = 500
        self.atualizar_posicao()

    def atualizar_posicao(self):
        x = GRADE_X + self.coluna * TAMANHO_CELULA + 5
        y = GRADE_Y + self.linha * TAMANHO_CELULA + 5
        self.image = pygame.transform.scale(self.image_original, (TAMANHO_CELULA - 10, TAMANHO_CELULA - 10))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.atirar()
        for proj in self.projeteis:
            proj.update()
        largura_tela = screen.get_width()
        self.projeteis = [p for p in self.projeteis if p.rect.x < largura_tela]

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown:
            novo_proj = Projetil(self.rect.right, self.rect.centery)
            self.projeteis.append(novo_proj)
            self.ultimo_tiro = agora

# Grade inicial
grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]
atualizar_grade_para_tela()

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

            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                atualizar_grade_para_tela()
                # Reposiciona todos os bonecos
                for linha in range(LINHAS):
                    for coluna in range(COLUNAS):
                        if isinstance(grade[linha][coluna], Rockeiro):
                            grade[linha][coluna].atualizar_posicao()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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
