#!/usr/bin/python


import sys


class FiniteAutomata(object):
    def __init__(self):
        self.states = set([])
        self.alphabet = set([])
        self.start = ''
        self.accepting = set([])
        self.transitions = list()

    @classmethod
    def from_file(self, filename):
        new = FiniteAutomata()
        with open(filename, mode='r') as f:
            new.states = f.readline().strip().split(' ')
            new.alphabet = f.readline().strip().split(' ')
            new.start = f.readline().strip()
            new.accepting = f.readline().strip().split(' ')
            for line in f:
                s, d, a = line.strip().split(' ')
                new.transitions.append((s, d, a))
        return new


class FiniteAutomataMenu(object):
    def __init__(self, fa):
        self.fa = fa

    def go(self):
        print self.menu()
        choice = raw_input('Choice: ')
        while choice != '6':
            if choice == '1':
                print ', '.join(self.fa.states)
            elif choice == '2':
                print ', '.join(self.fa.alphabet)
            elif choice == '3':
                print self.fa.start
            elif choice == '4':
                print ', '.join(self.fa.accepting)
            elif choice == '5':
                for t in self.fa.transitions:
                    print '%s ---- (%s) ----> %s' % (t[0], t[2], t[1])

            print '-' * 20
            choice = raw_input('Choice: ')

    def menu(self):
        return ''.join([
            '1. States\n',
            '2. Alphabet\n',
            '3. Start state\n',
            '4. Accepting states\n',
            '5. Transitions\n',
            '6. Exit\n'
        ])


def main():
    fa = FiniteAutomata.from_file('finite_automata.txt')
    fam = FiniteAutomataMenu(fa)
    fam.go()


if __name__ == "__main__":
    main()
