import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import encode
from balatro import *
import torch

ui = False
if ui:
    from IPython.display import display

run = Run(Deck.RED, stake=Stake.WHITE)
run.select_blind()
print(run.round)
print(encode.encode(run))

if ui:
    display(run)
