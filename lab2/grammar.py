#!/usr/bin/python


class Grammar(object):
    arrow_symbol = '->'

    def __init__(self):
        self.terminals = set([])
        self.non_terminals = set([])
        self.productions = list()

    @staticmethod
    def arrow():
        return ' %s ' % Grammar.arrow_symbol

    @classmethod
    def from_file(self, filename):
        new = Grammar()
        with open(filename, mode='r') as f:
            new.non_terminals = f.readline().strip().split(' ')
            new.terminals = f.readline().strip().split(' ')
            for line in f:
                non_terminal, result = line.strip().split(self.arrow())
                new.productions.append((non_terminal, result))
        return new


class GrammarMenu(object):
    def __init__(self, grammar):
        self.grammar = grammar

    def go(self):
        print self.menu()
        choice = raw_input('Choice: ')
        while choice != '5':
            if choice == '1':
                print 'Non-terminals:'
                print ', '.join(self.grammar.non_terminals)
            elif choice == '2':
                print 'Terminals:'
                print ', '.join(self.grammar.terminals)
            elif choice == '3':
                print 'Productions set:'
                for prod in self.grammar.productions:
                    print '%s%s%s' % (prod[0], self.grammar.arrow(), prod[1])
            elif choice == '4':
                pass
            print '-' * 20
            choice = raw_input('Choice: ')

    def menu(self):
        return '\
            1. Non-terminals\n\
            2. Terminals\n\
            3. Productions\n\
            4. Productions for non-terminal\n\
            5. Exit\n\
        '


def main():
    g = Grammar.from_file('grammar.txt')
    gm = GrammarMenu(g)
    gm.go()


if __name__ == "__main__":
    main()
