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
        self.affiliations = list(set([author.affiliation for author in authors]))

    def __str__(self):
        return "; ".join([str(author) for author in self.authors])

    def __html__(self):
        affiliations_added = {}
        inner_html = ""
        for author in self.authors:
            if author is None:
                continue
            elif author is not None and author.affiliation is None:
                segment = f"<span class='individual-author'>{author.name}</span>"
            elif author.affiliation not in affiliations_added:
                affiliation_num = len(affiliations_added) + 1

                segment = f"<span class='individual-author'>{author.name}<label for='author-affiliation-{affiliation_num}' class='margin-toggle sidenote-number'></label><input type='checkbox' id='author-affiliation-{affiliation_num}' class='margin-toggle'/></span>, <span class='sidenote'>{author.affiliation}</span>"

                affiliations_added[author.affiliation] = affiliation_num
            else:
                segment = f"<span class='individual-author'>{author.name}<span class='superscript'>{affiliations_added[author.affiliation]}</span>, </span>"
            inner_html += segment
        if inner_html.endswith(", </span>"):
            inner_html = inner_html[:-9] + "</span>" # adjust the trailing comma

        if inner_html == "":
            html = ""
        else:
            html = f"<p class='newthought' id='authors'>{inner_html}</p>"

        return html

class Author:
    def __init__(self, name, affiliation):
        self.name = name
        self.affiliation = affiliation

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
