"""Build static HTML site from directory of HTML templates and plain files."""

import click
import json
import jinja2
import pathlib
import os
import sys
import shutil

@click.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('-o','--output',help="Output directory.",type=click.Path())
@click.option('-v','--verbose', is_flag=True, help="Print more output.")
def main(input_dir, output,verbose):
    '''Templated static website generator.'''
    if not output: 
        output = input_dir+'/html'
        output = pathlib.Path(output)
        #os.makedirs(output)
    else:
        output = pathlib.Path(output)
        if output.exists():
            print(output, "already exists")
            sys.exit(2)
    
    input_dir = pathlib.Path(input_dir)
    
    try:
        with open(input_dir/"config.json", 'r') as t:
            try:
                dicty = json.loads(t.read())
            except ValueError as err:
                print("json error detected")
                sys.exit(2)
    except FileNotFoundError as err:
        print("file not found")
        sys.exit(2)
    
    try:
        template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(input_dir/"templates")),
        autoescape=jinja2.select_autoescape(['html', 'xml']),)
    except TemplateError:
        print("Jinja error detected")
        sys.exit(2)

    #print(input_dir, output)
    
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
        with open(output/url/"index.html", 'w', encoding = "utf-8") as t:
            t.write(matthog.render(cont)) 
        if verbose:
            print("Rendered", item['template'], "->", output/url/"index.html")

        
    '''
    fill = dicty[0]['context']['words']

    matthog = template_env.get_template('index.html')

    url = dicty[0]['url']
    url = url.lstrip("/")  # remove leading slash
      # convert str to Path object
    #output_dir = input_dir/"html"  # default, can be changed with --output option
    #doscoutput_path = input_dir/"html"
    doscoutput_path = output/url

    #print(input_dir)

    try:
        with open(doscoutput_path/"index.html", 'w', encoding = "utf-8") as t:
            t.write(matthog.render(words = fill)) 
            print("Rendered index.html ->", doscoutput_path/"index.html")
    except FileNotFoundError as err:
        print("file not found")
        sys.exit(2) '''




if __name__ == "__main__":
    main()