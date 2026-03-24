import datetime

class Video():
    def __init__(self, post_html):
        self.url = post_html.get_attribute('href')
        self.id = self.url.split('/')[-1]
        self._get_video_date()

    def _get_video_date(self):
        self.date = datetime.datetime.fromtimestamp(int(self.id) >> 32,
                                                    datetime.UTC)

