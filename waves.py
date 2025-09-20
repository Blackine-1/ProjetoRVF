import random
from funkeiro import Funkeiro
from boss import Boss  # Boss atualizado que cobre todas as linhas

class WaveManager:
    def __init__(self):
        # Lista de waves normais
        self.waves = [
            {"qtd": 5, "hp": 50, "velocidade": 1, "dano": 5},
            {"qtd": 8, "hp": 80, "velocidade": 1.2, "dano": 10},
            {"qtd": 10, "hp": 100, "velocidade": 1.5, "dano": 15},
        ]
        self.wave_index = 0
        self.inimigos_spawnados = 0
        self.spawn_timer = 0
        self.spawn_interval = 2000  # 2 segundos entre inimigos
        self.boss = None
        self.game_won = False

    def iniciar(self, agora):
        self.spawn_timer = agora

    def spawn_inimigo(self, agora, LINHAS, funkeiros):
        if self.wave_index < len(self.waves):
            wave = self.waves[self.wave_index]
            if agora - self.spawn_timer > self.spawn_interval and self.inimigos_spawnados < wave["qtd"]:
                linha_aleatoria = random.randint(0, LINHAS - 1)
                f = Funkeiro(linha_aleatoria,
                             hp=wave["hp"],
                             velocidade=wave["velocidade"],
                             dano=wave["dano"])
                funkeiros.append(f)
                self.inimigos_spawnados += 1
                self.spawn_timer = agora
        elif self.wave_index == len(self.waves) and self.boss is None:
            # Spawn do boss que ocupa todas as linhas
            self.boss = Boss(hp=2000, dano=20, velocidade=0.5, linhas=LINHAS)
            funkeiros.append(self.boss)

    def verificar_wave(self, agora, funkeiros):
        if self.wave_index < len(self.waves):
            wave = self.waves[self.wave_index]
            # Só passa para a próxima wave se todos os Funkeiros estiverem mortos
            if self.inimigos_spawnados >= wave["qtd"] and not any(isinstance(f, Funkeiro) and f.vivo for f in funkeiros):
                self.wave_index += 1
                self.inimigos_spawnados = 0
                self.spawn_timer = agora
        elif self.wave_index == len(self.waves):
            # Verifica se o boss morreu
            if self.boss and not self.boss.vivo:
                self.game_won = True
