#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Transition:

    def __init__(self, src: int, dst: int, read: str, write:str, moviment_tape: str) -> None:
        self.__src = src
        self.__dst = dst
        self.__read = read
        self.__write = write
        self.__moviment_tape = moviment_tape

    def getOrigin(self)->int:    return self.__src

    def getDest(self)->int:      return self.__dst

    def getRead(self)->str:    return self.__read

    def getWrite(self)->str:     return self.__write

    def get_move_cursor(self)->int:      return +1 if self.__moviment_tape == 'D' else -1


class TuringMachine:

    def __init__(self, acceptance_state:int, init_state: int) -> None:
        self.__transitions = set()
        self.__acceptance_state = acceptance_state
        self.__init_state = init_state
        self.__blank = 'B'
        self.__cursor = 0
        self.__tape = list()

    #Adicionado transições para a máquina de Turing
    def add_transition(self, transition:Transition):
        if transition != None:  self.__transitions.add(transition)

    def readerTape(self) -> str:   return self.__tape[self.__cursor]

    def writerTape(self, char): self.__tape[self.__cursor]  = char

    def execute(self, jail: str) -> bool:
        # nao pode haver o simbolo de espaço em branco pertencente a cadeia de entrada
        if self.__blank in jail:    raise Exception('Símbolo de espaço em branco não pode estar na cadeia de entrada')

        # Resetando posição do cursor na fita
        self.__cursor = 0

        # escrevendo a cadeia no inicio da fita
        jail = jail.replace('-', '')
        jail += self.__blank
        self.__tape = list( map(lambda char:char, jail) )

        return self.process(self.__init_state, self.readerTape())

    # Função de transição recursiva
    def process(self, currentState:int, reader:str) -> bool:
        if currentState == self.__acceptance_state: return True

        # obetendo transiçoes validas de acordo com estado atual e char na fita apontado pelo cursor da maquina
        transisitions = list(filter(lambda t: t.getOrigin() == currentState and t.getRead() == reader, self.__transitions))
        transisition = transisitions[0] if len(transisitions) == 1 else None
        # Nao ha nenhuma transição valida logo a maquina rejeita a cadeia
        if not transisition:    return False

        # Realizando o efeito de acorodo com a a transição obtida
        self.writerTape(transisition.getWrite())
        self.__cursor += transisition.get_move_cursor()
        # Movimento do cursor inválido mantendo ele na primeira posição
        self.__cursor = 0 if self.__cursor < 0 else self.__cursor
        return self.process(transisition.getDest(), self.readerTape())


def main():

    ACCEPT = 'aceita'
    REJECT = 'rejeita'
    RIGHT = 'D'
    LEFT = 'E'

    numStates = int(input())
    if numStates <= 0:  raise Exception('Entrada inválida, input->' + str(numStates))
    states = list(range(numStates))

    row = input().split()
    #numSymbolsFinals = row[0]
    symbolsFinals = set(row[1:])
    
    row = input().split()
    #numSymbolsTape = row[0]
    symbolsTape = set(row[1:])

    acceptance_state_index = int(input())
    if acceptance_state_index >= numStates:
        raise Exception('Indice do estado de aceitação inválido, input->' + str(acceptance_state_index) + ', numero de estados->', numStates)

    turing_machine = TuringMachine(init_state=states[0], acceptance_state=states[acceptance_state_index])

    numTransiction = int(input())
    for _ in range(numTransiction):
        row = input().split()
        if not {RIGHT, LEFT}.intersection(row[4]):   raise Exception("Símbolo de movimento do cursor deve pertencer ao conjunto {E, D}")
        turing_machine.add_transition( Transition( src=int(row[0]), dst=int(row[2]), read=row[1], write=row[3], moviment_tape=row[4] ) )

    numInputJail = int(input())
    for _ in range(numInputJail):
        jail = input()

        try:
            result = turing_machine.execute(jail)
        except Exception as e:
            print('\nFALHA AO PROCESSAR A CADEIA: ', jail)
            raise e

        # True: ACCEPT / FALSE: REJECT
        print(ACCEPT) if result else print(REJECT)


if __name__ == '__main__':

    main()
