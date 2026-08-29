from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

tasks = []

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask To-Do List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f2f2f2;
            text-align: center;
            padding: 50px;
        }

        .container {
            background: white;
            width: 500px;
            margin: auto;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 10px #aaa;
        }

        h1 {
            color: #2e7d32;
        }

        input {
            padding: 10px;
            width: 65%;
        }

        button {
            padding: 10px 15px;
            background: #2e7d32;
            color: white;
            border: none;
            cursor: pointer;
        }

        li {
            list-style: none;
            padding: 10px;
            margin: 5px;
            background: #eee;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>To-Do List</h1>

    <form method="POST" action="/add">
        <input type="text" name="task" placeholder="Enter a task" required>
        <button type="submit">Add Task</button>
    </form>

    <h2>Tasks</h2>

    <ul>
        {% for task in tasks %}
            <li>{{ task }}</li>
        {% endfor %}
    </ul>

</div>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML, tasks=tasks)


@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")

    if task:
        tasks.append(task)

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)