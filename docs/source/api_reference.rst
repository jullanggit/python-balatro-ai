API Reference
=============

This section details the public-facing classes and their methods.

Run Class
---------

.. autoclass:: balatro.Run
   :members:
   :exclude-members: _repr_html_, _add_card, _add_joker, _buy_shop_item, _calculate_buy_cost, _calculate_sell_value, _chance, _close_pack, _create_joker, _deal, _destroy_card, _destroy_joker, _disable_boss_blind, _discard, _end_hand, _end_round, _game_over, _get_card_suits, _get_poker_hands, _get_random_card, _get_random_consumable, _get_random_joker, _get_round_goal, _is_face_card, _lucky_check, _new_ante, _next_blind, _open_pack, _populate_shop, _populate_shop_cards, _random_boss_blind, _repr_frame, _repr_in_shop, _repr_opening_pack, _repr_playing_blind, _repr_selecting_blind, _sort_hand, _trigger_scored_card, _trigger_held_card, _trigger_held_card_round_end, _update_shop_costs, _use_consumable
   :undoc-members:
   :show-inheritance:

   .. automethod:: __init__

   .. rubric:: Public Methods

   .. automethod:: buy_and_use_shop_item
   .. automethod:: buy_shop_item
   .. automethod:: choose_pack_item
   .. automethod:: discard
   .. automethod:: move_joker
   .. automethod:: next_round
   .. automethod:: play_hand
   .. automethod:: reroll
   .. automethod:: reroll_boss_blind
   .. automethod:: select_blind
   .. automethod:: sell_item
   .. automethod:: skip_blind
   .. automethod:: skip_pack
   .. automethod:: use_consumable

   .. rubric:: Public Properties

   .. autoattribute:: ante
   .. autoattribute:: ante_tags
   .. autoattribute:: blind
   .. autoattribute:: blind_reward
   .. autoattribute:: boss_blind
   .. autoattribute:: consumable_slots
   .. autoattribute:: consumables
   .. autoattribute:: deck
   .. autoattribute:: deck_breakdown
   .. autoattribute:: deck_cards
   .. autoattribute:: deck_cards_left
   .. autoattribute:: discards
   .. autoattribute:: hand
   .. autoattribute:: hand_size
   .. autoattribute:: hands
   .. autoattribute:: joker_slots
   .. autoattribute:: jokers
   .. autoattribute:: money
   .. autoattribute:: poker_hand_info
   .. autoattribute:: reroll_cost
   .. autoattribute:: round
   .. autoattribute:: round_score
   .. autoattribute:: shop_cards
   .. autoattribute:: shop_packs
   .. autoattribute:: shop_vouchers
   .. autoattribute:: stake
   .. autoattribute:: state
   .. autoattribute:: tags
   .. autoattribute:: vouchers