
HelloNLP
============
                     
做更好的NLP开源者






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



