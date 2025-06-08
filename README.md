# Derivative Dash

Derivative Dash é um jogo educacional desenvolvido em Python/Pygame que integra conceitos do Cálculo Diferencial à
mecânica de jogos digitais. O objetivo principal é explorar, de forma interativa e lúdica, a relação entre derivadas,
pontos críticos e otimização, tornando o aprendizado de cálculo mais dinâmico e visual.

## Objetivos

- Criar uma ferramenta interativa para o ensino de derivadas.
- Demonstrar aplicações práticas de cálculo diferencial em tempo real.
- Explorar formas lúdicas de aprendizado através da tecnologia.

## Fundamentos Matemáticos

O projeto aplica conceitos fundamentais do cálculo diferencial:

- **Derivação analítica de funções polinomiais** para definir a dinâmica da pista.
- **Identificação de máximos e mínimos** (f’(x) = 0) como obstáculos no percurso.
- **Otimização** via ajuste da derivada para alcançar velocidades ideais.

## Como Funciona

No Derivative Dash, o jogador controla a inclinação de uma pista (representada pela derivada da função posição, f′(x)),
influenciando diretamente a velocidade de um veículo. Pontos críticos (onde a derivada é zero) tornam-se obstáculos
estratégicos, exigindo precisão matemática para evitar colisões e maximizar a performance.

- A inclinação da pista (derivada) determina aceleração e velocidade.
- Pontos de derivada zero são zonas de risco e exigem atenção.
- O sinal da derivada (negativo para descidas, positivo para subidas) simplifica a física do movimento.
- Erros de cálculo resultam em colisões, reforçando a importância da precisão.

A visualização via Pygame transforma conceitos abstratos (subidas, descidas, curvas) em desafios concretos, tornando a
otimização de funções um exercício prático e envolvente.

## Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://gitlab.com/AllysonFilipi/derivative-dash.git
   cd derivative-dash
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requeriments.txt
   ```

3. **Execute o jogo:**
   ```bash
   python3 main.py
   ```

## Como Jogar

- Use os controles indicados na tela para ajustar a inclinação da pista.
- Evite colisões nos pontos críticos (máximos, mínimos e descontinuidades).
- Busque otimizar a velocidade do veículo ajustando corretamente a derivada.

## Estrutura do Projeto

O projeto segue uma arquitetura modular:

```
derivative-dash/
├── assets/            # Recursos gráficos e sonoros
├── config/            # Configurações do jogo
│   └── settings.py    # Configurações gerais
├── src/               # Código fonte
│   ├── controllers/   # Controladores de entrada
│   ├── engine/        # Motor do jogo
│   ├── models/        # Modelos de dados
│   ├── utils/         # Funções utilitárias
│   └── views/         # Renderização e interface gráfica
└── main.py            # Ponto de entrada do jogo
```

### Componentes Principais

- **GameEngine**: Coordena todos os componentes do jogo
- **GameState**: Mantém o estado atual do jogo
- **Renderer**: Responsável pela renderização gráfica
- **InputHandler**: Processa entrada do usuário
- **Track**: Representa a pista e suas propriedades matemáticas
- **Car**: Representa o veículo controlado pelo jogador

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Autores

- Allyson Filipi Lopes de Oliveira
- Mariah Eduarda Pereira Bócoli
- Fernanda Brito Costa da Silva
- Matheus Victor Henrique da Silva
- Joatan Carlos Farias Feitosa
- Gustavo Henrique de Jesus da Silva

---

> Derivative Dash: Aprenda cálculo brincando!
