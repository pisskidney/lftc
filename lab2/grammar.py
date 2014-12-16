#!/usr/bin/python


import sys


class Grammar(object):
    arrow_symbol = '->'
    empty_string = 'E'

    def __init__(self):
        self.terminals = set([])
        self.non_terminals = set([])
        self.productions = list()

    @staticmethod
    def arrow():
        return ' %s ' % Grammar.arrow_symbol

    @classmethod
    def from_console(self):
        new = Grammar()
        print('Just enter an empty string when your done.')
        nterm = raw_input('Non-terminal: ')
        while nterm != '':
            new.non_terminals.add(nterm)
            nterm = raw_input('Non-terminal: ')
        term = raw_input('Terminal: ')
        while term != '':
            new.terminals.add(term)
            term = raw_input('Terminal: ')
        prod = raw_input('Production (ex: S -> aS or A -> E): ')
        while prod != '':
            nterm, result = prod.split(self.arrow())
            if len(result) == 1:
                if result != self.empty_string:
                    print 'Invalid production!'
                    continue
                new.productions.append((nterm, result))
            else:
                new.productions.append((nterm, result[0], result[1]))
            prod = raw_input('Production (ex: S -> aS or A -> E): ')
        return new

    @classmethod
    def from_file(self, filename):
        new = Grammar()
        with open(filename, mode='r') as f:
            new.non_terminals = f.readline().strip().split(' ')
            new.terminals = f.readline().strip().split(' ')
            for line in f:
                non_terminal, result = line.strip().split(self.arrow())
                if len(result) == 1:
                    assert result == self.empty_string, 'Invalid grammar!'
                    new.productions.append((non_terminal, result[0]))
                else:
                    new.productions.append([
                        non_terminal, result[0], result[1]
                    ])
        return new

    def is_regular(self):
        return self.is_right_regular() or self.is_left_regular()

    def is_right_regular(self):
        return all([
            prod[0] in self.non_terminals and
            (
                len(prod) == 2 or
                (prod[1] in self.terminals and prod[2] in self.non_terminals)
            )
            for prod in self.productions
        ])

    def is_left_regular(self):
        return all([
            prod[1] in self.non_terminals and prod[0] in self.terminals
            for prod in self.productions
        ])


class GrammarMenu(object):
    def __init__(self, grammar):
        self.grammar = grammar

    def go(self):
        print self.menu()
        choice = raw_input('Choice: ')
        while choice != '6':
            if choice == '1':
                print 'Non-terminals:'
                print ', '.join(self.grammar.non_terminals)
            elif choice == '2':
                print 'Terminals:'
                print ', '.join(self.grammar.terminals)
            elif choice == '3':
                print 'Productions set:'
                for prod in self.grammar.productions:
                    res = prod[1:]
                    print '%s%s%s' % (
                        prod[0], self.grammar.arrow(), ''.join(res)
                    )
            elif choice == '4':
                nterm = raw_input('Please give non-terminal: ')
                if nterm not in self.grammar.non_terminals:
                    print 'Invalid non-terminal!'
                else:
                    print 'Productions for non-terminal %s:' % nterm
                    for prod in self.grammar.productions:
                        if prod[0] == nterm:
                            print '%s%s%s%s' % (
                                prod[0], self.grammar.arrow(), prod[1], prod[2]
                            )
            elif choice == '5':
                print self.grammar.is_regular()

            print '-' * 20
            choice = raw_input('Choice: ')

    def menu(self):
        return ''.join([
            '1. Non-terminals\n',
            '2. Terminals\n',
            '3. Productions\n',
            '4. Productions for non-terminal\n',
            '5. Check if grammar is regular.\n',
            '6. Exit\n'
        ])


def main():
    g = Grammar.from_file('grammar.txt')
    g = Grammar.from_console()
    gm = GrammarMenu(g)
    gm.go()


if __name__ == "__main__":
    main()
