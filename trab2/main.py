# Classe para os estados dentro do grafo
class Node:

    def __init__(self, value: str) -> None: self.__value = value

    def getValue(self) -> str:  return self.__value

#Classe para representar as ligaÃ§Ãµes dos estados dentro do grafo
class Edge:

    def __init__(self, src: Node, dst: Node, cost: str, pop:str, push:str) -> None:
        self.__origin = src
        self.__dst = dst
        self.__cost = cost
        self.__popStack = pop
        self.__pushStack = push

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


#Classe para representar o autômato como um grafo
class Automaton:

    def __init__(self, start:Node, acceptStates: set, symbols:set, stackSymbols:list) -> None:
        self.__acceptStates = acceptStates
        self.__startNode = start
        self.__edges = set()
        self.__symbols = symbols
        self.__stackSymbols = stackSymbols

    def getAcceptState(self) -> set:    return self.__acceptStates

    def getStartState(self) -> Node:    return self.__startNode

    def insertEdge(self, src: Node, dst: Node, cost: str, pop: str, push:str):
        newEdge = Edge(src, dst, cost, pop, push)
        self.__edges.add(newEdge)

    def getTopElement(self, s:list):    return s[-1] if s else []

    def updateStack(self, s:list, edge:Edge):
        new_stack = s.copy()
        new_stack.pop()
        for symbol in edge.getPushStack():
            if symbol != "-":
                new_stack.append(symbol)
        return new_stack

    def verify(self, stateCurrent:Node):
        if not self.isAcceptState(stateCurrent):
            return False
        return True

    def consumesWord(self, edge:Edge, word:str)->str:
        if edge.getCost() == word[0]:
            return word[1:]
        return word

    def run(self, stateCurrent:Node, word:str, stack:list):
        if list(word):
            char = word[0]
        else:
            return self.verify(stateCurrent)

        edges = set(filter(lambda e: e.getOrigin() == stateCurrent and (e.getCost() == char or e.getCost() == "-") and e.getPopStack() == self.getTopElement(stack), self.__edges))
        transictions = list(map(lambda e:(e.getDest(), self.consumesWord(e, word), self.updateStack(stack, e)), edges))

        if not transictions:    return False

        for newState, newWord, newStack in transictions:
            if self.run(newState, newWord, newStack):   return True
        return False

    def isAcceptState(self, state:Node) -> bool:
        return self.__acceptStates.intersection({state})

    def show(self):
        for edge in self.__edges:
            print("Q{} -> {} -> Q{}".format(edge.getOrigin().getValue(), edge.getCost(), edge.getDest().getValue()))


# Funsão que executa uma cadeia de caracter no autômato
def processWord(automaton:Automaton, word:str) -> bool:
    #print('PALAVRA A PROCESSAR: ', word)

    currentState = automaton.getStartState()
    stack = ['Z']

    return automaton.run(currentState, word, stack)
    

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
    if numTransition > 50:  exit()


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
    for _ in range(numInputsWords):

        w = input()

        print(ACCEPT) if processWord(graph, w + SYMBOL_EMPTY) else print(REJECT)


if __name__ == '__main__':

    main()