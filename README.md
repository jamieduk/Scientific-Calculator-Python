# Scientific Calculator

A modern desktop **scientific calculator** built with Python and Pygame.
<img width="1050" height="760" alt="game frame" src="https://github.com/user-attachments/assets/8da3e988-4e04-4c04-a89b-6fe4a76d5ab7" />
It provides a dark-themed graphical interface with mouse and keyboard input, scientific functions, trigonometry, constants, calculation history, angle-mode switching, and a safe AST-based expression evaluator.

## Features

* Dark modern graphical interface
* Mouse and keyboard input
* Live expression evaluation
* Scientific calculations
* Degree and radian angle modes
* Calculation history
* Previous-answer (`ans`) support
* Automatic number formatting
* Error messages displayed directly in the calculator
* Hover effects and colour-coded buttons
* Expression length and complexity limits
* Safe expression parsing using Python's `ast` module
* No use of Python `eval()`

## Requirements

* Python 3
* Pygame

The calculator uses Pygame for the graphical interface and Python's standard-library modules for mathematical operations and expression parsing.

## Installation

Install Pygame:

```bash
python3 -m pip install pygame
```

Then run the calculator:

```bash
python3 calculator.py
```

Replace `calculator.py` with the actual filename if your script has a different name.

## Interface

The calculator opens at a resolution of:

* **Width:** 1050 pixels
* **Height:** 760 pixels

The interface contains:

1. Calculator title
2. Angle-mode indicator
3. Expression display
4. Result/status display
5. Recent calculation history
6. Scientific calculator buttons

The application also saves an initial screenshot as `render-1.png` when it starts.

## Calculator Functions

### Basic arithmetic

| Button | Operation                |
| ------ | ------------------------ |
| `+`    | Addition                 |
| `-`    | Subtraction              |
| `*`    | Multiplication           |
| `/`    | Division                 |
| `%`    | Modulo                   |
| `±`    | Toggle positive/negative |
| `1/x`  | Reciprocal               |

### Powers

| Button | Operation            |
| ------ | -------------------- |
| `x²`   | Square               |
| `xʸ`   | Power                |
| `10ˣ`  | 10 raised to a power |
| `eˣ`   | Exponential          |
| `!`    | Factorial            |

### Trigonometry

| Function | Description     |
| -------- | --------------- |
| `sin`    | Sine            |
| `cos`    | Cosine          |
| `tan`    | Tangent         |
| `asin`   | Inverse sine    |
| `acos`   | Inverse cosine  |
| `atan`   | Inverse tangent |

Trigonometric functions respect the selected angle mode.

### Hyperbolic functions

* `sinh`
* `cosh`
* `tanh`

### Logarithms

* `ln`
* `log10`

### Other functions

* `√` — Square root
* `abs` — Absolute value
* `floor` — Floor
* `round` — Round to nearest integer
* `!` — Factorial

The supported functions are explicitly restricted by the calculator's expression evaluator.

## Constants

The calculator supports:

| Constant   | Meaning                    |
| ---------- | -------------------------- |
| `π` / `pi` | Pi                         |
| `e`        | Euler's number             |
| `ans`      | Previous calculated answer |

For example:

```text
π * 2
```

or:

```text
ans + 10
```

The `ans` value is updated after a successful calculation.

## Angle Modes

The calculator supports:

### DEG

Trigonometric input is interpreted in degrees.

Example:

```text
sin(90)
```

returns:

```text
1
```

### RAD

Trigonometric input is interpreted in radians.

Example:

```text
sin(1.57079632679)
```

returns approximately:

```text
1
```

The current mode is displayed in the top-right of the calculator.

## Keyboard Controls

The calculator can be operated without the mouse.

| Key                        | Action                |
| -------------------------- | --------------------- |
| `Enter`                    | Calculate             |
| `Backspace`                | Delete last character |
| `Escape`                   | Clear expression      |
| `=`                        | Calculate             |
| `^`                        | Power                 |
| Other supported characters | Enter into expression |

The application also supports the numeric keypad Enter key.

## History

The calculator keeps the **three most recent completed calculations**.

For example:

```text
25*4=100     |     sqrt(81)=9
```

History is updated whenever `=` successfully evaluates an expression.

## Safe Expression Evaluation

The calculator does **not** directly execute arbitrary Python expressions.

Instead, expressions are parsed using Python's `ast` module and only explicitly supported operations are allowed.

Supported arithmetic operators include:

* `+`
* `-`
* `*`
* `/`
* `%`
* `**`

Only numeric constants, approved names, unary operators, binary operators, and approved single-argument functions are accepted.

This prevents calculator input from being treated as unrestricted Python code.

## Input Limits

To prevent excessively large or complex expressions:

* Maximum expression length: **240 characters**
* Maximum AST complexity: **100 nodes**
* Maximum factorial: **170**
* Exponents with an absolute value greater than **1000** are rejected

The calculator also rejects non-finite numerical results such as infinity and invalid numeric input.

## Error Handling

Invalid calculations are displayed directly in the calculator interface rather than causing the application to crash.

Examples include:

```text
Cannot divide by zero
```

```text
Unknown function
```

```text
Check the expression
```

```text
Factorial must be between 0 and 170
```

```text
Result is outside the supported range
```

## Example Expressions

```text
2+2
```

```text
25*4
```

```text
sqrt(81)
```

```text
sin(45)
```

```text
log(100)
```

```text
log10(1000)
```

```text
2**8
```

```text
5!
```

```text
pi*10
```

```text
ans/2
```

```text
sqrt(25)+sin(45)
```

## Project Structure

A minimal installation can contain:

```text
scientific-calculator/
├── calculator.py
├── README.md
└── render-1.png
```

`render-1.png` is generated automatically when the calculator starts.

## Running

Start the calculator with:

```bash
python3 calculator.py
```

The application opens its interactive Pygame window and prints:

```text
Scientific calculator ready. The interactive window is now open.
```

## Dependencies

The project uses:

### Python standard library

* `ast`
* `math`
* `operator`

### External package

* `pygame`

No database, web server, external API, or internet connection is required.

## License

Copyright © 2026 J~Net.

Provided for personal and educational use.
