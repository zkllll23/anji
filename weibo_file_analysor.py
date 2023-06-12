# 作者: zkllll23
# 微博文件分析
import pandas as pd  # 存取csv文件
import jieba  # 分词
from wordcloud import WordCloud  # 词云

if __name__ == '__main__':
    # 要分析的关键词
    analysis_keywords = ['装置艺术', '光装置', '交互体验', '疗愈', '沉浸感']
    # 停用词文件
    stopwords_file = r"停用词/stopwords.txt"
    # jieba停用词
    jieba.load_userdict(stopwords_file)
    # 从文件中读取wc_stopwords
    with open('停用词/wc_stopwords.txt', 'r', encoding='utf-8') as f:
        wc_stopwords = {line.strip() for line in f.readlines()}
    # 分析微博文件
    for analysis_keyword in analysis_keywords:
        # 读取csv数据，并转换时间格式
        df = pd.read_csv('微博清单/微博清单_{}_前100页.csv'.format(analysis_keyword), parse_dates=['发布时间'])
        # 读取微博内容转为列表
        weibo_text_list = df['微博内容'].values.tolist()
        # 列表转字符串
        weibo_text_str = ' '.join(weibo_text_list)
        # jieba分词
        jieba_text = " ".join(jieba.lcut(weibo_text_str))
        # 词云图
        wc = WordCloud(
            scale=5,
            margin=0,
            background_color='white',
            max_words=50,
            width=800,
            height=450,
            font_path=r"C:\Windows\Fonts\simhei.ttf",
            stopwords=wc_stopwords,
            random_state=800
        )
        wc.generate_from_text(jieba_text)
        wc.to_file('词云图/{}_词云图.png'.format(analysis_keyword))
        wc.to_image()
