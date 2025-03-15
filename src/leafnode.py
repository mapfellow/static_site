from htmlnode import *

class LeafNode(HTMLNode):

        def __init__(self, tag, value, props = None):
                super().__init__(tag, value, props = None)
                self.tag = tag
                self.value = value
                self.props = props

        def to_html(self):
                if self.value is None:
                        raise ValueError
                if self.tag is None:
                        return self.value
                if self.props is not None:
                        props = ""
                        for item in self.props:
                                props += f"{item}=\"{self.props[item]}\" "
                                #print(f"p {props}")
                        return f"<{self.tag} {props}>{self.value}</{self.tag}>"
                return f"<{self.tag}>{self.value}</{self.tag}>"
