import feedparser
import requests
import datetime
import os
from openai import OpenAI

# 配置 DeepSeek
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), 
    base_url="https://api.deepseek.com" # 确保是 DeepSeek 的地址
)

def start():
    print("正在搜索最新动态...")
    # 抓取新闻
    feed = feedparser.parse("https://news.google.com/rss/search?q=neutrino+energy+technology&hl=zh-CN")
    context = "\n".join([e.title for e in feed.entries[:5]])

    print("AI 正在构思文章...")
    try:
        # 注意：这里模型必须改为 deepseek-chat
        response = client.chat.completions.create(
            model="deepseek-chat", 
            messages=[{"role": "user", "content": f"请根据以下标题写一篇关于中微子能源的深度科普报道：\n{context}"}]
        )
        article_content = response.choices[0].message.content
    except Exception as e:
        print(f"AI 生成失败: {e}")
        return

    # 生成网页
    html_template = f"""
    <html>
    <head><meta charset="utf-8"><title>中微子能源周报</title></head>
    <body style="font-family:sans-serif; max-width:700px; margin:auto; padding:20px; line-height:1.7;">
        <h1>中微子能源每日快讯</h1>
        <p>发布时间: {datetime.date.today()}</p>
        <div style="white-space: pre-wrap;">{article_content}</div>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("网页 index.html 已生成")

if __name__ == "__main__":
    start()
