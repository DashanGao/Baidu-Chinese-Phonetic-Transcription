# coding=utf-8
# Author: Dashan Gao
# Data: 2020/02/21

"""
调用百度语音识别API，将一段任意长度的录音转换为文字。
1. 注册并登陆百度智能云。
2. 在百度智能云->语音技术 中创建应用。 得到应用对应的API Key 和Secret Key， 复制粘贴到下方代码中。
3. 将需要转音频的MP3文件路径粘贴到下方代码中。
5. 安装pydub库，命令行运行 pip3 install pydub
4. 运行代码 python3 audio_text_conversion.py
"""

import sys
import os
import json
import base64
import time
from glob import glob
from urllib.request import urlopen
from urllib.request import Request
from urllib.error import URLError
from urllib.parse import urlencode
from pydub import AudioSegment

timer = time.perf_counter

# ************** 需要自行设定 ************************
# 注册登陆百度智能云，创建应用得到API_KEY， SECRET_KEY
API_KEY = '*******************'
SECRET_KEY = '******************'
# 原始mp3音频文件路径
SOURCE_AUDIO_FILE = "PATH_TO_AUDIO.mp3"
# *************************************************

# 保存处理后短音频文件的文件夹路径
AUDIO_FILES_PATH = "output_audios/"
# 语音转文字结果保存文件路径
DES_TEXT_FILE = "result_text.txt"

FORMAT = 'wav'  # 文件后缀只支持 pcm/wav/amr 格式
ASR_URL = 'http://vop.baidu.com/server_api'
TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_voice_assistant_get'


def process_audio(audio_file, output_dir="output_audios/"):
    """
    处理音频文件，将长音频文件拆分为60s短音频，采样率16k，单声道
    :param audio_file: 音频文件路径
    :param output_dir: 输出文件路径
    """
    # 60s per each file. 每个短音频时长60秒。
    slice_length = 60 * 1000
    # 0.5s overlap between short audios. 为防止遗漏，两个音频之间有0.5秒的重叠
    overlap = 0.5 * 1000
    begin = 0
    index = 0
    # Make output dir 创建处理后短音频文件的路径
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    source_file_format = audio_file.split(".")[-1]
    audio = AudioSegment.from_file(audio_file, format=source_file_format)
    # Split and process source audio file. 拆分并处理音频文件
    while begin < len(audio):
        output_audio = audio[int(begin): int(begin+slice_length)]  #
        seconds = begin / 1000
        # 生成文件名
        output_file_name = output_dir + "{0:04d}_{minus}m{second}s.wav".format(index, minus=int(seconds/60),
                                                                               second=int(seconds) % 60)
        # change to 1 channel and 16k bitrate 设定单声道，16000采样率
        output_audio = output_audio.set_channels(1).set_frame_rate(16000)
        # 存储生成的短音频文件
        output_audio.export(output_file_name, format="wav")  # save audio file.
        begin += slice_length - overlap
        index += 1


class DemoError(Exception):
    pass


def fetch_token():
    """
    根据API_KEY， SECRET_KEY获取 access token
    :return: access token
    """
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = result_str.decode()
    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if SCOPE and (not SCOPE in result['scope'].split(' ')):  # SCOPE = False 忽略检查
            raise DemoError('Scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


def audio_to_text(token, audio_file):
    """
    Convert audio file into text. 调用API，将音频转换为文字。
    :param audio_file: short audio file with wav format, 1 channel and 16k bitrate. 音频文件路径
    :return: recognized text. 识别的文字
    """
    with open(audio_file, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % audio_file)
    speech = base64.b64encode(speech_data)
    speech = str(speech, 'utf-8')
    params = {'dev_pid': 1537,
              'format': FORMAT,
              'rate': 16000,
              'token': token,
              'cuid': '123456PYTHON',
              'channel': 1,
              'speech': speech,
              'len': length
              }
    post_data = json.dumps(params, sort_keys=False)
    req = Request(ASR_URL, post_data.encode('utf-8'))
    req.add_header('Content-Type', 'application/json')
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
    result_str = str(result_str, 'utf-8')
    result = json.loads(result_str)
    try:
        result_text = result["result"][0]
    except:
        result_text = "Error"
    return result_text


def main():
    # Process audio and split into multiple short audios, 60s each, with 1 channel and 16k bitrate.
    print("Start audio pre-processing...")
    process_audio(SOURCE_AUDIO_FILE, AUDIO_FILES_PATH)
    print("Audio pre-processing finished.")

    # 获取访问API所需token
    token = fetch_token()
    print("Token fetched.")

    # Read audio file paths. 读取音频文件
    audio_files = glob(AUDIO_FILES_PATH + "*")
    audio_files.sort()
    print("Start audio-to-text conversion...")
    des_text = open(DES_TEXT_FILE, "w+")
    for audio_file in audio_files:
        # Invoke API, convert audio to text. 调用API，音频转文字。
        result_text = audio_to_text(token, audio_file)
        audio_tag = audio_file.split("/")[-1].split(".")[0]
        # 打印识别结果并存储。
        print(audio_tag + "\t" + result_text)
        des_text.write(audio_tag + "\t" + result_text + "\n")
    des_text.close()
    print("\n********Audio-to-text conversion finished.********")


if __name__ == '__main__':
    main()
