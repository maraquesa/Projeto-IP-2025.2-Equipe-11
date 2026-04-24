# Cinbate

**Cinbate** é um jogo 2D multiplayer local (mesma máquina), para dois jogadores, em pixel art e com câmera em perspectiva top-down (cima para baixo). Cada jogador controla um personagem que se movimenta pelo mapa competindo diretamente com o adversário enquanto coleta diferentes tipos de itens.
A proposta central é a interação constante entre os jogadores, tanto por meio de colisões diretas, quanto pelo uso estratégico dos coletáveis secundários, que impactam a pontuação e o desempenho do oponente.

## Mecânicas

### Movimentação e Controle
O jogo oferece movimentação livre em oito direções, permitindo deslocamentos ortogonais e diagonais fluídos.
* **Jogador 1 (Márcio Cornélio):** Controlado pelas teclas `W`, `A`, `S`, `D`.
* **Jogador 2 (Ricardo Massa):** Controlado pelas setas do teclado `↑`, `←`, `↓`, `→`.

### Colisão entre Jogadores
Quando dois jogadores colidem, ambos são empurrados para direções opostas, respeitando o vetor de movimento de cada um. Evitando sobreposições e criando disputas físicas pelo controle do espaço e dos coletáveis.

### Limite de Tela (Wrap-around)
Não existem paredes invisíveis nas bordas do mapa. Ao ultrapassar qualquer limite da tela, o jogador reaparece instantaneamente no lado oposto (ex: sair pela direita e voltar pela esquerda), permitindo rotas de fuga estratégicas e uma arena infinita.

### Obstáculos Móveis
Para elevar o nível de dificuldade, foram implementados obstáculos móveis que circulam pela área de jogo.
* **Penalidade:** Cada colisão com um obstáculo subtrai **1 ponto** do jogador atingido.

---

## Sistema de Pontuação e Condição de Vitória

O sistema de jogo é baseado em uma corrida por pontos, onde o equilíbrio entre coletar e sabotar é a chave para a vitória.

### Coletáveis Principais (Pontos)
* **Função:** São o objetivo principal do jogo. Cada item coletado soma **+1 ponto**.
* **Comportamento:** Ao ser coletado, o item reaparece em uma nova posição aleatória.
* **Condição de Vitória:** Vence o jogador que atingir primeiro a marca de **10 pontos**.

### Coletáveis Secundários (Buffs e Sabotagem)
Surgem e desaparecem dinamicamente no mapa, oferecendo vantagens temporárias ou habilidades especiais:

| Bônus | Descrição | Ativação (P1 / P2) |
| :--- | :--- | :--- |
| **Velocidade** | Aumenta temporariamente a velocidade de movimento. | Automático na coleta |
| **Boomerang** | Permite 2 lançamentos de projétil que subtraem pontos do rival se atingirem o alvo. | `R` / `O` |
| **Teleporte** | Acionado projeta o jogador vários passos à frente na direção do movimento. | `T` / `M` |

##  Arquitetura

* **`main.py`**: gerencia o Game Loop, a alternância entre estados (menu, jogo ativo, vitória) e a renderização da interface (HUD).
* **`sprites.py`**: contém as definições de classes, para facilitar a gestão de colisões e atualizações em grupo. 
* **`operacoes.py`**: centraliza variáveis globais (velocidades, tempos, pontuações) e funções auxiliares de cálculo e detecção de colisão.
* **`menu.py`**: responsável pelas telas de menu, botões e feedback visual de vitória.

### Estrutura de Diretórios
```text
├── assets/          # Sprites, imagens de fundo e logos
├── fonts/           # Fonte pixel (VT323-Regular.ttf)
├── main.py          # Arquivo principal
├── menu.py          # Telas de menu e vitória
├── operacoes.py     # Lógica matemática e variáveis globais
└── sprites.py       # Classes de objetos do jogo
```

## Ferramentas, Bibliotecas e Frameworks

**Python**: Linguagem principal do projeto. Sua sintaxe clara foi fundamental para a aplicação de estruturas de dados e lógica de programação complexas.
* **Pygame**: A "engine" do jogo. Responsável por toda a infraestrutura:
    * Renderização gráfica e gerenciamento de janelas.
    * Captura de inputs (teclado/mouse).
    * Sistema de Sprites e detecção de colisões.
    * Controle de FPS (frames por segundo).
* **Pixilart**: Ferramenta utilizada para o design visual, onde criamos todos os personagens e elementos em *Pixel Art*.
* **Git & GitHub**: Pilares da colaboração. Utilizados para versionamento, controle de *branches* e integração do código entre os membros da equipe.
* **Math (Biblioteca Standard)**: Essencial para a física do jogo, permitindo o uso de funções trigonométricas para normalizar a velocidade nas diagonais.
* **Random (Biblioteca Standard)**: Garante a imprevisibilidade do jogo, controlando o surgimento aleatório dos coletáveis e obstáculos no mapa.

## Conceitos da Disciplina Aplicados

### Estruturas Condicionais (`if`, `elif`, `else`)
Utilizadas para o controle de fluxo e tomada de decisão em tempo real. São fundamentais para a mecânica de *wrap-around* (transposição de bordas), detecção de colisões e validação de uso de itens.
* **Exemplo:** Verificação se o jogador ultrapassou os limites da tela para reposicioná-lo no lado oposto.

### Laços de Repetição (`while`, `for`)
* **`while`**: Mantém o *Game Loop* ativo, garantindo que o jogo processe eventos e renderize quadros continuamente a 60 FPS.
* **`for`**: Utilizado para percorrer grupos de sprites, atualizar múltiplos bumerangues simultaneamente e inicializar listas de objetos coletáveis.

### Funções e Modularização
O código utiliza funções para encapsular lógicas matemáticas complexas e repetitivas, facilitando a manutenção e a legibilidade.
* **Exemplo:** A função `calcular_velocidade_diagonal()` utiliza trigonometria para normalizar o vetor de movimento, evitando que o jogador se mova mais rápido ao pressionar duas teclas.

### Listas e Índices
As listas são usadas para gerenciar coleções dinâmicas de dados, como a pontuação global (`pontuacao_lista`) e os pesos de spawn para coletáveis secundários. O acesso via índice permite uma comunicação rápida entre diferentes módulos do código.

### Dicionários
Empregados para gerenciar o estado complexo de bônus (*buffs/debuffs*) de cada jogador. Esta estrutura permite associar chaves textuais (como `'velocidade'` ou `'tele'`) a sub-dicionários que guardam os valores atuais e máximos de cada efeito.

### Tuplas
Utilizadas para armazenar coordenadas fixas (X, Y) e configurações de cores (RGB), garantindo que esses valores permaneçam imutáveis durante a execução, prevenindo bugs de sobrescrita acidental.

## Divisão de Trabalho

A organização das tarefas ocorreu de forma colaborativa, com cada integrante assumindo o protagonismo em frentes específicas, garantindo a integração final via Git:

* **Allana Bilar**: Desenvolveu a lógica de colisão entre jogadores (sistema de repulsão), a mecânica de transposição de tela (*wrap-around*), a organização da HUD e a documentação (README).
* **Amanda Pereira**: Responsável pela estruturação técnica do menu inicial e sistemas de navegação, além do refinamento das colisões com coletáveis.
* **Felipe de Queiroga**: Direção de Arte. Criou todos os assets em *pixel art* via Pixilart, definindo a identidade visual e design dos personagens.
* **Joaquim Goes**: Responsável pelo desenvolvimento da lógica estrutural do jogo. Focou na criação e gestão da mecânica dos coletáveis, no sistema de bônus, na implementação da movimentação base e do cálculo de pontuação.

## Desafios e Lições Aprendidas

### O Desafio da Velocidade Diagonal
Um dos maiores obstáculos técnicos foi a velocidade inconstante nas diagonais. Devido à soma vetorial, pressionar duas teclas (ex: `W` e `D`) fazia o personagem mover-se aproximadamente 40% mais rápido. Além disso, o Pygame processa apenas coordenadas inteiras, o que gerava imprecisões em velocidades decimais.

**A Solução: Sistema de Dívida de Movimento**
Implementamos uma função de normalização trigonométrica e um sistema de acumuladores:
1.  O excesso de pixel percorrido por arredondamento gera uma **"dívida"**.
2.  O personagem só executa o próximo movimento após "pagar" essa dívida com o valor acumulado dos frames seguintes.

### Evolução no Versionamento (Git/GitHub)
No início, o gerenciamento de *branches* e a resolução de conflitos via terminal foram processos desafiadores. Através da prática e do uso de ferramentas integradas (VS Code + GitHub), a equipe otimizou o fluxo de trabalho.
* **Lição:** A organização do ambiente de desenvolvimento e o gerenciamento estratégico de *commits* são tão vitais para o sucesso do projeto quanto a própria lógica de código.

## Galeria do Projeto
<img width="1869" height="972" alt="Captura de tela 2025-12-19 001648" src="https://github.com/user-attachments/assets/5d4cc3dc-bb5e-4e4c-9bfd-73173de59199" />

![WhatsApp Image 2025-12-19 at 00 40 39](https://github.com/user-attachments/assets/a2a599c5-6b6d-4f3b-87b7-26d454490d38)


<img width="1874" height="973" alt="Captura de tela 2025-12-18 203543" src="https://github.com/user-attachments/assets/9d2c5e49-f5b2-454b-a896-e0f6e8bf32c9" />
