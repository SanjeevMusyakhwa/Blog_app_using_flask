from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__, template_folder='templates')
# /// means relative path and //// means absolute pat for saving
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'

db= SQLAlchemy(app)    # link flask app to database  

# create database
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(25), default='N/A')
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post' + str(self.id)
# dummy data 
'''
all_posts = [
    {
        'title': 'Post 1',
        'author': 'mark',
        'content': 'content of post 1. This is Prashant.'
    },
    {
        'title': 'Post 2',
        'content': 'content of post 2. This is Anam.'
    },
    
    {
        'title': 'Post 3',
        'content': 'content of post 3. This is Preksha.'
    }
]
'''
# after this define a variable in route where this data is to be passed

@app.route('/', methods = ['GET','POST'])
def posts():
    if request.method == 'POST':
        # read from form and add them to db
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title = post_title, content= post_content, author = post_author)
        db.session.add(new_post) # add data in db for current session
        db.session.commit()     # save permanently in file

        return redirect('/')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html',posts = all_posts)

@app.route('/posts/new', methods = ['GET','POST'])        
def new_post():
    if request.method == 'POST':
        # read from form and add them to db
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title = post_title, content= post_content, author = post_author)
        db.session.add(new_post) # add data in db for current session
        db.session.commit()     # save permanently in file

        return redirect('/')
    else:
        return render_template('new_post.html')    
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()        
    return redirect('/')

@app.route('/posts/edit/<int:id>', methods = ['POST', 'GET'])
def edit(id):

    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit.html', post = post)    


@app.route('/posts/detail/<int:id>', methods=['GET'])
def post_detail(id):
    post = BlogPost.query.get_or_404(id)  # Fetch the post by ID or return a 404 if not found
    return render_template('post_detail.html', post=post)


if __name__ == "__main__":
    app.run(debug=1)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    