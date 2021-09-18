# Classe para os estados dentro do grafo
class Node:

    def __init__(self, value: str) -> None:
        self.__value = value

    def getValue(self) -> str:
        return self.__value

#Classe para representar as ligaÃ§Ãµes dos estados dentro do grafo
class Edge:

    def __init__(self, src: Node, dst: Node, cost: str) -> None:
        self.__origin = src
        self.__dst = dst
        self.__cost = cost

    def getOrigin(self) -> Node:
        return self.__origin

    def getDest(self) -> Node:
        return self.__dst

    def getCost(self) -> str:
        return self.__cost


#Classe para representar o autÃ´mato como um grafo
class Automaton:

    def __init__(self, start:Node, acceptStates: set, symbols:set ) -> None:
        self.__acceptStates = acceptStates
        self.__startNode = start
        self.__edges = set()
        self.__symbols = symbols

    def getAcceptState(self) -> set:
        return self.__acceptStates

    def getStartState(self) -> Node:
        return self.__startNode

    def insertEdge(self, src: Node, dst: Node, cost: str):
        newEdge = Edge(src, dst, cost)
        self.__edges.add(newEdge)

    def processState(self, stateCurrent:Node, char: str) -> set:
        if not self.__symbols.intersection({char}):
            raise ValueError('Cadeia invÃ¡lida')

        # Processando uma cadeia vazia
        if char == "-":
            return {stateCurrent}

        edges = set(filter(lambda edge: edge.getOrigin() == stateCurrent and edge.getCost() == char, self.__edges))
        return set(map(lambda edge: edge.getDest(), edges))


    def isAcceptState(self, states:set) -> bool:
        return self.__acceptStates.intersection(states)

    def show(self):
        for edge in self.__edges:
            print("Q{} -> {} -> Q{}".format(edge.getOrigin().getValue(), edge.getCost(), edge.getDest().getValue()))


# FunÃ§Ã£o que executa uma cadeia de caracter no autÃ´mato
def run(automaton: Automaton, word:str) -> bool:

    currentStates = {automaton.getStartState()}
    # Varrendo a cadeia de entrada
    for char in word:
        setStates = set()
        for currentState in currentStates:
            setStates = setStates.union(automaton.processState(currentState, char))

        currentStates = setStates
        if not currentStates:
            return False

    if not automaton.isAcceptState(currentStates):
        return False

    # Retorna True para caso a cadeia seja aceita pelo autÃ´mato e False caso contrÃ¡rio
    return True

def main():
    ACCEPT = "aceita"
    REJECT = "rejeita"
    STATE_INIT = "0"
    SYMBOL_EMPTY = "-"

    nodes = dict()

    numStates = int(input())

    row = input().split()
    numSymbols = int(row[0])
    symbols = set(row[1:] + [SYMBOL_EMPTY])

    row = input().split()
    numStateFinish = int(row[0])
    # Conjunto dos estados de aceitaÃ§Ã£o
    acceptanceState = set(map(lambda state: Node(value=state), row[1:]))
    for state in acceptanceState:
        nodes[state.getValue()] = state

    numTransition = int(input())
    if numTransition > 50:
        exit()

    # Criando o grafo do autÃ´mato
    stateInit = nodes[row[1]]
    nodes[STATE_INIT] = Node(value=STATE_INIT)
    stateInit = nodes[STATE_INIT]

    graph = Automaton(start=stateInit, acceptStates=acceptanceState, symbols=symbols)
    for _ in range(numTransition):
        row = input().split()

        # Mapeando os estados para manter as referÃªncias aos objetos no grafo
        if not nodes.get(row[0]):
            nodes[row[0]] = Node(value=row[0])

        if not nodes.get(row[2]):
            nodes[row[2]] = Node(value=row[2])

        # Inserindo os vertices no grafo
        graph.insertEdge(src=nodes.get(row[0]), dst=nodes.get(row[2]), cost=row[1])

    # print('ESTADOS', nodes)
    # PRINT DAS LIGAÃ‡Ã•ES DO AUTÃ”MATO. Ex: Q0 -> a -> Q1
    # graph.show()

    numWords = int(input())

    # Coletando e processando as cadeias e armazenando o resultado
    output = list()
    for _ in range(numWords):
        result = run(graph, input())

        if result:
            output.append(ACCEPT)
            print(ACCEPT)
        else:
            output.append(REJECT)
            print(REJECT)


if __name__ == '__main__':
    main()