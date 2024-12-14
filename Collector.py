from collector.keyword_collector import collect_keywords
from collector.news_collector import collect_news
from collector.summarize_collector import collect_summary

if __name__ == '__main__':
    collect_keywords()
    collect_news()
    collect_summary()