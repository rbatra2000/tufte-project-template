import argparse
import marko
import frontmatter
from _types import Title, Authors, Author, Link, Metadata, Venue, Award

import re

remapper = {
    r"<h2>(.*?)</h2>": r"<h2 class='section-header'>\1</h2>",
    r"<a href=\"(.*?)\">(.*?)</a>": r"<a class='pop' href='\1' target='_blank' rel='noopener noreferrer'>\2</a>"
}


def generate_premble(x):
    return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <title>{x}</title>
                <link rel="stylesheet" href="../style/tufte.css"/>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>

            <body>
                <article>
            """



SUFFIX = """
    </article>
  </body>
</html>
"""

def parse_frontmatter(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    fm = frontmatter.loads(content)
    title = Title(fm['title'])
    authors = Authors([Author(author['name'], author['affiliation']) for author in fm['authors']])
    award = Award(fm['award']) if fm['award'] else None
    venue = Venue(fm['venue'])
    preprint__link = Link("preprint", fm['preprint'])
    video__link = Link("video", fm['video'])
    publication__link = Link("publication", fm['publication'])
    code__link = Link("code", fm['code'])
    
    metadata = Metadata(title, authors, award, venue, preprint__link, video__link, publication__link, code__link)
    return metadata

def strip_frontmatter(content):
    if content.startswith('---'):
        second_delimiter_pos = content.find('---', 3)
        if second_delimiter_pos != -1:
            content = content[second_delimiter_pos + 3:].strip()
    return content

def sidenote_replacement(match):
    text = match.group(1)
    note = match.group(2)
    # Generate a unique ID for each margin note
    note_id = f"mn-{hash(text + note) & 0xFFFFFF:06x}"
    
    return f"""<span class="highlight">{text}</span>
            <label for="{note_id}" class="margin-toggle sidenote-number"></label>
            <input type="checkbox" id="{note_id}" class="margin-toggle"/>
            <span class="sidenote">
                {note}
            </span>"""

def create_sidenotes(content):
    # Find all marginnote tags and replace them with the appropriate HTML
    pattern = r'<sidenote>[\s\S]*?<text>(.*?)</text>[\s\S]*?<note>(.*?)</note>[\s\S]*?</sidenote>'
    
    return re.sub(pattern, sidenote_replacement, content)

def get_inner_markdown(text):
    return marko.convert(text.strip()).replace('<p>', '').replace('</p>', '')

def figure_replacement(match):
    src = match.group(1)
    alt = match.group(2)
    caption = get_inner_markdown(match.group(3))

    figure_id = f"mn-figure-{hash(src + alt) & 0xFFFFFF:06x}"
    
    if src.endswith('.mov') or src.endswith('.mp4'):
        return f"""<figure>
                    <video width="100%" controls autoplay loop muted playsinline>
                        <source src="{src}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    <label for="{figure_id}" class="margin-toggle">&#8853;</label>
                    <input type="checkbox" id="{figure_id}" class="margin-toggle"/>
                    <span class="marginnote">
                        {caption}
                    </span>
                </figure>"""
    elif src.endswith('.png') or src.endswith('.jpg') or src.endswith('.jpeg'):
        return f"""<figure>
                    <img src="{src}" alt="{alt}" />
                    <label for="{figure_id}" class="margin-toggle">&#8853;</label>
                    <input type="checkbox" id="{figure_id}" class="margin-toggle"/>
                    <span class="marginnote">
                        {caption}
                    </span>
                </figure>"""

def create_figures(content):
    # Remove debug print statement
    pattern = r'<figure>[\s\S]*?<src>([\s\S]*?)</src>[\s\S]*?<alt>([\s\S]*?)</alt>[\s\S]*?<caption>([\s\S]*?)</caption>[\s\S]*?</figure>'
    return re.sub(pattern, figure_replacement, content)

def parse_markdown(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    content_sans_frontmatter = strip_frontmatter(content)
    content_sans_frontmatter = marko.convert(content_sans_frontmatter)

    for k, v in remapper.items():
        content_sans_frontmatter = re.sub(k, v, content_sans_frontmatter)

    content_sans_frontmatter = create_figures(content_sans_frontmatter)
    content_sans_frontmatter = create_sidenotes(content_sans_frontmatter)
    
    return f"<section>{content_sans_frontmatter}</section>"


def main():
    """
    Main function to parse command line arguments and process markdown files.
    """ 
    parser = argparse.ArgumentParser(description='Process markdown files for website generation.')
    parser.add_argument('markdown_file', type=str, help='Path to the markdown file to process')
    parser.add_argument('--name', '-n', type=str, help='Name of the output file', default=None)
    
    args = parser.parse_args()

    metadata = parse_frontmatter(args.markdown_file)
    content = parse_markdown(args.markdown_file)

    html = generate_premble(metadata.title) + metadata.__html__() + content + SUFFIX

    if args.name is None:
        args.name = args.markdown_file.split('/')[-1].split('.')[0]

    with open(f"{args.name}.html", "w+") as outfile:
        outfile.write(html)

    return None

if __name__ == "__main__":
    main()
