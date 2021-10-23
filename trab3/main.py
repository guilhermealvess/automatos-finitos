

class State:

    def __init__(self, value) -> None:
        self.__value = value

    def getValue(self): return self.__value


class Transition:

    def __init__(self, src: State, dst: State, before: str, later:str, moviment_tape: str) -> None:
        self.__src = src
        self.__dst = dst
        self.__before = before
        self.__later = later
        self.__moviment_tape = moviment_tape

    def getOrigin(self):    return self.__src

    def getDest(self):      return self.__dst

    def getBefore(self):    return self.__before

    def getLater(self):     return self.__later

    def getMovimentTape(self):      return self.__moviment_tape


class Automaton:

    def __init__(self, state_accept:set, init_state: State) -> None:
        self.__transitions = set()
        self.__state_accept = state_accept
        self.__init_state = init_state

    def add_transition(self, transition:Transition):
        if transition != None:  self.__transitions.add(transition)

    def show(self):
        ...

    def isAcceptState(self, state: State) -> bool:
        return self.__state_accept.intersection({state})

    def execute(self, word: str, tape: list) -> bool:
        tape = list()
        return self.process(self.__init_state, word, tape)

    def process(self, currentState, word, tape):
        if tape == []:
            return True
        return self.process(currentState, word, tape)


def make_states(numStates):
    nodes = dict()
    for state in range(numStates):
        nodes[state] = State(value=state)
    return nodes


def main():

    ACCEPT = 'aceita'
    REJECT = 'rejeita'
    STATE_INITIAL = 0

    numStates = int(input())
    states_mapper = make_states(numStates)

    row = input().split()
    #numSymbolsFinals = row[0]
    symbolsFinals = set(row[1:])
    
    row = input().split()
    #numSymbolsTape
    symbolsTape = set(row[1:])

    index = int(input())
    if index >= numStates:
        raise Exception('')

    machine = Automaton(init_state=states_mapper.get(STATE_INITIAL, None))

    numTransiction = int(input())
    for _ in range(numTransiction):
        row = input()
        machine.add_transition( Transition( src=row[0], dst=row[2], before=row[1], later=row[3], moviment=row[4]) )

    numJail = int(input())
    for _ in range(numJail):
        word = input()

        result = machine.execute(word)

        if result:
            print(ACCEPT)
        else:
            print(REJECT)


if __name__ == '__main__':

    main()