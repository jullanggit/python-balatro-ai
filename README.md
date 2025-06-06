# python-balatro

## AI
- This project has been [forked](https://github.com/pjpuzzler/python-balatro) and is currently being extended with an AI

![WIP](https://img.shields.io/badge/Status-Work%20in%20Progress-yellow)
![Python](https://img.shields.io/badge/python-3.13-blue)

A Python implementation of the hit roguelike deckbuilder [**Balatro**](https://www.playbalatro.com) by LocalThunk. This project aims to capture the core gameplay mechanics of Balatro in an easy-to-use package so that developers can experiment with tasks such as machine learning.

**Note:** This is a work in progress. While the majority of core features are functional, there are likely bugs and things left to be tested.

![main preview](resources/previews/main_preview.png)

## Important Considerations

-   **Not a 1:1 Translation:**

    -   Little to no design patterns were reused from the game's code (written in Lua). This was done for several reasons, including:
        -   To maintain a natural and _Pythonic_ approach
        -   To challenge myself to write a unique implementation
        -   To avoid sifting through thousands of lines of code (i.e. my sanity)

-   **Bugs/Edge Cases:**

    -   As a result of this, there will likely be very subtle differences between this module and the actual game.
    -   I encourage you to report any problems/inconcistencies you find in the [**Issues**](../../issues) tab.

-   **Seed Incompatibility:**

    -   Likewise, seeds are **not** compatible between this module and the actual game, perhaps a project for a future date.

## Getting Started

```python
from balatro import *
```

```python
# Create a new run with the Yellow Deck on White Stake
run = Run(Deck.YELLOW, stake=Stake.WHITE)

run  # Rich Jupyter Notebook display
```

![selecting blind preview](resources/previews/selecting_blind_preview.png)

```python
# Alternatively, manually get information about the current state
print(f"Current Ante: {run.ante}")
print(f"Current Blind: {run.blind.value}")
print(f"Current Money: ${run.money}")
```

> Current Ante: 1\
> Current Blind: Small Blind\
> Current Money: $14

```python
# Select the Small Blind
run.select_blind()
# Or skip it
# run.skip_blind()

run
```

![playing blind preview](resources/previews/playing_blind_preview.png)

```python
# Play the flush
run.play_hand([0, 1, 2, 4, 6])
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

![shop preview](resources/previews/shop_preview.png)

```python
# Buy the Hallucination joker
run.buy_shop_card(0, 0)  # (item index, use (if consumable))

# Buy the Voucher
# run.redeem_shop_voucher(0) # (item index)

run
```

![shop preview 2](resources/previews/shop_preview2.png)

```python
# Open the Buffoon Pack
run.open_shop_pack(0) # (item index)

run
```

![opening pack preview](resources/previews/opening_pack_preview.png)

```python
# Take the Blueprint
run.choose_pack_item(0)
# Or skip the pack
# run.skip_pack()

# Move the Blueprint to the left
run.move_joker(1, 0)

# Use the Hermit
run.use_consumable(0)

# Proceed to the next round
run.next_round()
```

## Disclaimer

This project is an independent fan creation and is not affiliated with or endorsed by LocalThunk, the creator of Balatro. This module is intended for educational and non-commercial purposes only. All rights to Balatro, including its art and design, belong to LocalThunk.
