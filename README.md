由于大文件上传起来麻烦，我就不上传了。
详情可以访问我的飞桨项目获取相关内容：
获取或自己训练音色模型  https://aistudio.baidu.com/projectdetail/8875375
对话微调模型： https://aistudio.baidu.com/projectdetail/8864531
所需的关键库paddlespeech 也在上述飞桨项目中，如果pip安装paddlespeech失败，飞桨中可以打包下载，并放到和bot.py同一文件夹下即可
其他依赖遇到一个pip一个慢慢解决即可（涉及到的依赖太多，但是pip都能直接解决）
需要cuda和cudnn的支持，本人cuda12.6，cudnn 9.8.0，可供参考，cuda和cudnn的安装可以在csdn上搜索得到大量优质教程。
pip 下载 Paddlepaddle时，要注意选择适合自己cuda版本的。可直接在浏览器搜索paddlepaddle第一个就是一个类似pytorch下载的页面。
对话插件和语音合成插件暂不支持同时开启
需要搭配napcat等机器人框架使用，强烈建议napcat，使用反向ws连接bot.py运行所在端口。
python版本最好3.8——3.11.
