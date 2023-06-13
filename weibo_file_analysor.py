# 作者: zkllll23
# 微博文件分析
import pandas as pd  # 存取csv文件
import jieba  # 分词
from wordcloud import WordCloud  # 词云
import matplotlib.pyplot as plt  # 图的显示
from collections import Counter  # 计数器


def load_stopwords(file_path):
    """
    加载停用词
    :param file_path: 停用词文件路径
    :return: 停用词集合
    """
    stopwords = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            temp = line.strip()
            stopwords.add(temp)
    return stopwords


def analysis_text(analysis_keyword):
    """
    文本分析
    :param analysis_keyword: 分析关键词
    :return: 分词过滤后的关键词
    """
    # 读取csv数据，并转换时间格式
    df = pd.read_csv('微博清单/微博清单_{}_前100页.csv'.format(keyword), parse_dates=['发布时间'])
    # 读取微博内容转为列表
    weibo_text_list = df['微博内容'].values.tolist()
    # 列表转字符串
    weibo_text_str = ' '.join(weibo_text_list)
    # jieba分词
    seg_list = jieba.lcut(weibo_text_str)
    # 过滤停用词
    filtered_words = [word for word in seg_list if word not in stopword_list]
    return filtered_words


def generate_wordcloud(wordcloud_text):
    """
    生成词云图
    :param wordcloud_text: 词云内容
    """
    # 词云配置
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
    # 生成词云
    wc.generate_from_text(" ".join(wordcloud_text))
    # 生成词云图
    wc.to_file('词云图/{}_词云图.png'.format(keyword))
    wordcloud_image = wc.to_image()
    # 显示词云图像
    plt.imshow(wordcloud_image, interpolation='bilinear')
    plt.axis('off')
    plt.show()


# 统计词频
def count_word_frequency(count_text, cur_keyword):
    """
    统计词频
    :param count_text: 用于统计的内容
    :param cur_keyword: 当前关键词
    """
    # 统计词频
    word_frequency = Counter(jieba_text)
    # 词频排序
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)
    # 创建DataFrame对象
    df = pd.DataFrame(sorted_word_frequency, columns=['关键词', '频率'])
    # 定义要保存的CSV文件路径
    csv_file = '词频统计/{}_词频统计.csv'.format(keyword)
    # 将 DataFrame 写入CSV文件
    df.to_csv(csv_file, index=False, encoding='utf_8_sig')


if __name__ == '__main__':
    # 爬虫爬取关键词
    search_keywords = ['装置艺术', '光装置', '交互体验', '疗愈', '沉浸感']
    # 停用词文件
    stopwords_file = r"停用词/stopwords.txt"
    # 加载停用词
    stopword_list = load_stopwords(stopwords_file)
    # 从文件中读取wc_stopwords
    with open('停用词/wc_stopwords.txt', 'r', encoding='utf_8_sig') as f:
        wc_stopwords = {line.strip() for line in f.readlines()}

    # 分析微博文件
    for keyword in search_keywords:
        # jieba分词分析文本
        jieba_text = analysis_text(keyword)
        # 词频统计
        count_word_frequency(jieba_text, keyword)
        # 生成词云
        generate_wordcloud(jieba_text)
