#!/usr/bin/env python

import logging
import os
import sys
import shutil
import glob
import jinja2
import itertools

import begin


class Slide(object):

    def __init__(self, content):
        self.parse_specs(content.splitlines()[0])
        self.content = '\n'.join(content.splitlines()[1:])

    def parse_specs(self, specsline):
        specs = [s.strip() for s in specsline.split(',')]
        self.ismarkdown = 'html' not in specs
        self.issubslide = 'subslide' in specs
        self.classname = self.get_classname(specs)

    def get_classname(self, specs):
        for s in specs:
            if s.startswith('class'):
                return s.split('=')[1].strip('"\'')
        return None


def load_slides(fname, slide_marker='---'):
    logging.info('Loading slides from file %s', fname)
    with open(fname) as f:
        filecontent = f.read()
    return [Slide(content)
            for content in (('\n' if filecontent[0] == '#' else '') +
                            filecontent).split(slide_marker)]


def load_template(fname='template.html'):
    env = jinja2.Environment(loader=jinja2.PackageLoader('remedy',
                                                         'templates'))
    logging.info('Loading template from file %s', fname)
    return env.get_template(fname)


def group_slides(slides):
    output = []
    slidegroup = [slides[0]]
    for slide in slides[1:]:
        if not slide.issubslide:
            output.append(slidegroup)
            slidegroup = []
        slidegroup.append(slide)
    output.append(slidegroup)
    return output


def load_custom_header_modifications(fname=None):
    if fname:
        logging.info('Applying header modifications from file %s', fname)
        with open(fname) as f:
            return f.read()


def list_themes():
    context = os.path.dirname(__file__)
    raw_names = glob.glob(os.path.join(context,
                                       'templates/context/css/theme/*.css'))
    for name in raw_names:
        print(os.path.splitext(os.path.basename(name))[0])
    sys.exit(0)


def copy_context(outfilename):
    output_path = os.path.dirname(outfilename)
    context_origin = os.path.join(os.path.dirname(__file__),
                                  'templates', 'context')
    context_target = os.path.join(output_path, 'context')
    if not os.path.exists(context_target):
        logging.info('Copy context from %s to %s',
                     context_origin, context_target)
        shutil.copytree(context_origin, context_target)
    else:
        logging.info('Found context in "%s"', context_target)


@begin.start
@begin.logging
def main(*slides: "Markdown file(s) containing the slides",
         title: "Overall title of the presentation" ='Yes, this is a browser',
         theme: "Layout theme of the presentation (see css/theme/)" ='white',
         template: "Template of the presentation" ='template.html',
         separator: "Separator to split different slides" ='---',
         header: "Custom header modifications" =None,
         listthemes: "List available themes" =False,
         output: "Name of output file" ='presentation.html'):
    if listthemes:
        list_themes()

    if not len(slides):
        sys.stderr.write('No slides file\n')
        sys.exit(1)

    slides = group_slides(list(itertools.chain(
        *[load_slides(sl, separator)
          for sl in slides])))
    template = load_template(template)
    custom_header_modifications = load_custom_header_modifications(header)
    with open(output, "w") as f:
        f.write(template.render(
            slides=slides, title=title, theme=theme,
            additional_header=custom_header_modifications,
        ))

    copy_context(output)
