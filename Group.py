from Publication import Publication


class Group(object):

    def __init__(self, group_domen: str):
        self.group_domen: str = group_domen
        self.publication_count: int = 0
        self.keyword = str()
        self.publications: list[Publication] = list()
        self.error: str = str()
