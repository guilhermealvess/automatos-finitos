# Classe para os estados dentro do grafo
class Node:

    def __init__(self, value: str) -> None:
        self.__value = value

    def getValue(self) -> str:
        return self.__value

#Classe para representar as ligaÃ§Ãµes dos estados dentro do grafo
class Edge:

    def __init__(self, src: Node, dst: Node, cost: str, pop:str, push:str) -> None:
        self.__origin = src
        self.__dst = dst
        self.__cost = cost
        self.__popStack = pop
        self.__pushStack = push

    def __setPushStack(self, push):
        if push == "-":
            return

    def getOrigin(self) -> Node:
        return self.__origin

    def getDest(self) -> Node:
        return self.__dst

    def getCost(self) -> str:
        return self.__cost

    def getPopStack(self) -> str:
        return self.__popStack

    def getPushStack(self) -> str:
        return list(reversed(self.__pushStack))


#Classe para representar o autÃ´mato como um grafo
class Automaton:

    def __init__(self, start:Node, acceptStates: set, symbols:set, stackSymbols:list) -> None:
        self.__acceptStates = acceptStates
        self.__startNode = start
        self.__edges = set()
        self.__symbols = symbols
        self.__stackSymbols = stackSymbols
        self.__stack = [stackSymbols[-1]]

    def reset_stack(self):
        self.__stack = ['Z']

    def getSymbolOnTop(self) -> str:
        if len(self.__stack) == 0:
            return None
        return self.__stack[-1]

    def getAcceptState(self) -> set:
        return self.__acceptStates

    def getStartState(self) -> Node:
        return self.__startNode

    def insertEdge(self, src: Node, dst: Node, cost: str, pop: str, push:str):
        newEdge = Edge(src, dst, cost, pop, push)
        self.__edges.add(newEdge)

    def processState(self, stateCurrent:Node, char: str, stack:list) -> tuple:
        if not self.__symbols.intersection({char}):
            raise ValueError('Cadeia inválida')

        for edge in self.__edges:
            if edge.getOrigin() == stateCurrent and edge.getCost() == char and edge.getPopStack() == stack[-1]:
                self.__stack.pop()
                for symbol in edge.getPushStack():
                    if symbol != "-":
                        self.__stack.append(symbol)
                return edge.getDest(), self.__stack

        # Processando uma cadeia vazia
        edges = set(filter(lambda e: e.getCost() == char == "-" and e.getOrigin() == stateCurrent and e.getPopStack() == stack[-1], self.__edges))
        if len(edges) > 0:
            self.__stack.pop()
            for symbol in edge.getPushStack():
                self.__stack.append(symbol)
            return edge.getDest(), self.__stack
        else:
            raise ValueError('Não existe um caminho válido esta transição: (Q{}, {}, {})'.format(stateCurrent.getValue(), char, ''.join(list(reversed(self.__stack)))))
        

    def isAcceptState(self, state:Node) -> bool:
        return self.__acceptStates.intersection({state})

    def show(self):
        for edge in self.__edges:
            print("Q{} -> {} -> Q{}".format(edge.getOrigin().getValue(), edge.getCost(), edge.getDest().getValue()))


# FunÃ§Ã£o que executa uma cadeia de caracter no autômato
def processWord(automaton:Automaton, word:str) -> bool:
    automaton.reset_stack()
    currentState = automaton.getStartState()
    stack = [automaton.getSymbolOnTop()]
    for char in word:
        try:
            currentState, stack = automaton.processState(currentState, char, stack)
        except Exception as e:
            return False
    
    if not automaton.isAcceptState(currentState):
        return False
    
    return True

def main():
    ACCEPT = "aceita"
    REJECT = "rejeita"
    STATE_INIT = "0"
    SYMBOL_EMPTY = "-"
    FIRST_STACK_SYMBOLS = "Z"

    stateInit = Node(value=STATE_INIT)
    nodes = {STATE_INIT: stateInit}

    numStates = int(input())

    row = input().split()
    numSymbols = int(row[0])
    symbols = set(row[1:] + [SYMBOL_EMPTY])

    row = input().split()
    if row[-1] != FIRST_STACK_SYMBOLS:
        raise ValueError('Símbolo de pilha inválido')
    stackSymbols = list(map(lambda s: s.upper(), row[1:]))

    row = input().split()
    numStateFinish = int(row[0])
    # Conjunto dos estados de aceitaÃ§Ã£o
    def add_in_acceptance_state(state):
        if not nodes.get(state, False):
            new_state = Node(value=state)
            nodes[state] = new_state
            return new_state
        return nodes[state]
    acceptanceState = set(map(add_in_acceptance_state, row[1:]))
    for state in acceptanceState:
        nodes[state.getValue()] = state

    numTransition = int(input())
    if numTransition > 50:
        exit()


    graph = Automaton(start=stateInit, acceptStates=acceptanceState, symbols=symbols, stackSymbols=stackSymbols)
    for _ in range(numTransition):
        row = input().split()

        # Mapeando os estados para manter as referências aos objetos no grafo
        if not nodes.get(row[0]):
            nodes[row[0]] = Node(value=row[0])

        if not nodes.get(row[3]):
            nodes[row[3]] = Node(value=row[3])

        # Inserindo os vertices no grafo
        graph.insertEdge(src=nodes.get(row[0]), dst=nodes.get(row[3]), cost=row[1], pop=row[2], push=row[4])

    numInputsWords = int(input())

    # Coletando e processando as cadeias e armazenando o resultado
    output = []
    OUTPUT = ['aceita', 'aceita', 'rejeita', 'rejeita', 'rejeita', 'rejeita', 'aceita', 'rejeita', 'aceita', 'rejeita']
    for i in range(numInputsWords):

        result = processWord(graph, input() + SYMBOL_EMPTY)

        if result:
            output.append(ACCEPT)
            print(ACCEPT)
        else:
            output.append(REJECT)
            print(REJECT)

        """ print(OUTPUT[i].upper() + '\n')

    if OUTPUT == output:
        print('\n******* OK *******\n')
    else:
        print('\n******* ERR *******\n') """


if __name__ == '__main__':
    main()