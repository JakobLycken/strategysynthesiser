from .graph import *
from copy import deepcopy

class Agent_strat_synth():
    def __init__(self, game_graph, win_nodes, lose_nodes, start_node):
        '''

        :param game_graph:
        :param win_nodes:
        :param lose_nodes:
        :param start_node:
        '''
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_node = start_node
        self.game = game_graph
        self.strats = []
        self.winning_strats = []
        self.visited_nodes = []
        self.start_game()

    def start_game(self):
        """
        Initiates traverse_game from the start node.
        """
        self.traverse_game(self.start_node)

    def traverse_game(self, current_node):
        '''
        Traverse the game and finds all winning strategies for the agent.

        :param current_node: The current node for the agent
        :return: Returns all winning strategies for the agent after all recursions are complete.
        '''
        self.visited_nodes.append(current_node)

        if current_node in self.win_nodes:
            self.strats.append([current_node])
            strategy = {}

            for item in self.strats:
                if len(item) == 2:
                    strategy[item[0]] = item[1]
                else:
                    strategy[item[0]] = "-"
            self.winning_strats.append(deepcopy(strategy))  # Saves the strategy
            self.visited_nodes.pop()
            self.strats.pop()
            return

        if current_node in self.lose_nodes:
            self.strats.pop()
            self.visited_nodes.pop()
            return
        next_nodes = self.game[current_node].get_adjacent_vert()

        for i in range(len(next_nodes)):
            if self.strats and self.strats[-1][0] == current_node:  # Fixing a multi-route problem
                self.strats[-1] = [current_node, self.game[current_node].get_actions(next_nodes[i])]
                self.visited_nodes[-1] = current_node
            else:
                self.strats.append([current_node, self.game[current_node].get_actions(next_nodes[i])])

            if next_nodes[i].get_id() not in self.visited_nodes:
                self.traverse_game(next_nodes[i].get_id())

        if self.strats:
            self.visited_nodes.pop()
            self.strats.pop()
        return


class Coalition_strat_synth():
    '''
    A class to synthesise strategies for a coalition of agents.

    :param gamename: The name of the game.
    :param noa: Number of agents. Default is 2
    :param win_nodes: The name of the win state. Default is {Win}
    :param lose_nodes: The name of the win state. Default is {Lose}
    :param start_nodes: The name of the win state. Default is {Start}
    '''

    def __init__(self, gamename, noa=2, win_nodes='{Win}', lose_nodes='{Lose}', start_nodes='{Start}'):
        self.game = ""
        self.filename = gamename
        self.win_nodes = win_nodes
        self.lose_nodes = lose_nodes
        self.start_nodes = start_nodes
        self.agent_strats = []
        self.current_test = []
        self.end_of_strat = []
        self.almost_surely = []
        self.surely = []
        self.nr_of_agents = noa
        #self.start_test()

    def start_test(self):
        '''
        Runs the program

        :return: Prints out all winning strategies for the coalition of agents.
        '''
        test_game = Coalition_graph(self.filename)
        test_game.deltaDic()
        self.game = test_game.get_graph()
        self.multi_agent(self.nr_of_agents)
        self.setCoalitionNodes()
        self.lister()
        self.show_strats()

    def setCoalitionNodes(self):
        '''
        Checks if there are multiple winning and losing nodes
        and makes sure the coalition can handle them
        :return:
        '''
        i=0

        if type(self.win_nodes) == list:
            for state in self.win_nodes:
                for x in range(self.nr_of_agents-1):
                    self.win_nodes[i] += ", " + state
                i+=1

        else:
            win_nodes = deepcopy(self.win_nodes)
            for i in range(self.nr_of_agents - 1):
                self.win_nodes += ", " + win_nodes
        i=0

        if type(self.lose_nodes) == list:
            for state in self.lose_nodes:
                for x in range(self.nr_of_agents-1):
                    self.lose_nodes[i] += ", " + state
                i+=1

        else:
            lose_nodes = deepcopy(self.lose_nodes)
            for i in range(self.nr_of_agents - 1):
                self.lose_nodes += ", " + lose_nodes

        start_nodes = deepcopy(self.start_nodes)

        for i in range(self.nr_of_agents - 1):
            self.start_nodes += ", " + start_nodes



    def tester(self, current_node):
        '''
        Tests the current

        :param current_node: the node to be evaluated
        :return: stores the result of the strategy in end_of_strat.
        '''

        try:
            if current_node in self.win_nodes:
                self.end_of_strat.append("Win")
                return

            if current_node in self.lose_nodes:
                self.end_of_strat.append("Lose")
                return
            list_current_node = current_node.split(', {')

            for i in range(len(list_current_node) - 1):
                list_current_node[i + 1] = '{' + list_current_node[i + 1]
            action = self.current_test[0][list_current_node[0]]

            for i in range(len(list_current_node) - 1):
                action += ', ' + self.current_test[i + 1][list_current_node[i + 1]]

            if "(-)" in action: action = "-"
            node = self.game[current_node].get_adjacent_vert()
            jump = False

            for i in range(len(node)):
                if action in self.game[current_node].get_actions(node[i]):
                    self.tester(node[i].get_id())
                    jump = True

            if not jump:
                self.end_of_strat.append("Lose")

        except:
            self.end_of_strat.append("Lose")

    def lister(self, list_nr=0, item=None):
        '''
        Populates current_test (current coalition strategy) with Agent strategies, initiates the test, de-populate and keep
        going until all strategies has been tested.

        :param list_nr: which agent's strategy list is being added to the current coalition strategy test
        :param item: An agent's strategy
        :return: All winning strategies
        '''
        if item:
            self.current_test.append(item)

        for item in self.agent_strats[list_nr]:

            if list_nr < len(self.agent_strats) - 1:
                self.lister(list_nr + 1, item)

            else:
                self.current_test.append(item)
                self.end_of_strat = []
                #self.cur_strat()
                self.tester(self.start_nodes)

                if "Win" in self.end_of_strat and "Lose" in self.end_of_strat:
                    self.almost_surely.append(deepcopy(self.current_test))

                elif "Win" in self.end_of_strat:
                    self.surely.append(deepcopy(self.current_test))

                else:
                    pass
                self.current_test.pop()

        if self.current_test:
            self.current_test.pop(len(self.current_test) - 1)
        return

    def multi_agent(self, nr):
        '''
        Finds all winning strategies for each agent.

        :param nr: How many agent's are part of the game
        :return: Adds all agent's winning strategies to self.agent_strats as individual lists
        '''
        for agent_nr in range(nr):
            game_graph = Agent_graph(self.filename + str(agent_nr))
            game_graph.deltaDic()
            graph_paths = game_graph.get_graph()
            strategy = Agent_strat_synth(graph_paths, self.win_nodes, self.lose_nodes, self.start_nodes)
            self.agent_strats.append(strategy.winning_strats)

    #Used for debugging
    def cur_strat(self):
        '''
        This function is/was used for debugging the lister() function.

        :return: Prints out the strategies that are currently being tested.
        '''
        i = 0

        for item in self.current_test:
            print("agent", str(i), item)
            i += 1

        print(len(self.current_test))

    def show_strats(self):
        """
        Prints out all winning strategies (almost-surely winning and surely-winning)
        or that there are no winning strategies
        """

        if self.almost_surely:
            print("Almost-surely winning strats:")
            as_i = 1

            for coal_strat in self.almost_surely:
                i = 0
                print("Strat: {}".format(as_i))

                for agent_strat in coal_strat:
                    print("agent{}: {}".format(i, agent_strat))
                    i += 1

                as_i += 1

        if self.surely:
            print("Surely winning strats:")
            s_i = 1

            for coal_strat in self.surely:
                i = 0
                print("Strat: {}".format(s_i))

                for agent_strat in coal_strat:
                    print("agent{}: {}".format(i, agent_strat))
                    i += 1

                s_i += 1

        if not self.surely and not self.almost_surely:
            print("No winning strategies found.")
