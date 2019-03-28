# Built-ins
import logging

# Project
from parse_stuff import parse
from table import Item, ItemTable

# Third-party
import pobapi
from flask import Flask, request, render_template

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def my_form_post():
    text = request.form["text"]
    text.strip() #remove leading and trailing whitespaces 
    # TODO: Add error handling
    if text.startswith("https://pastebin.com/"):
        build = pobapi.from_url(text)
    else:
        build = pobapi.from_import_code(text)

    store = parse(build)

    character_class = list(store[0].keys())[0]
    character_items = [
        Item(item[0], item[1], item[2], item[3]) for item in list(store[0].values())[0]
    ]
    character_table = ItemTable(character_items, border=True)
    one_class = list(store[1].keys())[0]
    one_items = [
        Item(item[0], item[1], item[2], item[3]) for item in list(store[1].values())[0]
    ]
    one_table = ItemTable(one_items, border=True)
    two_class = list(store[2].keys())[0]
    two_items = [
        Item(item[0], item[1], item[2], item[3]) for item in list(store[2].values())[0]
    ]
    two_table = ItemTable(two_items, border=True)
    three_class = list(store[3].keys())[0]
    three_items = [
        Item(item[0], item[1], item[2], item[3]) for item in list(store[3].values())[0]
    ]
    three_table = ItemTable(three_items, border=True)
    four_class = list(store[4].keys())[0]
    four_items = [
        Item(item[0], item[1], item[2], item[3]) for item in list(store[4].values())[0]
    ]
    four_table = ItemTable(four_items, border=True)
    five_class = list(store[5].keys())[0]
    five_items = [
        Item(item[0], item[1], item[2], item[3]) for item in list(store[5].values())[0]
    ]
    five_table = ItemTable(five_items, border=True)
    six_class = list(store[6].keys())[0]
    six_items = [
        Item(item[0], item[1], item[2], item[3]) for item in list(store[6].values())[0]
    ]
    six_table = ItemTable(six_items, border=True)

    return render_template(
        "vendor.html",
        character_class=character_class,
        character_table=character_table,
        one_class=one_class,
        one_table=one_table,
        two_class=two_class,
        two_table=two_table,
        three_class=three_class,
        three_table=three_table,
        four_class=four_class,
        four_table=four_table,
        five_class=five_class,
        five_table=five_table,
        six_class=six_class,
        six_table=six_table,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
