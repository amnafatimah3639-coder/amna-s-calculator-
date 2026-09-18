import streamlit as st
import math

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Scientific Calculator")
st.caption("Basic + Advanced (Calculus-friendly) Calculator built with Python & Streamlit")

# ---------------------------------------------------------
# SESSION STATE (keeps the expression as you click buttons)
# ---------------------------------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

def press(key: str):
    """Append a symbol to the current expression."""
    st.session_state.expression += str(key)

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

# ---------------------------------------------------------
# SAFE MATH FUNCTIONS
# These wrap Python's math module so users can type
# sin(30), log(100), sqrt(16), fact(5), etc.
# ---------------------------------------------------------
def factorial(n):
    n = int(n)
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    return math.factorial(n)

def ncr(n, r):
    return math.comb(int(n), int(r))

def npr(n, r):
    return math.perm(int(n), int(r))

# Degrees-based trig (more intuitive for beginners)
def sin_d(x): return math.sin(math.radians(x))
def cos_d(x): return math.cos(math.radians(x))
def tan_d(x): return math.tan(math.radians(x))

# Whitelist of allowed names inside eval()
# This is CRITICAL for safety - never eval() raw user input
# without restricting what functions/names are available.
SAFE_NAMES = {
    # basic
    "abs": abs, "round": round, "pow": pow,
    # roots & powers
    "sqrt": math.sqrt, "cbrt": lambda x: math.copysign(abs(x) ** (1/3), x),
    # logs
    "log": math.log10, "ln": math.log, "log2": math.log2,
    # trig (degrees)
    "sin": sin_d, "cos": cos_d, "tan": tan_d,
    # trig (radians, for calculus users)
    "sin_r": math.sin, "cos_r": math.cos, "tan_r": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    # combinatorics / calculus-adjacent
    "fact": factorial, "ncr": ncr, "npr": npr,
    "exp": math.exp, "pi": math.pi, "e": math.e,
    "floor": math.floor, "ceil": math.ceil,
}

def safe_eval(expr: str):
    """
    Evaluate a math expression safely.
    - No access to builtins (prevents things like __import__)
    - Only functions/constants in SAFE_NAMES are usable
    - '^' is treated as power, like most calculators expect
    """
    if not expr.strip():
        return ""
    cleaned = expr.replace("^", "**").replace("÷", "/").replace("×", "*")
    try:
        result = eval(cleaned, {"__builtins__": {}}, SAFE_NAMES)
        return result
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as e:
        return f"Error: {e}"
    except SyntaxError:
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {e}"

# ---------------------------------------------------------
# INPUT BOX (type directly OR use buttons below)
# ---------------------------------------------------------
st.text_input(
    "Expression",
    key="expression",
    placeholder="e.g. sin(30) + sqrt(16) * fact(4)",
    label_visibility="collapsed",
)

# ---------------------------------------------------------
# BUTTON GRID
# ---------------------------------------------------------
def button_row(labels, cols):
    for col, label in zip(cols, labels):
        with col:
            st.button(label, on_click=press, args=(label,), use_container_width=True)

st.markdown("##### Advanced functions")
adv_rows = [
    ["sin(", "cos(", "tan(", "sqrt(", "log("],
    ["asin(", "acos(", "atan(", "ln(", "exp("],
    ["fact(", "ncr(", "npr(", "pi", "e"],
]
for row in adv_rows:
    button_row(row, st.columns(5))

st.markdown("##### Basic")
basic_rows = [
    ["7", "8", "9", "/", "("],
    ["4", "5", "6", "*", ")"],
    ["1", "2", "3", "-", "^"],
    ["0", ".", "%", "+", ","],
]
for row in basic_rows:
    button_row(row, st.columns(5))

c1, c2, c3 = st.columns(3)
with c1:
    st.button("⌫ Backspace", on_click=backspace, use_container_width=True)
with c2:
    st.button("C Clear", on_click=clear, use_container_width=True)
with c3:
    equals = st.button("= Evaluate", type="primary", use_container_width=True)

# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------
if equals or st.session_state.expression:
    result = safe_eval(st.session_state.expression)
    st.divider()
    if isinstance(result, str) and result.startswith("Error"):
        st.error(result)
    elif result != "":
        st.success(f"Result: **{result}**")

with st.expander("ℹ️ Supported functions"):
    st.markdown("""
    - **Basic:** `+  -  *  /  %  ^ (power)`
    - **Roots/Logs:** `sqrt(x)`, `cbrt(x)`, `log(x)` (base 10), `ln(x)` (natural), `log2(x)`
    - **Trig (degrees):** `sin(x)`, `cos(x)`, `tan(x)`, `asin(x)`, `acos(x)`, `atan(x)`
    - **Trig (radians):** `sin_r(x)`, `cos_r(x)`, `tan_r(x)`
    - **Combinatorics:** `fact(n)`, `ncr(n, r)`, `npr(n, r)`
    - **Constants:** `pi`, `e`
    - **Other:** `exp(x)`, `floor(x)`, `ceil(x)`, `abs(x)`, `round(x)`

    Example: `sin(30) + sqrt(16) * fact(4) / ncr(5,2)`
    """)
