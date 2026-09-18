import streamlit as st
import math

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="The Calculating Machine", page_icon="✒️", layout="centered")

# ---------------------------------------------------------
# STYLING — a little enamel-bodied typewriter/adding-machine
# that sits fully on one screen, no scrolling.
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Special+Elite&family=Courier+Prime:wght@400;700&display=swap');

:root{
  --paper:      #F4ECD8;
  --case:       #EFE3C4;
  --case-edge:  #C9AD73;
  --brass:      #B08D57;
  --brass-lt:   #E7CE9C;
  --desk:       #2B1F16;
  --key:        #34302A;
  --key-top:    #433D34;
  --ribbon:     #A24444;
  --ribbon-dk:  #7A2F2F;
  --ink:        #3A342C;
  --ink-faint:  #7A7160;
}

html, body, .stApp{
  height: 100vh;
  overflow: hidden;
  background:
    radial-gradient(ellipse at 50% 0%, #3a2a1c 0%, var(--desk) 60%);
}
header[data-testid="stHeader"]{ background: transparent; }
#MainMenu, footer { visibility: hidden; }

/* Streamlit's real scroll container -- turn it into a centering flexbox */
[data-testid="stAppViewContainer"]{
  height: 100vh;
  overflow: hidden;
}
section[data-testid="stMain"]{
  height: 100vh;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}
div[data-testid="stMainBlockContainer"], .block-container{
  margin: 0 !important;
}

/* tighten Streamlit's default vertical rhythm everywhere */
div[data-testid="stVerticalBlock"] > div[data-testid="stElementContainer"]{
  margin-bottom: 0.2rem !important;
}
div[data-testid="stHorizontalBlock"]{
  gap: 0.28rem !important;
}
div[data-testid="stElementContainer"]{ margin: 0 !important; }

/* ---------- THE MACHINE BODY ---------- */
.block-container{
  background:
    radial-gradient(circle at 8px 8px, rgba(0,0,0,0.05) 1px, transparent 1.4px) 0 0/16px 16px,
    radial-gradient(circle at 4px 12px, rgba(255,255,255,0.35) 1px, transparent 1.4px) 0 0/16px 16px,
    var(--case);
  max-width: 360px;
  margin: 0 auto !important;
  padding: 0.7rem 0.9rem 0.65rem 0.9rem !important;
  border-radius: 20px;
  border: 3px solid var(--case-edge);
  box-shadow:
    0 18px 0 -6px rgba(0,0,0,0.15),
    0 22px 40px rgba(0,0,0,0.55),
    inset 0 2px 3px rgba(255,255,255,0.5);
  position: relative;
}
/* little brass base the case rests on */
.block-container::after{
  content:"";
  position:absolute;
  left:50%; bottom:-13px;
  width:62%; height:12px;
  transform: translateX(-50%);
  background: linear-gradient(180deg, var(--brass) 0%, var(--brass-lt) 45%, var(--brass) 100%);
  border-radius: 0 0 10px 10px;
  box-shadow: 0 6px 10px rgba(0,0,0,0.5);
}

/* brass corner rivets */
.block-container::before{
  content:"";
  position:absolute; inset: 8px;
  border-radius: 20px;
  pointer-events:none;
  background-image:
    radial-gradient(circle, var(--brass-lt) 30%, var(--brass) 70%),
    radial-gradient(circle, var(--brass-lt) 30%, var(--brass) 70%),
    radial-gradient(circle, var(--brass-lt) 30%, var(--brass) 70%),
    radial-gradient(circle, var(--brass-lt) 30%, var(--brass) 70%);
  background-size: 9px 9px;
  background-repeat: no-repeat;
  background-position: 2px 2px, calc(100% - 2px) 2px, 2px calc(100% - 2px), calc(100% - 2px) calc(100% - 2px);
}

/* Nameplate */
.machine-title{
  font-family: 'Special Elite', cursive;
  color: var(--ink);
  font-size: 1rem;
  letter-spacing: 0.02em;
  text-align: center;
  margin-bottom: 0 !important;
}
.machine-sub{
  font-family: 'Courier Prime', monospace;
  color: var(--ink-faint);
  text-align: center;
  font-size: 0.55rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  margin: 0.05rem 0 0.4rem 0 !important;
}

/* Paper display window */
.stTextInput input{
  font-family: 'Courier Prime', monospace !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.05em;
  background: var(--paper) !important;
  color: var(--ink) !important;
  border: none !important;
  border-radius: 7px !important;
  padding: 0.32rem 0.5rem !important;
  box-shadow: inset 0 2px 5px rgba(0,0,0,0.18), inset 0 0 0 2px var(--case-edge);
}
.stTextInput input:focus{ outline: none !important; }

.result-strip{
  font-family: 'Courier Prime', monospace;
  font-size: 0.78rem;
  min-height: 1.05rem;
  color: var(--ink);
  background: var(--paper);
  border-radius: 7px;
  padding: 0.22rem 0.5rem;
  margin: 0.25rem 0 0.4rem 0 !important;
  box-shadow: inset 0 2px 5px rgba(0,0,0,0.14), inset 0 0 0 2px var(--case-edge);
}
.result-strip.error{ color: var(--ribbon-dk); }
.result-strip .cursor{
  display:inline-block; width:8px; background: var(--ink);
  animation: blink 1s steps(1) infinite; margin-left:2px;
}
@keyframes blink{ 50%{ opacity:0; } }

.section-label{
  font-family: 'Courier Prime', monospace;
  color: var(--ink-faint);
  font-size: 0.52rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin: 0.2rem 0 0.1rem 0.1rem !important;
}

/* ---------- UNIFORM ROUND KEYS ---------- */
.stButton > button{
  font-family: 'Special Elite', cursive !important;
  color: var(--paper) !important;
  background: radial-gradient(circle at 32% 28%, var(--key-top), var(--key) 72%) !important;
  border: 1px solid #17140f !important;
  border-radius: 10px !important;
  aspect-ratio: 1 / 1;
  width: 100% !important;
  height: clamp(20px, 4vh, 34px) !important;
  min-height: 0 !important;
  padding: 0 !important;
  font-size: clamp(0.45rem, 1.05vh, 0.65rem) !important;
  box-shadow: 0 2px 0 #0c0a08, 0 4px 5px rgba(0,0,0,0.4) !important;
  transition: transform 0.05s ease, box-shadow 0.05s ease !important;
}
.stButton > button:hover{ border-color: var(--ribbon) !important; }
.stButton > button:active{
  transform: translateY(2px) !important;
  box-shadow: 0 1px 0 #0c0a08, 0 2px 3px rgba(0,0,0,0.35) !important;
}
/* Evaluate key -- same shape & size, ribbon-red */
.stButton > button[kind="primary"]{
  background: radial-gradient(circle at 32% 28%, #b95a5a, var(--ribbon) 72%) !important;
  box-shadow: 0 3px 0 var(--ribbon-dk), 0 5px 7px rgba(0,0,0,0.4) !important;
}
.stButton > button[kind="primary"]:active{
  box-shadow: 0 1px 0 var(--ribbon-dk), 0 2px 3px rgba(0,0,0,0.35) !important;
}

.stExpander{ display:none; } /* keep the manual out of the way so nothing scrolls */
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="machine-title">The Calculating Machine</div>', unsafe_allow_html=True)
st.markdown('<div class="machine-sub">No. 7 &middot; Scientific Model</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE
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
# SAFE MATH ENGINE
# ---------------------------------------------------------
def factorial(n):
    n = int(n)
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    return math.factorial(n)

def ncr(n, r): return math.comb(int(n), int(r))
def npr(n, r): return math.perm(int(n), int(r))
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
# DISPLAY
# ---------------------------------------------------------
st.text_input(
    "Expression",
    key="expression",
    placeholder="type, or strike the keys...",
    label_visibility="collapsed",
)

result = safe_eval(st.session_state.expression)
if isinstance(result, str) and result.startswith("Error"):
    st.markdown(f'<div class="result-strip error">{result}</div>', unsafe_allow_html=True)
elif result != "":
    st.markdown(f'<div class="result-strip">{result}<span class="cursor">&nbsp;</span></div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="result-strip">&nbsp;</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# KEY GRID — every key is the same size & shape
# ---------------------------------------------------------
def button_row(labels, cols):
    for col, label in zip(cols, labels):
        with col:
            st.button(label, on_click=press, args=(label,), use_container_width=True)

st.markdown('<div class="section-label">Advanced</div>', unsafe_allow_html=True)
for row in [
    ["sin(", "cos(", "tan(", "sqrt(", "log("],
    ["asin(", "acos(", "atan(", "ln(", "exp("],
    ["fact(", "ncr(", "npr(", "pi", "e"],
]:
    button_row(row, st.columns(5))

st.markdown('<div class="section-label">Keyboard</div>', unsafe_allow_html=True)
for row in [
    ["7", "8", "9", "/", "("],
    ["4", "5", "6", "*", ")"],
    ["1", "2", "3", "-", "^"],
    ["0", ".", "%", "+", ","],
]:
    button_row(row, st.columns(5))

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.button("⌫", on_click=backspace, use_container_width=True)
with c2:
    st.button("C", on_click=clear, use_container_width=True)
with c3, c4:
    st.write("")
with c5:
    st.button("=", type="primary", use_container_width=True)
