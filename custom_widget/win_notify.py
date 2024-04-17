from plyer import notification
import resource_path

def notify(title=str, msg=str):
    '''
    title - Заголовок
    msg - само сообщение
    '''
    notification.notify(title=title,
                        message=msg,
                        app_name="AUPAn",
                        app_icon=resource_path.path('icon.ico'))

