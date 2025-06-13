from balatro import *
from IPython.display import display

run = Run(Deck.RED, stake=Stake.WHITE, seed=1)
print(run.round_score)
run.select_blind()
print(run.round_score)
run.discard([1, 2, 5, 6, 7])
run.play_hand([2, 3, 4, 5, 7])
display(run)
print(run.round_score)
