from flask import Blueprint, jsonify
from scraper.database import (
    get_posts,
    get_post_by_id
)

api=Blueprint("api",__name__)

@api.route("/api/posts",methods=["GET"])
def posts():
    posts = get_posts()
    return jsonify(posts)

@api.route("/api/posts/<int:post_id>", methods=["GET"])
def post_by_id(post_id):

    post = get_post_by_id(post_id)

    if post is None:
        return jsonify({
            "error": "Post not found"
        }), 404

    return jsonify(post)
