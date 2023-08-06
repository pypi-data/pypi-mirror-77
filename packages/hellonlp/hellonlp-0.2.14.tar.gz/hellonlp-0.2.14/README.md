HelloNLP,NLP with deep learning. Mainly focus on text classification, NER, Chabot , pre-trained models.

GitHub: https://github.com/hellonlp



HelloNLP
^^^^^^^^^^^                     
 - 分词1：无监督，通过信息熵的方式
 - 分词2：有监督，通过深度学习（同时引入结巴分词多种分词模式的思维）#开发中




Example
^^^^^^^^^^^
Quick start

>>>
pip3 install hellonlp
from hellonlp.ChineseWordSegmentation import segment_entropy
words = segment_entropy.get_words(["界面又好看",
                            "主要是大像素摄像头",
                            "心理准备一星期",
                            "厂家和快递都好评",
                            "还有听儿歌要下载米兔儿童",
                            "空调三匹太强劲",
                            "HelloNLP会一直坚持开源和贡献",
			    "HelloNLP第一版终于发布了，太激动了",])
print(words[:10])
