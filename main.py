import subprocess
import ffmpeg
import sys

# cropping the original clip to match the original audio recording
sys.path.append(r'C:\FFmpeg\bin')

stream = ffmpeg.input('clip.mp4')
stream = stream.trim(start=45, duration=29).filter('setpts', 'PTS-STARTPTS')
stream = stream.filter('fps', fps=25, round='up')
stream = ffmpeg.output(stream, 'new_video.mp4')
ffmpeg.run(stream)


# function for executing the command passed in the argument
def run_command(command):
    p = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )

    return p.stdout.decode().strip()


# function for splitting audio
def cut_audio(rec_name):
    rec_path = "./{}".format(rec_name)

    command = 'ffmpeg -i {rec_path} -f segment -segment_time 5 -c copy \
     -reset_timestamps 1 "C:\\Users\\user\\PycharmProjects\\Audio\\cutaudio\\out%d.mp3"'.format(
            rec_path=rec_path,
        )

    run_command(command)

# function for of creating a wave with random color
# for each segment of the video


def audio_wave(rec_video, i):
    cutvideo_path = "./cutaudio/{}".format(rec_video)

    command = 'ffmpeg -y -i {cutvideo_path} \
    -filter_complex "[0:a]showwaves=s=2500x720:mode=cline:colors=random,format=yuva420p" \
    -c:v libx264 -c:a aac cutwave/output{i}.mp4 '.format(
        cutvideo_path=cutvideo_path,
        i=i
    )

    run_command(command)

# function for creating a sound wave with sound


def result_wave(rec_name, rec_wave):
    wave_path = "./{}".format(rec_wave)
    rec_path = "./{}".format(rec_name)

    command = 'ffmpeg -i {wave_path} -i {rec_path} -c:v copy -c:a aac finall_wave.mp4'.format(
        wave_path=wave_path,
        rec_path=rec_path
    )

    run_command(command)


# function for creating a video clip with a sound wave
def final(f_wave, new_video):
    wave = "./{}".format(f_wave)
    video_path = "./{}".format(new_video)

    command = 'ffmpeg -y -i {wave} -i {video_path}  \
    -filter_complex "[0:v]scale=s=1280x200,format=yuva420p[fg]; \
    [1:v]scale=1280x720[bg];\
    [bg][fg]overlay=y=(H-200)" \
    -c:v libx264 -c:a aac \
    -shortest final.mp4'.format(
        wave=wave,
        video_path=video_path,
    )

    run_command(command)
# function to save the rec_name and new_video and starting the function turn_audio_to_video


def main():
    rec_name = "input.mp3"
    cut_audio(rec_name)
    # creating empty dictionaries for loops
    rec_video, rec_full_wave = [], []
    # loop to start the function for creating sound waves
    for i in range(6):
        rec_video.append("out{i}.mp3".format(i=i))
        audio_wave(rec_video[i], i)
        rec_full_wave.append("out{i}.mp4".format(i=i))
    # loop for combining all segments of sound waves into one
    for j in range(len(rec_full_wave)):
        rec_full_wave[j] = ffmpeg.input('./cutwave/output{j}.mp4'.format(j=j))
    full_wave = ffmpeg.concat(*rec_full_wave)
    full_wave = ffmpeg.output(full_wave, 'full_wave.mp4')
    ffmpeg.run(full_wave)
    rec_wave = "full_wave.mp4"
    result_wave(rec_name, rec_wave)
    new_video = "new_video.mp4"
    f_wave = "finall_wave.mp4"
    final(f_wave, new_video)


main()
