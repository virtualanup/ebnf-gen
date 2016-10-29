# First, Follow and Predict Set Generator from EBNF Grammar
A small tool to generate First set, Follow set and Predict set from EBNF Grammar. It also prints the epsilon productions.

Usage :
```sh
$ python3 ebnfgen.py grammar
```

    Sample grammar is
    program -> stmt_list $$
    stmt_list -> stmt stmt_list | epsilon
    stmt -> id := expr | read id | write expr
    expr -> term term_tail
    term_tail -> add_op term term_tail | epsilon
    term -> factor factor_tail
    factor_tail -> mult_op factor factor_tail | epsilon
    factor -> ( expr ) | id | number
    add_op -> + | -
    mult_op -> *|/

Copyright (c) 2016 Anup Pokhrel

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
