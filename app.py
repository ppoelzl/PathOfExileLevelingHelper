# Built-ins
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


@app.route("/", methods=["GET", "POST"])
def index():
    form = ImportForm()
    if form.validate_on_submit():
        return vendor(form)
    return render_template("index.html", form=form)


def vendor(form):
    # Remove excessive whitespace from user input
    text = form.import_code.data.strip()
    # TODO: Add error handling
    if text.startswith("https://pastebin.com/"):
        build = pobapi.from_url(text)
    else:
        build = pobapi.from_import_code(text)

    store = parse(build)
    tables = generate_table(store)

    return render_template("vendor.html", tables=tables)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
