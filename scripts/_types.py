class Title:
    def __init__(self, title):
        self.title = title
        self.has_colon = False
        self.precolon = None
        self.postcolon = None
        self.segment_title()

    def segment_title(self):
        if ":" in self.title:
            self.has_colon = True
            self.precolon = self.title.split(":")[0]
            self.postcolon = self.title.split(":")[1]
        else:
            self.has_colon = False

    def __str__(self):
        return self.title

    def __html__(self):
        if self.title is None:
            return ""
        if self.has_colon:
            html = f"<h1 class='title'><span class='main-title'>{self.precolon}:</span><span class='post-colon-title'> {self.postcolon}</span></h1>"
        else:
            html = f"<h1 class='title'><span class='main-title'>{self.title}</span></h1>"
        return html

class Date:
    def __init__(self, date):
        self.date = date

    def __str__(self):
        return self.date

    def __html__(self):
        if self.date is None:
            return ""
        return f"<p class='date'>{self.date}</p>"

class Authors:
    def __init__(self, authors):
        self.authors = authors
        self.author_map = {author.name: author.affiliation for author in authors}
        self.names = [author.name for author in authors]
        all_affiliations = []
        for author in authors:
            if isinstance(author.affiliation, list):
                all_affiliations.extend(author.affiliation)
            elif author.affiliation is not None:
                all_affiliations.append(author.affiliation)
        self.affiliations = list(set(all_affiliations))

    def __str__(self):
        return "; ".join([str(author) for author in self.authors])

    def __html__(self):
        affiliations_added = {}
        inner_html = ""
        authors = [a for a in self.authors if a is not None]

        for i, author in enumerate(authors):
            is_last = (i == len(authors) - 1)
            affs = author.affiliation if isinstance(author.affiliation, list) else ([author.affiliation] if author.affiliation else [])

            name_html = (
                f"<a class='pop' href='{author.link}' target='_blank' rel='noopener noreferrer'>{author.name}</a>"
                if author.link else author.name
            )

            # Name in its own span; labels+sidenotes interleaved after so each
            # sidenote immediately follows its label (keeps CSS counter correct).
            segment = f"<span class='individual-author'>{name_html}</span>"

            for j, affiliation in enumerate(affs):
                is_last_aff = (j == len(affs) - 1)
                label_class = "margin-toggle sidenote-number" if is_last_aff else "margin-toggle sidenote-number-comma-after"

                if affiliation not in affiliations_added:
                    affiliation_num = len(affiliations_added) + 1
                    affiliations_added[affiliation] = affiliation_num
                    note_id = f"author-affiliation-{affiliation_num}"
                    segment += (
                        f"<label for='{note_id}' class='{label_class}'></label>"
                        f"<input type='checkbox' id='{note_id}' class='margin-toggle'/>"
                        f"<span class='sidenote'>{affiliation}</span>"
                    )
                else:
                    affiliation_num = affiliations_added[affiliation]
                    prefix = "," if j > 0 else ""
                    segment += f"<span class='superscript'>{prefix}{affiliation_num}</span>"

            if not is_last:
                segment += ", "

            inner_html += segment

        if inner_html == "":
            return ""
        return f"<p class='newthought' id='authors'>{inner_html}</p>"

class Author:
    def __init__(self, name, affiliation, link):
        self.name = name
        self.affiliation = affiliation
        self.link = link

    def __str__(self):
        return f"{self.name}, {self.affiliation}"

class Link:
    def __init__(self, text, link):
        self.text = text
        self.link = link

    def __str__(self):
        return f"{self.text}: {self.link}"

    def __html__(self):
        if self.link == -1:
            return ""
        if self.link:
            return f"<span class='newthought'><a class='pop' href='{self.link}' target='_blank' rel='noopener noreferrer'>{self.text}</a></span>"
        else:
            return f"<span class='newthought'><a class='unpop' href=''>{self.text}</a></span>"

class Venue:
    def __init__(self, venue):
        self.venue = venue

    def __str__(self):
        return self.venue

    def __html__(self):
        if self.venue is None:
            return ""
        return f"<p class='proc-venue'>{self.venue}</p>"

class Award:
    def __init__(self, award):
        self.award = award

    def __str__(self):
        return self.award

    def __html__(self):
        if self.award is None:
            return ""
        return f"<p class='highlight_award'>{self.award}</p>"

class Metadata:
    def __init__(self, title, authors, date, venue, award, links):
        self.title = title
        self.authors = authors
        self.date = date
        self.venue = venue
        self.award = award
        self.links = links

    def __str__(self):
        s = f"Title: {self.title}\nAuthors: {str(self.authors)}\nVenue: {str(self.venue)}\n"
        for link in self.links:
            s += f"{link.text}: {link.link}\n"
        return s

    def format_links(self):
        inner_html = ""
        for link in self.links:
            inner_html += link.__html__()
        return f"<p class='links'>{inner_html}</p>"

    def __html__(self):
        inner_html = self.title.__html__() + self.authors.__html__() + self.date.__html__() + self.venue.__html__() + self.award.__html__() + self.format_links()
        return f"<section id = 'title-main'>{inner_html}</section>"


class Section:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):
        return f"{self.title}: {self.content}"

    def __html__(self):
        return f"<h2 class='section-header'>{self.title}</h2><p>{self.content}</p>"

class Figure:
    def __init__(self, caption, image_path):
        self.caption = caption
        self.image_path = image_path

    def __str__(self):
        return f"Figure [{self.image_path}]: {self.caption}"
