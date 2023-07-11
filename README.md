# **Core-Service**

## 简介

这是一个基于 LangChain 的核心服务器，目的在于连接 SQL 以及 Milvus 数据库，同时获取用户信息，搜索数据库、调用大模型等。
项目基于 Django 框架，计划支持 logging 的日志记录（待完成），后续加入 Agent 代理功能

## 开发思考

一个与模型的交流分别包括什么参数？  
参数提供包括两端，用户端和开发者端  
用户端的参数传入，开发者端的参数扔到 config 里

- 用户端（可能需要）的参数：
  - 提示词
  - 模型选择
    - 大模型选择
    - 子模型选择
  - 是否需要多轮对话
  - 数据库选择
- 开发端的参数：
  - 用户端所有参数的默认
  - 模型选择
  - 数据库索引方法、tokens 之类的...
  - 多轮对话记录方法
  - 嵌入方法
  - 数据库用什么

设计模式上的问题：

- 对话模块和检索模块需不需要融合？
- 聊天数据应该存在前端还是 Server 还是服务器？

## TASKs 推进

- [x] 正常对话
  - [x] 普通对话
  - [x] 多轮对话
- [ ] 提示词添加
- [ ] logging 添加
- [x] Milvus 数据库上传 (待测试)
  - [ ] TXT
  - [ ] PDF
  - [ ] CSV
- [ ] 连接 MySQL 数据库
- [x] Postgres 数据库测试
  - [x] TXT
  - [ ] PDF (待测试)
  - [ ] CSV (待测试)
- [x] Postgres 数据库测试
  - [x] 支持多轮搜索
- [ ] 调用搜索引擎查询

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
