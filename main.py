import pygame
import sys
import os
import random
import math

from personagens.ozzy import RockeiroOzzy
from personagens.axl import RockeiroAxl
from personagens.kurt import RockeiroKurt
from personagens.caixa import Caixa
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
# Seringa e moeda
# -------------------------------
def seringa():
    img = pygame.image.load(os.path.join('assets', 'seringa.png')).convert_alpha()
    img = pygame.transform.scale(img, (60, 60))
    rect = img.get_rect(topleft=(0,0))  # será reposicionado na GUI
    return rect, img

seringa_caixa, seringa_img = seringa()
moeda_img = pygame.image.load(os.path.join("assets", "ROBG.png")).convert_alpha()
moeda_img = pygame.transform.scale(moeda_img, (120, 80))

# -------------------------------
# Custos e personagens
# -------------------------------
custos = {"ozzy":50, "axl":75, "kurt":100, "caixa":50}
personagens_disponiveis = {
    "ozzy": RockeiroOzzy,
    "axl": RockeiroAxl,
    "kurt": RockeiroKurt,
    "caixa": lambda l,c,hp=300: Caixa(l,c,hp=hp)
}

# -------------------------------
# Botões
# -------------------------------
botoes_imgs = { 
    "ozzy": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "OBG.png")).convert_alpha(), (100,100)),
             "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "OBGH.png")).convert_alpha(), (100,100))},
    "axl": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "ABG.png")).convert_alpha(), (100,100)),
             "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "ABGH.png")).convert_alpha(), (100,100))},
    "kurt": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "KBG.png")).convert_alpha(), (100,100)),
              "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "KBGH.png")).convert_alpha(), (100,100))},
    "caixa": {"normal": pygame.transform.scale(pygame.image.load(os.path.join("assets", "CBG.png")).convert_alpha(), (100,100)),
              "hover": pygame.transform.scale(pygame.image.load(os.path.join("assets", "CBGH.png")).convert_alpha(), (100,100))}
}

botoes = {
    "ozzy": {"rect": pygame.Rect(0,0,100,100), "ativo":True},
    "axl": {"rect": pygame.Rect(0,0,100,100), "ativo":True},
    "kurt": {"rect": pygame.Rect(0,0,100,100), "ativo":True},
    "caixa": {"rect": pygame.Rect(0,0,100,100), "ativo":True}
}

# -------------------------------
# Funções de desenho GUI (barra inferior)
# -------------------------------
def desenhar_gui(personagem_selecionado):
    gui_altura = 160
    gui_rect = pygame.Rect(0, 0, TLARGURA, gui_altura)
    pygame.draw.rect(screen, (40,40,40), gui_rect)
    pygame.draw.rect(screen, (200,200,200), gui_rect, 3)

    x_inicial = 50
    y_inicial = 10
    largura_botao = 200
    altura_botao = 200
    espacamento = largura_botao + 40
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    i = 0
    for nome, botao in botoes.items():
        botao["rect"] = pygame.Rect(x_inicial + i*espacamento, y_inicial, largura_botao, altura_botao)
        img = pygame.transform.scale(
            botoes_imgs[nome]["hover"] if botao["rect"].collidepoint(mouse_x, mouse_y) else botoes_imgs[nome]["normal"],
            (largura_botao, altura_botao)
        )
        screen.blit(img, botao["rect"].topleft)

        # Indicação discreta do botão selecionado
        if personagem_selecionado == nome:
            overlay = pygame.Surface((largura_botao, altura_botao), pygame.SRCALPHA)
            overlay.fill((0, 100, 255, 10))  # azul claro, alpha 80
            screen.blit(overlay, botao["rect"].topleft)
        
        i += 1

    # Seringa
    seringa_largura = 80
    seringa_altura = 80
    seringa_caixa.topleft = (x_inicial + i*espacamento, y_inicial + (altura_botao-seringa_altura)//2)
    img_seringa = pygame.transform.scale(seringa_img, (seringa_largura, seringa_altura))
    screen.blit(img_seringa, seringa_caixa)
    pygame.draw.rect(screen, (0,250,0) if pa_mode else (255,255,255), seringa_caixa, 3)

    # Recursos
    recurso_largura = 300
    recurso_altura = 200
    contador_x = seringa_caixa.right + 30
    contador_y = y_inicial + (altura_botao-recurso_altura)//2
    contador_img_rect = pygame.Rect(contador_x, contador_y, recurso_largura, recurso_altura)
    screen.blit(pygame.transform.scale(moeda_img, (recurso_largura, recurso_altura)), contador_img_rect)
    valor_surface = fonte.render(f"{recursos[0]}", True, (255,255,255))
    valor_rect = valor_surface.get_rect(center=contador_img_rect.center)
    screen.blit(valor_surface, valor_rect)

    # Seringa à direita dos botões
    seringa_largura = 80
    seringa_altura = 80
    seringa_caixa.topleft = (x_inicial + i*espacamento, y_inicial + (altura_botao-seringa_altura)//2)
    img_seringa = pygame.transform.scale(seringa_img, (seringa_largura, seringa_altura))
    screen.blit(img_seringa, seringa_caixa)
    pygame.draw.rect(screen, (0,250,0) if pa_mode else (255,255,255), seringa_caixa, 3)

    # Recursos à direita da seringa
    recurso_largura = 300
    recurso_altura = 200
    contador_x = seringa_caixa.right + 30
    contador_y = y_inicial + (altura_botao-recurso_altura)//2
    contador_img_rect = pygame.Rect(contador_x, contador_y, recurso_largura, recurso_altura)
    screen.blit(pygame.transform.scale(moeda_img, (recurso_largura, recurso_altura)), contador_img_rect)
    valor_surface = fonte.render(f"{recursos[0]}", True, (255,255,255))
    valor_rect = valor_surface.get_rect(center=contador_img_rect.center)
    screen.blit(valor_surface, valor_rect)

# -------------------------------
# Funções de desenho existentes
# -------------------------------
def desenhar_grade():
    tempo = pygame.time.get_ticks() / 500
    oscilacao = int((1 + math.sin(tempo)) * 20)
    for lin in range(LINHAS):
        for col in range(COLUNAS-2):
            x = GRADE_X + col * TAMANHO_CELULA
            y = GRADE_Y + lin * TAMANHO_CELULA
            cor_base = (120, 30, 30,10)
            topo_esquerda = (min(cor_base[0] + oscilacao, 255),
                             min(cor_base[1] + oscilacao, 255),
                             min(cor_base[2] + oscilacao, 255))
            baixo_direita = (max(cor_base[0] - oscilacao, 0),
                             max(cor_base[1] - oscilacao, 0),
                             max(cor_base[2] - oscilacao, 0))
            pygame.draw.line(screen, topo_esquerda, (x, y), (x + TAMANHO_CELULA, y), 3)
            pygame.draw.line(screen, topo_esquerda, (x, y), (x, y + TAMANHO_CELULA), 3)
            pygame.draw.line(screen, baixo_direita, (x + TAMANHO_CELULA, y), (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 3)
            pygame.draw.line(screen, baixo_direita, (x, y + TAMANHO_CELULA), (x + TAMANHO_CELULA, y + TAMANHO_CELULA), 3)

def desenhar_personagens():
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            if grade[lin][col]:
                grade[lin][col].draw(screen)

# -------------------------------
# Atualização de personagens e inimigos
# -------------------------------
def atualizar_personagens():
    for lin in range(LINHAS):
        for col in range(COLUNAS):
            personagem = grade[lin][col]
            if personagem:
                if isinstance(personagem,Caixa):
                    personagem.update(funkeiros,recursos)
                elif hasattr(personagem,"projeteis"):
                    personagem.update(funkeiros)
                else:
                    personagem.update()
                if hasattr(personagem,"projeteis"):
                    proj_para_remover=[]
                    for proj in personagem.projeteis:
                        for f in funkeiros:
                            if f.vivo and proj.rect.colliderect(f.rect):
                                f.hp -= proj.dano
                                if f.hp <= 0:
                                    f.vivo=False
                                if proj not in proj_para_remover:
                                    proj_para_remover.append(proj)
                    for p in proj_para_remover:
                        if p in personagem.projeteis:
                            personagem.projeteis.remove(p)

def atualizar_inimigos():
    for f in funkeiros:
        if hasattr(f, "boss") and f.boss:
            f.update(grade, funkeiros)
        else:
            f.update(grade)
        if f.rect.left<=0:
            return tela_derrota()
    funkeiros[:] = [f for f in funkeiros if f.vivo]
    return None

# -------------------------------
# Telas
# -------------------------------
def tela_derrota():
    fundo = pygame.image.load(os.path.join("assets", "IMRVFD.jpg")).convert()
    fundo = pygame.transform.scale(fundo, (TLARGURA, TALTURA))
    pygame.mixer.music.load(os.path.join('assets','music','FRVFM.mp3'))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(0)
    screen.blit(fundo, (0, 0))
    fonte_grande = pygame.font.SysFont(None, 100)
    texto = fonte_grande.render("VOCÊ PERDEU!", True, (250, 0, 0))
    screen.blit(texto, (TLARGURA//2 - texto.get_width()//2, TALTURA//2 - texto.get_height()//2))
    pygame.display.flip()
    pygame.time.delay(6000)
    return "derrota"

def tela_vitoria():
    fundo = pygame.image.load(os.path.join("assets", "IMRVFV.jpg")).convert()
    fundo = pygame.transform.scale(fundo, (TLARGURA, TALTURA))
    pygame.mixer.music.load(os.path.join('assets','music','RFVV.mp3'))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(0)
    screen.blit(fundo, (0, 0))
    pygame.display.flip()       
    pygame.time.delay(6000)   
    return "vitoria"

# -------------------------------
# Função principal
# -------------------------------
def main():
    global personagem_selecionado, pa_mode, grade, recursos, funkeiros
    clock = pygame.time.Clock()

    grade = [[None for _ in range(COLUNAS)] for _ in range(LINHAS)]
    recursos = [100]
    personagem_selecionado = None
    pa_mode = False
    funkeiros = []

    pygame.mixer.music.load(os.path.join('assets','music','RVFF1.mp3'))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    wave_manager = WaveManager()
    wave_manager.iniciar(pygame.time.get_ticks())

    while True:
        for evento in pygame.event.get():
            if evento.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type==pygame.MOUSEBUTTONDOWN:
                x,y = evento.pos
                # GUI botões
                for nome,botao in botoes.items():
                    if botao["rect"].collidepoint(x,y):
                        personagem_selecionado=None if personagem_selecionado==nome else nome
                        pa_mode=False
                # GUI seringa
                if seringa_caixa.collidepoint(x,y):
                    pa_mode = not pa_mode
                    personagem_selecionado=None
                # Grade
                col = (x-GRADE_X)//TAMANHO_CELULA
                lin = (y-GRADE_Y)//TAMANHO_CELULA
                # define limite das colunas onde é permitido colocar personagens
                COLUNAS_VALIDAS = COLUNAS-2

                if 0<=lin<LINHAS and 0<=col<COLUNAS_VALIDAS:
                    if pa_mode and grade[lin][col]:
                        grade[lin][col]=None
                    elif grade[lin][col] is None and personagem_selecionado:
                        custo = custos[personagem_selecionado]
                        if recursos[0]>=custo:
                            classe = personagens_disponiveis[personagem_selecionado]
                            grade[lin][col]=classe(lin,col,hp=3000) if personagem_selecionado=="caixa" else classe(lin,col)
                            recursos[0]-=custo

        agora = pygame.time.get_ticks()
        wave_manager.spawn_inimigo(agora, LINHAS, funkeiros)
        wave_manager.verificar_wave(agora, funkeiros)
        if wave_manager.game_won:
            return tela_vitoria()

        atualizar_personagens()
        resultado_inimigos = atualizar_inimigos()
        if resultado_inimigos:
            return resultado_inimigos

        # Render
        screen.fill((60,60,60))
        desenhar_mapa()
        desenhar_grade()
        desenhar_personagens()
        for f in funkeiros: f.draw(screen)
        desenhar_gui(personagem_selecionado)

        pygame.display.flip()
        clock.tick(FPS)

# -------------------------------
# Executável
# -------------------------------
if __name__=="__main__":
    while True:
        tela_inicial()
        pygame.mixer.music.stop()
        resultado = main()
        if resultado in ("derrota","vitoria"):
            continue
        else:
            break
