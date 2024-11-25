from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample user data (in-memory storage for now)
users = {
    'testuser': {'password': 'testpass', 'balance': 1000}
}

@app.route('/')
def home():
    return render_template('bank_frontend.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            return redirect(url_for('dashboard', username=username))
        else:
            return 'Login Failed! Check your credentials.'

    return render_template('login.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    if username in users:
        balance = users[username]['balance']
        return render_template('dashboard.html', username=username, balance=balance)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
