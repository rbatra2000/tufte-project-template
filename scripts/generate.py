import argparse
import marko
from marko.ext.gfm import gfm
import frontmatter
from _types import Title, Authors, Author, Link, Metadata, Venue, Award, Date
from _utils import format_html

import re
import shutil
from pathlib import Path

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
            </head>

            <body>
                <article>
            """



SUFFIX = """
    </article>
    <script>
    function copyBibtex() {
        const bibtexCode = document.querySelector('#bibtex-content code').textContent.trim();
        navigator.clipboard.writeText(bibtexCode).then(function() {
            const btn = document.getElementById('copy-bibtex-btn');
            const originalSVG = btn.innerHTML;
            btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
            setTimeout(function() {
                btn.innerHTML = originalSVG;
            }, 2000);
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            alert('Failed to copy to clipboard');
        });
    }
</script>
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

def add_bibtex_copy_button(content):
    """Add copy button to BibTex sections and necessary JavaScript."""
    # Pattern to match BibTex h2 header followed by pre/code block
    # This matches: <h2 id="bibtex">BibTex</h2> followed by <pre><code>...</code></pre>
    # Handle case-insensitive matching for "bibtex" and flexible whitespace
    pattern = r'(<h2[^>]*id=["\']bibtex["\'][^>]*>)([\s\S]*?)(</h2>)\s*(<pre>)(<code>)([\s\S]*?)(</code>)(</pre>)'
    
    def bibtex_replacement(match):
        header_open = match.group(1)
        header_text = match.group(2).strip()
        header_close = match.group(3)
        pre_open = match.group(4)
        code_open = match.group(5)
        bibtex_content = match.group(6)
        code_close = match.group(7)
        pre_close = match.group(8)

        # Modify pre_open to include id (styling is in CSS)
        pre_with_id = pre_open.replace('<pre>', '<pre id="bibtex-content">')

        return f"""<div class="bibtex-container">
        {header_open}{header_text}{header_close}
        <button id="copy-bibtex-btn" onclick="copyBibtex()" title="Copy BibTeX">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
        </button>
        {pre_with_id}{code_open}{bibtex_content}{code_close}
        {pre_close}
    </div>"""
    
    return re.sub(pattern, bibtex_replacement, content, flags=re.IGNORECASE)

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
    content_sans_frontmatter = add_bibtex_copy_button(content_sans_frontmatter)

    return f"<section>{content_sans_frontmatter}</section>"

def extract_asset_paths(markdown_content, name):
    """Extract all asset paths referenced in the markdown file."""
    asset_paths = {}
    
    # Find all <src> tags in figure elements
    figure_pattern = r'<figure[^>]*>[\s\S]*?<src>([\s\S]*?)</src>[\s\S]*?</figure>'
    for match in re.finditer(figure_pattern, markdown_content):
        original_path = match.group(1).strip()
        if original_path and not original_path.startswith('http'):
            # Extract the asset name/path (remove ../assets/ or assets/ prefix)
            if 'assets/' in original_path:
                path_after_assets = original_path.split('assets/', 1)[-1]
                # If path starts with name/, remove that prefix since we'll look in assets/name/ first
                if path_after_assets.startswith(f"{name}/"):
                    asset_name = path_after_assets[len(name) + 1:]  # Remove "name/" prefix
                else:
                    asset_name = path_after_assets
            else:
                asset_name = Path(original_path).name
            # Store mapping from original path to asset name
            asset_paths[original_path] = asset_name
    
    return asset_paths

def copy_assets(asset_paths, output_dir, script_dir, name):
    """Copy all referenced assets from template assets folder to output directory."""
    template_base = script_dir.parent
    name_specific_assets = template_base / "assets" / name
    
    # Copy each referenced asset from template assets folder
    path_mapping = {}
    output_assets = output_dir / "assets"
    output_assets.mkdir(parents=True, exist_ok=True)
    
    # Track which assets we've already copied (by asset_name)
    copied_assets = set()
    
    for original_path, asset_name in asset_paths.items():
        asset_source = name_specific_assets / asset_name
        # Only copy once per unique asset
        if asset_name not in copied_assets:
            asset_dest = output_assets / asset_name
            asset_dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(asset_source, asset_dest)
            copied_assets.add(asset_name)
        # Map original path to new path
        path_mapping[original_path] = f"assets/{asset_name}"
    
    return path_mapping

def update_asset_paths_in_html(html_content, path_mapping):
    """Update asset paths in HTML content to match the new structure."""
    updated_content = html_content
    
    for old_path, new_path in path_mapping.items():
        # Replace in src attributes (handle various formats)
        updated_content = updated_content.replace(f'src="{old_path}"', f'src="{new_path}"')
        updated_content = updated_content.replace(f"src='{old_path}'", f"src='{new_path}'")
        # Replace in source tags (for video)
        updated_content = updated_content.replace(f'<source src="{old_path}"', f'<source src="{new_path}"')
        updated_content = updated_content.replace(f"<source src='{old_path}'", f"<source src='{new_path}'")
    
    return updated_content

def main():
    """
    Main function to parse command line arguments and process markdown files.
    """
    parser = argparse.ArgumentParser(description='Process markdown files for website generation.')
    parser.add_argument('name', type=str, help='Name of the markdown file (without .md) - used for both input and output folder')

    args = parser.parse_args()

    # Get the script directory to find the template base
    script_dir = Path(__file__).parent
    template_base = script_dir.parent
    
    name = args.name

    # Construct path to markdown file in markdowns/ folder
    markdown_file_path = template_base / "markdowns" / f"{name}.md"
    if not markdown_file_path.exists():
        raise FileNotFoundError(f"Markdown file not found: {markdown_file_path}")

    # Read markdown content to extract asset paths
    with open(markdown_file_path, 'r') as f:
        markdown_content = f.read()
    
    # Extract asset paths before processing
    asset_paths = extract_asset_paths(markdown_content, name)

    # Create output directory in public/ using the same name
    workspace_root = template_base.parent
    output_dir = workspace_root / "public" / name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy all assets and get path mapping (pass the name for asset lookup in assets/{name}/)
    path_mapping = copy_assets(asset_paths, output_dir, script_dir, name)

    # Parse and generate HTML
    metadata = parse_frontmatter(str(markdown_file_path))
    content = parse_markdown(str(markdown_file_path))

    _html = generate_premble(metadata.title) + metadata.__html__() + content + SUFFIX
    
    # Update asset paths in HTML
    _html = update_asset_paths_in_html(_html, path_mapping)
    
    fmt_html = format_html(_html)

    # Write index.html
    index_path = output_dir / "index.html"
    with open(index_path, "w+") as outfile:
        outfile.write(fmt_html)

    print(f"Generated website at: {output_dir}")
    print(f"Open: {index_path}")

    return None

if __name__ == "__main__":
    main()
