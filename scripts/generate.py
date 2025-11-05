import argparse
import marko
from marko.ext.gfm import gfm
import frontmatter
from _types import Title, Authors, Author, Link, Metadata, Venue, Award, Date
from _utils import format_html

import re

remapper = {
    r"<a href=\"(.*?)\">(.*?)</a>": r"<a class='pop' href='\1' target='_blank' rel='noopener noreferrer'>\2</a>",
}


def generate_premble(x):
    return f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <title>{x}</title>
                <link rel="stylesheet" href="../style/tufte.css"/>
                <link rel="icon" href="../icons/favicon.ico" sizes="32x32" />
                <link rel="icon" href="../icons/icon.svg" type="image/svg+xml" />
                <link rel="apple-touch-icon" href="../icons/apple-touch-icon.png" />
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
    title = Title(fm.get("title", None))
    date = Date(fm.get("date", None))
    authors = Authors([Author(author.get("name", None), author.get("affiliation", None), author.get("link", None)) for author in fm.get("authors", [])])
    venue = Venue(fm.get("venue", None))
    award = Award(fm.get("award", None))
    links_dict = fm.get("links", {})
    
    links = []
    for k, v in links_dict.items():
        links.append(Link(k, v))

    metadata = Metadata(title, authors, date, venue, award, links)
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
            <span class="sidenote">{note}</span>"""

def table_replacement(match):
    doc = gfm.parse(match.group(0).replace('<table>', '').replace('</table>', ''))
    return f"""<div class="table-wrapper">{gfm.render(doc)}</div>"""

def create_tables(content):
    # Find all table tags and replace them with the appropriate HTML
    pattern = r'<table>[\s\S]*?</table>'
    return re.sub(pattern, table_replacement, content)

def create_sidenotes(content):
    # Find all marginnote tags and replace them with the appropriate HTML
    pattern = r'<sidenote>[\s\S]*?<text>(.*?)</text>[\s\S]*?<note>(.*?)</note>[\s\S]*?</sidenote>'

    return re.sub(pattern, sidenote_replacement, content)

def get_inner_markdown(text):
    return marko.convert(text.strip()).replace('<p>', '').replace('</p>', '')

def fullwidth_figure_replacement(match):
    src = match.group(1)
    alt = match.group(2)
    caption = get_inner_markdown(match.group(3))

    return f"""<figure class="fullwidth">
                <img src="{src}" alt="{alt}"/>
                <figcaption>{caption}</figcaption>
            </figure>"""

def iframe_replacement(match):
    src = match.group(1)
    alt = match.group(2)
    caption = get_inner_markdown(match.group(3))

    figure_id = f"mn-figure-{hash(src + alt) & 0xFFFFFF:06x}"

    if caption == "":
        return f"""<figure class="iframe-wrapper">
                    <iframe src="{src}" frameborder="0" allowfullscreen></iframe>
                </figure>"""
    else:
        return f"""<figure class="iframe-wrapper">
                <iframe src="{src}" frameborder="0" allowfullscreen></iframe>
                <label for="{figure_id}" class="margin-toggle">&#8853;</label>
                <input type="checkbox" id="{figure_id}" class="margin-toggle"/>
                <span class="marginnote">
                    {caption}
                </span>
            </figure>"""

def iframe_fullwidth_replacement(match):
    src = match.group(1)
    return f"""<figure class="iframe-wrapper fullwidth">
                    <iframe src="{src}" frameborder="0" allowfullscreen></iframe>
                </figure>"""


def regular_figure_replacement(match):
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

def header_id_replacement(match):
    header_text = match.group(2)
    return f'<h{match.group(1)} id="{"-".join(header_text.lower().split())}">{header_text}</h{match.group(1)}>'

def update_header_ids(content):
    # Find all header tags and update the ids
    pattern = r'<h([1-6])>(.*?)</h\1>'
    return re.sub(pattern, header_id_replacement, content)

def create_figures(content):
    # Remove debug print statement
    regular_figure_pattern = r'<figure>[\s\S]*?<src>([\s\S]*?)</src>[\s\S]*?<alt>([\s\S]*?)</alt>[\s\S]*?<caption>([\s\S]*?)</caption>[\s\S]*?</figure>'

    fullwidth_figure_pattern = r'<figure class="fullwidth">[\s\S]*?<src>([\s\S]*?)</src>[\s\S]*?<alt>([\s\S]*?)</alt>[\s\S]*?<caption>([\s\S]*?)</caption>[\s\S]*?</figure>'

    iframe_pattern = r'<figure iframe>[\s\S]*?<src>([\s\S]*?)</src>[\s\S]*?<alt>([\s\S]*?)</alt>[\s\S]*?<caption>([\s\S]*?)</caption>[\s\S]*?</figure>'

    iframe_fullwidth_pattern = r'<figure iframe class="fullwidth">[\s\S]*?<src>([\s\S]*?)</src>[\s\S]*?<alt>([\s\S]*?)</alt>[\s\S]*?<caption>([\s\S]*?)</caption>[\s\S]*?</figure>'

    regular_figures_added = re.sub(regular_figure_pattern, regular_figure_replacement, content)
    fullwidth_figures_added = re.sub(fullwidth_figure_pattern, fullwidth_figure_replacement, regular_figures_added)
    iframe_figures_added = re.sub(iframe_pattern, iframe_replacement, fullwidth_figures_added)
    iframe_fullwidth_figures_added = re.sub(iframe_fullwidth_pattern, iframe_fullwidth_replacement, iframe_figures_added)

    return iframe_fullwidth_figures_added

def parse_markdown(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    content_sans_frontmatter = strip_frontmatter(content)
    content_sans_frontmatter = marko.convert(content_sans_frontmatter)
    content_sans_frontmatter = update_header_ids(content_sans_frontmatter)

    for k, v in remapper.items():
        content_sans_frontmatter = re.sub(k, v, content_sans_frontmatter)

    content_sans_frontmatter = create_figures(content_sans_frontmatter)
    content_sans_frontmatter = create_sidenotes(content_sans_frontmatter)
    content_sans_frontmatter = create_tables(content_sans_frontmatter)

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

    _html = generate_premble(metadata.title) + metadata.__html__() + content + SUFFIX
    fmt_html = format_html(_html)

    if args.name is None:
        args.name = args.markdown_file.split('/')[-1].split('.')[0]

    with open(f"{args.name}.html", "w+") as outfile:
        outfile.write(fmt_html)

    return None

if __name__ == "__main__":
    main()
