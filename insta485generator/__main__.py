"""Build static HTML site from directory of HTML templates and plain files."""

import click;
import json;
import jinja2;

@click.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('-o','--output',help="Output Directory.",type=click.Path())
@click.option('-v','--verbose', is_flag=True, help="Print more output.")
def main(input, output,verbose):
    print(verbose)
    
    if not output:
        output = input+'/html'
    else:
        output = output +'/html'
    print(output)


    """if verbose: 
        print("verbose activated")
    if output: 
        print("output activated")
    if(not verbose and not output):
        print("error detected, no args")

    template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(['html', 'xml']),
    )   
    template = template_env.get_template()
    """
    
    """Top level command line interface."""
    print("Usage: insta485generator [OPTIONS] INPUT_DIR \n Try insta485generator --help for help")

if __name__ == "__main__":
    main()