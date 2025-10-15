# AI-Chat-Engine README

## 项目介绍

`AI-Chat-Engine` 是一个基于 Python 开发的人工智能对话引擎应用，旨在提供便捷、可扩展的 AI 聊天交互体验。该项目支持多线程聊天处理、自定义 UI 组件以及样式定制，可用于构建个性化的 AI 聊天应用程序。


## 功能特点

- **多线程聊天**：通过 `chat_thread.py` 实现聊天过程的多线程处理，保障交互响应的流畅性。
- **自定义 UI 组件**：`ui_components.py` 提供可复用的界面组件，便于快速构建聊天界面。
- **样式可定制**：通过 `styles.qss` 支持 Qt 样式表定制，满足不同视觉风格需求。
- **一键打包**：借助 `main.spec` 可快速将应用打包为可执行程序，方便分发使用。


## 技术栈

- 主要语言：Python (90.2%)
- 打包工具：Inno Setup (9.8%)
- 界面框架：基于 Qt 技术栈构建 UI 交互
- 多线程：Python 原生线程库支持异步聊天处理


## 快速开始

### 环境依赖

- Python 3.8+
- PyQt5（用于 UI 渲染）
- 可选：PyInstaller（用于打包应用）

### 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/[你的用户名]/AI-Chat-Engine.git
   cd AI-Chat-Engine
   ```

2. 安装依赖：
   ```bash
   pip install PyQt5
   ```

3. 运行应用：
   ```bash
   python main.py
   ```

### 打包应用

若需将应用打包为可执行文件，可使用 PyInstaller：
```bash
pyinstaller main.spec
```


## 项目结构

```
AI-Chat-Engine/
├── main.py               # 应用入口
├── chat_app.py           # 聊天应用核心逻辑
├── chat_thread.py        # 多线程聊天处理
├── ui_components.py      # UI 组件定义
├── styles.qss            # 样式表文件
├── main.spec             # PyInstaller 打包配置
├── XAliss/               # （可选）相关资源或模块目录
└── README.md             # 项目说明文档
```


## 贡献指南

欢迎对本项目提出改进建议或提交代码贡献：
1. Fork 本仓库
2. 创建特性分支（`git checkout -b feature/your-feature`）
3. 提交修改（`git commit -m 'Add some feature'`）
4. 推送到分支（`git push origin feature/your-feature`）
5. 发起 Pull Request


## 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)，详情请查看 `LICENSE` 文件（若存在）。
