app.config['SECRET_KEY'] = 'thisIsSecret'
login_manager = LoginManager(app)
login_manager.login_view="login"
bcrypt = Bcrypt(app)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
#check if already logged in-if so send home
    if current_user.is_authenticated:
        return redirect(url_for('home'))
            # do the standard database stuff and find the user with email

    con = sqlite3.connect("login.db")
    curs = con.cursor()
    email = request.form['email']
    curs.execute("SELECT * FROM login where email = (?)",[email])

    row=curs.fetchone()
    if row==None:
        flash('Please try logging in again')
        return render_template('login.html')
    user = list(row);
    liUser = User(int(user[0]),user[1],user[2])
    password = request.form['password']
    match = bcrypt.check_password_hash(liUser.password, password)

    if match and email==liUser.email:
        login_user(liUser,remember=request.form.get('remember'))

        redirect(url_for('home'))
    else:
        flash('Please try logging in again')
    return render_template('login.html')
    return render_template('home.html')

#@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('login.db')
    curs = conn.cursor()
    curs.execute("SELECT * from login where user_id = (?)",[user_id])
    liUser= curs.fetchone()
    if liUser is None:
        return None
    else:
        return User(int(liUser[0]), liUser[1], liUser[2])

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def register_post():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        # standard DB stuff
    con = sqlite3.connect("login.db")
    curs = con.cursor()
    email= request.form['email']
    password = request.form['password']
    hashedPassword = bcrypt.generate_password_hash(password)
    con.execute('insert into login (email,password) VALUES (?,?)', [email, hashedPassword])
    con.commit()
    return render_template('home.html')
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id= id
        self.email =email
        self.password = password
        self.authenticated = False
        def is_active(self):
            return self.is_active()
        def is_anonymous(self):
            return False
        def is_active(self):
            return True
        def get_id(self):
            return self.id