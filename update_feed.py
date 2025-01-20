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
                card_link = card.find('a')
                model_url = f"{self.base_url}{card_link['href']}"
                title = card_link.find('header').text.strip()
                
                models.append({
                    'title': title,
                    'url': model_url,
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