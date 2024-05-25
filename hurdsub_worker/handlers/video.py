import subprocess
import re
import os

class VideoWorker:
    def run_ffmpeg(self, input_file, ui, progress_callback=None):
        self.ui = ui
        ffmpeg_path = 'bin/ffmpeg.exe'
        output_path = f'{os.path.splitext(input_file)[0]}.mp4'
        command = [ffmpeg_path, '-y', '-i', input_file, '-vf', 'ass=subs_sign.ass', '-c:v', 'h264_nvenc', '-c:a', 'copy', '-f', 'mp4', output_path]
        try:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            total_duration = None
            for line in process.stderr:
                
                if line.startswith("  Duration:"):
                    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+)", line)
                    if match:
                        hours, minutes, seconds = match.groups()
                        total_duration = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
                elif " time=" in line:
                    match = re.search(r"time=(\d+:\d+:\d+)", line)
                    if match and total_duration:
                        current_time = match.group(1)
                        h, m, s = map(int, current_time.split(':'))
                        current_seconds = h * 3600 + m * 60 + s
                        progress_percent = (current_seconds / total_duration) * 100
                        self.progress_callback(int(progress_percent))
            process.communicate()
            os.remove()
        except subprocess.CalledProcessError as e:
            print("Произошла ошибка при конвертации:", e)

    def progress_callback(self, progress_percent):
        self.ui.ui.progress_ffmpeg.setValue(progress_percent)


# input_file = '66.mkv'
# output_file = 'output_video.mp4'
# run_ffmpeg(input_file, output_file, progress_callback)