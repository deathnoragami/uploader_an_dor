from playwright.sync_api import sync_playwright
import re
from datetime import datetime, timedelta
import log_config

class PostDorama:
    def __init__(self):
        pass
    
    def post_malfurik(self, link, timming_list = None, name_file = None):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)
                context = browser.new_context(storage_state="assets/malfurik_storage.json")
                page = context.new_page()
                page.set_default_timeout(120000)
                page.goto(link)
                locator_series = page.query_selector(".rwmb-field.rwmb-group-wrapper")
                locator_seria = locator_series.query_selector_all(".rwmb-clone.rwmb-group-clone")[-1]
                title = locator_seria.query_selector("[id^='themeum_video_info_title']").get_attribute("value")
                video_link = locator_seria.query_selector("[id^='themeum_video_link']").get_attribute("value")
                if name_file == None:
                    string = video_link.split("/")[-1]
                    pattern = r'(\d+).*x*.mp4'
                    match = re.search(pattern, string)
                    number = int(match.group(1)) + 1
                    new_string = re.sub(pattern, f"{number:02d}", string)
                    new_video_link = video_link.rsplit("/", 1)[0] + "/" + new_string + 'x.mp4'
                    old_number = title.split()[0]
                    new_number = str(int(old_number) + 1)
                    new_title = f"{new_number} серия"
                else:
                    new_video_link = video_link.rsplit("/", 1)[0] + "/" + name_file
                    old_number = title.split()[0]
                    new_number = str(int(old_number) + 1)
                    new_title = f"{new_number} серия"
                locator_series.query_selector_all(".rwmb-button.button-primary.add-clone")[-1].click()
                new_seria = page.query_selector(".rwmb-field.rwmb-group-wrapper").query_selector_all(".rwmb-clone.rwmb-group-clone")[-1]
                new_seria.query_selector("[id^='themeum_video_info_title']").fill(new_title)
                new_seria.query_selector("[id^='themeum_video_link']").fill(new_video_link)
                for time in timming_list:
                    time_code = new_seria.query_selector_all("[id^='themeum_timecodes']")
                    if len(time_code) == 1:
                        time_code[0].fill(time)
                    else:
                        time_code[-1].fill(time)
                    new_seria.query_selector(".rwmb-button.button-primary.add-clone").click()
                page.click("#publish")
                
                browser.close()
                return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            return e
        
    def post_animaunt(self, timer, link, name_file):
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(storage_state="assets/animaunt_storage.json")
                page = context.new_page()
                page.set_default_timeout(120000)
                page.goto(link)
                page.locator("#xf_number_seria").fill(f'{int(name_file)}')
                page.locator("#xf_date_timer_seria").fill(f"{int(name_file)+1}")
                current_data = page.locator("#xf_date_timer").get_attribute("value")
                reform_current_data = datetime.fromisoformat(current_data)
                if timer == True:
                    new_data = reform_current_data + timedelta(weeks=1)
                    reform_new_data = new_data.strftime("%Y-%m-%dT%H:%M")
                    page.locator("#xf_date_timer").fill(reform_new_data)
                else:
                    data_now = datetime.fromisoformat(datetime.now().isoformat())
                    time_difference = reform_current_data - data_now
                    if time_difference.days < 2:
                        new_data = reform_current_data + timedelta(weeks=2)
                        reform_new_data = new_data.strftime("%Y-%m-%dT%H:%M")
                        page.locator("#xf_date_timer").fill(reform_new_data)
                page.get_by_label("установить текущую дату и время").check()
                page.locator(".panel-footer").locator("button[type='submit']").click()
                page.wait_for_timeout(2000)
                browser.close()
                return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            return e