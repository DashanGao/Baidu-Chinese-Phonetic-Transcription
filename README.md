# Chinese Audio To Text Conversion 中文语音转文字

--------------

This project uses Baidu audio API to convert Chinese audio in mp3 format into text. 
The length of the audio file is not limited. To convert Chinese audio to text, an account must be applied in `cloud.baidu.com`.

The long audio file is first aplited and converted into *wav* format files with *60s* length each and with 1 channel and 16k bitrate. 
Then, the API is invoked for each audio file to convert the audio into Chinese. The result is stored into a text file.


调用百度语音识别API，将一段任意长度的中文普通话mp3格式录音转换为文字。
1. 注册并登陆百度智能云。[百度智能云](https://login.bce.baidu.com/)
2. 在百度智能云->语音技术 中创建应用。得到应用对应的API Key 和Secret Key，复制粘贴到`audio_text_conversion.py`中。

* 首先选择人工智能中的语音技术
![选择语音技术](https://github.com/GaoDashan1/Audio_To_Text/blob/master/imgs/img1.png)
* 点击“创建应用”
![创建新应用](https://github.com/GaoDashan1/Audio_To_Text/blob/master/imgs/img2.png)
* 应用创建成功，获取API Key和Secret Key
![应用创建成功](https://github.com/GaoDashan1/Audio_To_Text/blob/master/imgs/img3.png)
3. 设定参数：打开`audio_text_conversion.py`文件（用任何文本编辑器，如命令行可使用vim）。将API Key和Secret Key输入`API_KEY`和`SECRET_KEY`中，并且将需要转音频的MP3文件路径复制到`SOURCE_AUDIO_FILE`。
5. 安装`pydub`库：在终端运行`pip3 install pydub`
4. 开始语音转文字：在终端运行代码 `python3 audio_text_conversion.py`





Requirement: pydub
