import encode
from balatro import *
import torch

ui = False
if ui:
    from IPython.display import display

run = Run(Deck.RED, stake=Stake.WHITE)
print(encode.encode(run))

if ui:
    display(run)
