from flask import Flask, request, make_response, redirect, render_template

app = Flask(__name__)

todos = ['Create simple flask project', 'Upload project to azure using terraform', 'Show my web']

@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip', user_ip)
    return response

@app.route('/index')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }


    return render_template('index.html', **context)