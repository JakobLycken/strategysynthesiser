# Strategy Synthesis for Multi-Agent Games of Imperfect Information
This is a tool, written in Python 3.7, to find all almost-winning and surely-winning strategies from games expanded by a MKBSC

Authors: Jakob Lycken and Simon Westerlund

Supervisor: Dilian Gurov

If there are any questions regarding the tool, you can mail Jakob at jlycken@kth.se
## Best used with the MKBSC tool
This tool is best paired with the `mkbsc` tool found [here](https://github.com/HelmerNylen/mkbsc) with the `stratsynth` folder placed in the same root folder as the `mkbsc` folder.


## The `stratsynth` package

### Documentation
For documentation and a tutorial, please refer to [user guide](stratsynth/README.md)

### strategy_tester.py
 Here is the meat and potatoes of the synthesiser. In this file is the two classes `Agent_strat_synth()` and `Coalition_strat_synth()` that finds winning strategies for the individual agent and the coalition of agents respectivily.
### graph.py 
The classes `Graph()`, `Agent_graph(Graph)` and `Coalition_graph(Graph)` creates a traversable graph for agents and the coalition in the form of dictionaries made of vertices from `vertex.py`.
### vertex.py
Creates the vertices.

Since the program is a stand alone product it can be used to find winning strategies as long as there are .dot files creates in the same style as by the MKBSC-tool. 
