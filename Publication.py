import datetime
import Config


class Publication(object):

    def __init__(self, data: dict):
        self.data: dict = data

    def get_date(self) -> datetime.date:
        tupled_date: tuple = tuple(datetime.datetime.fromtimestamp(self.data['date']).timetuple())
        return datetime.date(tupled_date[0], tupled_date[1], tupled_date[2])

    def get_str_time(self) -> str:
        tupled_date: tuple = tuple(datetime.datetime.fromtimestamp(self.data['date']).timetuple())
        time = datetime.time(tupled_date[3], tupled_date[4])
        return ('0' + str(time.hour) if len(str(time.hour)) < 2 else str(time.hour)) + ':' + ('0' + str(time.minute) if len(str(
            time.minute)) < 2 else str(time.minute))

    def get_text(self) -> str:
        return self.data['text']

    def get_comments_count(self) -> int:
        return self.data['comments']['count']

    def get_likes_count(self) -> int:
        return self.data['likes']['count']

    def get_reposts_count(self) -> int:
        return self.data['reposts']['count']

    def get_views_count(self) -> int | str:
        return self.data['views']['count'] if 'views' in self.data.keys() else Config.ABSENCE_MESSAGE

    def get_photo_urls(self) -> str:
        photo_urls: list = list()
        if 'attachments' in self.data.keys():
            for content in self.data['attachments']:
                if 'photo' in content:
                    photo_urls.append(content['photo']['sizes'][len(content['photo']['sizes']) - 1]['url'])
        return '\n'.join([*photo_urls]) if photo_urls else Config.ABSENCE_MESSAGE

    def get_links_urls(self) -> str:
        links: list = list()
        if 'attachments' in self.data.keys():
            for content in self.data['attachments']:
                if 'link' in content:
                    links.append(content['link']['url'])
        return '\n'.join([*links]) if links else Config.ABSENCE_MESSAGE

    def get_platform(self) -> str:
        return self.data['post_source']['platform'] if 'platform' in self.data['post_source'] else Config.ABSENCE_MESSAGE


if __name__ == '__main__':
    example = Publication()  # TODO: Вставить тестовые данные
    print('ДАТА ПУБЛИКАЦИИ', ' -> ', example.get_date())
    print('ВРЕМЯ ПУБЛИКАЦИИ', ' -> ', example.get_str_time())
    print('ПЛАТФОРМА', ' -> ', example.get_platform())
    print('ТЕКСТ', ' -> ', example.get_text())
    print('КОЛИЧЕСТВО ЛАЙКОВ', ' -> ', example.get_likes_count())
    print('КОЛИЧЕСТВО КОММЕНТОВ', ' -> ', example.get_comments_count())
    print('КОЛИЧЕСТВО РЕПОСТОВ', ' -> ', example.get_reposts_count())
    print('ПРИКРЕПЛЁННЫЕ ФОТО', ' -> ', example.get_photo_urls())
    print('ПРИКРЕПЛЁННЫЕ ССЫЛКИ', ' -> ', example.get_links_urls())
