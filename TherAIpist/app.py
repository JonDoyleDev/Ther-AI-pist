import os
import openai
from flask import Flask, request, render_template_string

app = Flask(__name__)

openai.api_key = "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"

html_template = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>TherAIpist</title>
    <style>
        * {
            box-sizing: border-box;
        }
        
        #disclaimer { 
            text-align: center;
            justify-content: center;
            color: red;
        }
        
        #paypal { 
            text-align: center;
            justify-content: center;
            color: #6C95CF;
        }
        
        #donations { 
            text-align: center;
            justify-content: center;
        }
        
        #user-question { 
            justify-content: center;
            text-align: center;
        }
        
        #callToAction { 
            text-align: center;
            justify-content: center;
            color: white;
        }
        
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #1c1c1c;
        }
        .container {
            max-width: 800px;
            margin: auto;
            background-color: #333333;
            padding: 20px;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 20px;
            text-align: center;
            color: #ffffff;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #ffffff;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #555555;
            border-radius: 4px;
            background-color: #555555;
            color: #ffffff;
        }
        input[type="submit"] {
            background-color: white;
            color: black;
            font-weight: 900;
            text-transform: uppercase;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        input[type="submit"]:hover {
            background-color: green;
        }
        hr {
            border: none;
            border-top: 1px solid #555555;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 18px;
            margin-bottom: 10px;
            color: #ffffff;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            margin-bottom: 10px;
            color: #ffffff;
        }
        strong {
            font-weight: bold;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Ther•AI•pist</h1>
    <form method="post" id="user-question">
        <label for="message">What problem or problems are you trying to work through right now?</label>
        <input type="text" name="message" id="message" required>
        <input type="submit" value="Help Me">
    </form>
    <ul>
        {% for entry in chat_history %}
            <li><strong>{{ entry[0] }}:</strong> {{ entry[1] }}</li>
        {% endfor %}
    </ul>
</div>
<div class="container" id="disclaimer"> 
    <h5>AI is not a doctor. If you are at risk of harm or need REAL therapy, seek help from a medical professional immediately.</h5>
</div>
<div class="container" id="donations">
    <h5 id="callToAction">Unfortunately it costs money to keep me alive, every donation helps!</h5> 
    <h3 id="paypal"><a href="https://www.paypal.me/digitalmud">Paypal</a></h3>
<div>
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def chat():
    chat_history = []
    if request.method == 'POST':
        user_message = request.form['message']
        chat_history.append(("You", user_message))

        prompt = f"{user_message}\nAI: Pretend you're a therapist, what advice do you have?\n"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5,
        )
        ai_message = response.choices[0].text.strip()
        chat_history.append(("TherAIpist Advice", ai_message))

    return render_template_string(html_template, chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
