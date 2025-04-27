from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from extractlinks import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    #Splits a list of nodes into two lists based on a delimiter.
    #The first list contains nodes before the delimiter, and the second list contains nodes after the delimiter.
    
    if not isinstance(old_nodes, list):
        raise ValueError("old_nodes must be a list")
    
    if not isinstance(delimiter, str):
        raise ValueError("delimiter must be a string")
    
    if not isinstance(text_type, TextType):
        raise ValueError("text_type must be an instance of TextType")
    
    if old_nodes == []:
        raise ValueError("old_nodes must not be empty")
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        if node.text == "":
            continue
        
        text = node.text

        try:
            first_delim_pos = text.index(delimiter)
            second_delim_pos = text.index(delimiter, first_delim_pos + len(delimiter))

            before_text = text[:first_delim_pos]
            delimiter_text = text[first_delim_pos + len(delimiter):second_delim_pos]
            after_text = text[second_delim_pos + len(delimiter):]

            if before_text:
                new_nodes.append(TextNode(before_text, TextType.NORMAL))
            if delimiter_text:
                new_nodes.append(TextNode(delimiter_text, text_type))
            if after_text:
                new_nodes.append(TextNode(after_text, TextType.NORMAL))
        except ValueError:

            # No matching delimiter found, adding node as is
            new_nodes.append(node)

    return new_nodes

def split_nodes_image(old_nodes):
    #Splits a list of nodes into two lists based on image nodes.
    #The first list contains nodes before the image, and the second list contains nodes after the image.
    
    if not isinstance(old_nodes, list):
        raise ValueError("old_nodes must be a list")
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        text = node.text
        img = extract_markdown_images(text)
        if len(img) == 0 and node.text != "":
            new_nodes.append(node)
            continue
        while img:
            alt_text = img[0][0]
            link_text = img[0][1]
        
            sections = text.split(f"![{alt_text}]({link_text})", 1)

            text_before = sections[0]

            if len(sections) != 2:
                raise ValueError("Invalid markdown image format")

            if text_before != "":
                new_nodes.append(TextNode(text_before, TextType.NORMAL))
            
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, link_text))
            
            if len(sections) > 1:
                text = sections[1]
                img = extract_markdown_images(text)
            else:
                text = ""
                img = []
        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes



def split_nodes_link(old_nodes):

    #Splits a list of nodes into two lists based on link nodes.
    #The first list contains nodes before the image, and the second list contains nodes after the link
    
    if not isinstance(old_nodes, list):
        raise ValueError("old_nodes must be a list")
    
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        
        text = node.text
        link = extract_markdown_links(text)
        if len(link) == 0 and node.text != "":
            new_nodes.append(node)
            continue
        while link:
            alt_text = link[0][0]
            link_text = link[0][1]
        
            sections = text.split(f"[{alt_text}]({link_text})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown link format")

            text_before = sections[0]

            if text_before != "":
                new_nodes.append(TextNode(text_before, TextType.NORMAL))
            new_nodes.append(TextNode(alt_text, TextType.LINK, link_text))
            
            if len(sections) > 1:
                text = sections[1]
                link = extract_markdown_links(text)
            else:
                text = ""
                link = []
        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes

def text_to_textnodes(text):
    #Converts a string to a list of TextNode objects.
    #The function uses the split_nodes_delimiter, split_nodes_image, and split_nodes_link functions to split the text into nodes.
    
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    
    if text == "":
        return []
    
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


    

   