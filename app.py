from flask import Flask, render_template
import json
app = Flask(__name__)

with open('sites.json') as fh:
    raw = fh.read()

data = json.loads(raw)
tags = {}

for entry in data['bookmarks']:
    if 'tags' in entry:
        for tag in entry['tags']:
            if not tag in tags:
                tags[tag] = 0
            tags[tag] += 1

tag_list = sorted(tags, key=lambda k: tags[k])
tag_list.reverse()

@app.route("/")
def main():
    return render_template('main.html',
        title="Open Source Web Sites",
        data=data,
        tags=tags,
        tag_list=tag_list
    )

if __name__ == "__main__":
    app.run(debug=True)
