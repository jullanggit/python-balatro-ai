# python-balatro

![WIP](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow)
![Python](https://img.shields.io/badge/python-3.13-blue)

A Python implementation of the hit roguelike deckbuilder **Balatro** by LocalThunk. This project aims to capture the core gameplay and mechanics of Balatro in a clean, lightweight, and modular Python package for uses such as machine learning.

**Note:** This is a work in progress. While some core features are functional, there are likely bugs and things left to be tested.

![game preview](game-preview.png)

## Important Considerations

-   **Not a 1:1 Translation:** This project is a _Pythonic implementation_ of Balatro, not a direct Lua-to-Python port.
-   **Bugs/Edge Cases:** While I strive for accuracy, with the nature of Balatro's many Jokers and complex interactions there are likely subtle differences between this module and the actual game.
-   **Seed Incompatibility:** Seeds are **not** compatible between this module and the original game. This is disappointing, but it would take much work to ensure compatibility, maybe work for a future date.

## Getting Started

```python
from balatro import *

# Create a new run with the Red Deck on White Stake
run = Run(Deck.RED, stake=Stake.WHITE)

# Get information about the current state
print(f"Current Ante: {run.ante}")
print(f"Current Blind: {run.blind}")
print(f"Available Money: {run.money}")

# Select the Small Blind
run.select_blind()
# Or skip it
run.skip_blind()

# Play a hand (example: playing the first five cards in your hand)
run.play_hand([0, 1, 2, 3, 4])

# Discard cards (example: discarding the last five cards in your hand)
run.discard([3, 4, 5, 6, 7])

...

# Buy the first pack in the shop
run.buy_shop_item(2, 0)

# Pick the first item
run.choose_pack_item(0)
# Or skip the pack
run.skip_pack()

...

# Use a consumable on some cards in your hand
run.use_consumable(1, [1, 3, 7])
# Or sell it
run.sell_item(1, 1)

...

# See your jokers
for i, joker in enumerate(run.jokers):
    print(f"{i}: {joker}")
# Rearrange them
run.move_joker(3, 0)
```

## Disclaimer

This project is an independent fan creation and is not affiliated with or endorsed by LocalThunk, the creator of Balatro. This module is intended for educational and non-commercial purposes only. All rights to Balatro, including its art and design, belong to LocalThunk.
