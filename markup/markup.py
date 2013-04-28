import sys, re

from handlers import *
from util import *
from rules import *


class Parser:
    """
    A Parser reads a text file, applying rules and controlling a
    handler.
    """

    def __init__(self, handler):
        self.handler = handler
        self.rules = []
        self.group_rules = []
        self.filters = []

    def addRule(self, rule):
        self.rules.append(rule)

    def addGroupRule(self, rule):
        self.group_rules.append(rule)

    def addFilter(self, pattern, name):
        def filter(block, handler):
            return re.sub(pattern, handler.sub(name), block)
        self.filters.append(filter)

    def parse(self, file):
        self.handler.start('document')

        for block in blocks(file):

            for rule in self.group_rules:
                if rule.out_condition(block):
                    rule.out_action(self.handler)
            for rule in self.group_rules:
                if rule.in_condition(block):
                    rule.in_action(self.handler)

            for filter in self.filters:
                block = filter(block, self.handler)
            for rule in self.rules:
                if rule.condition(block):
                    rule.action(block, self.handler)
                    break

        for rule in self.group_rules:
            if rule.inside:
                rule.out_action(self.handler)

        self.handler.end('document')


class BasicTextParser(Parser):
    """
    A specific Parser that adds rules and filters in its
    constructor.
    """
    def __init__(self, handler):
        Parser.__init__(self, handler)

        self.addGroupRule(TableRule())
        self.addGroupRule(ListRule())

        self.addRule(TableRowRule())
        self.addRule(ListItemRule())
        self.addRule(TitleRule())
        self.addRule(HeadingRule())
        self.addRule(ParagraphRule())

        self.addFilter(r'\*(.+?)\*', 'emphasis')
        self.addFilter(r'[^a-zA-Z0-9]([A-Z]+)[^a-zA-Z0-9]', 'strong')
        self.addFilter(r'(http://[\.a-zA-Z/]+)', 'url')
        self.addFilter(r'([\.a-zA-Z]+@[\.a-zA-Z]+[a-zA-Z]+)', 'mail')


if __name__ == '__main__':
    handler = HTMLRenderer()
    parser = BasicTextParser(handler)

    parser.parse(sys.stdin)
