# -*- coding: utf-8 -*-

import unittest
from textwrap import dedent

from docutils import nodes
from docutils.utils import new_document
from docutils.readers import Reader
from docutils.core import publish_parts

from commonmark import Parser
from recommonmark.parser import CommonMarkParser


class TestParsing(unittest.TestCase):

    def assertParses(self, source, expected, alt=False):  # noqa
        parser = CommonMarkParser()
        parser.parse(dedent(source), new_document('<string>'))
        self.assertMultiLineEqual(
            dedent(expected).lstrip(),
            dedent(parser.document.asdom().toprettyxml(indent='  ')),
        )

    def test_heading(self):
        self.assertParses(
            """
            # I

            ## A

            > some-blockquote

            [google](https://www.google.com)

            ## [B](#b)

            ![ello](some-image.img)

            * one
            * two

            1. ONE
            2. TWO
            """,
            """
            <?xml version="1.0" ?>
            <document source="&lt;string&gt;">
              <section ids="i" names="i">
                <title>I</title>
                <section ids="a" names="a">
                  <title>A</title>
                  <block_quote>
                    <paragraph>some-blockquote</paragraph>
                  </block_quote>
                  <paragraph>
                    <reference refuri="https://www.google.com">google</reference>
                  </paragraph>
                </section>
                <section ids="b" names="b">
                  <title>
                    <reference refuri="#b">B</reference>
                  </title>
                  <paragraph>
                    <image uri="some-image.img">ello</image>
                  </paragraph>
                  <bullet_list>
                    <list_item>
                      <paragraph>one</paragraph>
                    </list_item>
                    <list_item>
                      <paragraph>two</paragraph>
                    </list_item>
                  </bullet_list>
                  <enumerated_list>
                    <list_item>
                      <paragraph>ONE</paragraph>
                    </list_item>
                    <list_item>
                      <paragraph>TWO</paragraph>
                    </list_item>
                  </enumerated_list>
                </section>
              </section>
            </document>
            """
        )

if __name__ == '__main__':
    unittest.main()