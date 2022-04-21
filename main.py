import subprocess
import ffmpeg
import sys

#cropping the original clip to match the original audio recording
sys.path.append(r'C:\FFmpeg\bin')

stream = ffmpeg.input('clip.mp4')
stream = stream.trim(start=45, duration=29).filter('setpts', 'PTS-STARTPTS')
stream = stream.filter('fps', fps=25, round='up')
stream = ffmpeg.output(stream, 'new_video.mp4')
ffmpeg.run(stream)

#function for executing the command passed in the argument
def run_command(command):
    p = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    return p.stdout.decode().strip()


#a function for turning an audio recording into a video showing sound waves
#with a cropped clip superimposed on the background
#function argument rec_name is audio file name, new_video is clip name
def turn_audio_to_video(rec_name, new_video):
    rec_path = "./{}".format(rec_name)
    video_path = "./{}".format(new_video)
    video_name = "out.mp4"

    command = 'ffmpeg -y -i {rec_path} -i {video_path}  \
    -filter_complex "[0:a]showwaves=s=2500x720:mode=cline:colors=random,format=yuva420p[fg]; \
    [1:v]scale=2500x720[bg];\
    [bg][fg]overlay=x=25:y=(H-500)" \
    -map 0:a -c:v libx264 -c:a aac \
    -shortest ./{video_name}'.format(
        rec_path=rec_path,
        video_path=video_path,
        video_name=video_name,
    )

    print(video_name)
    run_command(command)
    return video_name

#function to save the rec_name and new_video and starting the function turn_audio_to_video
def main():
    rec_name = "input.mp3"
    new_video = "new_video.mp4"
    turn_audio_to_video(rec_name, new_video)


main()
