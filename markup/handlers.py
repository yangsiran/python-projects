class Handler:
    """
    An object that handles method calls from the Parser.

    The Parser will call the start() and end() methods at the
    beginning of each block, with the proper block name as a
    parameter. The sub() method will be used in regular expression
    substitution. When called with a name such as 'emphasis', it will
    return a proper substitution function.
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix+name, None)
        if callable(method): return method(*args)
    def start(self, name):
        self.callback('start_', name)
    def end(self, name):
        self.callback('end_', name)
    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name,match)
            return result if result else match.group(0)
        return substitution


class HTMLRenderer(Handler):
    """
    A specific handler used for rendering HTML.

    The methods in HTMLRenderer are accessed from the superclass
    Handler's start(), end() and sub() methods. They implement basic
    markup as used in HTML documents.
    """

    def start_document(self):
        print '<html><head><title>...</title></head></body>'
    def end_document(self):
        print '</body></html>'

    def start_paragraph(self):
        print '<p>'
    def end_paragraph(self):
        print '</p>'

    def start_heading(self):
        print '<h2>'
    def end_heading(self):
        print '</h2>'

    def start_list(self):
        print '<ul>'
    def end_list(self):
        print '</ul>'

    def start_listitem(self):
        print '<li>'
    def end_listitem(self):
        print '</li>'

    def start_table(self):
        print '<table border="1">'
    def end_table(self):
        print '</table>'

    def start_tablerow(self):
        print '<tr>'
    def end_tablerow(self):
        print '</tr>'

    def start_tablehead(self):
        print '<th>'
    def end_tablehead(self):
        print '</th>'

    def start_tabledata(self):
        print '<td>'
    def end_tabledata(self):
        print '</td>'

    def start_title(self):
        print '<h1>'
    def end_title(self):
        print '</h1>'

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)
    def sub_uppercase(self, match):
        return match.group(0).replace(match.group(1),
                                      '<strong>%s</strong>' % match.group(1))
    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))
    def sub_mail(self, match):
        return '<a href="mailto:%s">%s</a>' % (match.group(1), match.group(1))
    def feed(self, data):
        print data
