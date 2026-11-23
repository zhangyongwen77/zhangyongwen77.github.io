#!/usr/bin/env python3
"""Build portable static pages from the content directory."""
from datetime import date
import html
import json
from itertools import groupby
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "content/site.json").read_text(encoding="utf-8"))


def esc(value):
    return html.escape(str(value), quote=True)


def link(url, label):
    if urlparse(url).scheme not in {"http", "https"}:
        return esc(label)
    return f'<a href="{esc(url)}">{esc(label)} <span aria-hidden="true">↗</span></a>'


def render_research(item):
    figure = item.get("figure")
    illustration = ""
    if figure:
        credit = link(figure["source"], figure["credit"]) if figure.get("source") else ""
        illustration = (
            '<figure class="research-figure">'
            f'<img src="{esc(figure["src"])}" alt="{esc(figure["alt"])}" '
            f'width="{int(figure["width"])}" height="{int(figure["height"])}" loading="lazy">'
            f'<figcaption>{esc(figure["caption"])} {credit}</figcaption></figure>'
        )
    return (
        f'<article class="research-item">{illustration}<div class="research-copy">'
        f'<h3>{esc(item["title"])}</h3><p>{esc(item["description"])}</p></div></article>'
    )


research = "".join(render_research(item) for item in data["research"])


def render_person(person, featured=False, heading="h4"):
    name = esc(person["name"])
    photo = person.get("image", "")
    if photo and (ROOT / photo).is_file():
        crop = person.get("image_crop")
        crop_class = ""
        crop_style = ""
        frame_style = ""
        if crop:
            crop_class = " portrait-cropped"
            frame_style = f' style="aspect-ratio:{int(crop["width"])}/{int(crop["height"])}"'
            crop_style = (
                f' style="width:{100 * crop["source_width"] / crop["width"]:.6f}%;'
                f'height:{100 * crop["source_height"] / crop["height"]:.6f}%;'
                f'left:{-100 * crop["x"] / crop["width"]:.6f}%;'
                f'top:{-100 * crop["y"] / crop["height"]:.6f}%;"'
            )
        portrait = (
            f'<div class="person-portrait{crop_class}"{frame_style}><img src="{esc(photo)}" '
            f'alt="{name}"{crop_style} loading="lazy" decoding="async"></div>'
        )
    else:
        initials = "".join(part[0] for part in person["name"].split())
        portrait = f'<div class="person-portrait person-monogram" aria-hidden="true">{esc(initials)}</div>'
    role_class = "role team-leader" if person["role"] == "Team Leader" else "role"
    profiles = []
    if person.get("profile_url"):
        profiles.append(link(person["profile_url"], "University profile"))
    if featured and data.get("scholar_url"):
        profiles.append(link(data["scholar_url"], "Google Scholar"))
    profile = f'<div class="person-links">{" ".join(profiles)}</div>' if profiles else ""
    role = esc(person["role"])
    if person.get("start_year"):
        role += f' · {int(person["start_year"])} cohort'
    display_name = name
    if not featured and person.get("name_native"):
        display_name += f' <span class="native-name" lang="zh-Hans">{esc(person["name_native"])}</span>'
    return (
        f'<article class="person{" person-featured" if featured else ""}">{portrait}<div class="person-copy">'
        f'<p class="{role_class}">{role}</p><{heading}>{display_name}</{heading}>'
        f'<p class="person-bio">{esc(person.get("bio", ""))}</p>{profile}</div></article>'
    )


people = "".join(render_person(person, featured=True, heading="h3") for person in data["people"] if person["role"] == "Team Leader")
members = [person for person in data["people"] if person["role"] != "Team Leader"]
students = data.get("students", [])
if not people and not members and not students:
    people = '<div class="empty-state"><span class="empty-label">MEET THE GROUP</span><p>People make the research.</p><span>Profiles of the group leader, researchers, and students will appear here.</span></div>'
member_cards = "".join(render_person(person) for person in members)
if not member_cards and not students:
    member_cards = '<p class="students-pending">Member profiles will be added soon.</p>'

student_section = ""
if students:
    student_cards = "".join(render_person(person, heading="h5") for person in students)
    student_section = (
        '<section class="student-roster" id="students" aria-labelledby="current-students-title">'
        '<h4 id="current-students-title">Graduate Students</h4>'
        f'<div class="students-grid">{student_cards}</div></section>'
    )

alumni_section = ""
if data.get("alumni"):
    rows = "".join(
        f'<li><span>{esc(person["name"])}</span><small>{esc(person["cohorts"])}</small></li>'
        for person in data["alumni"]
    )
    alumni_section = (
        '<section class="students-section" id="alumni" aria-labelledby="alumni-title">'
        f'<h3 id="alumni-title">Alumni</h3><ul class="alumni-list">{rows}</ul></section>'
    )

def citation(paper):
    corresponding = set(paper.get("corresponding_authors", []))
    if not corresponding.issubset(paper["authors"]):
        raise ValueError(f'Corresponding author missing from the byline: {paper["title"]}')
    names = []
    for author in paper["authors"]:
        name = esc(author)
        if author in {"Yongwen Zhang", "Yong-Wen Zhang"}:
            name = f'<strong>{name}</strong>'
        if author in corresponding:
            name += '<sup class="corresponding" title="Corresponding author" aria-label="Corresponding author">*</sup>'
        names.append(name)
    authors = ", ".join(names)
    title = esc(paper["title"])
    if not title.endswith((".", "?", "!")):
        title += "."
    venue = f'<i>{esc(paper["journal"])}</i>'
    if paper.get("volume"):
        venue += f' <b>{esc(paper["volume"])}</b>'
    if paper.get("locator"):
        venue += f', {esc(paper["locator"])}'
    doi = paper.get("doi")
    reference = (f'<a href="https://doi.org/{esc(doi)}">https://doi.org/{esc(doi)}</a>'
                 if doi else link(paper["url"], "Publisher"))
    return (f'<li>{authors}. {title} {venue} ({esc(paper["year"])}). '
            f'{reference}</li>')


papers = json.loads((ROOT / "content/publications.json").read_text(encoding="utf-8"))
papers.sort(key=lambda paper: (-paper["year"], paper["title"].casefold()))
citations_by_year = {
    year: "".join(citation(paper) for paper in entries)
    for year, entries in groupby(papers, key=lambda paper: paper["year"])
}
year_links = " ".join(f'<a href="#year-{year}">{year}</a>' for year in citations_by_year)


def year_sections(heading_tag):
    return "\n".join(
        f'<section class="bibliography-year" aria-labelledby="year-{year}">'
        f'<{heading_tag} class="year-title" id="year-{year}">{year}</{heading_tag}>'
        f'<ol class="citations">{items}</ol></section>'
        for year, items in citations_by_year.items()
    )


def news_item(item):
    published = date.fromisoformat(item["date"])
    title = link(item["url"], item["title"]) if item.get("url") else esc(item["title"])
    figure = item.get("figure")
    illustration = ""
    if figure:
        illustration = (
            '<figure class="news-figure">'
            f'<a href="{esc(figure["full"])}" aria-label="View full-size figure for {esc(item["title"])}">'
            f'<img src="{esc(figure["preview"])}" alt="{esc(figure["alt"])}" '
            f'width="{int(figure["width"])}" height="{int(figure["height"])}" loading="lazy" decoding="async"></a>'
            f'<figcaption>{link(figure["source"], figure["caption"])}</figcaption></figure>'
        )
    return (
        f'<article class="news-item">{illustration}<div class="news-copy"><time datetime="{published.isoformat()}">'
        f'{published.day} {published:%B %Y}</time><h3>{title}</h3>'
        f'<p>{esc(item["text"])}</p></div></article>'
    )


news = "".join(news_item(item) for item in sorted(data["news"], key=lambda n: n["date"], reverse=True))
contact = ""
if data["email"]:
    contact += f'<a class="contact-link" href="mailto:{esc(data["email"])}">{esc(data["email"])} <span aria-hidden="true">↗</span></a>'
else:
    contact += '<p class="contact-placeholder">Contact details to be added</p>'
addresses = data["address"]
if isinstance(addresses, str):
    addresses = [addresses]
contact += "".join(f'<p>{esc(address)}</p>' for address in addresses if address)
preview = data.get("preview", True)
replacements = {
    "NAME": esc(data["name"]),
    "SHORT_NAME": esc(data["short_name"]),
    "AFFILIATION": esc(data["affiliation"]),
    "HEADLINE": esc(data["headline"]),
    "INTRODUCTION": esc(data["introduction"]),
    "RESEARCH": research,
    "PEOPLE": people,
    "MEMBERS": member_cards,
    "STUDENTS": student_section,
    "ALUMNI": alumni_section,
    "YEAR_LINKS": year_links,
    "NEWS_ITEMS": news or '<p>Group activities and research updates will appear here.</p>',
    "OPPORTUNITIES": esc(data["opportunities"]),
    "CONTACT": contact,
    "ROBOTS": '<meta name="robots" content="noindex, nofollow">' if preview else "",
    "PREVIEW": '<div class="preview-banner">DRAFT FOR REVIEW</div>' if preview else "",
}
for template, filename, year_heading in (
    ("page.html.tmpl", "index.html", "h3"),
    ("publications.html", "publications.html", "h2"),
):
    page = (ROOT / "scripts" / template).read_text(encoding="utf-8")
    page = page.replace("{{YEAR_SECTIONS}}", year_sections(year_heading))
    for key, value in replacements.items():
        page = page.replace("{{" + key + "}}", value)
    (ROOT / filename).write_text(page, encoding="utf-8")
    print(f"Generated {filename}")
