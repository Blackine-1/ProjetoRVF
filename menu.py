import pygame
import os
from config import *
import sys

def tela_inicial():
    clock = pygame.time.Clock()

    # carrega imagem de fundo
    fundo = pygame.image.load(os.path.join("assets", "IMRVF2.jfif")).convert()
    fundo = pygame.transform.scale(fundo, (TLARGURA, TALTURA))

    # carrega imagens dos botões (normal e hover)
    img_comecar = pygame.image.load(os.path.join("assets", "CM.png")).convert_alpha()
    img_comecar_hover = pygame.image.load(os.path.join("assets", "CMH.png")).convert_alpha()
    img_sair = pygame.image.load(os.path.join("assets", "SM.png")).convert_alpha()
    img_sair_hover = pygame.image.load(os.path.join("assets", "SMH.png")).convert_alpha()

    # redimensiona botões (200x60 como antes)
    img_comecar = pygame.transform.scale(img_comecar, (200, 200))
    img_comecar_hover = pygame.transform.scale(img_comecar_hover, (200, 200))
    img_sair = pygame.transform.scale(img_sair, (200, 200))
    img_sair_hover = pygame.transform.scale(img_sair_hover, (200, 200))

    # rects para clique
    botao_comecar = img_comecar.get_rect(center=(TLARGURA // 2, 400))
    botao_sair = img_sair.get_rect(center=(TLARGURA // 2, 630))

    # carrega música apenas uma vez
    pygame.mixer.music.load(os.path.join('assets', 'music','RVFOP.mp3'))
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    while True:
        # fundo
        screen.blit(fundo, (0, 0))

        # posição do mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # desenha botão começar
        if botao_comecar.collidepoint(mouse_x, mouse_y):
            screen.blit(img_comecar_hover, botao_comecar.topleft)
        else:
            screen.blit(img_comecar, botao_comecar.topleft)

        # desenha botão sair
        if botao_sair.collidepoint(mouse_x, mouse_y):
            screen.blit(img_sair_hover, botao_sair.topleft)
        else:
            screen.blit(img_sair, botao_sair.topleft)

        # eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                if botao_comecar.collidepoint(x, y):
                    return  # inicia o jogo
                elif botao_sair.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)
