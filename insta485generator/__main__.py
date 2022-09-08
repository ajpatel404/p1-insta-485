"""Build static HTML site from directory of HTML templates and plain files."""


import json
import pathlib
import os
import sys
import shutil
import jinja2
import click


@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('-o', '--output', help="Output directory.", type=click.Path())
@click.option('-v', '--verbose', is_flag=True, help="Print more output.")
def main(input_dir, output, verbose):
    """Templated static website generator."""
    if not output:
        output = input_dir+'/html'
        output = pathlib.Path(output)
    else:
        output = pathlib.Path(output)
        if output.exists():
            print(output, "already exists")
            sys.exit(2)
    input_dir = pathlib.Path(input_dir)
    try:
        with open(input_dir/"config.json", 'r', encoding="utf-8") as terr:
            try:
                dicty = json.loads(terr.read())
            except ValueError:
                print("json error detected")
                sys.exit(2)
    except FileNotFoundError:
        print("file not found")
        sys.exit(2)
    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(input_dir/"templates")),
        autoescape=jinja2.select_autoescape(['html', 'xml']),)
    if os.path.isdir(input_dir/"static"):
        shutil.copytree(input_dir/"static", output)
        if verbose:
            print("Copied", input_dir/"static", "->", output)
    else:
        os.makedirs(output)
    for item in dicty:
        url = item['url']
        url = url.lstrip("/")
        cont = item['context']
        if not os.path.isdir(output/url):
            os.makedirs(output/url)
        matthog = template_env.get_template(item['template'])
        with open(output/url/"index.html", 'w', encoding="utf-8") as terr:
            terr.write(matthog.render(cont))
        if verbose:
            print("Rendered", item['template'], "->", output/url/"index.html")


if __name__ == "__main__":
    main()
