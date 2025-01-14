# balatro-python

[![WIP](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow)](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow)

A Python module inspired by the hit roguelike deckbuilder Balatro by LocalThunk. This project aims to capture the core gameplay and mechanics of Balatro in a clean, lightweight, and modular Python implementation for uses such as Machine Learning.

**Note:** This is a work in progress. While some core features are functional, this module is not to be used yet.

## Important Considerations

-   **Not a 1:1 Translation:** This project is a _Pythonic_ interpretation of Balatro's mechanics, not a direct Lua-to-Python port.
-   **Bugs/Edge Cases:** While I strive for accuracy, there are likely many subtle differences from the actual game.
-   **Seed Incompatibility:** Due to fundamental implementation differences, seeds are **not** compatible between this module and the original game.

## Getting Started

```python
from balatro import *

# Create a new run with the Red Deck
run = Run(Deck.RED)

# Get information about the current state
print(f"Current Ante: {run.ante}")
print(f"Current Blind: {run.blind}")
print(f"Available Money: {run.money}")

run.select_blind()

# Play a hand (example: playing the first two cards in your hand)
run.play_hand([0, 1])

# Discard cards (example: discarding the first card in your hand)
run.discard([0])

# See your jokers
jokers = run.jokers
for i, joker in enumerate(jokers):
    print(f"{i}: {joker.joker_type} ({joker.edition})")

...
```

## Disclaimer

This project is an independent fan creation and is not affiliated with or endorsed by LocalThunk, the creator of Balatro. All rights to Balatro belong to LocalThunk. This module is intended for educational and recreational purposes only.
