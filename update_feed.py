#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from dateutil.parser import parse

class HuggingFaceTrendingFeed:
    def __init__(self):
        self.base_url = "https://huggingface.co"
        self.model_trending_url = f"{self.base_url}/models?sort=trending"
        self.output_dir = "docs"
        
        # 确保输出目录存在
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_trending_models(self):
        """获取 trending 模型列表"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        }
        response = requests.get(self.model_trending_url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        models = []
        # 查找所有模型卡片
        cards = soup.find_all('article', class_='overview-card-wrapper')
        
        for card in cards:
            try:
                # 模型链接和标题
                title_link = card.find('a', class_='header-link')
                model_url = f"{self.base_url}{title_link['href']}"
                title = title_link.text.strip()
                
                # 模型描述
                description = card.find('div', class_='card-description').text.strip()
                
                # 作者信息
                author = card.find('a', class_='user-link').text.strip()
                
                # 获取更新时间
                time_element = card.find('time')
                updated_time = parse(time_element['datetime']) if time_element else datetime.now()
                
                # 获取标签
                tags = [tag.text.strip() for tag in card.find_all('span', class_='tag')]
                
                models.append({
                    'title': title,
                    'url': model_url,
                    'description': description,
                    'author': author,
                    'updated_time': updated_time,
                    'tags': tags
                })
            except Exception as e:
                print(f"Error processing model card: {e}")
                continue
                
        return models

    def generate_rss_feed(self, models):
        """生成 RSS Feed"""
        fg = FeedGenerator()
        fg.title('HuggingFace Trending Models')
        fg.description('Latest trending models from HuggingFace')
        fg.link(href=self.model_trending_url)
        fg.language('en')
        
        for model in models:
            fe = fg.add_entry()
            fe.title(model['title'])
            fe.link(href=model['url'])
            
            # 构建详细描述
            content = f"{model['description']}\n\nAuthor: {model['author']}\nTags: {', '.join(model['tags'])}"
            fe.description(content)
            
            fe.author(name=model['author'])
            fe.published(model['updated_time'])
            
        fg.rss_file(os.path.join(self.output_dir, 'feed.xml'))

    def generate_json_feed(self, models):
        """生成 JSON Feed"""
        json_feed = {
            "version": "https://jsonfeed.org/version/1",
            "title": "HuggingFace Trending Models",
            "home_page_url": self.model_trending_url,
            "feed_url": "feed.json",
            "items": []
        }
        
        for model in models:
            item = {
                "id": model['url'],
                "url": model['url'],
                "title": model['title'],
                "content_text": f"{model['description']}\n\nAuthor: {model['author']}\nTags: {', '.join(model['tags'])}",
                "date_published": model['updated_time'].isoformat(),
                "authors": [{"name": model['author']}],
                "tags": model['tags']
            }
            json_feed["items"].append(item)
            
        with open(os.path.join(self.output_dir, 'feed.json'), 'w', encoding='utf-8') as f:
            json.dump(json_feed, f, ensure_ascii=False, indent=2)

    def update_feeds(self):
        """更新所有订阅源"""
        print("Fetching trending models...")
        models = self.fetch_trending_models()
        
        print("Generating RSS feed...")
        self.generate_rss_feed(models)
        
        print("Generating JSON feed...")
        self.generate_json_feed(models)
        
        print("Feeds updated successfully!")

if __name__ == "__main__":
    feed_generator = HuggingFaceTrendingFeed()
    feed_generator.update_feeds() 