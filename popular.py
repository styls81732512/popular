import pymysql
import jieba
import jieba.analyse
import datetime

# 拉取資料
def get_data():
    crawler_Date = datetime.datetime.now().strftime("%Y-%m-%d")
    crawler_Time = datetime.datetime.now().strftime("%H:00:00")
    crawler_Time2 = (datetime.datetime.strptime(crawler_Time, "%H:00:00") + datetime.timedelta(hours = -1)).strftime("%H:00:00")
    data = ''
    db = pymysql.connect(host='35.221.146.104', user='jiantong', password='ui1JYaq1NLXzeV7J', db='argus', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM `crawler` WHERE `crawler_Date` = '" + crawler_Date + "' AND `crawler_Time` BETWEEN '" + crawler_Time2 + "' AND '" + crawler_Time + "'"
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        db.commit()
        content = ''
        for i in data:
            content += i[4] + i[5] + i[7]
        content = content.replace(" ","")
        content = content.replace("\r\n","")
        return content
    except:
        return "error"

# 定義高頻詞統計
def get_tf(words, topK=50):
    tf_dic = dict()
    for w in words:
        tf_dic[w] = tf_dic.get(w, 0) + 1
    return sorted(tf_dic.items(), key=lambda x: x[1], reverse=True)[:topK]

# 獲取停用詞
def get_stopwords():
    with open('C:/Users/PC/Desktop/python/popular/key_stopword.txt', encoding='utf-8') as stopwords:
        return [line.strip() for line in stopwords]

# 結果
def demo_topk():
    jieba.load_userdict('C:/Users/PC/Desktop/python/popular/keyword.txt')
    split_words = list(jieba.cut(get_data()))

    stopwords = get_stopwords()

    split_words_stopwords = [word for word in split_words if word not in stopwords and len(word)> 1]

    data = get_tf(split_words_stopwords)         
    db = pymysql.connect(host='35.221.146.104', user='jiantong', password='ui1JYaq1NLXzeV7J', db='argus', charset='utf8')   
    cursor = db.cursor()
    for i in range(0, len(data), 1):
        insert_sql = 'INSERT INTO popular(popular_Word, popular_Qty, popular_Date, popular_Time)VALUES(%s, %s, now(), now())' 
        text = (data[i][0], data[i][1]) 
        cursor.execute(insert_sql, text) 
    db.commit()

demo_topk()



