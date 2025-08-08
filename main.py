import pygame
import os

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((700, 500))
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption("Rockeiros vs Funkeiros")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

# Dados da grade
LINHAS = 5
COLUNAS = 8
TAMANHO_CELULA = 70
GRADE_X = 50
GRADE_Y = 50

#classe projetil

class Projetil:
    def __init__(self, x, y, vx=2):
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(midleft=(x, y))
        self.vx = vx

    def update(self):
        self.rect.x += self.vx  # Move o projetil

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Classe do Rockeiro
class Rockeiro:
    def __init__(self, x, y):
        imagem_original = pygame.image.load(os.path.join('assets', 'riven.png'))
        self.image = pygame.transform.scale(imagem_original, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))

        #parte de tiros
        self.projeteis = []
        self.ultimo_tiro = pygame.time.get_ticks()
        self.cooldown = 2000 

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        self.atirar()
        for proj in self.projeteis:
            proj.update()
        # Remove projéteis fora da tela
        self.projeteis = [p for p in self.projeteis if p.rect.x < 700]

    def atirar(self):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown:
            novo_proj = Projetil(self.rect.right, self.rect.centery)
            self.projeteis.append(novo_proj)
            self.ultimo_tiro = agora   


# Grade vazia (5x8)
grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]

# Desenha a grade
def desenhar_grade():
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            x = GRADE_X + coluna * TAMANHO_CELULA
            y = GRADE_Y + linha * TAMANHO_CELULA
            pygame.draw.rect(screen, PRETO, (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)

# Converte posição do mouse para linha e coluna da grade
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

    # Desenha os bonecos da grade
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            celula = grade[linha][coluna]
            if isinstance(celula, Rockeiro):
                celula.draw(screen)
                for proj in celula.projeteis:
                    proj.draw(screen)

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
                if event.button == 1:  # Botão esquerdo do mouse
                    celula = pegar_celula(event.pos)
                    if celula:
                        lin, col = celula
                        if grade[lin][col] is None:
                            x = GRADE_X + col * TAMANHO_CELULA + 5
                            y = GRADE_Y + lin * TAMANHO_CELULA + 5
                            grade[lin][col] = Rockeiro(x, y)
                            print(f"Plantou na célula: linha {lin}, coluna {col}")

        # Atualiza todos os Rockeiros
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                celula = grade[linha][coluna]
                if isinstance(celula, Rockeiro):
                    celula.update()

        draw()

    pygame.quit()

# roda
if __name__ == "__main__":
    main()
