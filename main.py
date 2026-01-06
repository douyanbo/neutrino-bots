import feedparser, requests, datetime
from requests.auth import HTTPBasicAuth
from openai import OpenAI
import os

# 从系统环境变量读取密钥（安全做法）
API_KEY = os.getenv("OPENAI_API_KEY")
WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PWD = os.getenv("WP_PWD")

client = OpenAI(api_key=API_KEY)

def start():
    # 1. 抓取数据
    print("正在搜索最新动态...")
    news = feedparser.parse("https://news.google.com/rss/search?q=neutrino+energy+technology")
    context = "最新消息：\n" + "\n".join([e.title for e in news.entries[:5]])

    # 2. AI 写稿
    print("AI 正在构思文章...")
    prompt = f"请根据以下信息，写一篇关于中微子能源的科普美文，要求标题专业，内容丰富，适合发布在WordPress：\n{context}"
    response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    content = response.choices[0].message.content

    # 3. 发布到 WordPress
    post_data = {"title": f"中微子能源前沿报告 ({datetime.date.today()})", "content": content, "status": "publish"}
    res = requests.post(WP_URL, json=post_data, auth=HTTPBasicAuth(WP_USER, WP_PWD))
    if res.status_code == 201: print("发布成功！")
    else: print("发布失败，请检查配置")

if __name__ == "__main__":
    start()
