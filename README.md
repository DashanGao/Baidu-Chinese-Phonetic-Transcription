# Chinese Audio To Text Conversion 中文语音文字转换

--------------

This project uses Baidu audio API to convert Chinese audio in mp3 format into text. 
The length of the audio file is not limited. To convert Chinese audio to text, an account must be applied in `cloud.baidu.com`.

The long audio file is first aplited and converted into *wav* format files with *60s* length each and with 1 channel and 16k bitrate. 
Then, the API is invoked for each audio file to convert the audio into Chinese. The result is stored into a text file.


调用百度语音识别API，将一段任意长度的中文普通话mp3格式录音转换为文字。
1. 注册并登陆百度智能云。[百度智能云](https://login.bce.baidu.com/)
2. 在百度智能云->语音技术 中创建应用。得到应用对应的API Key 和Secret Key，复制粘贴到`audio_text_conversion.py`中。

⋅⋅⋅1. 首先选择人工智能中的语音技术
⋅⋅⋅![选择语音技术](https://github.com/GaoDashan1/Audio_To_Text/blob/master/imgs/img1.png)

⋅⋅⋅2. 点击“创建应用”
⋅⋅⋅ ![创建新应用](https://github.com/GaoDashan1/Audio_To_Text/blob/master/imgs/img2.png)

⋅⋅⋅3. 应用创建成功，获取API Key和Secret Key
⋅⋅⋅ ![应用创建成功](https://github.com/GaoDashan1/Audio_To_Text/blob/master/imgs/img3.png)

3. 将需要转音频的MP3文件路径粘贴到`python3 audio_text_conversion.py`中。
5. 安装`pydub`库，命令行运行`pip3 install pydub`
4. 运行代码 `python3 audio_text_conversion.py`





Requirement: pydub
