from .video import VideoWorker
from .sub import SubsWorker
import os
from PyQt5.QtCore import pyqtSignal

class Signals():
    progress = pyqtSignal(int)

def subs_extract(video_path: str) -> str | None:
    """
    Извлекает субтитры из видеофайла, расположенного по указанному пути video_path.

    Аргументы:
        video_path (str): Путь к видеофайлу, из которого будут извлечены субтитры.

    Возвращает:
        str | None: Путь к извлеченному файлу субтитров, если операция прошла успешно, иначе None.
    """
    return SubsWorker().subs_extract(video_path)

def subs_edit(path: str, path_save: str, srt_save: bool = True, actor_srt: bool = True) -> str:
    """
    Изменяет субтитры, расположенные по указанному пути path.

    Аргументы:
        path (str): Путь к файлу субтитров, который нужно изменить.
        path_save (str): Путь для сохранения измененных субтитров.
        srt_save (bool, optional): Сохранять ли файлы субтитров в формате srt.
        actor_srt (bool, optional): Добавлять ли информацию о актере в каждом строке субтитров.

    Возвращает:
        str: Путь к измененному файлу субтитров.
    """
    return SubsWorker().subs_edit(path, path_save, srt_save, actor_srt)


def sub_extract_and_edit(video_path: str, srt_save: bool = True, actor_srt: bool = True) -> str:
    """
    Извлекает субтитры из видеофайла, расположенного по указанному пути video_path, 
    затем изменяет эти субтитры.

    Аргументы:
        video_path (str): Путь к видеофайлу, из которого будут извлечены субтитры.
        srt_save (bool, optional): Сохранять ли файлы субтитров в формате srt.
        actor_srt (bool, optional): Добавлять ли информацию о актере в каждом строке субтитров.

    Возвращает:
        str | None: Путь к измененному файлу субтитров, если операция прошла успешно, иначе None.
    """
    path_sub = SubsWorker().subs_extract(video_path)
    if path_sub is None: return None
    path_sub_sign = SubsWorker().subs_edit(path_sub, os.path.dirname(video_path), srt_save, actor_srt)
    return path_sub_sign

def video_hardsub(video_path: str, ui):
    progress = VideoWorker().run_ffmpeg(video_path, ui)
