import pygame
import sys
import os
import random

# -------------------------------
# Personagens
# -------------------------------
from personagens.ozzy import RockeiroOzzy
from personagens.axl import RockeiroAxl
from personagens.kurt import RockeiroKurt
from personagens.caixa import Caixa

# -------------------------------
# Sistema de inimigos e configuração
# -------------------------------
from funkeiro import *
from config import *
from menu import *
from waves import WaveManager

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((TLARGURA, TALTURA))
pygame.display.set_caption("Jogo de Rockeiro")
fonte = pygame.font.SysFont(None, 30)

# -------------------------------
# Seringa
# -------------------------------
def seringa():
    seringa_img = pygame.image.load(os.path.join('assets', 'seringa.png')).convert_alpha()
    seringa_img = pygame.transform.scale(seringa_img, (60, 60))
    seringa_caixa = seringa_img.get_rect(topleft=(1300, 10))
    return seringa_caixa, seringa_img

seringa_caixa, seringa_img = seringa()

# -------------------------------
# Ícone da moeda
# -------------------------------
moeda_img = pygame.image.load(os.path.join("assets", "ROBG.png")).convert_alpha()
moeda_img = pygame.transform.scale(moeda_img, (300, 200))

# Custos dos personagens
custos = {
    "ozzy": 50,
    "axl": 75,
    "kurt": 100,
    "caixa": 50
}

# Dicionário com as classes
personagens_disponiveis = {
    "ozzy": RockeiroOzzy,
    "axl": RockeiroAxl,
    "kurt": RockeiroKurt,
    "caixa": lambda l, c, hp=300: Caixa(l, c, hp=hp)
}

# -------------------------------
# Botões
# -------------------------------
BSO = 760
botoes_imgs = {
    "ozzy": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "OBG.png")).convert_alpha(), (200, 200)),
             "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "OBGH.png")).convert_alpha(), (200,200))},
    "axl": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "ABG.png")).convert_alpha(), (200,200)),
             "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "ABGH.png")).convert_alpha(), (200,200))},
    "kurt": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "KBG.png")).convert_alpha(), (200,200)),
              "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "KBGH.png")).convert_alpha(), (200,200))},
    "caixa": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "CBG.png")).convert_alpha(), (200,200)),
              "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "CBGH.png")).convert_alpha(), (200,200))}
}

botoes = {
    "ozzy": {"rect": pygame.Rect(100, TALTURA - BSO, 200,150), "ativo": True},
    "axl": {"rect": pygame.Rect(300, TALTURA - BSO, 200,150), "ativo": True},
    "kurt": {"rect": pygame.Rect(500, TALTURA - BSO, 200,150), "ativo": True},
    "caixa": {"rect": pygame.Rect(700, TALTURA - BSO, 200,150), "ativo": True}
}

def desenhar_botoes():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for nome, botao in botoes.items():
        if botao["ativo"]:
            img = botoes_imgs[nome]["hover"] if botao["rect"].collidepoint(mouse_x, mouse_y) else botoes_imgs[nome]["normal"]
            screen.blit(img, botao["rect"].topleft)
            if personagem_selecionado == nome:
                pygame.draw.rect(screen, (0, 250, 0), botao["rect"], 3)
        else:
            pygame.draw.rect(screen, (100, 100, 100), botao["rect"])

def desenhar_grade():
    for lin in range(LINHAS):
        for col in range(COLUNAS - 2):
            x = GRADE_X + col*TAMANHO_CELULA
            y = GRADE_Y + lin*TAMANHO_CELULA
            pygame.draw.rect(screen, (200,200,200), (x,y,TAMANHO_CELULA,TAMANHO_CELULA),1)

# -------------------------------
# Telas de vitória e derrota
# -------------------------------
def tela_derrota():
    fonte_grande = pygame.font.SysFont(None, 100)
    texto = fonte_grande.render("VOCÊ PERDEU!", True, (250, 0, 0))
    pygame.mixer.music.load(os.path.join('assets', 'music', 'FRVFM.mp3'))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(0)

    screen.fill((0, 0, 0))
    screen.blit(texto, (TLARGURA//2 - texto.get_width()//2, TALTURA//2 - texto.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(3000)
    return "derrota"

def tela_vitoria():
    fonte_grande = pygame.font.SysFont(None, 100)
    texto = fonte_grande.render("VOCÊ VENCEU!", True, (0, 250, 0))
    pygame.mixer.music.load(os.path.join('assets', 'music', 'victory.mp3'))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(0)

    screen.fill((0, 0, 0))
    screen.blit(texto, (TLARGURA//2 - texto.get_width()//2, TALTURA//2 - texto.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(3000)
    return "vitoria"

# -------------------------------
# Função principal
# -------------------------------
def main():
    global personagem_selecionado, pa_mode, grade, recursos
    clock = pygame.time.Clock()

    # reset estado
    grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]
    recursos = [100]
    personagem_selecionado = None
    pa_mode = False
    funkeiros = []

    pygame.mixer.music.load(os.path.join('assets', 'music','RVFF1.mp3'))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    # WaveManager
    wave_manager = WaveManager()
    wave_manager.iniciar(pygame.time.get_ticks())

    while True:
        # --- eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                # seleção de personagem
                for nome, botao in botoes.items():
                    if botao["rect"].collidepoint(x, y):
                        personagem_selecionado = None if personagem_selecionado == nome else nome
                        pa_mode = False

                # seringa
                if seringa_caixa.collidepoint(x, y):
                    pa_mode = not pa_mode
                    personagem_selecionado = None

                # clique na grade
                col = (x - GRADE_X) // TAMANHO_CELULA
                lin = (y - GRADE_Y) // TAMANHO_CELULA
                if 0 <= lin < LINHAS and 0 <= col < COLUNAS:
                    if pa_mode and grade[lin][col]:
                        grade[lin][col] = None
                    elif grade[lin][col] is None and personagem_selecionado:
                        custo = custos[personagem_selecionado]
                        if recursos[0] >= custo:
                            classe = personagens_disponiveis[personagem_selecionado]
                            grade[lin][col] = classe(lin, col, hp=3000) if personagem_selecionado == "caixa" else classe(lin, col)
                            recursos[0] -= custo

        # --- spawn e controle de waves ---
        agora = pygame.time.get_ticks()
        wave_manager.spawn_inimigo(agora, LINHAS, funkeiros)
        wave_manager.verificar_wave(agora, funkeiros)

        if wave_manager.game_won:
            return tela_vitoria()

        # --- atualização dos personagens ---
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                personagem = grade[lin][col]
                if personagem:
                    if isinstance(personagem, Caixa):
                        personagem.update(funkeiros, recursos)
                    elif hasattr(personagem, "projeteis"):
                        personagem.update(funkeiros)
                    else:
                        personagem.update()

                    # colisão projétil
                    if hasattr(personagem, "projeteis"):
                        proj_para_remover = []
                        for proj in personagem.projeteis:
                            for f in funkeiros:
                                if proj.rect.colliderect(f.rect):
                                    f.hp -= proj.dano
                                    proj_para_remover.append(proj)
                                    if f.hp <= 0:
                                        f.vivo = False
                        for p in proj_para_remover:
                            if p in personagem.projeteis:
                                personagem.projeteis.remove(p)

        # --- atualização dos inimigos ---
        for f in funkeiros:
            f.update(grade)
            if f.rect.left <= 0:
                return tela_derrota()

        funkeiros = [f for f in funkeiros if f.vivo]

        # --- renderização ---
        screen.fill((60, 60, 60))
        desenhar_mapa()
        desenhar_grade()
        desenhar_botoes()
        screen.blit(seringa_img, seringa_caixa)
        if pa_mode:
            pygame.draw.rect(screen, (0, 250, 0), seringa_caixa, 3)

        # contador de recursos
        ultimo_botao_rect = botoes["caixa"]["rect"]
        contador_x = ultimo_botao_rect.right + 50
        contador_y = TALTURA - 760
        contador_img_rect = moeda_img.get_rect(topleft=(contador_x, contador_y))
        screen.blit(moeda_img, contador_img_rect)
        valor_surface = fonte.render(f"{recursos[0]}", True, (255, 255, 0))
        valor_rect = valor_surface.get_rect(center=contador_img_rect.center)
        screen.blit(valor_surface, valor_rect)

        # desenhar personagens e inimigos
        for lin in range(LINHAS):
            for col in range(COLUNAS):
                if grade[lin][col]:
                    grade[lin][col].draw(screen)

        for f in funkeiros:
            f.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


# -------------------------------
# Executável
# -------------------------------
if __name__ == "__main__":
    while True:
        tela_inicial()
        pygame.mixer.music.stop()
        resultado = main()
        if resultado in ("derrota", "vitoria"):
            continue  # volta para o menu
        else:
            break  # sair do jogo
