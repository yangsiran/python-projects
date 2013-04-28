import re


class Rule:
    """
    Base class for all rules.
    """

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)


class GroupRule:
    """
    Bass class for rules made up of more than one block.
    """

    inside = False

    def in_action(self, handler):
        handler.start(self.type)
        self.inside = True

    def out_action(self, handler):
        handler.end(self.type)
        self.inside = False


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
    """
    A table row is a block which lines all have same aligning left
    word border.
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


class TableRule(TableRowRule, GroupRule):
    """
    A table begin between a block that is not a list item and a
    subsequent list item. It ends after the last consecutive list item.
    """

    type = 'table'

    def in_condition(self, block):
        return not self.inside and TableRowRule.condition(self, block)

    def out_condition(self, block):
        return self.inside and not TableRowRule.condition(self, block)


class ListItemRule(Rule):
    """
    A list item is a paragraph that begins with a hyphen. As part of
    the formatting, the hyphen is removed.
    """

    type = 'listitem'

    def condition(self, block):
        return block.startswith('-')

    def action(self, block, handler):
        Rule.action(self, block[1:], handler)


class ListRule(ListItemRule, GroupRule):
    """
    A list begin between a block that is not a list item and a
    subsequent list item. It ends after the last consecutive list item.
    """

    type = 'list'

    def in_condition(self, block):
        return not self.inside and ListItemRule.condition(self, block)

    def out_condition(self, block):
        return self.inside and not ListItemRule.condition(self, block)


class ParagraphRule(Rule):
    """
    A paragraph is simple a block that isn't covered by and of the
    other rules.
    """

    type = 'paragraph'

    def condition(self, block):
        return True
