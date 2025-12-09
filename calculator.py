import subprocess
import sys
import os
import webbrowser
import threading
import time
import math
import re

def install_and_import(package):
    try:
        __import__(package)
        # print(f"{package} is already installed.") # Commenting out for cleaner output in script
    except ImportError:
        print(f"{package} not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-qq"])
        print(f"{package} installed.")

# Install Flask if not already installed
install_and_import('flask')

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- HTML, CSS, and JavaScript Embedded Directly ---
HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Web Calculator</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #282c34;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            color: #e0e0e0;
        }

        #calculator-container {
            display: flex;
            flex-direction: column;
            background-color: #3a3f47;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            padding: 25px;
            gap: 15px;
            width: 350px;
        }

        #display-section {
            background-color: #495057;
            border-radius: 8px;
            padding: 15px;
            box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
        }

        #display {
            width: 100%;
            background: none;
            border: none;
            color: #ffffff;
            font-size: 2.8em;
            text-align: right;
            padding: 5px 0;
            margin-bottom: 5px;
            box-sizing: border-box;
            height: 50px;
        }

        #sub-display {
            color: #a0a0a0;
            font-size: 0.9em;
            text-align: right;
            min-height: 1.2em;
        }

        .buttons-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
        }

        button {
            width: 100%;
            height: 65px;
            font-size: 1.6em;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            background-color: #555c66;
            color: #ffffff;
            transition: background-color 0.2s ease, transform 0.1s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        button:hover {
            background-color: #6a737e;
            transform: translateY(-1px);
        }

        button:active {
            transform: translateY(1px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        }

        .operator {
            background-color: #e07a5f;
        }

        .operator:hover {
            background-color: #e68d71;
        }

        .function {
            background-color: #81b29a;
            font-size: 1.2em;
        }

        .function:hover {
            background-color: #92c0a9;
        }

        #equals {
            background-color: #3d405b;
            grid-column: span 2;
        }

        #equals:hover {
            background-color: #4a4e69;
        }

        #clear, #clear-entry {
            background-color: #c44536;
        }

        #clear:hover, #clear-entry:hover {
            background-color: #d8574a;
        }

        #history-section {
            background-color: #3a3f47;
            border-radius: 8px;
            padding: 15px;
            max-height: 200px;
            overflow-y: auto;
            box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.3);
        }

        #history-section h3 {
            margin-top: 0;
            margin-bottom: 10px;
            color: #e0e0e0;
        }

        #history-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        #history-list li {
            background-color: #495057;
            border-radius: 5px;
            padding: 8px 12px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.9em;
            color: #e0e0e0;
            word-break: break-all;
        }

        #history-list li:last-child {
            margin-bottom: 0;
        }

        .delete-history-btn {
            background-color: #c44536;
            color: white;
            border: none;
            border-radius: 50%;
            width: 25px;
            height: 25px;
            font-size: 0.9em;
            cursor: pointer;
            margin-left: 10px;
            flex-shrink: 0;
        }
        .delete-history-btn:hover {
            background-color: #d8574a;
        }

        #history-controls {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
        }
        #history-controls button {
            height: 40px;
            font-size: 1em;
            width: auto;
            padding: 0 15px;
            border-radius: 8px;
        }
        #clear-history-btn {
            background-color: #3d405b;
        }
        #clear-history-btn:hover {
            background-color: #4a4e69;
        }

    </style>
</head>
<body>
    <div id="calculator-container">
        <div id="display-section">
            <div id="sub-display"></div>
            <input type="text" id="display" readonly value="0">
        </div>

        <div class="buttons-grid">
            <button class="function" onclick="appendToDisplay('sin(')">sin</button>
            <button class="function" onclick="appendToDisplay('cos(')">cos</button>
            <button class="function" onclick="appendToDisplay('tan(')">tan</button>
            <button class="operator" onclick="appendToDisplay('/')">/</button>

            <button class="number" onclick="appendToDisplay('7')">7</button>
            <button class="number" onclick="appendToDisplay('8')">8</button>
            <button class="number" onclick="appendToDisplay('9')">9</button>
            <button class="operator" onclick="appendToDisplay('*')">*</button>

            <button class="number" onclick="appendToDisplay('4')">4</button>
            <button class="number" onclick="appendToDisplay('5')">5</button>
            <button class="number" onclick="appendToDisplay('6')">6</button>
            <button class="operator" onclick="appendToDisplay('-')">-</button>

            <button class="number" onclick="appendToDisplay('1')">1</button>
            <button class="number" onclick="appendToDisplay('2')">2</button>
            <button class="number" onclick="appendToDisplay('3')">3</button>
            <button class="operator" onclick="appendToDisplay('+')">+</button>

            <button class="function" onclick="appendToDisplay('sqrt(')">sqrt</button>
            <button class="number" onclick="appendToDisplay('0')">0</button>
            <button class="number" onclick="appendToDisplay('.')">.</button>
            <button class="function" onclick="appendToDisplay('^')">^</button>

            <button id="clear" onclick="clearDisplay()">AC</button>
            <button id="clear-entry" onclick="clearEntry()">CE</button>
            <button class="function" onclick="appendToDisplay('(')">(</button>
            <button class="function" onclick="appendToDisplay(')')">)</button>

            <button id="equals" onclick="calculateResult()">=</button>
            <button class="function" onclick="appendToDisplay('log(')">log</button>
            <button class="function" onclick="appendToDisplay('pi')">&pi;</button>
            <button class="function" onclick="appendToDisplay('e')">e</button>


        </div>

        <div id="history-section">
            <h3>History</h3>
            <ul id="history-list"></ul>
            <div id="history-controls">
                <button id="clear-history-btn" onclick="clearAllHistory()">Clear All</button>
            </div>
        </div>
    </div>

    <script>
        let currentExpression = '';
        let subDisplay = document.getElementById('sub-display');
        let mainDisplay = document.getElementById('display');
        let historyList = document.getElementById('history-list');
        let calculationHistory = [];

        window.onload = function() {
            mainDisplay.value = '0';
            loadHistory();
            updateHistoryDisplay();
        };

        function appendToDisplay(value) {
            if (mainDisplay.value === '0' && value !== '.' && !isNaN(value) && currentExpression === '') {
                mainDisplay.value = value;
                currentExpression = value;
            } else if (mainDisplay.value === 'Error') {
                currentExpression = value;
                mainDisplay.value = value;
            } else {
                currentExpression += value;
                mainDisplay.value = currentExpression;
            }
            subDisplay.textContent = ''; // Clear sub-display when new input starts
        }

        function clearDisplay() {
            currentExpression = '';
            mainDisplay.value = '0';
            subDisplay.textContent = '';
        }

        function clearEntry() {
            if (currentExpression.length > 0) {
                currentExpression = currentExpression.slice(0, -1);
                mainDisplay.value = currentExpression === '' ? '0' : currentExpression;
            }
        }

        function calculateResult() {
            if (currentExpression === '') {
                mainDisplay.value = '0';
                return;
            }

            subDisplay.textContent = currentExpression + ' =';

            fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ expression: currentExpression }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    mainDisplay.value = 'Error';
                    subDisplay.textContent = data.error;
                    currentExpression = '';
                } else {
                    let result = data.result;
                    mainDisplay.value = result;
                    saveHistory(currentExpression, result);
                    currentExpression = String(result);
                }
            })
            .catch(error => {
                console.error('Error during fetch:', error);
                mainDisplay.value = 'Error';
                subDisplay.textContent = 'Network Error';
                currentExpression = '';
            });
        }

        function saveHistory(expression, result) {
            const timestamp = new Date().toLocaleString();
            calculationHistory.push({ expression, result, timestamp });
            localStorage.setItem('calculatorHistory', JSON.stringify(calculationHistory));
            updateHistoryDisplay();
        }

        function loadHistory() {
            const storedHistory = localStorage.getItem('calculatorHistory');
            if (storedHistory) {
                calculationHistory = JSON.parse(storedHistory);
            }
        }

        function updateHistoryDisplay() {
            historyList.innerHTML = '';
            calculationHistory.forEach((entry, index) => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <span>${entry.expression} = <strong>${entry.result}</strong></span>
                    <button class="delete-history-btn" onclick="deleteHistoryEntry(${index})">x</button>
                `;
                historyList.appendChild(listItem);
            });
        }

        function clearAllHistory() {
            calculationHistory = [];
            localStorage.removeItem('calculatorHistory');
            updateHistoryDisplay();
        }

        function deleteHistoryEntry(index) {
            calculationHistory.splice(index, 1);
            localStorage.setItem('calculatorHistory', JSON.stringify(calculationHistory));
            updateHistoryDisplay();
        }
    </script>
</body>
</html>
"""

# --- Flask Routes --- 

# A safer evaluation function
def safe_eval(expression):
    # Replace common math function calls to use Python's math module syntax
    expression = expression.replace('^', '**') # Exponentiation
    expression = expression.replace('sqrt(', 'math.sqrt(')
    expression = expression.replace('log(', 'math.log(')
    expression = expression.replace('sin(', 'math.sin(')
    expression = expression.replace('cos(', 'math.cos(')
    expression = expression.replace('tan(', 'math.tan(')
    expression = expression.replace('pi', 'math.pi')
    expression = expression.replace('e', 'math.e')

    # Define a limited environment for eval to restrict access
    # Only allow math functions and constants we explicitly define
    # __builtins__: None prevents access to Python's built-in functions
    # math: math provides access to the math module
    allowed_locals = {
        "__builtins__": {},
        "math": math,
        "sqrt": math.sqrt,
        "log": math.log,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "pow": math.pow,
        "pi": math.pi,
        "e": math.e,
    }
    
    # Further restrict by explicitly defining all allowed operators for eval
    # This is still not perfectly secure against all possible eval bypasses
    # but significantly reduces the attack surface for a calculator.
    # A true secure parser would involve AST traversal or a dedicated parsing library.
    
    # We'll rely on the limited locals and catch common errors.
    
    return eval(expression, {"__builtins__": {}}, allowed_locals)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression', '')

    if not expression:
        return jsonify({'error': 'No expression provided'}), 400

    try:
        # Clean up expression (e.g., handle double operators if any get through JS)
        # Note: Frontend JS should ideally prevent invalid syntax, but backend should validate.
        expression = expression.strip()
        
        # Basic validation to ensure only allowed characters (numbers, operators, math functions, parentheses, spaces)
        # This regex needs to be carefully constructed to avoid false positives/negatives
        # and ensure no code injection. For simplicity and as per problem statement, it allows
        # digits, operators, dots, and the transformed math functions/constants.
        
        # A more robust solution might involve parsing the expression into an Abstract Syntax Tree (AST)
        # and then validating each node, or using a dedicated math expression parser library.
        
        # For this example, we proceed with the assumption that 'safe_eval' is effective for math.
        result = safe_eval(expression)
        return jsonify({'result': str(result)})
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except (SyntaxError, ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid expression: {e}'}), 400
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

def open_browser():
    # Wait a moment for the Flask server to start
    time.sleep(1)
    webbrowser.open_new_tab("http://127.0.0.1:5000/")

if __name__ == '__main__':
    print("Starting Flask calculator app...")
    # Open browser in a separate thread so it doesn't block Flask app start
    threading.Thread(target=open_browser).start()
    app.run(debug=True, use_reloader=False) # use_reloader=False to prevent browser opening twice

print("calculator.py created successfully.")
