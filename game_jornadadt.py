import pygame
import sys

# ==========================================================
# JOGO: Jornada do Design Thinking — Edição Boss
# ----------------------------------------------------------
# Como jogar:
# - Setas ou A/D: mover personagem
# - Espaço: pular
# - E: conversar/interagir
# - Mouse: clicar nos botões das respostas
# - Enter: continuar depois do feedback
#
# Instalação:
# python -m pip install pygame
#
# Execução:
# python jogo_design_thinking.py
# ==========================================================

pygame.init()

# -----------------------------
# CONFIGURAÇÕES GERAIS
# -----------------------------
LARGURA = 1000
ALTURA = 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jornada do Design Thinking: Edeilson Contra o Mundo 2")

RELOGIO = pygame.time.Clock()
FPS = 60
MAPA_LARGURA = 7600

# Cores
BRANCO = (255, 255, 255)
PRETO = (20, 20, 20)
CINZA = (120, 120, 120)
CINZA_CLARO = (220, 220, 220)
AZUL_CEU = (135, 206, 235)
VERDE = (60, 170, 90)
VERDE_ESCURO = (30, 110, 60)
MARROM = (125, 80, 45)
AMARELO = (255, 220, 90)
LARANJA = (240, 150, 60)
VERMELHO = (220, 70, 70)
AZUL = (70, 130, 220)
ROXO = (145, 90, 200)
ROXO_ESCURO = (80, 45, 130)
DOURADO = (230, 180, 40)
ROSA = (230, 100, 160)

FONTE_PEQUENA = pygame.font.SysFont("arial", 18)
FONTE_MEDIA = pygame.font.SysFont("arial", 24)
FONTE_GRANDE = pygame.font.SysFont("arial", 38, bold=True)
FONTE_TITULO = pygame.font.SysFont("arial", 48, bold=True)

# Estados do jogo
MENU = "menu"
JOGANDO = "jogando"
QUIZ = "quiz"
BOSS = "boss"
VITORIA = "vitoria"
GAME_OVER = "game_over"

estado_jogo = MENU

# -----------------------------
# DADOS DAS PERGUNTAS DOS NPCs
# -----------------------------
perguntas = [
    {
        "npc": "Lia, a Pesquisadora",
        "etapa": "Empatizar",
        "fala": "Para começar, precisamos entender quem vive o problema.",
        "pergunta": "Qual ação representa melhor a etapa de EMPATIZAR?",
        "opcoes": ["Criar a solução final", "Entrevistar e observar usuários", "Escolher a tecnologia", "Ignorar reclamações"],
        "correta": 1,
        "explicacao": "Empatizar é observar, escutar e compreender as pessoas envolvidas."
    },
    {
        "npc": "Caio, o Observador",
        "etapa": "Empatizar",
        "fala": "Nem sempre o usuário fala tudo diretamente. Às vezes precisamos observar sua rotina.",
        "pergunta": "Por que a observação é importante no Design Thinking?",
        "opcoes": ["Porque substitui todos os testes", "Porque revela comportamentos e dificuldades reais", "Porque elimina a criatividade", "Porque serve apenas para decorar o projeto"],
        "correta": 1,
        "explicacao": "Observar ajuda a perceber necessidades que o usuário talvez não consiga explicar."
    },
    {
        "npc": "Bia, a Entrevistadora",
        "etapa": "Empatizar",
        "fala": "Boas perguntas ajudam a entender melhor a experiência das pessoas.",
        "pergunta": "Qual pergunta é mais adequada para uma entrevista de empatia?",
        "opcoes": ["Você gostou, sim ou não?", "Por que essa situação incomoda você?", "Minha ideia é perfeita, certo?", "Você usaria qualquer coisa?"],
        "correta": 1,
        "explicacao": "Perguntas abertas ajudam a entender motivações, sentimentos e contexto."
    },
    {
        "npc": "Davi, o Analista",
        "etapa": "Definir",
        "fala": "Agora precisamos organizar tudo que descobrimos.",
        "pergunta": "O que acontece na etapa de DEFINIR?",
        "opcoes": ["Transformar descobertas em um problema claro", "Fazer o produto final", "Começar pelo marketing", "Pular a pesquisa"],
        "correta": 0,
        "explicacao": "Definir é formular o problema central de forma clara e útil."
    },
    {
        "npc": "Rafa, o Sintetizador",
        "etapa": "Definir",
        "fala": "Um bom problema não é genérico. Ele mostra quem sofre, o que sofre e por quê.",
        "pergunta": "Qual exemplo é uma boa definição de problema?",
        "opcoes": ["O hospital é ruim", "O app precisa ser bonito", "Pacientes ficam ansiosos por não saberem o tempo de espera", "Vamos criar um sistema qualquer"],
        "correta": 2,
        "explicacao": "Uma boa definição descreve uma necessidade específica de um público específico."
    },
    {
        "npc": "Sofia, a Estrategista",
        "etapa": "Definir",
        "fala": "Se definirmos mal o desafio, podemos resolver o problema errado.",
        "pergunta": "Por que a etapa de definição é tão importante?",
        "opcoes": ["Porque impede novas ideias", "Porque direciona o projeto para o problema certo", "Porque substitui o teste", "Porque elimina o usuário"],
        "correta": 1,
        "explicacao": "Definir bem evita desperdício de esforço em soluções que não resolvem a dor real."
    },
    {
        "npc": "Mika, a Criativa",
        "etapa": "Idear",
        "fala": "Agora é hora de pensar em várias possibilidades.",
        "pergunta": "Qual atitude representa melhor a etapa de IDEAR?",
        "opcoes": ["Gerar várias ideias", "Escolher a primeira ideia", "Evitar colaboração", "Copiar sem pensar"],
        "correta": 0,
        "explicacao": "Idear é abrir possibilidades antes de selecionar a melhor solução."
    },
    {
        "npc": "Noah, o Brainstormer",
        "etapa": "Idear",
        "fala": "Durante a ideação, quantidade pode ajudar a chegar em qualidade.",
        "pergunta": "Em um brainstorming inicial, o ideal é:",
        "opcoes": ["Julgar cada ideia imediatamente", "Gerar ideias variadas sem bloquear a criatividade", "Permitir apenas uma pessoa falar", "Ignorar o problema definido"],
        "correta": 1,
        "explicacao": "No começo da ideação, é melhor explorar muitas ideias antes de filtrar."
    },
    {
        "npc": "Clara, a Facilitadora",
        "etapa": "Idear",
        "fala": "Ideias ficam melhores quando pessoas diferentes colaboram.",
        "pergunta": "Por que a colaboração é útil na ideação?",
        "opcoes": ["Porque traz diferentes pontos de vista", "Porque deixa o processo mais lento sem motivo", "Porque remove o usuário", "Porque evita testes"],
        "correta": 0,
        "explicacao": "Perspectivas diferentes ajudam a criar soluções mais completas e criativas."
    },
    {
        "npc": "Theo, o Inventor",
        "etapa": "Prototipar",
        "fala": "Uma ideia precisa virar algo visível e testável.",
        "pergunta": "O que é um PROTÓTIPO?",
        "opcoes": ["Produto final obrigatório", "Versão simples para testar uma ideia", "Relatório sem usuário", "Uma etapa sem feedback"],
        "correta": 1,
        "explicacao": "Protótipo é uma versão simples que permite visualizar e testar a solução."
    },
    {
        "npc": "Iris, a Desenhista",
        "etapa": "Prototipar",
        "fala": "Nem todo protótipo precisa ser programado.",
        "pergunta": "Qual destes pode ser um protótipo?",
        "opcoes": ["Um desenho de tela no papel", "Apenas o produto vendido", "Uma ideia escondida", "Uma reclamação solta"],
        "correta": 0,
        "explicacao": "Protótipos podem ser desenhos, fluxos, maquetes, telas ou versões simples."
    },
    {
        "npc": "Téo, o Construtor",
        "etapa": "Prototipar",
        "fala": "Prototipar cedo evita gastar energia demais no caminho errado.",
        "pergunta": "Qual é uma vantagem de prototipar rapidamente?",
        "opcoes": ["Testar ideias antes de investir muito", "Impedir mudanças", "Eliminar o problema", "Pular a empatia"],
        "correta": 0,
        "explicacao": "Protótipos rápidos permitem aprender cedo e corrigir a rota."
    },
    {
        "npc": "Nina, a Testadora",
        "etapa": "Testar",
        "fala": "Agora precisamos ver como a solução funciona na prática.",
        "pergunta": "Qual é o objetivo da etapa de TESTAR?",
        "opcoes": ["Receber feedback e melhorar", "Evitar opiniões", "Encerrar sem ajuste", "Apagar tudo"],
        "correta": 0,
        "explicacao": "Testar ajuda a validar, corrigir falhas e melhorar a solução."
    },
    {
        "npc": "Luan, o Validador",
        "etapa": "Testar",
        "fala": "Um teste bom mostra se o usuário entende e usa a solução.",
        "pergunta": "Durante um teste, o que devemos observar?",
        "opcoes": ["Se o usuário entende e consegue usar", "Se o criador acha bonito", "Se ninguém questiona", "Se o projeto parece caro"],
        "correta": 0,
        "explicacao": "O teste observa compreensão, dificuldades, reações e sugestões do usuário."
    },
    {
        "npc": "Eva, a Iteradora",
        "etapa": "Testar",
        "fala": "Quando o teste mostra falhas, isso não é fracasso. É aprendizado.",
        "pergunta": "O que significa dizer que Design Thinking é iterativo?",
        "opcoes": ["Que nunca volta etapas", "Que pode repetir etapas para melhorar a solução", "Que só acontece uma vez", "Que ignora feedback"],
        "correta": 1,
        "explicacao": "Iterar é voltar, ajustar e testar novamente para evoluir a solução."
    }
]

perguntas_boss = [
    {
        "pergunta": "BOSS 1: Um grupo criou um app sem conversar com usuários. Qual etapa foi ignorada?",
        "opcoes": ["Empatizar", "Testar", "Prototipar", "Idear"],
        "correta": 0,
        "explicacao": "Sem escutar e observar usuários, a equipe ignorou a empatia."
    },
    {
        "pergunta": "BOSS 2: A equipe tem muitas entrevistas, mas não sabe qual problema resolver. O que falta?",
        "opcoes": ["Definir o problema", "Finalizar o produto", "Fazer propaganda", "Apagar os dados"],
        "correta": 0,
        "explicacao": "Depois da empatia, é preciso sintetizar as descobertas e definir o desafio."
    },
    {
        "pergunta": "BOSS 3: Um protótipo recebeu críticas dos usuários. Qual deve ser a próxima atitude?",
        "opcoes": ["Ignorar tudo", "Melhorar com base no feedback", "Culpar os usuários", "Parar o projeto"],
        "correta": 1,
        "explicacao": "Feedback serve para ajustar e evoluir a solução."
    }
]

# -----------------------------
# CLASSES
# -----------------------------
class Botao:
    def __init__(self, x, y, largura, altura, texto, cor=AZUL, cor_hover=ROXO):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.cor = cor
        self.cor_hover = cor_hover

    def desenhar(self, tela):
        mouse_pos = pygame.mouse.get_pos()
        cor_atual = self.cor_hover if self.rect.collidepoint(mouse_pos) else self.cor
        pygame.draw.rect(tela, cor_atual, self.rect, border_radius=12)
        pygame.draw.rect(tela, PRETO, self.rect, 2, border_radius=12)
        desenhar_texto_centralizado(tela, self.texto, FONTE_MEDIA, BRANCO, self.rect.centerx, self.rect.centery)

    def clicado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.rect.collidepoint(evento.pos)


class Jogador:
    def __init__(self, x, y):
        self.nome = "Edeilson"
        self.rect = pygame.Rect(x, y, 42, 60)
        self.vel_x = 0
        self.vel_y = 0
        self.velocidade = 5
        self.forca_pulo = -16
        self.no_chao = False
        self.direcao = 1

    def atualizar(self, plataformas):
        teclas = pygame.key.get_pressed()
        self.vel_x = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.vel_x = -self.velocidade
            self.direcao = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.vel_x = self.velocidade
            self.direcao = 1

        self.vel_y += 0.8
        if self.vel_y > 18:
            self.vel_y = 18

        self.rect.x += self.vel_x
        self.colidir(self.vel_x, 0, plataformas)

        self.rect.y += self.vel_y
        self.no_chao = False
        self.colidir(0, self.vel_y, plataformas)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > MAPA_LARGURA:
            self.rect.right = MAPA_LARGURA
        if self.rect.top > ALTURA + 200:
            self.rect.x = 60
            self.rect.y = 300
            self.vel_y = 0

    def pular(self):
        if self.no_chao:
            self.vel_y = self.forca_pulo

    def colidir(self, vel_x, vel_y, plataformas):
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma):
                if vel_x > 0:
                    self.rect.right = plataforma.left
                if vel_x < 0:
                    self.rect.left = plataforma.right
                if vel_y > 0:
                    self.rect.bottom = plataforma.top
                    self.vel_y = 0
                    self.no_chao = True
                if vel_y < 0:
                    self.rect.top = plataforma.bottom
                    self.vel_y = 0

    def desenhar(self, tela, camera_x):
        corpo = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(tela, BRANCO, corpo, border_radius=10)
        pygame.draw.rect(tela, PRETO, corpo, 2, border_radius=10)

        cabeca = pygame.Rect(corpo.x + 6, corpo.y - 28, 30, 30)
        pygame.draw.ellipse(tela, BRANCO, cabeca)
        pygame.draw.ellipse(tela, PRETO, cabeca, 2)
        olho_x = cabeca.centerx + (6 * self.direcao)
        pygame.draw.circle(tela, PRETO, (olho_x, cabeca.y + 12), 3)

        nome_surface = FONTE_PEQUENA.render(self.nome, True, PRETO)
        tela.blit(nome_surface, (corpo.centerx - nome_surface.get_width() // 2, corpo.y - 58))


class NPC:
    def __init__(self, x, y, nome, cor, indice_pergunta):
        self.rect = pygame.Rect(x, y, 46, 62)
        self.nome = nome
        self.cor = cor
        self.indice_pergunta = indice_pergunta
        self.respondido = False

    def desenhar(self, tela, camera_x):
        npc_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(tela, self.cor, npc_rect, border_radius=10)
        pygame.draw.rect(tela, PRETO, npc_rect, 2, border_radius=10)

        cabeca = pygame.Rect(npc_rect.x + 7, npc_rect.y - 27, 32, 32)
        pygame.draw.ellipse(tela, BRANCO, cabeca)
        pygame.draw.ellipse(tela, PRETO, cabeca, 2)
        pygame.draw.circle(tela, PRETO, (cabeca.x + 12, cabeca.y + 13), 3)
        pygame.draw.circle(tela, PRETO, (cabeca.x + 22, cabeca.y + 13), 3)

        icone = "✓" if self.respondido else "?"
        cor_icone = VERDE_ESCURO if self.respondido else VERMELHO
        desenhar_texto_centralizado(tela, icone, FONTE_GRANDE, cor_icone, npc_rect.centerx, npc_rect.y - 50)

        nome_surface = FONTE_PEQUENA.render(self.nome.split(",")[0], True, PRETO)
        tela.blit(nome_surface, (npc_rect.centerx - nome_surface.get_width() // 2, npc_rect.bottom + 5))


class BossFinal:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 95, 120)
        self.nome = "Tanilson"
        self.desbloqueado = False

    def desenhar(self, tela, camera_x, desbloqueado):
        boss_rect = pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        cor = ROXO_ESCURO if desbloqueado else CINZA
        pygame.draw.rect(tela, cor, boss_rect, border_radius=18)
        pygame.draw.rect(tela, PRETO, boss_rect, 3, border_radius=18)

        cabeca = pygame.Rect(boss_rect.x + 18, boss_rect.y - 52, 60, 60)
        pygame.draw.ellipse(tela, cor, cabeca)
        pygame.draw.ellipse(tela, PRETO, cabeca, 3)

        # Chifres/coroa
        pygame.draw.polygon(tela, DOURADO, [(cabeca.x + 8, cabeca.y + 6), (cabeca.x + 18, cabeca.y - 24), (cabeca.x + 28, cabeca.y + 6)])
        pygame.draw.polygon(tela, DOURADO, [(cabeca.x + 34, cabeca.y + 6), (cabeca.x + 44, cabeca.y - 24), (cabeca.x + 54, cabeca.y + 6)])
        pygame.draw.circle(tela, VERMELHO, (cabeca.x + 20, cabeca.y + 28), 5)
        pygame.draw.circle(tela, VERMELHO, (cabeca.x + 40, cabeca.y + 28), 5)

        aviso = "BOSS" if desbloqueado else "BLOQUEADO"
        desenhar_texto_centralizado(tela, aviso, FONTE_PEQUENA, PRETO, boss_rect.centerx, boss_rect.bottom + 16)

# -----------------------------
# FUNÇÕES AUXILIARES
# -----------------------------
def desenhar_texto_centralizado(tela, texto, fonte, cor, x, y):
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect(center=(x, y))
    tela.blit(superficie, rect)


def quebrar_texto(texto, fonte, largura_maxima):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = linha_atual + palavra + " "
        if fonte.size(teste)[0] <= largura_maxima:
            linha_atual = teste
        else:
            if linha_atual.strip():
                linhas.append(linha_atual.strip())
            linha_atual = palavra + " "

    if linha_atual:
        linhas.append(linha_atual.strip())

    return linhas


def desenhar_caixa_texto(tela, x, y, largura, altura, titulo, texto):
    caixa = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(tela, BRANCO, caixa, border_radius=14)
    pygame.draw.rect(tela, PRETO, caixa, 3, border_radius=14)

    titulo_surface = FONTE_MEDIA.render(titulo, True, AZUL)
    tela.blit(titulo_surface, (x + 20, y + 12))

    linhas = quebrar_texto(texto, FONTE_PEQUENA, largura - 40)
    pos_y = y + 46
    for linha in linhas:
        linha_surface = FONTE_PEQUENA.render(linha, True, PRETO)
        tela.blit(linha_surface, (x + 20, pos_y))
        pos_y += 23


def desenhar_cenario(tela, camera_x, plataformas):
    tela.fill(AZUL_CEU)

    pygame.draw.circle(tela, AMARELO, (850, 90), 45)

    for nx in [180, 650, 1200, 1750, 2400, 3000, 3600, 4300, 5000, 5700, 6400, 7100]:
        x = nx - camera_x * 0.4
        pygame.draw.circle(tela, BRANCO, (int(x), 90), 25)
        pygame.draw.circle(tela, BRANCO, (int(x + 25), 80), 30)
        pygame.draw.circle(tela, BRANCO, (int(x + 55), 92), 25)

    for mx in range(0, MAPA_LARGURA, 450):
        x = mx - camera_x * 0.25
        pontos = [(x, 470), (x + 220, 210), (x + 440, 470)]
        pygame.draw.polygon(tela, VERDE_ESCURO, pontos)

    # Placas de fase
    placas = [
        (200, "Empatizar"),
        (1700, "Definir"),
        (3200, "Idear"),
        (4700, "Prototipar"),
        (6100, "Testar"),
        (7250, "Boss")
    ]
    for px, texto in placas:
        rx = px - camera_x
        pygame.draw.rect(tela, DOURADO, (rx, 465, 150, 38), border_radius=8)
        pygame.draw.rect(tela, PRETO, (rx, 465, 150, 38), 2, border_radius=8)
        desenhar_texto_centralizado(tela, texto, FONTE_PEQUENA, PRETO, rx + 75, 484)

    for plataforma in plataformas:
        rect = pygame.Rect(plataforma.x - camera_x, plataforma.y, plataforma.width, plataforma.height)
        pygame.draw.rect(tela, VERDE, rect)
        pygame.draw.rect(tela, MARROM, (rect.x, rect.y + 14, rect.width, rect.height - 14))
        pygame.draw.rect(tela, PRETO, rect, 2)


def desenhar_barra(tela, x, y, largura, altura, atual, maximo, cor, titulo):
    pygame.draw.rect(tela, BRANCO, (x, y, largura, altura), border_radius=8)
    pygame.draw.rect(tela, PRETO, (x, y, largura, altura), 2, border_radius=8)
    proporcao = max(0, atual) / maximo
    pygame.draw.rect(tela, cor, (x + 3, y + 3, int((largura - 6) * proporcao), altura - 6), border_radius=6)
    texto = FONTE_PEQUENA.render(f"{titulo}: {atual}/{maximo}", True, PRETO)
    tela.blit(texto, (x + 10, y - 24))


def desenhar_hud(tela, pontuacao, total, etapa_atual, vida_jogador):
    painel = pygame.Rect(15, 15, 520, 96)
    pygame.draw.rect(tela, BRANCO, painel, border_radius=12)
    pygame.draw.rect(tela, PRETO, painel, 2, border_radius=12)

    texto1 = FONTE_PEQUENA.render(f"Perguntas corretas: {pontuacao}/{total}", True, PRETO)
    texto2 = FONTE_PEQUENA.render("Controles: A/D ou setas = andar | Espaço = pular | E = interagir", True, PRETO)
    texto3 = FONTE_PEQUENA.render(f"Missão atual: {etapa_atual}", True, AZUL)
    texto4 = FONTE_PEQUENA.render("Vidas: " + "♥ " * vida_jogador, True, VERMELHO)

    tela.blit(texto1, (30, 25))
    tela.blit(texto2, (30, 48))
    tela.blit(texto3, (30, 71))
    tela.blit(texto4, (360, 25))


def encontrar_npc_proximo(jogador, npcs):
    area_interacao = jogador.rect.inflate(90, 70)
    for npc in npcs:
        if area_interacao.colliderect(npc.rect):
            return npc
    return None


def jogador_perto_do_boss(jogador, boss):
    area_interacao = jogador.rect.inflate(120, 90)
    return area_interacao.colliderect(boss.rect)


def desenhar_menu(tela, botao_iniciar):
    tela.fill(AZUL_CEU)
    desenhar_texto_centralizado(tela, "Jornada do Design Thinking", FONTE_TITULO, PRETO, LARGURA // 2, 95)
    desenhar_texto_centralizado(tela, "Edeilson Contra o Mundo 2", FONTE_GRANDE, ROXO_ESCURO, LARGURA // 2, 145)
    desenhar_texto_centralizado(tela, "Criado por Arthur Bispo", FONTE_MEDIA, PRETO, LARGURA // 2, 185)

    subtitulo = "Explore o mapa, converse com 15 personagens, responda perguntas e enfrente um boss final para provar que entendeu o conteúdo."
    linhas = quebrar_texto(subtitulo, FONTE_MEDIA, 780)
    y = 215
    for linha in linhas:
        desenhar_texto_centralizado(tela, linha, FONTE_MEDIA, PRETO, LARGURA // 2, y)
        y += 32

    instrucoes = [
        "O jogo tem 5 áreas: Empatizar, Definir, Idear, Prototipar e Testar.",
        "Cada área possui 3 perguntas. O boss só libera após completar todas.",
        "No boss final contra Tanilson, respostas corretas causam dano. Respostas erradas tiram vida."
    ]

    y = 330
    for item in instrucoes:
        desenhar_texto_centralizado(tela, item, FONTE_PEQUENA, PRETO, LARGURA // 2, y)
        y += 30

    botao_iniciar.desenhar(tela)


def desenhar_tela_vitoria(tela, pontuacao, botao_reiniciar):
    tela.fill((245, 245, 255))
    desenhar_texto_centralizado(tela, "Vitória!", FONTE_TITULO, PRETO, LARGURA // 2, 90)
    desenhar_texto_centralizado(tela, "Edeilson derrotou Tanilson!", FONTE_GRANDE, ROXO_ESCURO, LARGURA // 2, 150)
    desenhar_texto_centralizado(tela, f"Pontuação final: {pontuacao}/{len(perguntas)}", FONTE_GRANDE, AZUL, LARGURA // 2, 220)

    if pontuacao >= 13:
        mensagem = "Excelente! A turma demonstrou domínio muito forte das etapas do Design Thinking."
    elif pontuacao >= 10:
        mensagem = "Muito bom! A turma entendeu a maior parte do conteúdo e conseguiu aplicar os conceitos."
    elif pontuacao >= 7:
        mensagem = "Resultado razoável. A turma entendeu a base, mas precisa revisar algumas etapas."
    else:
        mensagem = "É melhor revisar o conteúdo com calma antes de considerar a atividade concluída."

    linhas = quebrar_texto(mensagem, FONTE_MEDIA, 780)
    y = 295
    for linha in linhas:
        desenhar_texto_centralizado(tela, linha, FONTE_MEDIA, PRETO, LARGURA // 2, y)
        y += 35

    resumo = "Resumo: Empatizar entende pessoas; Definir organiza o problema; Idear gera soluções; Prototipar cria uma versão simples; Testar coleta feedback e melhora a solução."
    linhas_resumo = quebrar_texto(resumo, FONTE_PEQUENA, 820)
    y = 380
    for linha in linhas_resumo:
        desenhar_texto_centralizado(tela, linha, FONTE_PEQUENA, PRETO, LARGURA // 2, y)
        y += 26

    botao_reiniciar.desenhar(tela)


def desenhar_game_over(tela, botao_reiniciar):
    tela.fill((40, 35, 55))
    desenhar_texto_centralizado(tela, "Game Over", FONTE_TITULO, BRANCO, LARGURA // 2, 130)
    desenhar_texto_centralizado(tela, "Tanilson venceu desta vez.", FONTE_GRANDE, VERMELHO, LARGURA // 2, 210)
    desenhar_texto_centralizado(tela, "Revise as etapas do Design Thinking e tente novamente.", FONTE_MEDIA, BRANCO, LARGURA // 2, 290)
    botao_reiniciar.desenhar(tela)

# -----------------------------
# CONFIGURAÇÃO DO MUNDO
# -----------------------------
def criar_mundo():
    plataformas = [pygame.Rect(0, 520, MAPA_LARGURA, 80)]

    # Plataformas jogáveis organizadas em pequenas ilhas.
    # A distância horizontal entre elas fica curta o bastante para o pulo alcançar.
    # A altura muda aos poucos, evitando prender o personagem ou exigir saltos impossíveis.
    extras = [
        # Área 1 — Empatizar
        (300, 430), (560, 390), (820, 430),
        # Área 2 — Definir
        (1450, 430), (1710, 390), (1970, 430),
        # Área 3 — Idear
        (2900, 430), (3160, 390), (3420, 430),
        # Área 4 — Prototipar
        (4350, 430), (4610, 390), (4870, 430),
        # Área 5 — Testar
        (5800, 430), (6060, 390), (6320, 430),
    ]
    for x, y in extras:
        plataformas.append(pygame.Rect(x, y, 190, 32))

    cores = [LARANJA, LARANJA, LARANJA, ROXO, ROXO, ROXO, VERDE_ESCURO, VERDE_ESCURO, VERDE_ESCURO, AZUL, AZUL, AZUL, VERMELHO, VERMELHO, VERMELHO]

    # NPCs intercalados: alguns no chão, outros sobre plataformas fáceis de alcançar.
    # Altura do NPC = topo da plataforma - 62. Ex.: plataforma em y=430 => NPC em y=368.
    # Assim eles ficam próximos, mas ainda mantêm a dinâmica de fase/plataforma.
    posicoes = [
        # Empatizar
        (250, 458), (625, 328), (895, 368),
        # Definir
        (1390, 458), (1775, 328), (2045, 368),
        # Idear
        (2840, 458), (3225, 328), (3495, 368),
        # Prototipar
        (4290, 458), (4675, 328), (4945, 368),
        # Testar
        (5740, 458), (6125, 328), (6395, 368),
    ]

    npcs = []
    for i, pos in enumerate(posicoes):
        npcs.append(NPC(pos[0], pos[1], perguntas[i]["npc"], cores[i], i))

    jogador = Jogador(60, 430)
    boss = BossFinal(7250, 400)
    return jogador, plataformas, npcs, boss


jogador, plataformas, npcs, boss = criar_mundo()
pontuacao = 0
vida_jogador = 3
boss_vida = 3
indice_boss = 0
pergunta_atual = None
npc_atual = None
feedback = ""
mostrar_feedback = False
respondeu_boss_atual = False

# Checkpoint: posição para onde o jogador volta quando erra uma pergunta.
# Começa no spawn inicial e é atualizado sempre que o jogador acerta uma pergunta.
checkpoint_x = jogador.rect.x
checkpoint_y = jogador.rect.y
errou_pergunta_mapa = False

botao_iniciar = Botao(390, 455, 220, 60, "Iniciar jogo")
botao_reiniciar = Botao(390, 465, 220, 60, "Jogar novamente")
botoes_resposta = []


def preparar_botoes_quiz():
    global botoes_resposta
    botoes_resposta = []
    y = 286
    for i in range(4):
        botoes_resposta.append(Botao(150, y, 700, 48, "", AZUL, ROXO))
        y += 58


def abrir_quiz(npc):
    global estado_jogo, pergunta_atual, npc_atual, feedback, mostrar_feedback, errou_pergunta_mapa
    npc_atual = npc
    pergunta_atual = perguntas[npc.indice_pergunta]
    feedback = ""
    mostrar_feedback = False
    errou_pergunta_mapa = False
    preparar_botoes_quiz()
    estado_jogo = QUIZ


def abrir_boss():
    global estado_jogo, pergunta_atual, feedback, mostrar_feedback, respondeu_boss_atual
    pergunta_atual = perguntas_boss[indice_boss]
    feedback = ""
    mostrar_feedback = False
    respondeu_boss_atual = False
    preparar_botoes_quiz()
    estado_jogo = BOSS


def todas_perguntas_respondidas():
    return all(npc.respondido for npc in npcs)


def reiniciar_jogo():
    global jogador, plataformas, npcs, boss, pontuacao, vida_jogador, boss_vida, indice_boss, estado_jogo
    global checkpoint_x, checkpoint_y, errou_pergunta_mapa
    jogador, plataformas, npcs, boss = criar_mundo()
    pontuacao = 0
    vida_jogador = 3
    boss_vida = 3
    indice_boss = 0
    checkpoint_x = jogador.rect.x
    checkpoint_y = jogador.rect.y
    errou_pergunta_mapa = False
    estado_jogo = JOGANDO

# -----------------------------
# LOOP PRINCIPAL
# -----------------------------
rodando = True
while rodando:
    RELOGIO.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if estado_jogo == MENU:
            if botao_iniciar.clicado(evento):
                estado_jogo = JOGANDO

        elif estado_jogo == JOGANDO:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogador.pular()
                if evento.key == pygame.K_e:
                    npc = encontrar_npc_proximo(jogador, npcs)
                    if npc and not npc.respondido:
                        abrir_quiz(npc)
                    elif jogador_perto_do_boss(jogador, boss):
                        if todas_perguntas_respondidas():
                            abrir_boss()

        elif estado_jogo == QUIZ:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not mostrar_feedback:
                for i, botao in enumerate(botoes_resposta):
                    if botao.rect.collidepoint(evento.pos):
                        correta = pergunta_atual["correta"]
                        if i == correta:
                            feedback = "Correto! Checkpoint salvo! " + pergunta_atual["explicacao"]
                            pontuacao += 1
                            npc_atual.respondido = True
                            checkpoint_x = jogador.rect.x
                            checkpoint_y = jogador.rect.y
                            errou_pergunta_mapa = False
                        else:
                            feedback = "Ainda não. Você voltará para o último checkpoint. " + pergunta_atual["explicacao"]
                            npc_atual.respondido = False
                            errou_pergunta_mapa = True

                        mostrar_feedback = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and mostrar_feedback:
                    if errou_pergunta_mapa:
                        jogador.rect.x = checkpoint_x
                        jogador.rect.y = checkpoint_y
                        jogador.vel_x = 0
                        jogador.vel_y = 0
                    estado_jogo = JOGANDO

        elif estado_jogo == BOSS:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not mostrar_feedback:
                for i, botao in enumerate(botoes_resposta):
                    if botao.rect.collidepoint(evento.pos):
                        correta = pergunta_atual["correta"]
                        if i == correta:
                            boss_vida -= 1
                            feedback = "Golpe certeiro! " + pergunta_atual["explicacao"]
                        else:
                            vida_jogador -= 1
                            feedback = "O Guardião contra-atacou! " + pergunta_atual["explicacao"]
                        mostrar_feedback = True

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and mostrar_feedback:
                    if boss_vida <= 0:
                        estado_jogo = VITORIA
                    elif vida_jogador <= 0:
                        estado_jogo = GAME_OVER
                    else:
                        indice_boss += 1
                        if indice_boss >= len(perguntas_boss):
                            # Se acabou a lista e o boss ainda vive, ele repete a última pergunta para manter a batalha funcionando.
                            indice_boss = len(perguntas_boss) - 1
                        abrir_boss()

        elif estado_jogo == VITORIA:
            if botao_reiniciar.clicado(evento):
                reiniciar_jogo()

        elif estado_jogo == GAME_OVER:
            if botao_reiniciar.clicado(evento):
                reiniciar_jogo()

    # -----------------------------
    # ATUALIZAÇÃO
    # -----------------------------
    if estado_jogo == JOGANDO:
        jogador.atualizar(plataformas)

    camera_x = jogador.rect.centerx - LARGURA // 2
    camera_x = max(0, min(camera_x, MAPA_LARGURA - LARGURA))

    # -----------------------------
    # DESENHO
    # -----------------------------
    if estado_jogo == MENU:
        desenhar_menu(TELA, botao_iniciar)

    elif estado_jogo == JOGANDO:
        desenhar_cenario(TELA, camera_x, plataformas)

        for npc in npcs:
            npc.desenhar(TELA, camera_x)

        boss_desbloqueado = todas_perguntas_respondidas()
        boss.desenhar(TELA, camera_x, boss_desbloqueado)
        jogador.desenhar(TELA, camera_x)

        etapa_atual = "fale com os personagens"
        npc_proximo = encontrar_npc_proximo(jogador, npcs)
        if npc_proximo and not npc_proximo.respondido:
            etapa_atual = perguntas[npc_proximo.indice_pergunta]["etapa"]
            desenhar_caixa_texto(TELA, 220, 410, 560, 92, npc_proximo.nome, "Pressione E para conversar e responder a pergunta.")
        elif jogador_perto_do_boss(jogador, boss):
            if boss_desbloqueado:
                etapa_atual = "Boss final desbloqueado"
                desenhar_caixa_texto(TELA, 220, 400, 560, 105, boss.nome, "Você completou as 15 perguntas. Pressione E para enfrentar o boss final.")
            else:
                faltam = len([npc for npc in npcs if not npc.respondido])
                etapa_atual = f"faltam {faltam} perguntas"
                desenhar_caixa_texto(TELA, 220, 400, 560, 105, boss.nome, f"Ainda estou bloqueado. Responda todas as perguntas do mapa. Faltam {faltam}.")

        desenhar_hud(TELA, pontuacao, len(perguntas), etapa_atual, vida_jogador)

    elif estado_jogo == QUIZ:
        TELA.fill((235, 240, 255))
        desenhar_texto_centralizado(TELA, pergunta_atual["etapa"], FONTE_TITULO, AZUL, LARGURA // 2, 55)
        desenhar_caixa_texto(TELA, 90, 105, 820, 118, pergunta_atual["npc"], pergunta_atual["fala"])

        pergunta_linhas = quebrar_texto(pergunta_atual["pergunta"], FONTE_MEDIA, 790)
        y = 245
        for linha in pergunta_linhas:
            desenhar_texto_centralizado(TELA, linha, FONTE_MEDIA, PRETO, LARGURA // 2, y)
            y += 30

        for i, botao in enumerate(botoes_resposta):
            botao.texto = f"{chr(65 + i)}) {pergunta_atual['opcoes'][i]}"
            botao.desenhar(TELA)

        if mostrar_feedback:
            caixa_feedback = pygame.Rect(80, 525, 840, 62)
            pygame.draw.rect(TELA, BRANCO, caixa_feedback, border_radius=12)
            pygame.draw.rect(TELA, PRETO, caixa_feedback, 2, border_radius=12)
            linhas = quebrar_texto(feedback + " Pressione ENTER para continuar.", FONTE_PEQUENA, 800)
            y = 538
            for linha in linhas[:2]:
                desenhar_texto_centralizado(TELA, linha, FONTE_PEQUENA, PRETO, LARGURA // 2, y)
                y += 22

    elif estado_jogo == BOSS:
        TELA.fill((45, 35, 70))
        desenhar_texto_centralizado(TELA, "BOSS FINAL", FONTE_TITULO, DOURADO, LARGURA // 2, 45)
        desenhar_texto_centralizado(TELA, "Tanilson", FONTE_GRANDE, BRANCO, LARGURA // 2, 92)

        desenhar_barra(TELA, 120, 135, 300, 26, vida_jogador, 3, VERMELHO, "Jogador")
        desenhar_barra(TELA, 580, 135, 300, 26, boss_vida, 3, ROXO, "Boss")

        pergunta_linhas = quebrar_texto(pergunta_atual["pergunta"], FONTE_MEDIA, 850)
        y = 210
        for linha in pergunta_linhas:
            desenhar_texto_centralizado(TELA, linha, FONTE_MEDIA, BRANCO, LARGURA // 2, y)
            y += 32

        for i, botao in enumerate(botoes_resposta):
            botao.texto = f"{chr(65 + i)}) {pergunta_atual['opcoes'][i]}"
            botao.desenhar(TELA)

        if mostrar_feedback:
            caixa_feedback = pygame.Rect(80, 525, 840, 62)
            pygame.draw.rect(TELA, BRANCO, caixa_feedback, border_radius=12)
            pygame.draw.rect(TELA, PRETO, caixa_feedback, 2, border_radius=12)
            linhas = quebrar_texto(feedback + " Pressione ENTER para continuar.", FONTE_PEQUENA, 800)
            y = 538
            for linha in linhas[:2]:
                desenhar_texto_centralizado(TELA, linha, FONTE_PEQUENA, PRETO, LARGURA // 2, y)
                y += 22

    elif estado_jogo == VITORIA:
        desenhar_tela_vitoria(TELA, pontuacao, botao_reiniciar)

    elif estado_jogo == GAME_OVER:
        desenhar_game_over(TELA, botao_reiniciar)

    pygame.display.flip()

pygame.quit()
sys.exit()
