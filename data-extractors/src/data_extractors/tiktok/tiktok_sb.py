import datetime

from selenium.webdriver.remote.webelement import WebElement


class Video:
    def __init__(self, post_html: WebElement) -> None:
        href = post_html.get_attribute("href")
        assert href is not None
        self.url: str = href
        self.id: str = self.url.split("/")[-1]
        self._get_video_date()

    def _get_video_date(self) -> None:
        self.date: datetime.datetime = datetime.datetime.fromtimestamp(
            int(self.id) >> 32,
            datetime.UTC,
        )
