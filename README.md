# Audio_To_Text

--------------

This project uses Baidu audio API to convert Chinese audio in mp3 format into text. 
The length of the audio file is not limited. To convert Chinese audio to text, an account must be applied in `cloud.baidu.com`.

The long audio file is first aplited and converted into *wav* format files with *60s* length each and with 1 channel and 16k bitrate. 
Then, the API is invoked for each audio file to convert the audio into Chinese. The result is stored into a text file.


调用百度语音识别API，将一段任意长度的录音转换为文字。
1. 注册并登陆百度智能云。
2. 在百度智能云->语音技术 中创建应用。 得到应用对应的API Key 和Secret Key， 复制粘贴到下方代码中。
3. 将需要转音频的MP3文件路径粘贴到下方代码中。
5. 安装pydub库，命令行运行 pip3 install pydub
4. 运行代码 python3 audio_text_conversion.py

Requirement: pydub
