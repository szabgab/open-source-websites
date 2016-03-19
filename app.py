from flask import Flask, render_template, redirect, abort
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
                tags[tag] = { 'count' : 0, 'entries' : [] }
            tags[tag]['count'] += 1
            tags[tag]['entries'].append(entry)

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

@app.route("/technology")
def redirect_to():
    return redirect('/')

@app.route("/technology/<name>")
def technology(name):
    if name in tags:
        return render_template('technology.html',
            title="Open Source Web sites using " + name,
            technology=name,
            details=tags[name]
        )
    else:
        return render_template('404.html'), 404

@app.route("/about")
def about():
    return render_template('about.html',
        title = "About Open Soure Web Sites"
    )

if __name__ == "__main__":
    app.run(debug=True)
