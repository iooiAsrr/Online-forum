from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL配置
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'ApologizeYa.110'
app.config['MYSQL_DB'] = 'blog'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


@app.route('/')
def home():
    return redirect(url_for('index'))


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and user['password'] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message="用户名或密码无效。")

    return render_template('login.html')


# 注册页面
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()

        session['logged_in'] = True
        session['username'] = username

        return redirect(url_for('index'))

    return render_template('register.html')


# 首页
@app.route('/index')
def index():
    if 'logged_in' in session and session['logged_in']:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM posts")
        posts = cur.fetchall()
        cur.close()
        return render_template('index.html', posts=posts, username=session['username'])
    else:
        return redirect(url_for('login'))


# 发表帖子页面
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = session['username']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)", (title, content, author))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('create_post.html')


# 用户登出
@app.route('/logout')
def logout():
    session.clear()  # 清除用户会话信息
    return redirect(url_for('login'))


# 帖子列表页面
@app.route('/post_list')
def post_list():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts")
    posts = cur.fetchall()
    cur.close()

    return render_template('post_list.html', posts=posts)


# 帖子详情页面
@app.route('/post_detail/<int:post_id>')
def post_detail(post_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cur.fetchone()
    cur.close()

    return render_template('post_detail.html', post=post)


# 登录验证
def is_admin():
    return 'logged_in' in session and session['logged_in'] and session.get('username') == 'admin'


# 管理员后台页面
@app.route('/admin')
def admin():
    if 'logged_in' in session and session['logged_in'] and session['username'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM posts")
        posts = cur.fetchall()
        cur.close()
        return render_template('admin.html', posts=posts)
    else:
        return redirect(url_for('login'))


# 添加帖子页面
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if 'logged_in' in session and session['logged_in'] and session['username'] == 'admin':
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            author = session['username']

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO posts (title, content, author) VALUES (%s, %s, %s)", (title, content, author))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('admin'))
        else:
            return render_template('add_post.html')
    else:
        return redirect(url_for('login'))


# 编辑帖子页面
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def admin_edit_post(post_id):
    if 'logged_in' in session and session['logged_in'] and session['username'] == 'admin':
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']

            cur = mysql.connection.cursor()
            cur.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s", (title, content, post_id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('admin'))
        else:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
            post = cur.fetchone()
            cur.close()
            return render_template('edit_post.html', post=post)
    else:
        return redirect(url_for('login'))


# 删除帖子
@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    if 'logged_in' in session and session['logged_in'] and session['username'] == 'admin':
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM posts WHERE id = %s", (post_id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
