import streamlit as st
import math

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="The Calculating Machine", page_icon="✒️", layout="centered")

# ---------------------------------------------------------
# VINTAGE TYPEWRITER STYLING
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Courier+Prime:wght@400;700&display=swap');

:root{
  --paper:      #EDE3CC;
  --paper-dark: #E0D3B0;
  --desk:       #2B1F16;
  --desk-grain: #241a12;
  --key:        #26221E;
  --key-top:    #34302A;
  --ribbon:     #8C2F2F;
  --ink:        #3A342C;
  --ink-faint:  #6B6355;
}

/* Desk background */
.stApp{
  background:
    repeating-linear-gradient(90deg, var(--desk) 0px, var(--desk) 2px, var(--desk-grain) 2px, var(--desk-grain) 4px);
}

/* Hide default Streamlit chrome that breaks the illusion */
header[data-testid="stHeader"]{ background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* The "sheet of paper" the whole app sits on */
.block-container{
  background: var(--paper);
  max-width: 640px;
  margin-top: 2.2rem;
  padding: 0 2.6rem 2.6rem 2.6rem !important;
  box-shadow: 0 25px 50px rgba(0,0,0,0.55), 0 2px 0 rgba(0,0,0,0.2);
  position: relative;
}

/* Carriage roller bar across the top of the page */
.block-container::before{
  content: "";
  display: block;
  height: 26px;
  margin: 0 -2.6rem 1.6rem -2.6rem;
  background: repeating-linear-gradient(90deg, var(--key) 0px, var(--key) 14px, #171310 14px, #171310 16px);
  box-shadow: inset 0 -4px 6px rgba(0,0,0,0.4);
}

/* Title, typed onto the paper */
.machine-title{
  font-family: 'Special Elite', cursive;
  color: var(--ink);
  font-size: 2rem;
  letter-spacing: 0.04em;
  text-align: center;
  margin-bottom: 0.1rem;
}
.machine-sub{
  font-family: 'Courier Prime', monospace;
  color: var(--ink-faint);
  text-align: center;
  font-size: 0.85rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-bottom: 1.6rem;
  border-top: 1px dashed var(--ink-faint);
  border-bottom: 1px dashed var(--ink-faint);
  padding: 0.4rem 0;
}

/* Expression input styled as a typed line on paper */
.stTextInput input{
  font-family: 'Courier Prime', monospace !important;
  font-size: 1.15rem !important;
  letter-spacing: 0.08em;
  background: var(--paper-dark) !important;
  color: var(--ink) !important;
  border: none !important;
  border-bottom: 2px solid var(--ink) !important;
  border-radius: 0 !important;
  padding: 0.7rem 0.6rem !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.12);
}
.stTextInput input:focus{
  outline: none !important;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.18);
}

/* Section labels */
.section-label{
  font-family: 'Courier Prime', monospace;
  color: var(--ink-faint);
  font-size: 0.78rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  margin: 1.3rem 0 0.5rem 0;
}

/* Round typewriter keys */
.stButton > button{
  font-family: 'Special Elite', cursive !important;
  font-size: 0.95rem !important;
  color: var(--paper) !important;
  background: radial-gradient(circle at 35% 30%, var(--key-top), var(--key) 70%) !important;
  border: 1px solid #141110 !important;
  border-radius: 50% !important;
  aspect-ratio: 1 / 1;
  width: 100% !important;
  box-shadow:
    0 4px 0 #0d0b09,
    0 6px 8px rgba(0,0,0,0.45) !important;
  transition: transform 0.05s ease, box-shadow 0.05s ease !important;
}
.stButton > button:hover{
  color: #fff !important;
  border-color: var(--ribbon) !important;
}
.stButton > button:active{
  transform: translateY(3px) !important;
  box-shadow: 0 1px 0 #0d0b09, 0 2px 3px rgba(0,0,0,0.4) !important;
}

/* The Evaluate key -- the ribbon-red return lever */
.stButton > button[kind="primary"]{
  background: radial-gradient(circle at 35% 30%, #a83f3f, var(--ribbon) 70%) !important;
  border-radius: 10px !important;
  aspect-ratio: auto;
  box-shadow: 0 4px 0 #5c1f1f, 0 6px 8px rgba(0,0,0,0.45) !important;
}
.stButton > button[kind="primary"]:active{
  box-shadow: 0 1px 0 #5c1f1f, 0 2px 3px rgba(0,0,0,0.4) !important;
}

/* Printed result line */
.result-line{
  font-family: 'Courier Prime', monospace;
  font-size: 1.3rem;
  color: var(--ink);
  letter-spacing: 0.06em;
  margin-top: 1.2rem;
  padding-top: 0.8rem;
  border-top: 2px solid var(--ink);
}
.result-line .cursor{
  display: inline-block;
  width: 10px;
  background: var(--ink);
  animation: blink 1s steps(1) infinite;
  margin-left: 2px;
}
@keyframes blink{ 50% { opacity: 0; } }

.error-line{
  font-family: 'Courier Prime', monospace;
  color: var(--ribbon);
  font-size: 1.05rem;
  margin-top: 1.2rem;
  padding-top: 0.8rem;
  border-top: 2px solid var(--ribbon);
}

.stExpander{
  font-family: 'Courier Prime', monospace;
  background: var(--paper-dark) !important;
  border: 1px dashed var(--ink-faint) !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="machine-title">The Calculating Machine</div>', unsafe_allow_html=True)
st.markdown('<div class="machine-sub">No. 7 &mdash; Scientific Model</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE (keeps the expression as you click keys)
# ---------------------------------------------------------
if "expression" not in st.session_state:
    st.session_state.expression = ""

def press(key: str):
    st.session_state.expression += str(key)

def clear():
    st.session_state.expression = ""

def backspace():
    st.session_state.expression = st.session_state.expression[:-1]

# ---------------------------------------------------------
# SAFE MATH FUNCTIONS
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

def sin_d(x): return math.sin(math.radians(x))
def cos_d(x): return math.cos(math.radians(x))
def tan_d(x): return math.tan(math.radians(x))

SAFE_NAMES = {
    "abs": abs, "round": round, "pow": pow,
    "sqrt": math.sqrt, "cbrt": lambda x: math.copysign(abs(x) ** (1/3), x),
    "log": math.log10, "ln": math.log, "log2": math.log2,
    "sin": sin_d, "cos": cos_d, "tan": tan_d,
    "sin_r": math.sin, "cos_r": math.cos, "tan_r": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "fact": factorial, "ncr": ncr, "npr": npr,
    "exp": math.exp, "pi": math.pi, "e": math.e,
    "floor": math.floor, "ceil": math.ceil,
}

def safe_eval(expr: str):
    if not expr.strip():
        return ""
    cleaned = expr.replace("^", "**").replace("÷", "/").replace("×", "*")
    try:
        return eval(cleaned, {"__builtins__": {}}, SAFE_NAMES)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except ValueError as e:
        return f"Error: {e}"
    except SyntaxError:
        return "Error: Invalid expression"
    except Exception as e:
        return f"Error: {e}"

# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------
st.text_input(
    "Expression",
    key="expression",
    placeholder="type here, or strike the keys below...",
    label_visibility="collapsed",
)

# ---------------------------------------------------------
# KEY GRID
# ---------------------------------------------------------
def button_row(labels, cols):
    for col, label in zip(cols, labels):
        with col:
            st.button(label, on_click=press, args=(label,), use_container_width=True)

st.markdown('<div class="section-label">Advanced</div>', unsafe_allow_html=True)
adv_rows = [
    ["sin(", "cos(", "tan(", "sqrt(", "log("],
    ["asin(", "acos(", "atan(", "ln(", "exp("],
    ["fact(", "ncr(", "npr(", "pi", "e"],
]
for row in adv_rows:
    button_row(row, st.columns(5))

st.markdown('<div class="section-label">Keyboard</div>', unsafe_allow_html=True)
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
    st.button("⌫", on_click=backspace, use_container_width=True)
with c2:
    st.button("C", on_click=clear, use_container_width=True)
with c3:
    equals = st.button("= Strike", type="primary", use_container_width=True)

# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------
if equals or st.session_state.expression:
    result = safe_eval(st.session_state.expression)
    if isinstance(result, str) and result.startswith("Error"):
        st.markdown(f'<div class="error-line">{result}</div>', unsafe_allow_html=True)
    elif result != "":
        st.markdown(
            f'<div class="result-line">{result}<span class="cursor">&nbsp;</span></div>',
            unsafe_allow_html=True,
        )

with st.expander("Operator's Manual"):
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
