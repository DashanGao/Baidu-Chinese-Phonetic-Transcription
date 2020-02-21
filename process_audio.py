from pydub import AudioSegment
import os

source_file = "Path to .mp3 file"
output_dir = "output_audios/"


def process_audio(audio_file, output_dir="output_audios/"):
    slice_length = 60 * 1000  # 60s per each file
    overlap = 0.5 * 1000  # 0.5s overlap between short audios.
    begin = 0
    index = 0
    # Make output dir
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    source_file_format = audio_file.split(".")[-1]
    audio = AudioSegment.from_file(audio_file, format=source_file_format)
    # Split and process source audio file.
    while begin < len(audio):
        output_audio = audio[int(begin): int(begin+slice_length)]  #
        seconds = begin / 1000
        output_file_name = output_dir + "{0:04d}_{minus}m{second}s.wav".format(index, minus=int(seconds/60),
                                                                               second=int(seconds) % 60)
        output_audio = output_audio.set_channels(1).set_frame_rate(16000)  # change to 1 channel and 16k bitrate
        output_audio.export(output_file_name, format="wav")  # save audio file.
        begin += slice_length - overlap
        index += 1


if __name__ == '__main__':
    process_audio(source_file, output_dir)
