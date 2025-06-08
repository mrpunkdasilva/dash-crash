import math

# Biblioteca de funções matemáticas para o jogo
FUNCTIONS = [
    {
        "name": "Senoide",
        "formula": "f(x) = 50·sen(0.01x) + 0.001x² + 300",
        "f": lambda x: 50 * math.sin(0.01 * x) + 0.001 * x**2 + 300,
        "df": lambda x: 50 * 0.01 * math.cos(0.01 * x) + 0.002 * x,
        "range": (0, 1000),
        "checkpoints": 4
    }
]

def get_function(index=0):
    """Retorna uma função da biblioteca pelo índice"""
    if 0 <= index < len(FUNCTIONS):
        return FUNCTIONS[index]
    return FUNCTIONS[0]

def evaluate_function(func, x):
    """Avalia uma função em um ponto x"""
    return func(x)

def evaluate_derivative(func_derivative, x):
    """Avalia a derivada de uma função em um ponto x"""
    return func_derivative(x)

def check_derivative_answer(user_answer, actual_derivative, tolerance=0.5):
    """Verifica se a resposta do usuário está correta dentro de uma tolerância"""
    try:
        user_value = float(user_answer)
        error = abs(user_value - actual_derivative)
        return error < tolerance
    except ValueError:
        return False