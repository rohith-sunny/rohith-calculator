const display = document.getElementById('display');
const clearButton = document.getElementById('clear');
const addButton = document.getElementById('add');
const subtractButton = document.getElementById('subtract');
const multiplyButton = document.getElementById('multiply');
const divideButton = document.getElementById('divide');
const equalsButton = document.getElementById('equals');
const decimalButton = document.getElementById('decimal');

const digitButtons = [
    document.getElementById('digit_0'),
    document.getElementById('digit_1'),
    document.getElementById('digit_2'),
    document.getElementById('digit_3'),
    document.getElementById('digit_4'),
    document.getElementById('digit_5'),
    document.getElementById('digit_6'),
    document.getElementById('digit_7'),
    document.getElementById('digit_8'),
    document.getElementById('digit_9')
];

let currentOperand = '';
let previousOperand = '';
let operator = null;
let shouldResetDisplay = false;

function add(a, b) { return a + b; }
function subtract(a, b) { return a - b; }
function multiply(a, b) { return a * b; }
function divide(a, b) { 
    if (b === 0) {
        alert("Cannot divide by zero!");
        return NaN;
    }
    return a / b; 
}

function appendNumber(number) {
    if (shouldResetDisplay) {
        display.value = number;
        shouldResetDisplay = false;
    } else {
        if (display.value === '0' && number !== '.') {
            display.value = number;
        } else {
            display.value += number;
        }
    }
}

function chooseOperator(op) {
    if (currentOperand === '' && display.value === '0') return; // Prevent setting operator if nothing is entered
    if (previousOperand !== '' && operator !== null && !shouldResetDisplay) {
        calculate();
    }
    previousOperand = display.value;
    operator = op;
    shouldResetDisplay = true;
}

function calculate() {
    let computation;
    const prev = parseFloat(previousOperand);
    const current = parseFloat(display.value);
    if (isNaN(prev) || isNaN(current)) return;

    switch (operator) {
        case '+':
            computation = add(prev, current);
            break;
        case '-':
            computation = subtract(prev, current);
            break;
        case '*':
            computation = multiply(prev, current);
            break;
        case '/':
            computation = divide(prev, current);
            break;
        default:
            return;
    }
    display.value = computation;
    operator = null;
    previousOperand = '';
    shouldResetDisplay = true;
}

function clearCalculator() {
    display.value = '0';
    currentOperand = '';
    previousOperand = '';
    operator = null;
    shouldResetDisplay = false;
}

// Event Listeners
digitButtons.forEach(button => {
    if (button) { // Check if button exists
        button.addEventListener('click', () => appendNumber(button.textContent));
    }
});

decimalButton.addEventListener('click', () => {
    if (shouldResetDisplay) {
        display.value = '0.';
        shouldResetDisplay = false;
    } else if (!display.value.includes('.')) {
        display.value += '.';
    }
});

clearButton.addEventListener('click', clearCalculator);
addButton.addEventListener('click', () => chooseOperator('+'));
subtractButton.addEventListener('click', () => chooseOperator('-'));
multiplyButton.addEventListener('click', () => chooseOperator('*'));
divideButton.addEventListener('click', () => chooseOperator('/'));
equalsButton.addEventListener('click', calculate);