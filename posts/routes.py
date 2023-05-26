from flask import Blueprint, request, render_template, abort, flash, redirect, url_for
from package.models import Post
from package import db
from posts.forms import create_post, postForm
from flask_login import login_required, current_user

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "post"])
@login_required
def new_post():
    form = create_post()
    legend = "New Post"
    if form.validate_on_submit():
        posts = Post(title=form.Title.data, content=form.Content.data, author=current_user)
        db.session.add(posts)
        db.session.commit()
        flash("Your Post  Has been created!", "success")
        return redirect(url_for("main.home"))
    return render_template("create-post.html", title="new post", form=form, legend=legend)


@posts.route("/post/<int:post_id>")
def postid(post_id):
    post = Post.query.get(post_id)
    return render_template("post.html", post=post, titile=Post.title)


@posts.route("/post/<int:post_id>/update", methods=["GET", "post"])
@login_required
def update(post_id):
    legend = "Update Post"
    form = postForm()
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(404)
    if form.validate_on_submit():
        post.title = form.Title.data
        post.content = form.Content.data
        db.session.commit()
        flash("Your Post Has Been Updated!", "success")
        return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.Title.data = post.title
        form.Content.data = post.content
    return render_template("create-post.html", form=form, title="Update Post", legend=legend)


@posts.route("/post/<int:post_id>/delete", methods=["GET","post"])
@login_required
def delete(post_id):
    post = Post.query.get(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post Has Been Deleted!", "success")
    return redirect(url_for("main.home"))
