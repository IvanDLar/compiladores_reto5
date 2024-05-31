_Instrucciones : https://experiencia21.tec.mx/courses/482333/assignments/15445488_

## Las reglas de la gramática implementada

Rule 0 S' -> statements
Rule 1 statements -> statement
Rule 2 statement -> assignment
Rule 3 statement -> conditional
Rule 4 statement -> expression
Rule 5 conditional -> IF LPAREN comparison RPAREN OPEN_CURLY statements CLOSE_CURLY
Rule 6 conditional -> IF LPAREN comparison RPAREN OPEN_CURLY statements CLOSE_CURLY ELSE OPEN_CURLY statements CLOSE_CURLY
Rule 7 assignment -> VARIABLE LBRACK expression RBRACK EQUAL expression
Rule 8 assignment -> VARIABLE EQUAL expression
Rule 9 assignment -> VARIABLE EQUAL flow
Rule 10 comparison -> expression GREATER expression
Rule 11 comparison -> expression LESS expression
Rule 12 comparison -> expression GREATER_EQUAL expression
Rule 13 comparison -> expression LESS_EQUAL expression
Rule 14 comparison -> expression EQUAL_EQUAL expression
Rule 15 comparison -> expression NOT_EQUAL expression
Rule 16 flow -> VARIABLE CONNECT flow_functions
Rule 17 flow_functions -> flow_function_call CONNECT flow_functions
Rule 18 flow_functions -> flow_function_call
Rule 19 flow_function_call -> VARIABLE LPAREN params RPAREN
Rule 20 expression -> expression PLUS term
Rule 21 expression -> expression MINUS term
Rule 22 expression -> term
Rule 23 expression -> string
Rule 24 string -> STRING
Rule 25 expression -> NONE
Rule 26 term -> exponent
Rule 27 term -> term TIMES exponent
Rule 28 term -> term DIV exponent
Rule 29 exponent -> factor
Rule 30 exponent -> factor EXP factor
Rule 31 factor -> NUMBER
Rule 32 factor -> VARIABLE
Rule 33 factor -> LPAREN expression RPAREN
Rule 34 factor -> list
Rule 35 factor -> list_empty
Rule 36 list_empty -> LBRACK RBRACK
Rule 37 list -> LBRACK list_elements RBRACK
Rule 38 list_elements -> list_elements COMMA expression
Rule 39 list_elements -> expression
Rule 40 expression -> VARIABLE LBRACK expression RBRACK
Rule 41 factor -> function_call
Rule 42 function_call -> VARIABLE LPAREN RPAREN
Rule 43 function_call -> VARIABLE LPAREN params RPAREN
Rule 44 params -> params COMMA expression
Rule 45 params -> expression

## Descripción de las funciones implementadas como herramientas y accesorios a la gramática

## Demostración de una o varias expresiones y el árbol de sintaxis abstracto demostrando

1. Precedencia de operadores
2. Llamadas a funciones
3. Asignación de variables
4. Implementación de flujos de imágenes
5. Aplicación de filtros de Open CV
6. Cada una de las nuevas características implementadas

## Vínculos a videos de reflexión de cada participante
