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
        stripped = line.strip()
        if not stripped:
            continue

        # Check if we're entering or exiting a code block
        if '<code>' in stripped:
            in_code_block = True
        if '</code>' in stripped:
            in_code_block = False

        # Check if line contains a closing tag
        if re.match(r'<\/', stripped) and not in_code_block:
            indent_level = max(0, indent_level - 1)

        # Add indentation; preserve original indentation inside code blocks
        if in_code_block and '<code>' not in stripped:
            formatted_lines.append(line)
        else:
            formatted_lines.append(' ' * (indent_level * indent_size) + stripped)

        # Check if line contains an opening tag (not self-closing)
        if not in_code_block and re.search(r'<[^\/][^>]*[^\/]>$', stripped) and not re.search(r'<(?:img|br|hr|input|link|meta|code)[^>]*>$', stripped):
            indent_level += 1
    
    result = '\n'.join(formatted_lines)
    # Collapse whitespace between <pre> and <code> so pre-wrap doesn't render blank lines
    result = re.sub(r'(<pre[^>]*>)\s*(<code[^>]*>)', r'\1\2', result)
    result = re.sub(r'(</code>)\s*(</pre>)', r'\1\2', result)
    # Remove the newline immediately after <code> (when it's inside a <pre>)
    result = re.sub(r'(<pre[^>]*><code[^>]*>)\n', r'\1', result)
    # Remove whitespace immediately before </code></pre>
    result = re.sub(r'\n\s*(</code></pre>)', r'\1', result)
    return result
