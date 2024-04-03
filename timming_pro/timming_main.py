import pymiere
import json
import os


def add_timming():
    try:
        app = pymiere.objects.app.project
        sequence = app.activeSequence
        if sequence:
            project_name = app.name
            project_path = app.path
            sequence_name = sequence.name
            clips_video = sequence.videoTracks[2].clips
            clips_audio = sequence.audioTracks[1].clips
            main_track = sequence.videoTracks[0].clips
            numClips = main_track.numItems
            lastClip = main_track[numClips - 1]
            endtime = lastClip.end.seconds
            startTimeVideo = []
            for clip in clips_video:
                startTimeVideo.append(clip.start.seconds)
                startTimeVideo.append(clip.name)
                
            startTimeAudio = []
            for clip in clips_audio:
                startTimeAudio.append(clip.start.seconds)
                
            data = {
                    "projectname": os.path.splitext(project_name)[0],
                    "sequencename": sequence_name,
                    "starttimevideo": startTimeVideo,
                    "starttimeaudio": startTimeAudio,
                    "endtime": endtime,
                    "path_project": project_path      
            }    

            with open('assets/timming.json', 'a', encoding='UTF-8') as file:
                json.dump(data, file, ensure_ascii=False)
                file.write('\n')
            return data
    except ValueError as e:
        if "Premiere Pro is not running" in str(e):
            return False
        
        
      
def format_timming(data):
    if len(data["starttimevideo"]) == 4 and len(data["starttimeaudio"]) == 1:
        timming = f'Преролл: {format_time(data["starttimevideo"][0])}\n' \
                    f'5 сек в миде: {format_time(data["starttimeaudio"][0])}\n' \
                    f'30 Плашка: {format_time(data["starttimevideo"][2])}\n' \
                    f'Вотермарка с 0 до {format_time(data["endtime"], round_up=False)} минуты'
        name_ad = f"{data['starttimevideo'][1].split('.mp4')[0] if '.mp4' in data['starttimevideo'][1] else data['starttimevideo'][1].split('.mov')[0]}\n" \
                    f'Начитка\n' \
                    f'Плашка'
    elif len(data["starttimevideo"]) == 8 and len(data["starttimeaudio"]) == 1:
        timming = f'Преролл {format_time(data["starttimevideo"][0])}\n' \
                    f'Аудио {format_time(data["starttimeaudio"][0])}\n' \
                    f'Плашка {format_time(data["starttimevideo"][2])}\n' \
                    f'Преролл {format_time(data["starttimevideo"][4])}\n' \
                    f'Плашка {format_time(data["starttimevideo"][6])}\n' \
                    f'Вотермарка с 00:00 по {format_time(data["endtime"], round_up=False)} минуты'
        name_ad = f"{data['starttimevideo'][1].split('.mp4')[0] if '.mp4' in data['starttimevideo'][1] else data['starttimevideo'][1].split('.mov')[0]}\n" \
                    f'Начитка\n' \
                    f"{data['starttimevideo'][3].split('.mp4')[0] if '.mp4' in data['starttimevideo'][3] else data['starttimevideo'][3].split('.mov')[0]}\n" \
                    f"{data['starttimevideo'][5].split('.mp4')[0] if '.mp4' in data['starttimevideo'][5] else data['starttimevideo'][5].split('.mov')[0]}\n" \
                    f"{data['starttimevideo'][7].split('.mp4')[0] if '.mp4' in data['starttimevideo'][7] else data['starttimevideo'][7].split('.mov')[0]}"
    elif len(data["starttimevideo"]) == 8 and len(data["starttimeaudio"]) == 2:
        timming = f'Преролл {format_time(data["starttimevideo"][0])}\n' \
                    f'Аудио {format_time(data["starttimeaudio"][0])}\n' \
                    f'Плашка {format_time(data["starttimevideo"][2])}\n' \
                    f'Аудио {format_time(data["starttimeaudio"][1])}\n' \
                    f'Преролл {format_time(data["starttimevideo"][4])}\n' \
                    f'Плашка {format_time(data["starttimevideo"][6])}\n' \
                    f'Вотермарка с 00:00 по {format_time(data["endtime"], round_up=False)} минуты' 
        name_ad = f"{data['starttimevideo'][1].split('.mp4')[0] if '.mp4' in data['starttimevideo'][1] else data['starttimevideo'][1].split('.mov')[0]}\n" \
                    f'Начитка\n' \
                    f"{data['starttimevideo'][3].split('.mp4')[0] if '.mp4' in data['starttimevideo'][3] else data['starttimevideo'][3].split('.mov')[0]}\n" \
                    f'Начитка\n' \
                    f"{data['starttimevideo'][5].split('.mp4')[0] if '.mp4' in data['starttimevideo'][5] else data['starttimevideo'][5].split('.mov')[0]}\n" \
                    f"{data['starttimevideo'][7].split('.mp4')[0] if '.mp4' in data['starttimevideo'][7] else data['starttimevideo'][7].split('.mov')[0]}"  
    elif len(data["starttimevideo"]) == 12 and len(data["starttimeaudio"]) == 3:
        timming = f'Преролл: {format_time(data["starttimevideo"][0])}\n' \
                    f'5 сек в миде: {format_time(data["starttimeaudio"][0])}\n' \
                    f'30 Плашка: {format_time(data["starttimevideo"][2])}\n' \
                    f'Преролл: {format_time(data["starttimevideo"][4])}\n' \
                    f'5 сек в миде: {format_time(data["starttimeaudio"][1])}\n' \
                    f'30 Плашка: {format_time(data["starttimevideo"][6])}\n' \
                    f'Преролл: {format_time(data["starttimevideo"][8])}\n' \
                    f'5 сек в миде: {format_time(data["starttimeaudio"][2])}\n' \
                    f'30 Плашка: {format_time(data["starttimevideo"][10])}\n' \
                    f'Вотермарка с 00:00 до {format_time(data["endtime"], round_up=False)} минуты'
        name_ad = f"{data['starttimevideo'][1].split('.mp4')[0] if '.mp4' in data['starttimevideo'][1] else data['starttimevideo'][1].split('.mov')[0]}\n" \
                    f'Начитка\n' \
                    f'Плашка\n' \
                    f"{data['starttimevideo'][5].split('.mp4')[0] if '.mp4' in data['starttimevideo'][5] else data['starttimevideo'][5].split('.mov')[0]}\n" \
                    f'Начитка\n' \
                    f'Плашка\n' \
                    f"{data['starttimevideo'][9].split('.mp4')[0] if '.mp4' in data['starttimevideo'][9] else data['starttimevideo'][9].split('.mov')[0]}\n" \
                    f'Начитка\n' \
                    f'Плашка'     
    else:
        timming = f'Я получил {len(data["starttimevideo"])} данных видео\n' \
                  f'{len(data["starttimeaudio"])} данных аудио\n' \
                  f'Для аниме должно быть 4:1, для дорамы 8:1 \nили 8:2, фильм 12:3 \nпроверьте проект'   
        name_ad = ""
    
    return timming, name_ad

def get_list(data):
    if len(data["starttimevideo"]) == 4 and len(data["starttimeaudio"]) == 1:
        timming_list = [format_time(data["starttimevideo"][0]),
                format_time(data["starttimeaudio"][0]),
                format_time(data["starttimevideo"][2]),
                format_time(data["endtime"], round_up=False)]
    elif len(data["starttimevideo"]) == 8 and len(data["starttimeaudio"]) == 1:
        timming_list = [format_time(data["starttimevideo"][0]),
                            format_time(data["starttimeaudio"][0]),
                            format_time(data["starttimevideo"][2]),
                            format_time(data["starttimevideo"][4]),
                            format_time(data["starttimevideo"][6]),
                            format_time(data["endtime"], round_up=False)]
    elif len(data["starttimevideo"]) == 8 and len(data["starttimeaudio"]) == 2:
        timming_list = [format_time(data["starttimevideo"][0]),
                            format_time(data["starttimeaudio"][0]),
                            format_time(data["starttimevideo"][2]),
                            format_time(data["starttimeaudio"][1]),
                            format_time(data["starttimevideo"][4]),
                            format_time(data["starttimevideo"][6]),
                            format_time(data["endtime"], round_up=False)]
    else:
        timming_list = None
    return timming_list
        
def format_time(sec, round_up=True):
    if sec < 3600:
        mm = int(sec // 60)
        ss = int(sec % 60)
        if round_up:
            if (sec - ss) % 1 >= 0.75 or ss == 60:
                ss += 1
        if ss == 60:
            mm += 1
            ss = 0
        return f"{mm:02d}:{ss:02d}"
    else:
        hh = int(sec // 3600)
        mm = int((sec % 3600) // 60)
        ss = int(sec % 60)
        if round_up:
            if (sec - ss) % 1 >= 0.75 or ss == 60:
                ss += 1
        if ss == 60:
            mm += 1
            ss = 0
        if mm == 60:
            hh += 1
            mm = 0
        return f"{hh:02d}:{mm:02d}:{ss:02d}"
