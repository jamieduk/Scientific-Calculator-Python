import ast
import math
import operator
import pygame

WIDTH, HEIGHT = 1050, 760
COLORS = {
    "background": (13, 18, 31),
    "panel": (24, 32, 51),
    "panel_light": (32, 43, 66),
    "text": (239, 244, 255),
    "muted": (151, 163, 190),
    "number": (43, 56, 84),
    "operator": (37, 99, 155),
    "function": (91, 69, 150),
    "constant": (25, 120, 111),
    "danger": (151, 55, 72),
    "accent": (28, 183, 133),
    "accent_hover": (38, 208, 154),
    "error": (255, 120, 130),
}

BUTTON_ROWS = [
    ["sin", "cos", "tan", "√", "asin", "acos", "atan", "abs"],
    ["sinh", "cosh", "tanh", "ln", "log10", "eˣ", "xʸ", "!"],
    ["7", "8", "9", "/", "(", ")", "C", "⌫"],
    ["4", "5", "6", "*", "DEG", "RAD", "e", "π"],
    ["1", "2", "3", "-", "x²", "10ˣ", "ans", "="],
    ["0", ".", "±", "+", "%", "1/x", "floor", "round"],
]


def checked_number(value):
    if isinstance(value, bool):
        raise ValueError("Boolean values are not supported")
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("Invalid number") from None
    if not math.isfinite(number):
        raise ValueError("Result is outside the supported range")
    return number


def safe_evaluate(expression, degrees=False, answer=0.0):
    if len(expression) > 240:
        raise ValueError("Expression is too long")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError:
        raise ValueError("Check the expression") from None

    if sum(1 for _ in ast.walk(tree)) > 100:
        raise ValueError("Expression is too complex")

    def factorial(value):
        integer = round(value)
        if abs(value - integer) > 1e-10:
            raise ValueError("Factorial needs a whole number")
        if integer < 0 or integer > 170:
            raise ValueError("Factorial must be between 0 and 170")
        return checked_number(math.factorial(int(integer)))

    def call(name, value):
        if name in {"sin", "cos", "tan"}:
            angle = math.radians(value) if degrees else value
            return getattr(math, name)(angle)
        if name in {"asin", "acos", "atan"}:
            result = getattr(math, name)(value)
            return math.degrees(result) if degrees else result
        if name in {"sinh", "cosh", "tanh"}:
            return getattr(math, name)(value)
        if name == "sqrt":
            return math.sqrt(value)
        if name == "log":
            return math.log(value)
        if name == "log10":
            return math.log10(value)
        if name == "exp":
            return math.exp(value)
        if name == "abs":
            return abs(value)
        if name == "floor":
            return float(math.floor(value))
        if name == "round":
            return float(round(value))
        if name == "factorial":
            return factorial(value)
        raise ValueError("Unknown function")

    binary_operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numbers are supported")
            return checked_number(node.value)
        if isinstance(node, ast.Name):
            if node.id == "pi":
                return math.pi
            if node.id == "e":
                return math.e
            if node.id == "ans":
                return checked_number(answer)
            raise ValueError("Unknown name")
        if isinstance(node, ast.UnaryOp):
            value = visit(node.operand)
            if isinstance(node.op, ast.USub):
                return -value
            if isinstance(node.op, ast.UAdd):
                return value
            raise ValueError("Unsupported unary operation")
        if isinstance(node, ast.BinOp):
            operation = binary_operations.get(type(node.op))
            if operation is None:
                raise ValueError("Unsupported operation")
            left = visit(node.left)
            right = visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Exponent is too large")
            if isinstance(node.op, (ast.Div, ast.Mod)) and right == 0:
                raise ValueError("Cannot divide by zero")
            return checked_number(operation(left, right))
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.keywords:
                raise ValueError("Unsupported function call")
            if len(node.args) != 1:
                raise ValueError("Functions need one argument")
            return checked_number(call(node.func.id, visit(node.args[0])))
        raise ValueError("Unsupported syntax")

    try:
        return visit(tree)
    except OverflowError:
        raise ValueError("Result is outside the supported range") from None
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero") from None


def format_number(value):
    if abs(value) < 1e15 and math.isclose(value, round(value), abs_tol=1e-12):
        return str(int(round(value)))
    return f"{value:.12g}"


def fitted_text(text, width, maximum=36, minimum=15, font_name="dejavusans"):
    for size in range(maximum, minimum - 1, -1):
        font = pygame.font.SysFont(font_name, size)
        surface = font.render(text, True, COLORS["text"])
        if surface.get_width() <= width:
            return surface
    font = pygame.font.SysFont(font_name, minimum)
    return font.render(text, True, COLORS["text"])


def centered_text(surface, text, rectangle, size=25, color=None, bold=False):
    font = pygame.font.SysFont("dejavusans", size, bold=bold)
    image = font.render(text, True, color or COLORS["text"])
    position = (
        rectangle.x + (rectangle.width - image.get_width()) // 2,
        rectangle.y + (rectangle.height - image.get_height()) // 2,
    )
    surface.blit(image, position)


class Calculator:
    def __init__(self):
        self.expression = "sin(45) + sqrt(81)"
        self.angle_mode = "DEG"
        self.answer = 0.0
        self.history = []
        self.result = ""
        self.status = "Ready"
        self.refresh()

    def refresh(self):
        if not self.expression:
            self.result = ""
            self.status = "Ready"
            return
        try:
            value = safe_evaluate(
                self.expression,
                degrees=self.angle_mode == "DEG",
                answer=self.answer,
            )
            self.result = format_number(value)
            self.status = "Ready"
        except ValueError as error:
            self.result = ""
            self.status = str(error)

    def evaluate(self):
        try:
            value = safe_evaluate(
                self.expression,
                degrees=self.angle_mode == "DEG",
                answer=self.answer,
            )
            self.answer = value
            self.result = format_number(value)
            item = f"{self.expression} = {self.result}"
            self.history.insert(0, item)
            self.history = self.history[:3]
            self.status = "Calculated"
        except ValueError as error:
            self.result = ""
            self.status = str(error)

    def press(self, label):
        if label in {"DEG", "RAD"}:
            self.angle_mode = label
            self.refresh()
            return

        if label == "=":
            self.evaluate()
            return
        if label == "C":
            self.expression = ""
            self.refresh()
            return
        if label == "⌫":
            self.expression = self.expression[:-1]
            self.refresh()
            return
        if label == "±":
            if self.expression:
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression
            self.refresh()
            return
        if label == "1/x":
            if self.expression:
                self.expression = f"1/({self.expression})"
            self.refresh()
            return
        if label == "ans":
            self.expression += "ans"
            self.refresh()
            return

        tokens = {
            "√": "sqrt(",
            "ln": "log(",
            "eˣ": "exp(",
            "xʸ": "**",
            "x²": "**2",
            "10ˣ": "10**",
            "π": "pi",
            "e": "e",
            "floor": "floor(",
            "round": "round(",
        }
        function_tokens = {
            "sin", "cos", "tan", "asin", "acos", "atan",
            "abs", "sinh", "cosh", "tanh", "log10",
        }

        if label in function_tokens:
            self.expression += label + "("
        else:
            self.expression += tokens.get(label, label)
        self.refresh()


def button_color(label):
    if label == "=":
        return COLORS["accent"]
    if label in {"C", "⌫"}:
        return COLORS["danger"]
    if label in {"DEG", "RAD"}:
        return COLORS["constant"]
    if label in {"π", "e", "ans"}:
        return COLORS["constant"]
    if label in {"+", "-", "*", "/", "%", "xʸ", "x²", "10ˣ", "±", "1/x"}:
        return COLORS["operator"]
    if label.isdigit() or label in {".", "(", ")"}:
        return COLORS["number"]
    return COLORS["function"]


def build_buttons():
    margin, gap = 24, 10
    columns = 8
    button_width = (WIDTH - margin * 2 - gap * (columns - 1)) // columns
    button_height = 70
    rectangles = {}

    for row_index, row in enumerate(BUTTON_ROWS):
        for column_index, label in enumerate(row):
            x = margin + column_index * (button_width + gap)
            y = 280 + row_index * (button_height + gap)
            rectangles[label] = pygame.Rect(x, y, button_width, button_height)
    return rectangles


def draw_interface(screen, calculator, buttons, clock):
    screen.fill(COLORS["background"])
    title_font = pygame.font.SysFont("dejavusans", 30, bold=True)
    title = title_font.render("SCIENTIFIC CALCULATOR", True, COLORS["text"])
    screen.blit(title, (24, 18))

    subtitle_font = pygame.font.SysFont("dejavusans", 16)
    subtitle = subtitle_font.render(
        "Click the buttons or type an expression",
        True,
        COLORS["muted"],
    )
    screen.blit(subtitle, (25, 51))

    mode_rect = pygame.Rect(840, 18, 186, 43)
    pygame.draw.rect(screen, COLORS["constant"], mode_rect, border_radius=12)
    centered_text(
        screen,
        f"ANGLE: {calculator.angle_mode}",
        mode_rect,
        18,
        bold=True,
    )

    display_rect = pygame.Rect(24, 78, WIDTH - 48, 116)
    pygame.draw.rect(screen, COLORS["panel"], display_rect, border_radius=15)

    expression_width = display_rect.width - 40
    expression_surface = fitted_text(
        calculator.expression or "Ready",
        expression_width,
        maximum=38,
        minimum=16,
        font_name="dejavusansmono",
    )
    screen.blit(expression_surface, (display_rect.x + 20, display_rect.y + 14))

    result_color = (
        COLORS["error"] if calculator.status != "Ready" and not calculator.result
        else COLORS["accent"]
    )
    result_text = calculator.result if calculator.result else calculator.status
    result_surface = fitted_text(
        result_text,
        expression_width,
        maximum=30,
        minimum=14,
    )
    result_surface = result_surface.copy()
    result_surface.fill(result_color, special_flags=pygame.BLEND_RGBA_MULT)
    screen.blit(result_surface, (display_rect.x + 20, display_rect.y + 68))

    history_rect = pygame.Rect(24, 204, WIDTH - 48, 61)
    pygame.draw.rect(screen, COLORS["panel"], history_rect, border_radius=12)
    if calculator.history:
        history_text = "     |     ".join(calculator.history[:2])
    else:
        history_text = "History: completed calculations appear here"
    history_surface = fitted_text(
        history_text,
        history_rect.width - 30,
        maximum=18,
        minimum=12,
    )
    screen.blit(history_surface, (history_rect.x + 15, history_rect.y + 18))

    mouse_position = pygame.mouse.get_pos()
    for row in BUTTON_ROWS:
        for label in row:
            rectangle = buttons[label]
            color = button_color(label)
            if label == calculator.angle_mode:
                color = COLORS["accent"]
            elif rectangle.collidepoint(mouse_position):
                color = tuple(min(255, channel + 24) for channel in color)

            shadow = rectangle.copy()
            shadow.move_ip(0, 4)
            pygame.draw.rect(screen, (5, 8, 15), shadow, border_radius=12)
            pygame.draw.rect(screen, color, rectangle, border_radius=12)

            font_size = 21 if len(label) <= 3 else 16
            centered_text(
                screen,
                label,
                rectangle,
                font_size,
                bold=label in {"=", "C", "DEG", "RAD"},
            )

    clock.tick(60)
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Scientific Calculator")
    clock = pygame.time.Clock()
    calculator = Calculator()
    buttons = build_buttons()

    draw_interface(screen, calculator, buttons, clock)
    pygame.image.save(screen, "render-1.png")
    print("Scientific calculator ready. The interactive window is now open.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for label, rectangle in buttons.items():
                    if rectangle.collidepoint(event.pos):
                        calculator.press(label)
                        break

            elif event.type == pygame.KEYDOWN:
                if event.key in {pygame.K_RETURN, pygame.K_KP_ENTER}:
                    calculator.press("=")
                elif event.key == pygame.K_BACKSPACE:
                    calculator.press("⌫")
                elif event.key == pygame.K_ESCAPE:
                    calculator.press("C")
                elif event.unicode == "=":
                    calculator.press("=")
                elif event.unicode == "^":
                    calculator.press("xʸ")
                elif event.unicode:
                    calculator.press(event.unicode)

        draw_interface(screen, calculator, buttons, clock)

    pygame.quit()


if __name__ == "__main__":
    main()