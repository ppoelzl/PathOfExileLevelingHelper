# Built-ins
import logging

# Project
from parse_stuff import parse
from table import generate_table

# Third-party
import pobapi
from flask import Flask, request, render_template

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def import_code_form_post():
    # Remove excessive whitespace from user input
    text = request.form["text"].strip()
    # TODO: Add error handling
    if text.startswith("https://pastebin.com/"):
        build = pobapi.from_url(text)
    else:
        build = pobapi.from_import_code(text)

    store = parse(build)
    tables = generate_table(store)

    return render_template("vendor.html", tables=tables)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
