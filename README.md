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

* Write a handler for something other than markup, such as analyzes
the document
* Supporting for LATEX output.

## Project 2: Paint A Pertty Picture

This project made a graphic of sunspots data from the Internet by a
graphics-generating package called ReportLab.
Many other packages in this kind can be used to slove such problems.

## Project 3: XML For All Ocaasions

Using a single XML file to generate a complete web site.

In the second implementation, a mix-in class was used to handle some
administrative details such as gathering character data, managing Boolean state
variables, or dispatching the events to custiom event handles.
(Only dispatching events thing was focused on in this project.)

**There is a problem: support for non-ascii characters.**

## Project 4: In the News

The second implementation add some classes to build the abstraction and
flexibility. That is making a kind of *Source* class at font end, and a kind of
*Destination* class at the back end, with the *Agent* class sitting in the
middle.

**This project is waiting for more further extending.**

## Project 5: Virtual Tea Party

This project implement a chat application use the aysncore and asynchat module
in the standard library. That allow more than one user connect to the server
simultaneously. The second version even support the command line interpretion.
This project show us the basic concept of network programming.
