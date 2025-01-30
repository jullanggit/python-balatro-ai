# python-balatro

![WIP](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow)
![Python](https://img.shields.io/badge/python-3.13-blue)

A Python implementation of the hit roguelike deckbuilder [**Balatro**](https://www.playbalatro.com) by LocalThunk. This project aims to capture the core gameplay and mechanics of Balatro in a clean, lightweight, and modular Python package for uses such as machine learning.

**Note:** This is a work in progress. While some core features are functional, there are likely bugs and things left to be tested.

![main preview](resources/previews/main_preview.png)

## Important Considerations

-   **Not a 1:1 Translation:**

    -   This project is a _Pythonic implementation_ of Balatro, not a direct Lua-to-Python translation.
    -   Thanks to LocalThunk the source code for the game is readily available, but the goal of this project was to avoid relying on it heavily so as to keep things as clean and Pythonic.

-   **Bugs/Edge Cases:**

    -   I try my best to sniff out as many edge cases as possible, sifting through the source code for specifics when needed.
    -   However with Balatro's many Jokers and complex interactions there will inevitably be subtle differences between this module and the actual game mechanics.

-   **Seed Incompatibility:**

    -   Seeds are **not** compatible between this module and the actual game.
    -   This is disappointing, but it would take much, much, much, work to do so, perhaps a project for a future date.

## Getting Started

```python
from balatro import *
```

```python
# Create a new run with the Black Deck on Black Stake
run = Run(Deck.BLACK, stake=Stake.BLACK)

run  # Display it
```

![selecting blind preview](resources/previews/selecting_blind_preview.png)

```python
# Alternatively, manually get information about the current state
print(f"Current Ante: {run.ante}")
print(f"Current Blind: {run.blind}")
print(f"Available Money: {run.money}")
```

> Current Ante: 1\
> Current Blind: Blind.SMALL_BLIND\
> Available Money: 4

```python
# Select the small blind
run.select_blind()

# Or skip it
# run.skip_blind()

run
```

![playing blind preview](resources/previews/playing_blind_preview.png)

```python
# Play the flush
run.play_hand([0, 1, 2, 5, 7])

# Alternatively, discard
# run.discard([3, 4, 6])

run
```

WIP: Cashing Out Screen

```python
# Continue to the shop
run.cash_out()

run
```

```python
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
