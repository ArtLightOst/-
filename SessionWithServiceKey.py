import datetime
from threading import Thread
from time import sleep
from Group import Group
from Publication import Publication
from Tools import timing_of_method_execution, search_for_group_domens
from vk import Session, API
import Config


class SessionWithServiceKey(object):

    def __init__(self, access_token: str = Config.TOKEN):
        self.session = Session(access_token = access_token)
        self.vk_api = API(self.session)
        self.groups: list[Group] = list()

    @timing_of_method_execution
    def get_posts_from_single_group(self, group_domen: str, keyword: str,
                                    left_date: datetime.date,
                                    right_date: datetime.date) -> None:
        iteration: int = 1
        group: Group = Group(group_domen = group_domen)
        sleep(1)
        try:
            publication_count: int = self.vk_api.wall.get(domain = group_domen,
                                                          v = Config.API_VERSION)["count"]
            group.publication_count = publication_count
            group.keyword = keyword
        except Exception as Ex:
            match Ex.code:
                case Config.ACCESS_DENIED_CODE:
                    group.error = Config.ACCESS_DENIED_MESSAGE
                    self.groups.append(group)
                    return
                case Config.INCORRECT_REFERENCE_CODE:
                    group.error = Config.INCORRECT_REFERENCE_MESSAGE
                    self.groups.append(group)
                    return
                case _:
                    group.error = Config.ERROR_MESSAGE
                    self.groups.append(group)
                    return

        for offset in range(0, publication_count, 100):
            temp = self.search_100_posts_from_single_group(group = group_domen,
                                                           keyword = keyword,
                                                           offset = offset)
            for publication in temp:
                if left_date <= publication.get_date() <= right_date:
                    group.publications.append(publication)
                else:
                    self.groups.append(group)
                    return
            if iteration == Config.RPS:
                sleep(1)
                iteration = 1
            else:
                sleep(0.1)
                iteration += 1
        self.groups.append(group)
        return

    def search_100_posts_from_single_group(self, group: str, keyword: str, offset: int) -> list[Publication]:
        response = self.vk_api.wall.search(domain = group,
                                           query = keyword,
                                           owners_only = 1,
                                           v = Config.API_VERSION,
                                           count = 100,
                                           offset = offset)['items']
        return [Publication(j) for j in response]

    @timing_of_method_execution
    def get_posts_from_list_of_groups(self, groups: str,
                                      keyword: str,
                                      left_date: tuple | None = None,
                                      right_date: tuple | None = None):
        left_date = datetime.date(left_date[2], left_date[0], left_date[1]) if left_date else datetime.date(1970, 1, 1)
        right_date = datetime.date(right_date[2], right_date[0], right_date[1]) if right_date else datetime.date.today()
        list_of_groups: list[str] | None = search_for_group_domens(groups)
        if list_of_groups:
            threads: list[Thread] = []
            for group in set(list_of_groups):
                threads.append(Thread(target = self.get_posts_from_single_group, args = (group, keyword, left_date, right_date)))
            for thread in threads:
                thread.start()
                thread.join()
        else:
            print("Группы не опознаны")


if __name__ == '__main__':
    example = SessionWithServiceKey()
    with open(file = 'test_references.txt', mode = 'rt', encoding = 'utf-8') as ex:
        test = ex.read()
    example.get_posts_from_list_of_groups(test, input("Ключевое слово >> "))
    for i in example.groups:
        if not i.error:
            print("Группа -> ", i.group_domen)
            print("Всего публикаций -> ", i.publication_count)
            print("Запрос -> ", i.keyword)
            print("Найдено публикаций -> ", len(i.publications), '\n')
        else:
            print("Группа -> ", i.group_domen)
            print("Ошибка -> ", i.error, '\n')
