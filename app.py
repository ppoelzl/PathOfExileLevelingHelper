# Built-ins
import json
import logging

# Project
from config import Config
from forms import ImportForm
from parse_stuff import parse
from table import generate_table

# Third-party
import pobapi
from flask import Flask, render_template

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(Config)

with open("quest_data.json", "r") as f:
    quest_data = json.load(f)
with open("skill_data.json", "r") as f:
    skill_data = json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    form = ImportForm()
    if form.validate_on_submit():
        # Remove excessive whitespace from user input
        import_code = form.import_code.data.strip()
        return vendor(import_code)
    return render_template("index.html", form=form)


@app.route("/about")
def about():
    return render_template("about.html")


def vendor(import_code):
    # TODO: Proper error handling
    try:
        if import_code.startswith("https://pastebin.com/"):
            build = pobapi.from_url(import_code)
        else:
            build = pobapi.from_import_code(import_code)
    except ValueError:
        form = ImportForm()
        form["import_code"].errors = ["Not a valid pastebin.com URL or import code."]
        return render_template("index.html", form=form)

    store = parse(build)
    tables = generate_table(store)

    return render_template("vendor.html", tables=tables)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
