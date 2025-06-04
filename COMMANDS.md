## Start a run
```python
from balatro import *
# Plasma Deck, White Stake
run = Run(Deck.PLASMA, stake=Stake.WHITE)
```

## Blind Selection
```python
# Select Blind
run.select_blind()
# Skip Blind
run.skip_blind()
```

## Round
```python
# Play a Hand (Order is 4th card, 2nd, 3rd, 8th and 6th in Hand)
run.play_hand([3, 1, 2, 7, 5])
# Discard a Hand (First four cards here)
run.discard([0, 1, 2, 3]) 
# Use a consumable (This also works outside of a round for most, in this example
# the consumable in the first slot gets used and does something to the 6th and 1st card. 
# For most consumables you do not have to specify the cards)
run.use_consumable(0, [5, 0])
# Once the required score is reached, cash out and enter shop
run.cash_out()
```

## Shop (Main Interface)
```python
# Buy the Card (Joker/Consumable/whatever) from the first Slot
run.buy_shop_card(0, 0)
# Buy and use the Card from the second Slot
run.buy_shop_card(1, 1)
# Buy the voucher on the first slot
run.redeem_shop_voucher(0)
# Buy the Booster Pack on the second slot
run.open_shop_pack(1)
# Reroll
run.reroll()
```

## Booster Pack
```python
# Choose the first Booster Pack option
run.choose_pack_item(0)
# Skip the Booster Pack
run.skip_pack()
```
