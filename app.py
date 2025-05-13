from flask import Flask, request
from sympy import solve, Eq, Symbol
import re

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    from_number = request.form.get('From')
    msg_body = request.form.get('Body')

    response = process_math(msg_body.strip())

    return f'<Response><Message>{response}</Message></Response>', 200, {'Content-Type': 'application/xml'}

def process_math(msg):
    try:
        if "=" in msg:
            x = Symbol('x')
            left, right = msg.split("=")
            equation = Eq(eval(left), eval(right))
            sol = solve(equation, x)
            return f'Solution: x = {sol[0]}'
        else:
            result = eval(msg)
            return f'Result: {result}'
    except:
        return "Sorry, couldn't understand or solve that equation."

if __name__ == '__main__':
    app.run()
