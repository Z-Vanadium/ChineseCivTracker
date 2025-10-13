# ChineseCivTracker 项目简介

## 项目概述

ChineseCivTracker 是一个专为中国《文明VI》CCB 模组 PVP 社区设计的对局数据统计与分析平台。项目旨在系统性地收集、整理和分析中国玩家社群的游戏数据，为社区发展、战术研究和平衡性讨论提供数据支持。

## 核心功能

### 数据收集模块

数据收集由 [CCB 多人游戏助手](https://steamcommunity.com/sharedfiles/filedetails/?id=3556319230) 负责，在每局游戏结束后自动向服务器发送对局信息。

数据收集范围包括

- 模组版本
  - CCB、CCB 地图、CCB 扩展、CCB 多人游戏助手
  - 其他附加模组
- 地图类型
- 玩家 ID 
- 领袖选择
- 游戏回合数
- 关键时间点

### 数据分析模块

[TBD]

## 技术架构

### 数据流程架构

```
文明VI游戏 → Lua Mod收集 → HTTP GET请求 → Flask API接收 → 数据处理 → 数据库存储 → 数据分析展示
```

### 技术栈

#### 游戏端

- Lua

#### 服务器端

- 数据收集：Python Flask

- 数据处理：Python Numpy

#### 数据储存

- SQLite

#### 数据查询

- 提供 API 接口