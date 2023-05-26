from flask import Blueprint, request, render_template
from package.models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("home.html", posts=posts, title="home")


@main.route("/about", methods=["Post", "Get"])
def about():
    return render_template("about.html")
