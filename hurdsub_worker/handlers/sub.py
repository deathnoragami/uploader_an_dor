import pysubs2
import os
import subprocess
from pathlib import Path


NAME_SUB='/subs.ass'
NAME_SIGN_SUB='subs_sign.ass'
NAME_TEXT_SUB='/subs_text.ass'

class SubsWorker:
    def comparator(self, sub: str) -> bool:
        if (
            'text' not in sub
            and 'sign' not in sub
            and 'надпись' not in sub
            and 'caption' not in sub
            and 'title' not in sub
            and 'song' not in sub
            and 'screen' not in sub
            and 'typedigital' not in sub
            and 'phonetics' not in sub
        ):
            return True
        return False

    def subs_extract(self, video_path) -> str | None:
        ffmpeg_path = './bin/ffmpeg.exe'
        subs_path = os.path.dirname(video_path) + NAME_SUB
        ffmpeg_command = [
            ffmpeg_path, '-i', video_path, '-map', f'0:s:m:language:rus', subs_path
        ]
        completed_process = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)            
        if "Stream map '0:s:m:language:rus' matches no streams." in completed_process.stderr.decode('utf-8'):
            ffmpeg_command = [
                ffmpeg_path, '-i', video_path, '-map', f'0:s:1', subs_path
            ]
            subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)  
        return subs_path

    def subs_edit(self, path: str, path_save: str = ".", save_srt:bool = True, actor_srt:bool = True) -> None:
        try:
            subs = pysubs2.load(path)
            save_sing = True
            to_delete = []
            to_delete_sign = []
            char = '{'
            for i, sub in enumerate(subs.events):
                if self.comparator(sub.name.lower()):
                    to_delete.append(i)
                elif self.comparator(sub.name.lower()):
                    to_delete.append(i)
                else:
                    to_delete_sign.append(i)
            if len(to_delete) == len(subs.events):
                to_delete = [
                    i for i, sub in enumerate(subs.events) if char not in sub.text
                ]
                save_sing = False
                
            to_delete.sort()
            for i in reversed(to_delete):
                del subs[i]
            if save_sing:
                subs.save(NAME_SIGN_SUB)
            subs = pysubs2.load(path)
            to_delete_sign.sort()
            for i in reversed(to_delete_sign):
                del subs[i]
            subs.save(path_save + NAME_TEXT_SUB)
            if save_srt:
                subs = pysubs2.load(path_save + NAME_TEXT_SUB)
                if actor_srt:
                    for event in subs.events:
                        actor = event.name if event.name else ''
                        if event.text and actor:
                            event.text = f'{actor}: {event.text}'
                subs.save(path_save + '/sub.srt')
            os.remove(path_save + NAME_TEXT_SUB)
            os.remove(path_save + NAME_SUB)
            return NAME_SIGN_SUB
        except:
            return None