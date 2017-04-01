from app import app

@app.route('/')
@app.route('/indexxx')
def index():
    return "Hello, World!"