# Strategy Synthesis for Multi-Agent Games of Imperfect Information
This is a tool, written in Python 3.7, to find all almost-winning and surely-winning strategies from games expanded by a MKBSC

Authors: Jakob Lycken and Simon Westerlund

Supervisor: Dilian Gurov


---
Requirements
TBD
---
Quick documentation

###Usage example

Since the program is a stand alone product it can be used to find winning strategies as log as there are .dot files. 

```python
#!/usr/bin/env python3
from strategy_tester import *




gamename = "supervisor"
Coalition_strat_synth(gamename, noa=2)

```

