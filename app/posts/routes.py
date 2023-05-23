from flask import Flask, render_template, request, flash, redirect, url_for
import markdown
from flask_login import login_required, current_user
from app.posts import bp
from app.models.post import Post
from app.extensions import db
from werkzeug.exceptions import abort

@bp.route('/')
@login_required
def index():
    posts = Post.query.all()
    return render_template('posts/index.html', posts = posts, author_id=current_user.id)

@bp.route('/categories')
@login_required
def categories():
    return render_template('posts/categories.html')

def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return post

@bp.route('/<int:post_id>')
@login_required
def post(post_id):
    post = get_post(post_id)
    return render_template('posts/post.html', post = post)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author_id = current_user.id

        if not title:
            flash('Title is required!')
        else:
            current_post = Post(author_id=author_id, title=title, content=content)
            db.session.add(current_post)
            db.session.commit()
            return redirect(url_for('posts.index'))
        
    return render_template('posts/create.html')

@bp.route('/<int:id>/edit', methods=('GET', 'POST'))
@login_required
def edit(id):
    post = get_post(id)

    if post.author_id != current_user.id:
        flash('You are not the author of this post')
        return redirect(url_for('posts.index'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required')
        else:
            post.title = title
            post.content = content
            db.session.add(post)
            db.session.commit()
            flash('Sucessfully edited the post')
            return redirect(url_for('posts.index'))
    
    return render_template('posts/edit.html', post = post)

@bp.route('<int:id>/delete>', methods=('POST',))
def delete(id):
    post = get_post(id)

    if post.author_id != current_user.id:
        flash('You are not the author of this post')
        return redirect(url_for('posts.index'))
    
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('posts.index'))
