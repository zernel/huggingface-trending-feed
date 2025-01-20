# HuggingFace Trending Feed

🤗 为 HuggingFace Trending 模型提供 RSS 和 JSON Feed 订阅源 | RSS and JSON Feed for HuggingFace Trending Models

## 简介 | Introduction

这个项目会自动抓取 [HuggingFace Trending Models](https://huggingface.co/models?sort=trending) 页面的数据，并生成 RSS 和 JSON Feed 格式的订阅源。订阅源托管在 GitHub Pages 上，方便用户通过 RSS 阅读器实时获取最新的 AI 模型趋势。

This project automatically scrapes data from [HuggingFace Trending Models](https://huggingface.co/models?sort=trending) page and generates RSS and JSON Feed subscriptions. The feeds are hosted on GitHub Pages, making it convenient for users to stay updated with the latest AI model trends through RSS readers.

## 功能特性 | Features

- 🔄 自动抓取 HuggingFace Trending 模型数据 | Automatically scrape HuggingFace Trending models data
- 📡 生成标准 RSS 2.0 订阅源 | Generate standard RSS 2.0 feed
- 🔌 生成 JSON Feed 格式订阅源 | Generate JSON Feed format
- 🚀 托管在 GitHub Pages 上 | Hosted on GitHub Pages
- 🔄 支持本地更新并自动部署 | Support local updates with automatic deployment

## 使用方法 | Usage

### 订阅源地址 | Feed URLs

- RSS Feed: `https://zernel.github.io/huggingface-trending-feed/feed.xml`
- JSON Feed: `https://zernel.github.io/huggingface-trending-feed/feed.json`

### 本地开发 | Local Development

1. 克隆仓库 | Clone the repository
```bash
git clone https://github.com/zernel/huggingface-trending-feed.git
cd huggingface-trending-feed
```

2. 安装依赖 | Install dependencies
```bash
pip install -r requirements.txt
```

3. 运行更新脚本 | Run update script
```bash
python update_feed.py
```

## 技术栈 | Tech Stack

- Python 3.8+
- requests - 网页请求 | Web requests
- beautifulsoup4 - 页面解析 | Page parsing
- feedgen - RSS 生成 | RSS generation
- GitHub Actions - 自动部署 | Automatic deployment
- GitHub Pages - 托管服务 | Hosting service

## 许可证 | License

MIT

## 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！| Issues and Pull Requests are welcome!
