# Mini Compiler (Lexical → Syntax → Semantic → TAC → Assembly-Like)

This mini compiler demonstrates the fundamental phases of compiler construction by compiling a simplified C-style language. It performs lexical analysis, parsing, symbol table management, intermediate (three-address) code generation, and produces assembly-like output.

---

## ✨ Features

✅ Lexical Analysis (keywords, identifiers, constants, operators, punctuation, comments)\
✅ Syntax Parsing using PLY (YACC)\
✅ Expression evaluation\
✅ Variable declarations and assignments\
✅ `if` and `while` control structures\
✅ `print()` statements\
✅ Symbol Table maintenance\
✅ Three-Address Code (TAC) generation\
✅ Assembly-style instruction output\
✅ Basic error handling

---

## 🧠 Language Support

The compiler accepts C-style syntax:

```c
int a = 5 + 3;
print(a);

if (a > b) {
    print(b);
}

while (c > 0) {
    print(c);
}
```

Supported:

Variables

Arithmetic (+, -, \*, /)

Comparison (> < >= <= ==)

Control flow

Looping

Nested blocks

🛠️ Technology Used

| Component | Tool       |
| --------- | ---------- |
| Lexer     | PLY (Lex)  |
| Parser    | PLY (YACC) |
| Language  | Python     |
| Platform  | CLI        |

## 📁 Project Structure

```
MiniCompiler_Project/

├── parser.py
├── input.txt
├── parser.out
├── parsetab.py
└── README.md
```

▶️ How to Run

Install PLY:

pip install ply

Run the compiler:

python parser.py < input.txt

📌 Output Shows

Lexical Analysis Summary

Parse Messages

Symbol Table

Three-Address Code (TAC)

Assembly-like representation (labels, jumps)

✅ Parsing completed successfully!

--- SYMBOL TABLE ---

```
a = t7
b = t8
```

--- THREE ADDRESS CODE ---

```
t1 = 5 + 3
t2 = t1 - 2
```

✅ Conclusion

Overall, this mini compiler illustrates how real-world compilers translate high-level code into intermediate and assembly-like representations, reinforcing key concepts in compiler architecture.
