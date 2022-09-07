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
        os.makedirs(output)
    else:
        output = pathlib.Path(output)
        if output.exists():
            print(output, "already exists")
            sys.exit(2)
        else:
            #output = output/"html"
            os.makedirs(output)
    
    inpdir = pathlib.Path(input_dir + "/config.json")
    try:
        with open(inpdir, 'r') as t:
            try:
                dicty = json.loads(t.read())
            except ValueError as err:
                print("json error detected")
                sys.exit(2)
    except FileNotFoundError as err:
        print("file not found")
        sys.exit(2)
    
    purename = pathlib.PurePath(input_dir+"/templates")
    
    try:
        template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(purename)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),)
    except TemplateError:
        print("Jinja error detected")
        sys.exit(2)

    #for item in dicty:
        #print(item)
    
    fill = dicty[0]['context']['words']

    matthog = template_env.get_template('index.html')

    url = dicty[0]['url']
    url = url.lstrip("/")  # remove leading slash
    input_dir = pathlib.Path(input_dir)  # convert str to Path object
    #output_dir = input_dir/"html"  # default, can be changed with --output option
    #doscoutput_path = input_dir/"html"
    doscoutput_path = output/url

    #print(input_dir)

    if os.path.isdir(input_dir/"static"):
        os.mkdir(doscoutput_path/"css")
        shutil.copy(input_dir/"static/css/style.css", doscoutput_path/"css")
        print("Copied", input_dir/"static", "->", input_dir/"html")

    try:
        with open(doscoutput_path/"index.html", 'w', encoding = "utf-8") as t:
            t.write(matthog.render(words = fill)) 
            print("Rendered index.html ->", doscoutput_path/"index.html")
    except FileNotFoundError as err:
        print("file not found")
        sys.exit(2) 




if __name__ == "__main__":
    main()