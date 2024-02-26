from playwright.sync_api import sync_playwright
import re
from datetime import datetime, timedelta

class PostAnimaunt():
    def __init__(self, link_animaunt, link_malfurik, number_seria):
        pattern = re.compile(r'\d+')
        # try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(storage_state="assets/animaunt_storage.json")
            page = context.new_page()
            page.goto(link_animaunt)
            number_seria = pattern.findall(number_seria.split('.')[0])[0]
            page.locator("#xf_number_seria").fill(f'{int(number_seria)}')
            page.locator("#xf_date_timer_seria").fill(f"{int(number_seria)+1}")
            current_data = page.locator("#xf_date_timer").get_attribute("value")
            reform_current_data = datetime.fromisoformat(current_data)
            new_data = reform_current_data + timedelta(weeks=1)
            reform_new_data = new_data.strftime("%Y-%m-%dT%H:%M")
            print(current_data, reform_current_data, new_data, reform_new_data)
            page.locator("#xf_date_timer").fill(reform_new_data)
            
            page.get_by_label("установить текущую дату и время").check() # чекбокс
            
            # page.get_by_role("link", name=" Плеер Все серии").click()
            # page.locator("#tabplayer1").get_by_text("+").click() 
            
            # form_add_player = page.query_selector(".tab-pane.active#tabplayer1")
            # player_blocks = form_add_player.query_selector_all(".col-sm-12.playerNewBlock1")
            # input_values = []
            # for player_block in player_blocks:
            #     inputs = player_block.query_selector_all("input")
            #     input_values.extend([input.input_value() for input in inputs])
            # inputs = player_blocks[-1].query_selector_all("input")
            # inputs[-1].fill(input_values[-3])
            # inputs[-2].fill(input_values[-4])
            page.wait_for_timeout(20000)
        # except Exception as e:
        #     print(e)