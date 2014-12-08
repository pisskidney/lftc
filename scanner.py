#!/usr/bin/python


import re, sys


class CompilerError(Exception):
    pass


class HashTable(object):

    default_val = -(2**32)

    def __init__(self, array=None):
        if array is None:
            self.array = [self.default_val for _ in xrange(8)]
        else:
            self.array = array
        self.nr_elements = 0
        self.mask = len(self.array) - 1

    def insert(self, val):
        if self.nr_elements + 1 > int(2.0/3 * len(self.array)):
            self.expand()
        raw_hash = hash(val)
        ok = False
        for _ in xrange(33 - self.mask):
            potential_hash = raw_hash & self.mask
            if self.array[potential_hash] == self.default_val:
                self.array[potential_hash] = val
                ok = True
                self.nr_elements += 1
                break
            raw_hash = raw_hash >> 1
        if not ok:
            raise KeyError('Too many collisions!')
        return potential_hash

    def contains(self, val):
        raw_hash = hash(val)
        for _ in xrange(33 - self.mask):
            potential_hash = raw_hash & self.mask
            if self.array[potential_hash] == val:
                return True
            raw_hash = raw_hash >> 1
        return False

    def get(self, index):
        if self.array[index] == self.default_val:
            raise KeyError('Invalid key')
        return self.array[index]

    def index(self, val):
        raw_hash = hash(val)
        for _ in xrange(33 - self.mask):
            potential_hash = raw_hash & self.mask
            if self.array[potential_hash] == val:
                return potential_hash
            raw_hash = raw_hash >> 1
        raise ValueError('%s is not in the hash table.' % val)
        return None

    def expand(self):
        self.mask = self.mask * 4 + 3
        ht = HashTable(
            array=[self.default_val for _ in xrange(len(self.array) * 4)]
        )
        ht.mask = self.mask
        for v in self.array:
            if v != self.default_val:
                ht.insert(v)
        self.array = ht.array


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
        for idd, t in self.coding.iteritems():
            if t == token:
                return idd
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
        for lineno, line in enumerate(f):
            line = line.rstrip()
            tokens = re.split(' |\(|\)|\[|\]', line)
            for token in tokens:
                if not token:
                    continue
                if token not in self.codifier.reserved:
                    if self.atomic(token):
                        idd = self.cst.getid_or_add(token)
                        self.pif.add(self.codifier.id_for('constant'), idd)
                    elif self.identifier(token):
                        idd = self.ist.getid_or_add(token)
                        self.pif.add(self.codifier.id_for('identifier'), idd)
                    else:
                        raise CompilerError('Unrecognized token on line: %d\nToken: %s' % (lineno, token))
                else:
                    self.pif.add(self.codifier.id_for(token), -1)

    def identifier(self, token):
        if len(token) > 8:
            return False
        if not token.isalnum():
            return False
        return True

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
        self.data = HashTable()

    def getid_or_add(self, v):
        if not self.data.contains(v):
            return self.data.insert(v)
        return self.data.index(v)

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

    try:
        scanner.scan('source.ppp')
    except CompilerError as e:
        print e
        sys.exit()

    print scanner.ist.data.__dict__
    print scanner.cst.data.__dict__
    print scanner.pif

if __name__ == "__main__":
    main()
