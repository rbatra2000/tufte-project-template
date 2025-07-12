import re

def format_html(html):
    """
    Format HTML with proper indentation using regex.
    
    Args:
        html (str): The HTML content to format.
        
    Returns:
        str: Formatted HTML with proper indentation.
    """
    # Define patterns for elements that should be on their own line
    block_elements = r'<\/?(?:html|head|body|div|section|article|header|footer|nav|main|aside|p|h[1-6]|ul|ol|li|form|fieldset|figure|figcaption|video|source|pre|code|blockquote|iframe)(?:\s[^>]*)?>'
    
    # Add line breaks before and after block elements
    html = re.sub(f'({block_elements})', r'\n\1\n', html)
    
    # Remove excessive blank lines
    html = re.sub(r'\n\s*\n+', '\n\n', html)
    
    # Initialize variables for indentation
    formatted_lines = []
    indent_level = 0
    indent_size = 4  # Number of spaces per indent level
    in_code_block = False
    
    # Process each line
    for line in html.split('\n'):
        line = line.strip()
        if not line:
            continue
        
        # Check if we're entering or exiting a code block
        if '<code>' in line:
            in_code_block = True
        if '</code>' in line:
            in_code_block = False
            
        # Check if line contains a closing tag
        if re.match(r'<\/', line) and not in_code_block:
            indent_level = max(0, indent_level - 1)
            
        # Add indentation (skip indentation if in code block)
        if in_code_block:
            formatted_lines.append(line)
        else:
            formatted_lines.append(' ' * (indent_level * indent_size) + line)
        
        # Check if line contains an opening tag (not self-closing)
        if not in_code_block and re.search(r'<[^\/][^>]*[^\/]>$', line) and not re.search(r'<(?:img|br|hr|input|link|meta|code)[^>]*>$', line):
            indent_level += 1
    
    return '\n'.join(formatted_lines)
