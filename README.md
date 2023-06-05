## grammer

```
program ::= {statement}
statement ::= "PRINT" (expression | string) nl
    | "IF" comparison "THEN" nl {statement} "ENDIF" nl
    | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
    | "LABEL" ident nl
    | "GOTO" ident nl
    | "LET" ident "=" expression nl
    | "INPUT" ident nl
comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
expression ::= term {("-" | "+") term}
term ::= unary {("/" | "*") unary}
unary ::= ["+" | "-"] primary
primary ::= number | ident
nl ::= "\n"+
```

## credit

This is my implementation of teeny-tiny language by Austin Henley.
It is based on his blog posts `Let's make a Teeny Tiny compiler` [part1][part1], [part2][part2], [part3][part3].
Thanks for very very useful text.

<!-- link -->
[part1]: https://austinhenley.com/blog/teenytinycompiler1.html
[part2]: https://austinhenley.com/blog/teenytinycompiler2.html
[part3]: https://austinhenley.com/blog/teenytinycompiler3.html
