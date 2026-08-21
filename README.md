# Arshad's Journal

This is a static personal journal hosted on GitHub Pages.

## Add a post

Create a Markdown file inside a year folder:

```text
year/
  2026/
    my-new-post.md
```

Start the file with the post title as an H1. Hashtags anywhere in the file become searchable filters:

```markdown
# The title of my new post

#engineering #lessons

Write the post here...
```

Run the local generator when previewing or testing:

```bash
python3 build.py
```

The same workflow is available through the Makefile:

```bash
make build                         # Generate the catalogue and HTML pages
make check                         # Compile scripts, build, and check formatting
make serve                         # Build and serve locally at port 4173
make publish MESSAGE="Add my post" # Build, commit, and push to main
```

The generator creates `posts.json`, embeds the catalogue into `index.html` so the page also works when opened directly as a `file://` URL, and creates a standalone HTML page for every post. Push the changed files to `main`; the GitHub Pages workflow runs the generator again before deployment.

The Medium archive was imported from `https://arshad404.medium.com/feed`. To refresh it, download that feed to `/tmp/arshad-medium.xml`, run `python3 import_medium.py`, and then run `python3 build.py`.