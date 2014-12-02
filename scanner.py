#!/usr/bin/python


import re


class Codifier(object):
    def __init__(self, coding=None):
        if coding:
            self.coding = coding

    @classmethod
    def from_file(cls, filename):
        coding = dict()
        f = open(filename, mode='r')
        for line in f:
            s, c = line.rstrip().split(' ')
            coding[int(c)] = s
        new = cls(coding=coding)
        return new

    @property
    def reserved(self):
        return self.coding.values()

    def id_for(self, token):
        for id, token in self.coding.iteritems():
            if token == token:
                return id
        return None


class Scanner(object):
    def __init__(self, codifier, pif=None, id_sym_table=None, const_sym_table=None):
        if pif is None:
            self.pif = ProgramInternalForm()
        else:
            self.pif = pif
        if id_sym_table is None:
            self.ist = SymbolTable()
        else:
            self.ist = id_sym_table
        if const_sym_table is None:
            self.cst = SymbolTable()
        else:
            self.cst = const_sym_table
        self.codifier = codifier

    def scan(self, source):
        f = open(source, mode='r')
        for line in f:
            line = line.rstrip()
            tokens = re.split(' |\(|\)|\[|\]', line)
            print tokens
            for token in tokens:
                if not token:
                    continue
                if token not in self.codifier.reserved:
                    if self.atomic(token):
                        idd = self.cst.getid_or_add(token)
                        self.pif.add(self.codifier.id_for('identifier'), token)
                    else:
                        idd = self.ist.getid_or_add(token)
                        self.pif.add(self.codifier.id_for('constant'), token)

    def atomic(self, token):
        if token in (True, False):
            return True
        try:
            float(token)
            return True
        except (TypeError, ValueError):
            pass
        regex = re.compile('\'\S*\'')
        if regex.match(token):
            return True
        return False


class SymbolTable(object):
    def __init__(self):
        self.data = dict()

    def getid_or_add(self, v):
        if v not in self.data:
            self.data[v] = len(self.data)
        return self.data[v]

    def __repr__(self):
        return unicode(self.data)


class ProgramInternalForm(object):
    def __init__(self):
        self.data = list()

    def add(self, t_type, token):
        self.data.append((t_type, token))

    def __repr__(self):
        return unicode(self.data)


class Program(object):
    def __init__(self, pif, st):
        self.st = st
        self.pif = pif


def main():
    co = Codifier().from_file('codification.txt')
    ist = SymbolTable()
    cst = SymbolTable()
    pif = ProgramInternalForm()
    scanner = Scanner(co, pif, ist, cst)
    scanner.scan('source.ppp')
    print scanner.ist
    print scanner.cst
    print scanner.pif

if __name__ == "__main__":
    main()
