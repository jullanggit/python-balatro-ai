Getting Started
===============

Installation
------------

.. code-block:: bash

   pip install python-balatro

Basic Usage
-----------

Here's a simple example to get you started:

.. code-block:: python

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
        print(f"{i}: {joker.joker_type} ({joker.edition})")
    # Rearrange them
    run.move_joker(3, 0)

Next Steps
----------

*   Explore the full API documentation in :doc:`api_reference`.
*   Learn about the available Enums in :doc:`enums`.