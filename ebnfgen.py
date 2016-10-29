#!/bin/python3
import sys
from collections import defaultdict


class GrammarParser:
    epsilon = 'EPSILON'

    def __init__(self, grammar):
        self.nt = set()
        self.productions = defaultdict(list)

        self.non_entry_nt = set()

        self.first = defaultdict(set)
        self.follow = defaultdict(set)
        self.predict = defaultdict(set)

        self.symbols = set()
        self.eps = defaultdict(lambda: False)
        self.nt_order = []

        grammar = grammar.replace("→", "->")
        grammar = grammar.replace("ε", self.epsilon)

        for production in filter(lambda x: "->" in x, grammar.split("\n")):
            nt, rhs = production.split("->")
            nt = nt.strip()
            if nt not in self.nt_order:
                self.nt_order.append(nt)

            self.nt.add(nt)
            self.symbols.add(nt)
            for s_prod in rhs.split("|"):
                cur_prod = []
                for symbol in s_prod.split():
                    symbol = symbol.strip()
                    self.non_entry_nt.add(symbol)
                    cur_prod.append(symbol)

                    if symbol == self.epsilon:
                        self.eps[nt] = True
                        self.first[nt].add(self.epsilon)
                    else:
                        self.symbols.add(symbol)
                self.productions[nt].append(cur_prod)

        self.terminals = self.symbols - self.nt

        self.start_symbols = self.nt - self.non_entry_nt

        for terminal in self.terminals:
            self.first[terminal].add(terminal)


        # Calculate the first set
        changed = True
        while changed:
            changed = False
            for nt in self.nt:
                for prod in self.productions[nt]:
                    found = False
                    for symbol in prod:
                        if len(self.first[symbol] - self.first[nt]) > 0:
                            changed = True
                            self.first[nt] |= (self.first[symbol] - set(self.epsilon))
                        if self.epsilon not in self.first[symbol]:
                            break
                    else:
                        if self.epsilon not in self.first[nt]:
                            self.first[nt].add(self.epsilon)
                            changed = True

        # Calculate the follow set
        # The start_symbols represent the non terminals that don't appear in
        # rhs
        if not self.start_symbols:
            self.start_symbols.add(self.nt_order[0])

        for nt in self.start_symbols:
            # EOL can follow those symbols
            self.follow[nt].add("$")

        changed = True
        while changed:
            changed = False

            for nt in self.nt:
                for prod in self.productions[nt]:

                    for symbol1, symbol2 in zip(prod, prod[1:]):
                        # The first symbol must be non-terminal
                        if symbol1 in self.nt:
                            first_sym2 = self.first[
                                symbol2] - set([self.epsilon])
                            if len(first_sym2 - self.follow[symbol1]) > 0:
                                changed = True
                                self.follow[symbol1] |= first_sym2

                    last_item = prod[-1]
                    if last_item in self.nt and len(self.follow[nt] - self.follow[last_item]) > 0:
                        changed = True
                        self.follow[last_item] |= self.follow[nt]

                    if len(prod) > 1:
                        last = prod[-1]
                        if self.epsilon in self.first[last]:
                            second_last = prod[-2]
                            if len(self.follow[nt] - self.follow[second_last]) > 0:
                                changed = True
                                self.follow[second_last] |= self.follow[nt]
        # Calculate the predict set
        for nt in self.nt:
            for prod in self.productions[nt]:
                # We use tuple of nt and the production as a tuple(immutable) as the key
                key = (nt, tuple(prod))
                self.predict[key] |= self.first[prod[0]]
                is_eps = all([self.eps[x] if x in self.nt else False for x in prod ])
                # print(nt," ", prod, end="")
                if is_eps or (len(prod) == 1 and prod[0] == self.epsilon):
                    self.predict[key] |= self.follow[nt]
                # No epsilon in predict set
                self.predict[key].discard(self.epsilon)

    def is_eps(self, symbol):
        if symbol not in self.nt:
            return False
        return self.eps[symbol]



    def _print_set(self, pset):
        # This is just some dirty hack to print the non terminals before terminals and in the same
        # order that they appeared. Also, don't print set of epsilon
        for symbol, f_set in filter(lambda x:x[0] != self.epsilon, sorted(pset.items(),
                                    key=lambda x: self.nt_order.index(x[0]) if
                                    x[0] in self.nt_order else len(self.nt_order) + 1)):
            print("{}\t:\t{}".format(symbol, ', '.join(sorted(filter(lambda x: x in self.symbols,f_set)))))

    def print_first_set(self):
        self._print_set(self.first)

    def print_follow_set(self):
        self._print_set(self.follow)

    def print_predict_set(self):
        for nt in sorted(self.nt, key=lambda x: self.nt_order.index(x)):
            for prod in self.productions[nt]:
                print("{} -> {}\t: {} ".format(nt, " ".join(prod), ",".join(self.predict[(nt, tuple(prod))])))

    def print_eps(self):
        eps_list = [symbol for symbol, iseps in self.eps.items() if iseps]
        print("Epsilon Productions : ", ",".join(eps_list))



if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("{} <grammar>".format(sys.argv[0]))
    else:
        gf = open(sys.argv[1]).read()
        ebnf = GrammarParser(gf)
        print("\nFirst set\n")
        ebnf.print_first_set()

        print("\n Follow set\n")
        ebnf.print_follow_set()

        print("\nPredict Set\n")
        ebnf.print_predict_set()

        print()
        ebnf.print_eps()
