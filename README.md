# remedy

Remedy is yet another translator from markdown to
[reveal.js](http://lab.hakim.se/reveal-js/#/). It is very similar to other
solutions to the same problem, but it allows for a bit more control over the
resulting html document. Specifically, you can pipe in additional header code
and thus include custom css and javascript. Furthermore, you can have
individual slides be marked by certain keywords.

Note that remedy requires python3.


## Installation

Should just be a simple

    pip install remedy

Alternatively, you can run the `setup.py`.


## Simple example


Imagine the following markdown script

    # My first remedy

    ---

    ## Remedy is no solution for everything

    - You might want to use reveal directly
    - there are other markdown to reveal.js converters

    ---html,subslide

    <div class='special-class'>
        Something is happening in here that's to complicated to express in markdown.
        Maybe something that requires elaborate styling or javascript?
    </div>

    ---subslide

    ## Another markdown slide

    We all know how to write markdown, right?

    ---

    ## Final slide

    Good bye!

stored in `slides.md`. You can then use

    python -m remedy slides.md

To create an html file called `presentation.html` that contains a slide show
for your presentation.

Maybe, we also have an additional bit of header code in a separate file
`header_mod.html` that styles your `"special-class"`:

    <style>
    .special-class {
        font-size: 24pt !important;
    }
    </style>

This can be included by simply calling

    python -m remedy --header=header_mod.html slides.md

Try `python -m remedy -h` for more options.

## Contributing

I believe that `remedy` is a pretty nice tool if you do so too, but you miss
that one really neat feature. Code it yourself and send me a pull request. If
you find a bug, ideally fix it yourself and send me a pull request.

Note that there are tests. They should pass after you apply your changes. Also,
I'm trying to stick to pep8 with respect to code formatting. You should do so
as well.
