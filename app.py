from flask import Flask, request, render_template as render, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.name}')"
    
db.create_all()

@app.route('/')
def home():
    return render('home.html')


@app.route('/signup')
def signup():
    return render('signup.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(username=username, name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render('register.html')


@app.route("/login")
def login_page():
    return render('login.html')

@app.route('/login-user', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"
    return render('login.html')

if __name__ == '__main__':
    app.run(debug=True)