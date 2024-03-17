import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    __EXCPMSG_NO_CHILDREN = "A parent node must have at least one child node."
    __EXCPMSG_NO_TAG      = "A tag must be specified for the parent node." 

    def __assertExceptionMessage(self, exception, msg, method_to_test):
        with self.assertRaises(exception) as cm:
            method_to_test()
        self.assertEqual(
            msg,
            str(cm.exception)
        )


    def test_toHTML_onlyLeafNodesAsChildren(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(expected, node.to_html())


    def test_toHTML_whenTagIsNone(self):
        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.__assertExceptionMessage(
            ValueError, 
            TestParentNode.__EXCPMSG_NO_TAG,
            node.to_html
        )


    def test_toHTML_whenChildrenIsNone(self):
        node = ParentNode(
            "p",
            None
        )

        self.__assertExceptionMessage(
            ValueError,
            TestParentNode.__EXCPMSG_NO_CHILDREN,
            node.to_html
        )


    def test_toHTML_withAttributes(self):
        style_attr = 'style="color: #999999; margin-bottom: 20px"'
        id_attr = 'id="p1"'
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {
                "style": "color: #999999; margin-bottom: 20px",
                "id": "p1",
            }
        )

        expected = f'<p {style_attr} {id_attr}><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(expected, node.to_html())


    def test_toHTML_nestedParentNodes(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "head",
                    [
                        LeafNode("title", "Why HTML Development Sucks"),
                    ]
                ),
                ParentNode(
                    "body",
                    [
                        LeafNode("h1", "Front-end Development is the Worst"),
                        #LeafNode("p", ""),
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the "),
                                LeafNode("a", "backend", { "href": "https://www.boot.dev" }),
                                LeafNode(None, ", where the real programming happens.")
                            ],
                        ),
                    ],
                )
            ],
            { "lang": "en-US" }
        )

        expected = '<html lang="en-US"><head><title>Why HTML Development Sucks</title></head><body><h1>Front-end Development is the Worst</h1><p>Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the <a href="https://www.boot.dev">backend</a>, where the real programming happens.</p></body></html>'

        self.assertEqual(expected, node.to_html())


    def test_toHTML_withNestedParentNodes_and_oneParentNodeTagNone(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "head",
                    [
                        LeafNode("title", "Why HTML Development Sucks"),
                    ]
                ),
                ParentNode(
                    "body",
                    [
                        LeafNode("h1", "Front-end Development is the Worst"),
                        #LeafNode("p", ""),
                        ParentNode(
                            None,
                            [
                                LeafNode(None, "Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the "),
                                LeafNode("a", "backend", { "href": "https://www.boot.dev" }),
                                LeafNode(None, ", where the real programming happens.")
                            ],
                        ),
                    ],
                )
            ],
            { "lang": "en-US" }
        )

        self.__assertExceptionMessage(ValueError, TestParentNode.__EXCPMSG_NO_TAG, node.to_html)


    def test_toHTML_withNestedParentNodes_and_oneParentNodeChildrenIsEmpty(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "head",
                    []
                ),
                ParentNode(
                    "body",
                    [
                        LeafNode("h1", "Front-end Development is the Worst"),
                        #LeafNode("p", ""),
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the "),
                                LeafNode("a", "backend", { "href": "https://www.boot.dev" }),
                                LeafNode(None, ", where the real programming happens.")
                            ],
                        ),
                    ],
                )
            ],
            { "lang": "en-US" }
        )

        self.__assertExceptionMessage(ValueError, TestParentNode.__EXCPMSG_NO_CHILDREN, node.to_html)


    def test_toHTML_withNestedParentNodes_and_oneLeafNodeValueNone(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "head",
                    [
                        LeafNode("title"),  # value is None
                    ]
                ),
                ParentNode(
                    "body",
                    [
                        LeafNode("h1", "Front-end Development is the Worst"),
                        #LeafNode("p", ""),
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the "),
                                LeafNode("a", "backend", { "href": "https://www.boot.dev" }),
                                LeafNode(None, ", where the real programming happens.")
                            ],
                        ),
                    ],
                )
            ],
            { "lang": "en-US" }
        )

        self.__assertExceptionMessage(ValueError, "A value is required for HTML leaf node", node.to_html)


    def test_toHTML_withNestedParentNodes_and_oneLeafNodeValueEmptyString(self):
        node = ParentNode(
            "html",
            [
                ParentNode(
                    "head",
                    [
                        LeafNode("title", ""),
                    ]
                ),
                ParentNode(
                    "body",
                    [
                        LeafNode("h1", "Front-end Development is the Worst"),
                        #LeafNode("p", ""),
                        ParentNode(
                            "p",
                            [
                                LeafNode(None, "Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the "),
                                LeafNode("a", "backend", { "href": "https://www.boot.dev" }),
                                LeafNode(None, ", where the real programming happens.")
                            ],
                        ),
                    ],
                )
            ],
            { "lang": "en-US" }
        )

        expected = '<html lang="en-US"><head><title></title></head><body><h1>Front-end Development is the Worst</h1><p>Real programmers code, not silly markup languages. They code on Arch Linux, not Mac OS, and certainly not Windows. They use Vim, not VS Code. They use C, not HTML. Come to the <a href="https://www.boot.dev">backend</a>, where the real programming happens.</p></body></html>'

        self.assertEqual(expected, node.to_html())


