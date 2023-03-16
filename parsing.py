from selectolax.parser import HTMLParser
from selectolax.parser import Node as HTMLNode
import models
from env import BASE_URL


class ProblemRow:
    def __init__(self, node: HTMLNode) -> None:
        self.node = node
        self.children: list[HTMLNode] = self.node.select("td").matches
        self.problem: models.Problem = models.Problem

    def get_problem_data(self):
        # 0, 3, 4
        simple_cell = lambda i: self.children[i].text().strip()
        # 2
        complex_cell = (
            lambda i: self.children[1]
            .select("div")
            .matches[i]
            .text()
            .strip()
            .replace("\n                        ", "")
        )

        self.problem.id = simple_cell(0)
        self.problem.difficulty = simple_cell(3)
        self.problem.passed_count = simple_cell(4)[1:]

        self.problem.tag_id = complex_cell(1)
        self.problem.name = complex_cell(0)

        self.problem.contest_id = None
        self.problem.url = BASE_URL + self.children[0].css_first("a").attrs["href"]

        return {
            "id": str(self.problem.id),
            "tag_id": self.problem.tag_id if self.problem.tag_id != "" else None,
            "contest_id": self.problem.contest_id,
            "name": str(self.problem.name),
            "difficulty": int(self.problem.difficulty),
            "passed_count": int(self.problem.passed_count)
            if self.problem.passed_count != ""
            else 0,
            "url": str(self.problem.url),
        }

    def get_problem(self):
        return self.problem(**self.get_problem_data())


class TagRow:
    def __init__(self, node: HTMLNode) -> None:
        self.node = node
        self.children: list[HTMLNode] = self.node.select("td").matches
        self.tag: models.Tag = models.Tag

    def get_row_data(self):
        self.tag.id = self.node.attrs["value"]
        self.tag.name = self.node.text().strip()

        return {
            "id": str(self.tag.id),
            "name": str(self.tag.name),
        }

    def get_tag(self):
        return self.tag(**self.get_row_data())


def get_problemset(html: str) -> set[models.Problem]:
    problemset: set[models.Problem] = set()
    parser = HTMLParser(html)

    table = parser.css_first("table.problems")
    # first row is header row
    rows = table.select("tr").matches[1:]
    for row in rows:
        r = ProblemRow(row)
        problem = r.get_problem()
        if problem not in problemset:
            problemset.add(problem)
    return problemset


def get_tagset(html: str) -> set[models.Tag]:
    tagset: set[models.Tag] = set()
    parser = HTMLParser(html)

    label = parser.css_first("select")
    # first option is empty, second is "any tag"
    options = label.select("option").matches[2:]
    for option in options:
        o = TagRow(option)
        tag = o.get_tag()
        if tag not in tagset:
            tagset.add(tag)
    return tagset

def get_page_count(html: str) -> int:
    parser = HTMLParser(html)
    pages = parser.css_first("div.pagination")
    page = int(pages.select("li").matches[-2].text().strip())
    return page

