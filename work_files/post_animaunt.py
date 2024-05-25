from playwright.sync_api import sync_playwright
import re
from datetime import datetime, timedelta
import log_config

class PostAnimaunt():
    def __init__(self, link_animaunt, number_seria, name_video, data_time):
        self.link_animaunt = link_animaunt
        self.number_seria = number_seria
        self.name_video = name_video
        self.pattern = re.compile(r'\d+')
        self.data_time = data_time
            
    def post(self):
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=True)
                context = browser.new_context(storage_state="assets/animaunt_storage.json")
                page = context.new_page()
                page.goto(self.link_animaunt)
                number_seria = self.pattern.findall(self.number_seria.split('.')[0])[0]
                page.locator("#xf_number_seria").fill(f'{int(number_seria)}')
                page.locator("#xf_date_timer_seria").fill(f"{int(number_seria)+1}")
                current_data = page.locator("#xf_date_timer").get_attribute("value")
                reform_current_data = datetime.fromisoformat(current_data)
                new_data = reform_current_data + timedelta(weeks=1)
                reform_new_data = new_data.strftime("%Y-%m-%dT%H:%M")
                page.locator("#xf_date_timer").fill(reform_new_data)
                page.get_by_label("установить текущую дату и время").check() # чекбокс
                
                # КАЛЕНДАРЬ ЗАПОЛНЕНИЕ 1 СЕРИИ
                page.query_selector(".fa.fa-calendar-check-o.position-left").click()
                table_div = page.query_selector(".table.table-lg.table-hover")
                page.query_selector(".btn.bg-teal.btn-sm.btn-raised.position-right.legitRipple").click()
                if not len(table_div.query_selector_all("input")) > 2:
                    pass
                else:
                    data2 = table_div.query_selector_all("input")[-1] # дата 2
                    data1 = table_div.query_selector_all("input")[-2] # дата 1
                    name = table_div.query_selector_all("input")[-3] # Название
                    data2.fill(self.data_time)
                    data1.fill(self.data_time)
                    name.fill(f"Эпизод {int(number_seria)}")
                
                # ПЛЕЕР
                page.get_by_role("link", name=" Плеер").click()
                page.locator("#tabplayer1").get_by_text("+").click() 
                form_add_player = page.query_selector(".tab-pane.active#tabplayer1")
                player_blocks = form_add_player.query_selector_all(".col-sm-12.playerNewBlock1")
                input_values = []
                for player_block in player_blocks:
                    inputs = player_block.query_selector_all("input")
                    input_values.extend([input.input_value() for input in inputs])
                inputs = player_blocks[-1].query_selector_all("input")
                
                if self.name_video:
                    last_slash = input_values[-3].rfind("/")
                    path_video = input_values[-3][:last_slash]
                    inputs[-1].fill(f"{path_video}/{self.name_video}")
                else:
                    last_link_video = input_values[-3]
                    match = re.search(r'(\d+)(x?)(?=\.\w+$)', last_link_video)
                    if match:
                        file_number = int(match.group(1))
                        x_symbol = match.group(2)
                        new_file_number = file_number + 1
                        new_file_number = f"{new_file_number:02d}{x_symbol}"
                        new_path_video = re.sub(r'(\d+)(x?)(?=\.\w+$)', new_file_number, last_link_video)
                        inputs[-1].fill(new_path_video)
                inputs[-2].fill(f"{int(number_seria)} серия")
                panel_footer = page.locator(".panel-footer")
                panel_footer.locator("button[type='submit']").click()
                browser.close()
                return True
        except Exception as e:
            log_config.setup_logger().exception(e)
            return e