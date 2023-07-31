# **Core-Service**

## 简介

这是一个基于 LangChain 的核心服务器，目的在于连接 SQL 以及 Milvus 数据库，同时获取用户信息，搜索数据库、调用大模型等。
项目基于 Flask 框架，计划支持 logging 的日志记录（待完成），后续加入 Agent 代理功能.

## 安装方式

克隆此仓库后，需要配置config以及环境变量，随后可以使用Docker compose部署。

### 配置config

进入config路径下，选择自己所要使用的config, 进行配置。如果仅为测试，推荐使用 ```config_test.yml```。

### 配置环境

复制 ```.env_copy``` 位 ```.env```, 填写```OPENAI_API_KEY```以及在```FLASK_ENV=```中填写刚才刚才config对应的环境： test, dev, 或 pro。

### Docker Compose安装 

检查环境中是否有docker compoer：
```bash
docker compose version
```

如果没有，请下载docker compose安装。这里给出Ubuntu的安装方法  
```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

其他环境请查看详细教程[docker-compose 官方文档](https://docs.docker.com/compose/install/linux/)


### 运行Docker环境
直接运行sh脚本
```bash
sudo ./build.sh
```
或者运行
```bash
docker-compose build
docker-compose up
```

## 任务推进

- [x] 正常对话
  - [x] 普通对话
  - [x] 多轮对话
- [ ] 提示词添加
- [ ] 敏感词添加
- [x] 商讨 Agent 问题
- [x] logging 添加
- [x] Milvus 数据库上传 **此功能非最终版本，待完善**
  - [ ] TXT
  - [ ] PDF
  - [ ] CSV
- [ ] 连接 MySQL 数据库 
- [x] milvus 数据库测试 **此功能非最终版本，待完善**
  - [x] 支持多轮搜索
- [ ] 调用搜索引擎查询
- [x] Splitter 三种不同方式（待测试）
- [x] util更新
- [x] config重构
- [x] Docker部署
- [x] AWS测试

## APIS

### Chat API

端点:  
**POST /chat**

描述：
该 API 端点支持与 AI 模型进行对话。它接受一个带有对话历史记录、待提问的查询和其他详细信息的 JSON 载荷。返回的是 AI 的回复（字符串）以及更新的对话历史记录。

请求体：

- API 期待在 HTTP 请求体中收到一个带有以下属性的 JSON 对象：

- query（字符串，必需）：要发送给 AI 的消息或问题。

- model_name（字符串，可选）：用于生成回复的 AI 模型的名称，例如"OpenAI"。

- history（数组，可选）：对话历史记录对象的数组。每个对象都有一个 type 属性，可以是"human"或"ai"，以及一个 data 属性，包含另一个对象，该对象有一个 content 属性，包含消息文本。如果未提供此属性或是一个空数组，则假设对话从头开始。例如：

```json
{
  "history": [
    {
      "type": "human",
      "data": {
        "content": "你叫什么名字？"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "我是由OpenAI开发的AI模型。"
      }
    }
  ]
}
```

- with_memory（布尔值，可选）：在生成回复时是否要考虑对话历史记录。如果未提供，默认为 false。

响应：
API 返回一个带有以下属性的 JSON 对象：

- reply（字符串）：AI 对查询的回复。
- history（数组）：更新的对话历史记录对象数组，包括最新的查询和回复。

示例：
以下是一个请求示例：

```json
{
  "query": "今天的天气如何？",
  "model_name": "OpenAI",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "你叫什么名字？"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "我是由OpenAI开发的AI模型。"
      }
    }
  ],
  "with_memory": true
}
```

以及一个响应示例：

```json
{
  "reply": "很抱歉，作为AI，我没有实时功能来提供当前的天气。",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "你叫什么名字？"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "我是由OpenAI开发的AI模型。"
      }
    },
    {
      "type": "human",
      "data": {
        "content": "今天的天气如何？"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "很抱歉，作为AI，我没有实时功能来提供当前的天气。"
      }
    }
  ]
}
```

### Query View API

端点:  
**POST /query**

描述：  
该 API 端点用于处理和响应与 AI 对话系统的交互请求。它接受一个带有待提问的查询、AI 模型的名称、对话历史记录、记忆开关、数据库开关以及集合名称的 JSON 载荷。返回的是 AI 的回复或者错误信息。

当 with_database 为真时，系统将调用 search 函数。这个函数将在 Milvus 数据库的指定集合中进行搜索并生成响应。在这种情况下，集合名称 collection_name 是必需的。当 with_database 为假时，系统将简单地进行一次对话，并不涉及数据库搜索。

请求体：

API 期待在 HTTP 请求体中收到一个带有以下属性的 JSON 对象：

- query（字符串，必需）：要发送给 AI 的消息或问题。

- model_name（字符串，可选）：用于生成回复的 AI 模型的名称，例如"OpenAI"。

- history（数组，可选）：对话历史记录对象的数组，参考上文的历史数组格式。

- with_memory（布尔值，可选）：在生成回复时是否要考虑对话历史记录。如果未提供，默认为 false。

- with_database（布尔值，可选）：是否需要在数据库中查找对应的集合来生成回复。如果未提供，默认为 false。

- collection_name（字符串，可选）：如果使用数据库，此为需要查询的集合名称。

错误：  
如果出现错误，API 会返回一个包含错误信息的 JSON 对象。

示例：  
以下是一个请求示例：

```json
{
  "query": "今天的天气如何？",
  "model_name": "OpenAI",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "你叫什么名字？"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "我是由OpenAI开发的AI模型。"
      }
    }
  ],
  "with_memory": true,
  "with_database": true,
  "collection_name": "weather_collection"
}
```

正确响应示例：

```json
{
  "reply": "今天的天气是晴朗，温度约为27摄氏度。",
  "history": [
    {
      "type": "human",
      "data": {
        "content": "你叫什么名字？"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "我是由OpenAI开发的AI模型。"
      }
    },
    {
      "type": "human",
      "data": {
        "content": "今天的天气如何？"
      }
    },
    {
      "type": "ai",
      "data": {
        "content": "今天的天气是晴朗，温度约为27摄氏度。"
      }
    }
  ]
}
```

错误响应示例：

```json
{
  "error": "数据库中找不到名为'weather_collection'的集合。"
}
```

### File Upload API

端点:  
**POST /upload**

描述：

该 API 端点支持文件上传。它接收一个带有文件和集合名称的 POST 请求。文件通过前端使用 formData 发送。返回结果是 JSON 格式，表示上传结果的状态和相关信息。

请求体：
API 期待在 HTTP POST 请求中接收以下参数：

- file（文件，必需）：要上传的文件。
- collection_name（字符串，必需）：文件需要上传到的集合名称。

响应：
API 返回一个 JSON 对象，包含以下属性：

- result（字符串）：上传操作的结果状态，例如："success"。

- message（字符串，可选）：关于上传结果的额外消息，例如上传失败时的错误信息。这个字段可能在 result 为"success"时不出现。

- error（字符串，可选）：如果上传过程中出现错误，此字段会包含错误信息。

示例：
以下是一个可能的响应示例：

```json
{
  "result": "success"
}
```

以及一个发生错误时的响应示例：

```json
{
  "error": "文件大小超过限制"
}
```
