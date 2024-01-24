import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By

class RealmStatus():
    def __init__(self):
        self.driver = None

    def start(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://worldofwarcraft.blizzard.com/en-gb/game/status/classic1x-eu")

    def stop(self):
        self.driver.close()

    def retrieve_realms(self):
        self.driver.refresh()
        self.driver.implicitly_wait(1.0)

        table = self.driver.find_element(By.CLASS_NAME, "RealmsTable")
        rows = table.find_elements(By.CLASS_NAME, "SortTable-row")

        realms = {}

        def _get_status(column):
            if len(column.find_elements(By.CLASS_NAME, "Icon--checkCircleGreen")) > 0:
                return "Online"
            elif len(column.find_elements(By.CLASS_NAME, "Icon--lockedFilled")) > 0:
                return "Locked"
            else:
                return "Offline"

        for row in rows:
            columns = row.find_elements(By.CLASS_NAME, "SortTable-col")
            realm_type = columns[5].text
            
            if realm_type == "Seasonal":
                name = columns[1].text
                status = _get_status(columns[0])
                realms[name] = status

        return realms

    def __del__(self):
        if self.driver is not None:
            self.stop()

    @staticmethod
    def format_status(status):
        if status == "Online":
            return "✅"
        elif status == "Locked":
            return "🔒"
        else:
            return "❌"
