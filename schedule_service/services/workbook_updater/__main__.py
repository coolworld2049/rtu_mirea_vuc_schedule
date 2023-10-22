import pathlib

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from bs4 import BeautifulSoup
from loguru import logger

from schedule_service._logging import configure_logging
from schedule_service.settings import schedule_updater_settings


class ScheduleWorkbookUpdater:
    SCHEDULE_URL = "https://vuc.mirea.ru/raspisanie/"

    def __init__(
        self,
        workbooks_dir="files",
    ):
        self.workbooks_dir = pathlib.Path(__file__).parent.joinpath(workbooks_dir)

    def parse_schedule_files(self):
        with requests.get(self.SCHEDULE_URL) as response:
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            main_class = soup.find("main", class_="main")
            a_tags = main_class.find_all("a")
            schedule_links = {
                f"{x.text.strip().split(' ')[1]}-course": x.get("href") for x in a_tags
            }
            return schedule_links

    def update_workbooks(self):
        files = self.parse_schedule_files()
        for dir_name, link in files.items():
            dir = self.workbooks_dir.joinpath(dir_name)
            dir.mkdir(exist_ok=True)
            file_name = str(link).split("/")[-1]
            save_path = dir.joinpath(file_name)
            fs = save_path.open("wb")
            with requests.get(link, stream=True) as r:
                for chunk in r.iter_content(chunk_size=4096):
                    fs.write(chunk)
            fs.close()
            logger.info(f"Workbook {dir.name} updated - {str(link).split('/')[-1]}")


def main():
    configure_logging()
    schedule_downloader = ScheduleWorkbookUpdater()
    schedule_downloader.update_workbooks()
    apscheduler = BlockingScheduler()
    apscheduler.remove_all_jobs()
    apscheduler.add_job(
        schedule_downloader.update_workbooks,
        trigger="cron",
        id="update_workbooks",
        **schedule_updater_settings.model_dump(exclude_none=True),
    )
    apscheduler.start()


if __name__ == "__main__":
    main()
