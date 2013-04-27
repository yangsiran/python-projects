import re

class Rule:
    """
    Base class for all rules.
    """
    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

class HeadingRule(Rule):
    """
    A heading is a single line that is at most 70 characters and
    that doesn't end with a colon.
    """
    type = 'heading'
    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'

class TitleRule(HeadingRule):
    """
    The title is the first block in the document, provided that it is
    a heading.
    """
    type = 'title'
    first = True
    def condition(self, block):
        if not self.first: return False
        self.first = False
        return HeadingRule.condition(self, block)

class TableRowRule(Rule):
    r"""
    A table row is a block which lines all have same aligning left
    word border.
    >>> rule = TableRowRule()
    >>> rule.condition('aaa\n   bbb')
    True
    >>> rule.condition('aaa\n   bbb\n   ccc')
    True
    >>> rule.condition('aaa\n  bbb\n   ccc')
    False
    """
    type = 'tablerow'
    def condition(self, block):
        aligns = re.findall(r'\n( +)', block)
        if aligns:
            align = len(aligns[0])
            if not filter(lambda x: len(x) != align, aligns):
                return True
        return False
    def action(self, block, handler):
        handler.start(self.type)
        column_type = 'tablehead'
        for line in block.split('\n'):
            handler.start(column_type)
            handler.feed(line.strip())
            handler.end(column_type)
            column_type = 'tabledata'
        handler.end(self.type)
        return True

INTABLE = False

class TableInRule(TableRowRule):
    """
    A table begin between a block that is not a list item and a
    subsequent list item.
    """
    type = 'table'
    def condition(self, block):
        return not INTABLE and TableRowRule.condition(self, block)
    def action(self, block, handler):
        handler.start(self.type)
        globals()['INTABLE'] = True
        return False

class TableOutRule(TableRowRule):
    """
    A table ends after the last consecutive list item.
    """
    type = 'table'
    def condition(self, block):
        return INTABLE and not TableRowRule.condition(self, block)

    def action(self, block, handler):
        handler.end(self.type)
        globals()['INTABLE'] = False
        return False

class ListItemRule(Rule):
    """
    A list item is a paragraph that begins with a hyphen. As part of
    the formatting, the hyphen is removed.
    """
    type = 'listitem'
    def condition(self, block):
        return block.startswith('-')
    def action(self, block, handler):
        return Rule.action(self, block[1:], handler)

INLIST = False

class ListInRule(ListItemRule):
    """
    A list begin between a block that is not a list item and a
    subsequent list item.
    """
    type = 'list'
    def condition(self, block):
        return not INLIST and ListItemRule.condition(self, block)
    def action(self, block, handler):
        handler.start(self.type)
        globals()['INLIST'] = True
        return False

class ListOutRule(ListItemRule):
    """
    A list ends after the last consecutive list item.
    """
    type = 'list'
    def condition(self, block):
        return INLIST and not ListItemRule.condition(self, block)
    def action(self, block, handler):
        handler.end(self.type)
        globals()['INLIST'] = False
        return False

class ParagraphRule(Rule):
    """
    A paragraph is simple a block that isn't covered by and of the
    other rules.
    """
    type = 'paragraph'
    def condition(self, block):
        return True

if __name__ == '__main__':
    import doctest, rules
    doctest.testmod(rules)
