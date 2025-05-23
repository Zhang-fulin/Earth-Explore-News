
# Earth-Explore-News

Earth-Explore-News 是一个自动化新闻提取与摘要项目，旨在从多个新闻网站获取最新新闻并使用大语言模型进行摘要处理。最终结果将被存储到 Supabase 数据库中，方便用户查看和分析。

## 项目依赖

在开始使用项目之前，确保已安装以下依赖项：

### 安装 Playwright
Playwright 是一个用于浏览器自动化的工具，用于抓取新闻内容。

```bash
pip install playwright
playwright install-deps
playwright install
```

### 安装 News-Please
News-Please 是一个用于从新闻网站提取文章内容的 Python 库。

```bash
pip install news-please
```

### 安装 OpenAI
此项目使用 OpenAI 的 API 来生成新闻摘要。

```bash
pip install openai
```

## 配置说明

1. 确保你已经配置了 Supabase 数据库，提供存储新闻数据的功能。
2. 使用 OpenAI API 获取新闻摘要，请确保你有 OpenAI API 密钥，并将其设置为环境变量。

## 用法

1. 运行 Playwright 安装，确保浏览器驱动正确安装。
2. 使用 `news-please` 提取新闻内容。
3. 调用 OpenAI API 生成摘要。
4. 将摘要结果存储到 Supabase 数据库中。

## 注意事项

- 请确保你的网络连接良好，以便顺利抓取新闻内容。
- 如果需要，可以根据实际需求调整新闻源。

## 许可证

此项目采用 MIT 许可证，详情请见 [LICENSE](LICENSE)。
