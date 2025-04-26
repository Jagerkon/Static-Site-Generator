from textnode import TextNode, TextType


def main():
    # Create an instance of TextNode
    node = TextNode("Hello, World!", TextType.NORMAL, "link.com")  
    print(node)

main()