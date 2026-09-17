```python
import streamlit as st
import math
import random


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="wide"
)


# ============================================================
# SESSION STATE
# ============================================================
# Streamlit reruns our Python program whenever the user
# interacts with a widget.
#
# session_state allows us to remember information between
# those reruns.

if "history" not in st.session_state:
    st.session_state.history = []

if "memory" not in st.session_state:
    st.session_state.memory = 0.0

if "answer" not in st.session_state:
    st.session_state.answer = 0.0


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_history(expression, result):
    """Add a calculation to the history."""

    st.session_state.history.append(
        f"{expression} = {result}"
    )


def format_result(result):
    """
    Make floating-point results easier to read.
    """

    if isinstance(result, float):

        # Turn 5.0 into 5
        if result.is_integer():
            return int(result)

        # Avoid displaying extremely long decimals
        return round(result, 10)

    return result


def to_radians(value, mode):
    """
    Convert degrees to radians when necessary.

    Python's math.sin(), math.cos(), etc. use radians.
    """

    if mode == "Degrees":
        return math.radians(value)

    return value


def from_radians(value, mode):
    """
    Convert radians back to degrees for inverse
    trigonometric functions.
    """

    if mode == "Degrees":
        return math.degrees(value)

    return value


# ============================================================
# PAGE TITLE
# ============================================================

st.title("🧮 Scientific Calculator")

st.write(
    "A beginner-friendly scientific calculator "
    "built with Python and Streamlit."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙️ Settings")


# Angle mode
angle_mode = st.sidebar.radio(
    "Trigonometry Angle Mode",
    ["Degrees", "Radians"]
)


st.sidebar.divider()


# ============================================================
# MEMORY SECTION
# ============================================================

st.sidebar.subheader("🧠 Memory")

memory_col1, memory_col2 = st.sidebar.columns(2)


# MC = Memory Clear
with memory_col1:

    if st.button("MC"):
        st.session_state.memory = 0.0
        st.sidebar.success("Memory cleared.")


# MR = Memory Recall
with memory_col2:

    if st.button("MR"):
        st.session_state.answer = st.session_state.memory
        st.sidebar.success(
            f"Memory recalled: {st.session_state.memory}"
        )


st.sidebar.write(
    f"Current Memory: **{st.session_state.memory}**"
)


# ============================================================
# HISTORY
# ============================================================

st.sidebar.divider()

st.sidebar.subheader("📜 Calculation History")


if st.session_state.history:

    # Show newest calculations first
    for calculation in reversed(
        st.session_state.history[-10:]
    ):
        st.sidebar.write(calculation)

    if st.sidebar.button("🗑️ Clear History"):

        st.session_state.history = []

        st.rerun()

else:

    st.sidebar.info("No calculations yet.")


# ============================================================
# MAIN CALCULATOR
# ============================================================

st.header("🔢 Calculator")


# ------------------------------------------------------------
# Number inputs
# ------------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    number1 = st.number_input(
        "First Number",
        value=0.0,
        key="first_number"
    )


with col2:

    number2 = st.number_input(
        "Second Number",
        value=0.0,
        key="second_number"
    )


# ------------------------------------------------------------
# Operation
# ------------------------------------------------------------

operation = st.selectbox(
    "Select Operation",
    [
        "Addition (+)",
        "Subtraction (-)",
        "Multiplication (×)",
        "Division (÷)",
        "Power (xʸ)",
        "Percentage (%)",
        "Modulus (%)",

        "Square Root (√)",
        "Cube Root (∛)",
        "Factorial (!)",
        "Absolute Value",

        "sin",
        "cos",
        "tan",

        "asin",
        "acos",
        "atan",

        "sinh",
        "cosh",
        "tanh",

        "log₁₀",
        "Natural Log (ln)"
    ]
)


# ============================================================
# CALCULATE
# ============================================================

if st.button(
    "🟰 Calculate",
    type="primary",
    use_container_width=True
):

    try:

        # ====================================================
        # BASIC OPERATIONS
        # ====================================================

        if operation == "Addition (+)":

            result = number1 + number2

            expression = (
                f"{number1} + {number2}"
            )


        elif operation == "Subtraction (-)":

            result = number1 - number2

            expression = (
                f"{number1} - {number2}"
            )


        elif operation == "Multiplication (×)":

            result = number1 * number2

            expression = (
                f"{number1} × {number2}"
            )


        elif operation == "Division (÷)":

            if number2 == 0:

                st.error(
                    "❌ Division by zero is not allowed."
                )

                st.stop()

            result = number1 / number2

            expression = (
                f"{number1} ÷ {number2}"
            )


        elif operation == "Power (xʸ)":

            result = number1 ** number2

            expression = (
                f"{number1}^{number2}"
            )


        elif operation == "Percentage (%)":

            result = (
                number1 * number2 / 100
            )

            expression = (
                f"{number2}% of {number1}"
            )


        elif operation == "Modulus (%)":

            if number2 == 0:

                st.error(
                    "❌ Modulus by zero is not allowed."
                )

                st.stop()

            result = number1 % number2

            expression = (
                f"{number1} % {number2}"
            )


        # ====================================================
        # ROOTS
        # ====================================================

        elif operation == "Square Root (√)":

            if number1 < 0:

                st.error(
                    "❌ Square root of a negative number "
                    "is not a real number."
                )

                st.stop()

            result = math.sqrt(number1)

            expression = f"√{number1}"


        elif operation == "Cube Root (∛)":

            # math.cbrt() works with negative numbers too.
            result = math.cbrt(number1)

            expression = f"∛{number1}"


        # ====================================================
        # FACTORIAL
        # ====================================================

        elif operation == "Factorial (!)":

            if number1 < 0:

                st.error(
                    "❌ Factorial cannot be negative."
                )

                st.stop()

            if not number1.is_integer():

                st.error(
                    "❌ Factorial requires a whole number."
                )

                st.stop()

            result = math.factorial(
                int(number1)
            )

            expression = f"{int(number1)}!"


        # ====================================================
        # ABSOLUTE VALUE
        # ====================================================

        elif operation == "Absolute Value":

            result = abs(number1)

            expression = f"|{number1}|"


        # ====================================================
        # TRIGONOMETRY
        # ====================================================

        elif operation == "sin":

            angle = to_radians(
                number1,
                angle_mode
            )

            result = math.sin(angle)

            expression = (
                f"sin({number1}°)"
                if angle_mode == "Degrees"
                else f"sin({number1})"
            )


        elif operation == "cos":

            angle = to_radians(
                number1,
                angle_mode
            )

            result = math.cos(angle)

            expression = (
                f"cos({number1}°)"
                if angle_mode == "Degrees"
                else f"cos({number1})"
            )


        elif operation == "tan":

            angle = to_radians(
                number1,
                angle_mode
            )

            # cos(angle) close to zero means tan is
            # undefined.
            if abs(math.cos(angle)) < 1e-12:

                st.error(
                    "❌ Tangent is undefined at this angle."
                )

                st.stop()

            result = math.tan(angle)

            expression = (
                f"tan({number1}°)"
                if angle_mode == "Degrees"
                else f"tan({number1})"
            )


        # ====================================================
        # INVERSE TRIGONOMETRY
        # ====================================================

        elif operation == "asin":

            if not -1 <= number1 <= 1:

                st.error(
                    "❌ asin requires a value between -1 and 1."
                )

                st.stop()

            result = math.asin(number1)

            result = from_radians(
                result,
                angle_mode
            )

            expression = f"asin({number1})"


        elif operation == "acos":

            if not -1 <= number1 <= 1:

                st.error(
                    "❌ acos requires a value between -1 and 1."
                )

                st.stop()

            result = math.acos(number1)

            result = from_radians(
                result,
                angle_mode
            )

            expression = f"acos({number1})"


        elif operation == "atan":

            result = math.atan(number1)

            result = from_radians(
                result,
                angle_mode
            )

            expression = f"atan({number1})"


        # ====================================================
        # HYPERBOLIC FUNCTIONS
        # ====================================================

        elif operation == "sinh":

            result = math.sinh(number1)

            expression = f"sinh({number1})"


        elif operation == "cosh":

            result = math.cosh(number1)

            expression = f"cosh({number1})"


        elif operation == "tanh":

            result = math.tanh(number1)

            expression = f"tanh({number1})"


        # ====================================================
        # LOGARITHMS
        # ====================================================

        elif operation == "log₁₀":

            if number1 <= 0:

                st.error(
                    "❌ log₁₀ requires a positive number."
                )

                st.stop()

            result = math.log10(number1)

            expression = f"log₁₀({number1})"


        elif operation == "Natural Log (ln)":

            if number1 <= 0:

                st.error(
                    "❌ ln requires a positive number."
                )

                st.stop()

            result = math.log(number1)

            expression = f"ln({number1})"


        # ====================================================
        # SAVE RESULT
        # ====================================================

        result = format_result(result)

        st.session_state.answer = result

        add_history(
            expression,
            result
        )

        st.success(
            f"### Result: {result}"
        )


    except OverflowError:

        st.error(
            "❌ The number is too large to calculate."
        )


    except ValueError:

        st.error(
            "❌ This mathematical operation is invalid."
        )


    except Exception:

        st.error(
            "❌ Something went wrong. "
            "Please check your input."
        )


# ============================================================
# ANSWER / MEMORY CONTROLS
# ============================================================

st.divider()

st.header("🧠 Answer & Memory")


answer_col1, answer_col2, answer_col3, answer_col4 = (
    st.columns(4)
)


# Previous answer
with answer_col1:

    st.metric(
        "Ans",
        st.session_state.answer
    )


# M+
with answer_col2:

    if st.button(
        "M+",
        use_container_width=True
    ):

        st.session_state.memory += (
            st.session_state.answer
        )

        st.success("Added to memory.")


# M-
with answer_col3:

    if st.button(
        "M−",
        use_container_width=True
    ):

        st.session_state.memory -= (
            st.session_state.answer
        )

        st.success("Subtracted from memory.")


# Clear answer
with answer_col4:

    if st.button(
        "Clear Ans",
        use_container_width=True
    ):

        st.session_state.answer = 0.0

        st.rerun()


# ============================================================
# CONSTANTS
# ============================================================

st.divider()

st.header("📐 Mathematical Constants")


constant1, constant2 = st.columns(2)


with constant1:

    st.info(
        f"π = {math.pi}"
    )


with constant2:

    st.info(
        f"e = {math.e}"
    )


# ============================================================
# EXTRA TOOLS
# ============================================================

st.divider()

st.header("🛠️ Calculator Tools")


tool = st.selectbox(
    "Choose a tool",
    [
        "Percentage Calculator",
        "Quadratic Equation Solver",
        "Prime Number Checker",
        "Factorial Calculator",
        "GCD & LCM Calculator",
        "Unit Converter",
        "BMI Calculator",
        "Random Number Generator",
        "Scientific Notation",
        "Number System Converter"
    ]
)


# ============================================================
# PERCENTAGE CALCULATOR
# ============================================================

if tool == "Percentage Calculator":

    st.subheader("📊 Percentage Calculator")

    value = st.number_input(
        "Original value",
        value=100.0
    )

    percentage = st.number_input(
        "Percentage",
        value=10.0
    )

    if st.button("Calculate Percentage"):

        result = (
            value * percentage / 100
        )

        st.success(
            f"{percentage}% of {value} = {result}"
        )


# ============================================================
# QUADRATIC EQUATION
# ============================================================

elif tool == "Quadratic Equation Solver":

    st.subheader(
        "📐 Quadratic Equation Solver"
    )

    st.write(
        "Solve an equation in the form:"
    )

    st.latex(
        r"ax^2 + bx + c = 0"
    )

    a = st.number_input(
        "a",
        value=1.0
    )

    b = st.number_input(
        "b",
        value=0.0
    )

    c = st.number_input(
        "c",
        value=0.0
    )

    if st.button("Solve Equation"):

        if a == 0:

            st.error(
                "❌ a cannot be zero."
            )

        else:

            discriminant = (
                b**2 - 4*a*c
            )

            st.write(
                f"Discriminant = {discriminant}"
            )

            if discriminant > 0:

                x1 = (
                    -b + math.sqrt(discriminant)
                ) / (2*a)

                x2 = (
                    -b - math.sqrt(discriminant)
                ) / (2*a)

                st.success(
                    f"x₁ = {x1}"
                )

                st.success(
                    f"x₂ = {x2}"
                )


            elif discriminant == 0:

                x = -b / (2*a)

                st.success(
                    f"x = {x}"
                )


            else:

                real_part = -b / (2*a)

                imaginary_part = (
                    math.sqrt(-discriminant)
                    / (2*a)
                )

                st.info(
                    f"x₁ = {real_part} + "
                    f"{imaginary_part}i"
                )

                st.info(
                    f"x₂ = {real_part} - "
                    f"{imaginary_part}i"
                )


# ============================================================
# PRIME NUMBER CHECKER
# ============================================================

elif tool == "Prime Number Checker":

    st.subheader(
        "🔢 Prime Number Checker"
    )

    number = st.number_input(
        "Enter a whole number",
        value=17,
        step=1
    )

    if st.button("Check Number"):

        number = int(number)

        if number < 2:

            st.info(
                f"{number} is not prime."
            )

        else:

            is_prime = True

            for i in range(
                2,
                int(math.sqrt(number)) + 1
            ):

                if number % i == 0:

                    is_prime = False

                    break

            if is_prime:

                st.success(
                    f"{number} is prime! 🎉"
                )

            else:

                st.info(
                    f"{number} is not prime."
                )


# ============================================================
# FACTORIAL CALCULATOR
# ============================================================

elif tool == "Factorial Calculator":

    st.subheader(
        "❗ Factorial Calculator"
    )

    number = st.number_input(
        "Enter a non-negative whole number",
        min_value=0,
        value=5,
        step=1
    )

    if st.button("Calculate Factorial"):

        result = math.factorial(
            int(number)
        )

        st.success(
            f"{int(number)}! = {result}"
        )


# ============================================================
# GCD & LCM
# ============================================================

elif tool == "GCD & LCM Calculator":

    st.subheader(
        "🔗 GCD & LCM Calculator"
    )

    a = st.number_input(
        "First integer",
        value=12,
        step=1
    )

    b = st.number_input(
        "Second integer",
        value=18,
        step=1
    )

    if st.button("Calculate"):

        a = int(a)
        b = int(b)

        gcd = math.gcd(a, b)

        if a == 0 or b == 0:

            lcm = 0

        else:

            lcm = abs(
                a * b
            ) // gcd

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"GCD = {gcd}"
            )

        with col2:

            st.success(
                f"LCM = {lcm}"
            )


# ============================================================
# UNIT CONVERTER
# ============================================================

elif tool == "Unit Converter":

    st.subheader(
        "📏 Basic Unit Converter"
    )

    conversion = st.selectbox(
        "Choose conversion",
        [
            "Kilometers → Miles",
            "Miles → Kilometers",
            "Meters → Feet",
            "Feet → Meters",
            "Kilograms → Pounds",
            "Pounds → Kilograms",
            "Celsius → Fahrenheit",
            "Fahrenheit → Celsius"
        ]
    )

    value = st.number_input(
        "Enter value",
        value=1.0
    )

    if st.button("Convert"):

        if conversion == "Kilometers → Miles":

            result = value * 0.621371


        elif conversion == "Miles → Kilometers":

            result = value * 1.609344


        elif conversion == "Meters → Feet":

            result = value * 3.28084


        elif conversion == "Feet → Meters":

            result = value * 0.3048


        elif conversion == "Kilograms → Pounds":

            result = value * 2.20462


        elif conversion == "Pounds → Kilograms":

            result = value * 0.453592


        elif conversion == "Celsius → Fahrenheit":

            result = (
                value * 9/5
            ) + 32


        else:

            result = (
                value - 32
            ) * 5/9


        st.success(
            f"Result = {format_result(result)}"
        )


# ============================================================
# BMI CALCULATOR
# ============================================================

elif tool == "BMI Calculator":

    st.subheader(
        "⚖️ BMI Calculator"
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        value=60.0
    )

    height = st.number_input(
        "Height (meters)",
        min_value=0.1,
        value=1.65
    )

    if st.button("Calculate BMI"):

        bmi = weight / (
            height ** 2
        )

        st.success(
            f"BMI = {round(bmi, 2)}"
        )


# ============================================================
# RANDOM NUMBER GENERATOR
# ============================================================

elif tool == "Random Number Generator":

    st.subheader(
        "🎲 Random Number Generator"
    )

    minimum = st.number_input(
        "Minimum",
        value=1,
        step=1
    )

    maximum = st.number_input(
        "Maximum",
        value=100,
        step=1
    )

    if st.button("Generate"):

        if minimum > maximum:

            st.error(
                "❌ Minimum cannot be greater "
                "than maximum."
            )

        else:

            result = random.randint(
                int(minimum),
                int(maximum)
            )

            st.success(
                f"🎲 Random number = {result}"
            )


# ============================================================
# SCIENTIFIC NOTATION
# ============================================================

elif tool == "Scientific Notation":

    st.subheader(
        "🔬 Scientific Notation"
    )

    number = st.number_input(
        "Enter a number",
        value=1234567.0,
        format="%.10f"
    )

    if st.button("Convert"):

        if number == 0:

            st.info(
                "0 = 0 × 10⁰"
            )

        else:

            scientific = f"{number:.6e}"

            st.success(
                f"Scientific notation: {scientific}"
            )


# ============================================================
# NUMBER SYSTEM CONVERTER
# ============================================================

elif tool == "Number System Converter":

    st.subheader(
        "🔄 Number System Converter"
    )

    decimal_number = st.number_input(
        "Enter a decimal integer",
        value=10,
        step=1
    )

    if st.button("Convert"):

        number = int(
            decimal_number
        )

        st.write(
            f"Binary: `{bin(number)}`"
        )

        st.write(
            f"Octal: `{oct(number)}`"
        )

        st.write(
            f"Decimal: `{number}`"
        )

        st.write(
            f"Hexadecimal: `{hex(number)}`"
        )


# ============================================================
# HELP SECTION
# ============================================================

st.divider()

with st.expander("📚 How does this calculator work?"):

    st.markdown(
        """
        ### 🔢 Basic Operations

        Enter one or two numbers and select an operation.

        ### 📐 Trigonometry

        Choose **Degrees** or **Radians** from the sidebar.

        Python's math functions internally use radians,
        so the application converts degrees when necessary.

        ### 🧠 Memory

        **M+** → Add current answer to memory.

        **M−** → Subtract current answer from memory.

        **MR** → Recall memory.

        **MC** → Clear memory.

        **Ans** → Shows the previous answer.

        ### 📜 History

        Your recent calculations appear in the sidebar.

        ### 🛠️ Extra Tools

        The calculator also contains mathematical and
        conversion tools for additional functionality.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🧮 Scientific Calculator • "
    "Built with Python + Streamlit"
)
```
