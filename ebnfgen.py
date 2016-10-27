#!/bin/python3
import sys
from collections import defaultdict


class GrammarParser:
    epsilon = 'epsilon'

    def __init__(self, grammar):
        self.nt = set()
        self.productions = defaultdict(list)

        self.first = defaultdict(set)
        self.follow = defaultdict(set)

        self.symbols = set()
        self.eps = defaultdict(lambda: False)
        grammar = grammar.replace("→", "->")
        grammar = grammar.replace("ε", "epsilon")

        for production in filter(lambda x: "->" in x, grammar.split("\n")):
            nt, rhs = production.split("->")
            nt = nt.strip()
            self.nt.add(nt)
            self.symbols.add(nt)
            for s_prod in rhs.split("|"):
                cur_prod = []
                for symbol in s_prod.split():
                    symbol = symbol.strip()

                    cur_prod.append(symbol)

                    if symbol == self.epsilon:
                        self.eps[nt] = True
                        self.first[nt].add(self.epsilon)
                    else:
                        self.symbols.add(symbol)
                self.productions[nt].append(cur_prod)

        self.terminals = self.symbols - self.nt
        for terminal in self.terminals:
            self.first[terminal].add(terminal)
        changed = True

        while changed:
            changed = False
            for nt in self.nt:
                for prod in self.productions[nt]:
                    found = False
                    for symbol in prod:
                        if self.epsilon not in self.first[symbol]:
                            if self.epsilon not in self.first[symbol]:
                                if len(self.first[symbol] - self.first[nt]) > 0:
                                    changed = True
                                self.first[nt] |= self.first[symbol]
                                break
                    else:
                        if self.epsilon not in self.first[nt]:
                            print(".")
                            self.first[nt].add(self.epsilon)
                            changed = True

        # Now, get the first and follow set

    def print_first_set(self):
        for symbol, f_set in self.first.items():
            print("{}\t:\t{}".format(symbol, ', '.join(f_set)))

    def first_set(self):
        return self.first

    def follow_set(self):
        return []


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("{} <grammar>".format(sys.argv[0]))
    else:
        gf = open(sys.argv[1]).read()
        ebnf = GrammarParser(gf)
        print("\nFirst set\n")
        ebnf.print_first_set()
