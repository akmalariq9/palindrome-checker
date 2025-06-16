import re
from datetime import datetime
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'otomata-palindrome-checker-group-3'  
app.config['HISTORY_SIZE'] = 10 

def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    return cleaned == cleaned[::-1]

def init_history():
    """Initialize the history in session if not exists."""
    if 'history' not in session:
        session['history'] = []

def add_to_history(text: str, is_pal: bool):
    """Add a new item to the history."""
    init_history()
    
    history_item = {
        'text': text,
        'is_palindrome': is_pal,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    session['history'].insert(0, history_item)
    session['history'] = session['history'][:app.config['HISTORY_SIZE']]
    
    session.modified = True

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error_message = None
    input_string = ""
    
    if request.method == "POST":
        input_string = request.form.get("input_string", "").strip()
        
        if not input_string:
            error_message = "Please enter a word or phrase to check."
        elif not re.match(r'^[a-zA-Z0-9\s\W]+$', input_string):
            error_message = "Only alphanumeric characters, spaces and punctuation are allowed."
        else:
            is_pal = is_palindrome(input_string)
            if is_pal:
                result = {
                    'message': f"'{input_string}' is a palindrome!",
                    'icon': 'fa-smile-beam'
                }
            else:
                result = {
                    'message': f"'{input_string}' is not a palindrome.",
                    'icon': 'fa-frown'
                }
            
            add_to_history(input_string, is_pal)
    
    history = session.get('history', [])
    
    return render_template(
        "index.html",
        result=result,
        error_message=error_message,
        input_string=input_string,
        history=history
    )

@app.route("/clear-history", methods=["POST"])
def clear_history():
    """Clear the palindrome checking history."""
    if 'history' in session:
        session.pop('history')
    return '', 204  

if __name__ == "__main__":
    app.run(debug=True)
