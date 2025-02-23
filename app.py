from flask import Flask, render_template_string, request
import json

app = Flask(__name__)

DATA_FILE = "universities.json"

DEFAULT_UNIVERSITIES = [
    "Harvard University",
    "Stanford University",
    "Massachusetts Institute of Technology (MIT)",
    "University of Oxford",
    "California Institute of Technology (Caltech)",
    "University of Cambridge",
    "Princeton University",
    "Yale University",
    "University of Chicago",
    "Columbia University"
]

def load_universities():
    try:
        with open(DATA_FILE, "r") as file:
            universities = json.load(file)
            return universities if universities else DEFAULT_UNIVERSITIES
    except FileNotFoundError:
        print("Error: Data file not found. Using default universities.")
        return DEFAULT_UNIVERSITIES
    except json.JSONDecodeError:
        print("Error: Data file is corrupted. Using default universities.")
        return DEFAULT_UNIVERSITIES

def get_universities(search_query=""):
    universities = load_universities()
    if not universities:
        print("Error: No university data available.")
    print(f"Searching for: {search_query}")  # Debugging output
    print(f"Available universities: {universities}")  # Debugging output
    return [u for u in universities if search_query.lower() in u.lower()]

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>University List</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            text-align: center;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            margin-bottom: 20px;
        }
        input[type="text"] {
            padding: 10px;
            width: 300px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 15px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            background: white;
            padding: 10px;
            margin: 5px auto;
            width: 50%;
            border-radius: 5px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .no-results {
            color: red;
            font-weight: bold;
        }
        .error {
            color: darkred;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Search for a University</h1>
    <form method="GET" action="/">
        <input type="text" name="search" placeholder="Search University" value="{{ search_query }}">
        <button type="submit">Search</button>
    </form>
    {% if search_query and universities %}
        <ul>
            {% for university in universities %}
                <li>{{ university }}</li>
            {% endfor %}
        </ul>
    {% elif search_query %}
        <p class="no-results">No universities found.</p>
        <p class="error">Cannot find any university matching "{{ search_query }}".</p>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def university_list():
    search_query = request.args.get('search', '').strip().lower()
    universities = get_universities(search_query)
    return render_template_string(html_template, universities=universities, search_query=search_query)

if __name__ == '__main__':
    app.run(debug=True)
