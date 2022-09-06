"""Build static HTML site from directory of HTML templates and plain files."""

import click
import json
import jinja2
import pathlib
import os

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-o','--output',help="Output Directory.",type=click.Path())
@click.option('-v','--verbose', is_flag=True, help="Print more output.")
def main(input, output,verbose):
    if not output:
        output = input+'/html'
    else:
        output = output +'/html'

    q = pathlib.Path(output)
    if q.exists():
        print(output, "already exists")

    inptest = pathlib.Path(input)
    '''if not inptest.exists():
        print(input, "does not exist") '''
    
    inpdir = input+"/config.json"

    with open(inpdir, 'r') as t:
        dicty = json.loads(t.read())
    
    tempname = input+'/templates'
    purename = pathlib.PurePath(tempname)
    
    template_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(purename)),
    autoescape=jinja2.select_autoescape(['html', 'xml']),)

    fill = dicty[0]['context']['words']
    matthog = template_env.get_template('index.html')

    url = dicty[0]['url']
    url = url.lstrip("/")  # remove leading slash
    input = pathlib.Path(input)  # convert str to Path object
    output_dir = input/"html"  # default, can be changed with --output option
    doscoutput_path = output_dir/url

    
    #newp = os.path.join(parent,dest)
    os.mkdir(doscoutput_path)
    #fulldir = pathlib.Path(parent+"/html/index.html")
    with open(doscoutput_path/"index.html", 'w', encoding = "utf-8") as f:
        f.write(matthog.render(words = fill)) 


    #print(matthog.render(words = fill))

    #print("Usage: insta485generator [OPTIONS] INPUT_DIR \n Try insta485generator --help for help")

if __name__ == "__main__":
    main()