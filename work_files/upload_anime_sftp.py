from PyQt5.QtWidgets import QMessageBox
from connect_firebase import Connect
import os
import pysftp


def upload(folder, 
           number_seria,
           server_name=None):
    db = Connect()
    with open('assets/session_timmers', 'r') as file:
        uid = file.read()
        user_data = db.find_user_uid(uid)
        maunt_login = user_data.get('maunt_login')
        maunt_pass = user_data.get('maunt_pass')
        print(maunt_login, maunt_pass)
        print(os.getenv("ANIMAUNT_IP_SERVER"))
        
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        with pysftp.Connection(os.getenv("ANIMAUNT_IP_SERVER"), username=maunt_login, password=maunt_pass, port=22, cnopts=cnopts) as sftp:
            sftp.chdir('/home/video/mp4')
            if server_name == None:
                list_dir = sorted(sftp.listdir_attr(), key=lambda k: k.st_mtime, reverse=False)
                name_folder = None
                folder_name = folder
                for attr in list_dir:
                    if folder_name.lower() in attr.filename.lower():
                        name_folder = attr.filename
                
                if name_folder == None:
                    sftp.close()
                    return
                
                file_name = number_seria
                sftp.chdir(name_folder)
                # Сообщение что чтото нашел
                reply = QMessageBox.question(None, "Оповещение", f"Найден каталог {name_folder}", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                
                if reply == QMessageBox.Yes:
                    print("Гружу")
                    # sftp.put(Полная директория файла, callback=progress)
                    # sftp.close()
                    # return
                else:
                    print("Не гружу")
            else:
                sftp.chdir(server_name)
                # sftp.put(Полная директория файла, callback=progress)
                # sftp.close()
                print("Сервер есть")
                
    db.close()
