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
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Roboto', Arial, sans-serif;
            background-color: #f0f2f5;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            max-width: 800px;
            background-color: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        h1 {
            font-size: 32px;
            margin-bottom: 20px;
            text-align: center;
            color: #333333;
        }

        #disclaimer {
            text-align: center;
            justify-content: center;
            color: red;
            margin-top: 20px;
            font-size: 14px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #333333;
        }

        input[type="text"] {
            width: 100%;
            padding: 12px;
            margin-bottom: 20px;
            border: 1px solid #dddddd;
            border-radius: 4px;
            background-color: #ffffff;
            color: #333333;
        }

        input[type="submit"] {
            background-color: #3498db;
            color: #ffffff;
            font-weight: 900;
            text-transform: uppercase;
            padding: 12px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 100%;
        }

        input[type="submit"]:hover {
            background-color: #2980b9;
        }

        hr {
            border: none;
            border-top: 1px solid #dddddd;
            margin-bottom: 20px;
        }

        h2 {
            font-size: 20px;
            margin-bottom: 10px;
            color: #333333;
        }

        ul {
            list-style: none;
            padding: 0;
        }

        li {
            margin-bottom: 10px;
            color: #333333;
        }

        strong {
            font-weight: bold;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Ther•AI•pist</h1>
    <form method="post">
        <label for="message">What problem or problems are you trying to work through right now?</label>
        <input type="text" name="message" id="message" required>
        <input type="submit" value="Help Me">
    </form>
    <hr>
    <h2>Ther•AI•pist's Advice</h2>
    <ul>
        {% for entry in chat_history %}
            <li><strong>{{ entry[0] }}:</strong> {{ entry[1] }}</li>
        {% endfor %}
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def chat():
    chat_history = []
    if request.method == 'POST':
        user_message = request.form['message']
        chat_history.append(("You", user_message))

        prompt = f"User wants help with '{user_message}'\nAI: Pretend you're a therapist, what advice do you have? \n"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.5,
        )
        ai_message = response.choices[0].text.strip()
        chat_history.append(("TherAIpist", ai_message))

    return render_template_string(html_template, chat_history=chat_history)

if __name__ == '__main__':
    app.run(debug=True)
