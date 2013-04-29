## Project 1: Instant Markup

Markup the text from strand input into html format.
It Support blocks title, heading, paragraph, list and table.
And inline elements like emphasis, strong(all uppercase word), url,
email can be used too.

The second version of this project is a good example for mordularity and
OO design. There are four kinds of components in it:

* *A parser*: An object that reads the text and control the process of convert.
* *Rules*: Each rule is mapped with one kind of block, and used to detect the
applicable block type and to format it appropriatebly.
* *Filters*: Filters are used to wrap up regular expression to deal with
in-line elements.
* *Handlers*: Handlers used by parser is responsible for generate output. Each
handler is for a individual kind of markup.

### Further Exploration

* Supporting for LATEX output.
