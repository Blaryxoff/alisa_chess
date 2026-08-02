#!/usr/bin/env python3
"""
Direct test of the black color selection issue
"""

import os
import sys
sys.path.append('/Users/blaryx/www/chess')

from game import Game

def test_black_comp_move():
    """Test comp_move when user selects black (computer plays first move as white)"""

    print("Testing comp_move for black selection...")

    # Create a new game (same as when user starts)
    game = Game()

    # Simulate user selecting black
    game.set_user_color('BLACK')
    game.set_skill_state('WAITING_MOVE')

    print(f"Board FEN: {game.board.fen()}")
    print(f"User color: {game.get_user_color()}")
    print(f"Skill level: {game.skill_level}")
    print(f"Time level: {game.time_level}")

    # Try to make computer's first move (white's move)
    print("Calling comp_move()...")
    result = game.comp_move()

    if result:
        print(f"✅ SUCCESS: Computer move: {result}")
        print(f"New board FEN: {game.board.fen()}")
        return True
    else:
        print("❌ FAILED: comp_move() returned None")
        return False

if __name__ == "__main__":
    test_black_comp_move()
