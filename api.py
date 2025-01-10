from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import User, BlogPost, db

api = Blueprint('api', __name__)

# Get all posts (Public API)
@api.route('/posts/', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    posts_list = [{'id': post.id, 'title': post.title, 'content': post.content} for post in posts]
    return jsonify(posts_list)

# Get a single post by ID (Public API)
@api.route('/posts/<int:post_id>/', methods=['GET'])
def get_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    post_data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'author': post.author.username,
        'date_posted': post.date_posted
    }
    return jsonify(post_data)

# Create a new post (Authenticated API)
@api.route('/posts/', methods=['POST'])
@login_required
def create_post_api():
    data = request.get_json()
    post_title = data.get('title')
    post_content = data.get('content')

    # Ensure data is provided
    if not post_title or not post_content:
        return jsonify({'error': 'Missing required fields'}), 400

    # Create new post
    new_post = BlogPost(title=post_title, content=post_content, user_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        'message': 'Post created successfully!',
        'post': {'id': new_post.id, 'title': new_post.title, 'content': new_post.content}
    }), 201

# Edit a post (Authenticated API)
@api.route('/posts/<int:post_id>/', methods=['PUT'])
@login_required
def edit_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to edit this post'}), 403

    data = request.get_json()
    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    db.session.commit()

    return jsonify({
        'message': 'Post updated successfully!',
        'post': {'id': post.id, 'title': post.title, 'content': post.content}
    })

# Delete a post (Authenticated API)
@api.route('/posts/<int:post_id>/', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to delete this post'}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully!'})
