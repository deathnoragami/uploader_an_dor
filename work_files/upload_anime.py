import work_files.upload_anime_sftp as upload_anime_sftp
from work_files.database_title import DatabaseManager
import os


def upload_anime(file_path_image,
                 file_path_video,
                 check_sftp,
                 check_mult,
                 check_nolink):
    print(file_path_image, file_path_video, check_mult, check_nolink, check_sftp)
    
    if file_path_video is not None and check_sftp:
        dbm = DatabaseManager()
        dbm.add_entry(file_path_image, file_path_video, "Югио Поспеши | Yu Gi Yo Go Rush", check_sftp, check_mult, check_nolink, "animunt.org", "anime")
        if dbm.search_by_path_pic_anime(file_path_image):
            print("Есть в БД.")
        else:
            print("Нет в БД.")
        # upload_anime_sftp()
    else:
        pass
        # заливка только в вк