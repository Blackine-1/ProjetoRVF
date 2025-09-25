import random
from funkeiro import Funkeiro
from boss import Boss  # Boss atualizado que cobre todas as linhas

class WaveManager:
    def __init__(self):
        # Waves normais com mistura de tipos
        # Cada wave é uma lista de dicionários representando tipos de inimigos
        self.waves = [
            [   # Wave 1
                {"tipo": "fraco", "qtd": 3},
            ],
            [   # Wave 2
                {"tipo": "fraco", "qtd": 3},
                {"tipo": "medio", "qtd": 2},
            ],
            [   # Wave 3
                {"tipo": "medio", "qtd": 4},
                {"tipo": "rapido", "qtd": 2},
            ],
            [   # Wave 4
                {"tipo": "fraco", "qtd": 3},
                {"tipo": "medio", "qtd": 3},
                {"tipo": "rapido", "qtd": 3},
            ],
            [   # Wave 5 (pré-boss)
                {"tipo": "medio", "qtd": 4},
                {"tipo": "rapido", "qtd": 4},
                {"tipo": "forte", "qtd": 2},
            ],
        ]
        self.wave_index = 0
        self.inimigos_spawnados = 0
        self.spawn_timer = 0
        self.spawn_interval = 1800
        self.boss = None
        self.game_won = False

        # Tipos de inimigos com stats
        self.tipo_stats = {
            "fraco": {"hp": 50, "velocidade": 1.0, "dano": 5},
            "medio": {"hp": 120, "velocidade": 1.4, "dano": 15},
            "rapido": {"hp": 80, "velocidade": 2.0, "dano": 10},
            "forte": {"hp": 200, "velocidade": 1.2, "dano": 25},
        }

    def iniciar(self, agora):
        self.spawn_timer = agora
        self.inimigos_spawnados = 0
        self.wave_inimigos_restantes = list(self.waves[self.wave_index])

    def spawn_inimigo(self, agora, LINHAS, funkeiros):
        if self.wave_index < len(self.waves):
            if agora - self.spawn_timer > self.spawn_interval:
                # Escolhe um tipo de inimigo que ainda tenha quantidade restante
                for tipo_info in self.wave_inimigos_restantes:
                    if tipo_info["qtd"] > 0:
                        tipo = tipo_info["tipo"]
                        stats = self.tipo_stats[tipo]
                        linha_aleatoria = random.randint(0, LINHAS-1)
                        f = Funkeiro(
                            linha=linha_aleatoria,
                            hp=stats["hp"],
                            velocidade=stats["velocidade"],
                            dano=stats["dano"]
                        )
                        funkeiros.append(f)
                        tipo_info["qtd"] -= 1
                        self.spawn_timer = agora
                        break
        elif self.wave_index == len(self.waves) and self.boss is None:
            self.boss = Boss(hp=2500, dano=25, linhas=LINHAS)
            funkeiros.append(self.boss)

    def verificar_wave(self, agora, funkeiros):
        if self.wave_index < len(self.waves):
            # Se todos os inimigos da wave foram spawnados e mortos, passa para próxima
            wave_inimigos_vivos = [f for f in funkeiros if isinstance(f, Funkeiro) and f.vivo]
            if all(t["qtd"] == 0 for t in self.wave_inimigos_restantes) and not wave_inimigos_vivos:
                self.wave_index += 1
                if self.wave_index < len(self.waves):
                    self.wave_inimigos_restantes = list(self.waves[self.wave_index])
                self.spawn_timer = agora
        elif self.wave_index == len(self.waves):
            if self.boss and not self.boss.vivo:
                self.game_won = True
