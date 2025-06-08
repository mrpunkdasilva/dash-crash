#!/usr/bin/env python3
"""
Derivative Dash - Um jogo educacional sobre cálculo diferencial
"""

from src.engine.game_engine import GameEngine

def main():
    """Função principal do jogo"""
    game = GameEngine()
    game.run()

if __name__ == "__main__":
    main()