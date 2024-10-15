from folder import *
from pathlib import Path
from parser.parser import *

ROOT = Path(__file__).parents[1]

def main():
    public = ROOT / "public"
    content = ROOT / "content"
    template = ROOT / "template/template.html"
    static = ROOT / "static"

    clean(public)
    copy(static, public)

    generate_page(content/"index.md", template , public)

def generate_page(src, template, dest):
    print(f"Generating page from {src} to {dest}/{src.stem}.html using {template}")
    if not dest.exists():
        dest.mkdir(parents=True)
    with open(src) as f, open(template) as t, open(dest/f"{src.stem}.html", "w") as out:
        markdown = f.read()
        title = extract_title(markdown)
        html = markdown_to_html_node(markdown)
        doc = t.read()
        doc = doc.replace("{{ Title }}", title).replace("{{ Content }}", html.to_html())
        out.write(doc)


if __name__ == "__main__":
    main()