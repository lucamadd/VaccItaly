from flask import Flask, render_template
from flask_cors import cross_origin, CORS
app = Flask(__name__,
            static_url_path='', 
            static_folder='static')
#cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')



if __name__ == '__main__':
    try:
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(host='0.0.0.0', port=8080)
        
    except RuntimeError as msg:
        exit()