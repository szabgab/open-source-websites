from flask import Flask, render_template, redirect, abort
import json
import re
app = Flask(__name__)


def load_sites():
    #global sites
    global tags
    global tag_list
    global entry_of_site

    with open('sites.json') as fh:
        raw = fh.read()
        sites = json.loads(raw)

    with open('tags.json') as fh:
        raw = fh.read()
        tag_details_src = json.loads(raw)
        tag_details = {}
        for tag in tag_details_src['bookmarks']:
            tag_details[tag['title']] = tag

#    print tag_details
    tags = {}
    entry_of_site = {}

    for entry in sites['bookmarks']:
        url = re.sub(r'https?://', '', entry["url"])
        site = re.sub(r'/.*', '', url)
        entry["site"] = site
        entry_of_site[site] = entry

        if 'tags' in entry:
            for tag in entry['tags']:
                if not tag in tags:
                    tags[tag] = { 'count' : 0, 'entries' : [] }
                tags[tag]['count'] += 1
                tags[tag]['entries'].append(entry)
                if tag in tag_details:
                    tags[tag]["url"] = tag_details[tag]["url"]
                    tags[tag]["comment"] = tag_details[tag]["comment"]

    tag_list = sorted(tags, key=lambda k: tags[k])
    tag_list.reverse()

@app.route("/")
def main():
    return render_template('main.html',
        title="Open Source Web Sites",
#        sites=sites,
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

@app.route("/site/<name>")
def site(name):
    if not name in entry_of_site:
        return render_template('404.html'), 404

    return render_template('site.html', entry=entry_of_site[name])


@app.route("/about")
def about():
    return render_template('about.html',
        title = "About Open Soure Web Sites"
    )

if __name__ == "__main__":
    load_sites()
    app.run(debug=True)
