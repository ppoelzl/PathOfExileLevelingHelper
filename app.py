# Built-ins
import logging

# Project
from config import Config
from forms import ImportForm
from parse_stuff import parse
from table import generate_table

# Third-party
import pobapi
from flask import Flask, url_for, redirect, render_template, session

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(Config)


@app.route("/index", methods=["GET", "POST"])
def index():
    form = ImportForm()
    if form.validate_on_submit():
        # Remove excessive whitespace from user input
        session["text"] = form.import_code.data.strip()
        return redirect(url_for("vendor"))
    return render_template("index.html", title="help", form=form)


@app.route("/vendor")
def vendor():
    # TODO: Add error handling
    text = session["text"]
    if text.startswith("https://pastebin.com/"):
        build = pobapi.from_url(text)
    else:
        build = pobapi.from_import_code(text)

    store = parse(build)
    tables = generate_table(store)

    return render_template("vendor.html", tables=tables)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
