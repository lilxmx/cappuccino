<div align="center">
<h1><span style="font-size: 60px;">☕️</span> 卡布奇诺</h1>
<p>中文 | <a href="./README.md">English</a></p>
<p>一个解放你双手的本地自动化智能体 🤖</p>
<p>放心将任务交予我，去静享一杯醇香的卡布奇诺 ☕️</p>
<p>待你悠然归来，任务早已悄然完成 🍃</p>
</div>

## 💡 概述

**卡布奇诺**是一个能操控电脑帮你解决繁琐任务的 GUI Agent，只需一条简单的指令，AI 就能生成详细的任务规划并执行。与解析图片元素或使用浏览器接口的其他现有方案不同，**卡布奇诺**是基于桌面屏幕的纯视觉方案，因为我们觉得解析过程容易丢失空间关联信息。

你可以直接使用 API 调用 LLM 快速上手，也可以在本地服务器上部署 LLM 以获得更高的安全性。通过 python 脚本或可视化界面 🖥️ [cappuccino-client](https://github.com/GML-FMGroup/cappuccino-client) 发送操控指令。

## ✨ 特点

- **本地部署：** 本方案架构的各个部分均提供开源模型的选择方便进行本地部署，信息传输均通过本地局域网进行，保护您的隐私。
- **快速上手：** 我们提供了基于 React 构建的 GUI 客户端用于操控 Agent，小白友好。
- **可拓展性：** 当前架构支持添加更多的执行器以拓展 Agent 的能力。

## 🤔 未来计划

我们将支持更多模型，优化 Agent 的性能，并致力于开发我们自己的小参数 LLM 用来降低部署成本、提高运行速度。

希望有更多的人关注我们的项目或加入我们，我们也会进一步丰富我们的系统，打造可用于本地部署的类 Manus 产品，适配更多的软件操作。

你的 star🌟 是我们更新的最大动力！

<img src="./assets/cappuccino_group.png" alt="cappuccino_group" width="20%">

>欢迎大家进我们的社区交流群，参与项目的共建或交流。

## 📰 更新

- **[2025/03/19]** 🧠 升级了系统架构以支持更复杂的任务。
- **[2025/03/09]** 🖥️ 我们开发了 GUI 客户端 cappuccino-client，以便更轻松地发送命令。
- **[2025/03/04]** 💥 已支持 Deepseek-v3 作为规划器。
- **[2025/02/27]** 🏆 现在你可以使用 qwen 和 gpt-4o 体验 cappuccino。

## 🎥 演示

https://github.com/user-attachments/assets/18b6013a-6d45-44d3-bd09-b0b08e0cd2c8

## 👨‍💻 快速开始

### 0. 硬件准备

目前该项目支持部署在 Windows 和 Mac，由于系统的快捷键和操作方式等差异，不同系统的体验可能会有区别，我们后续还会进行更多的系统适配。

### 1. 模型部署

本项目支持使用供应商的 API 或本地部署 LLM。若您需要本地部署，请使用 OpenAI 兼容的 API 服务，我们推荐使用 vLLM 进行部署，具体可以参考 [官网教程](https://qwen.readthedocs.io/zh-cn/latest/deployment/vllm.html#openai-compatible-api-service) 。

模型选择上，我们推荐使用 deepseek-v3 作为规划器，qwen-vl-max 作为分发器&校验器，qwen2.5-vl-7b 作为执行器。

### 2. 服务端配置与启动

以下操作在需要被控制的计算机上执行。

#### 2.1 克隆仓库

```bash
git clone https://github.com/GML-FMGroup/cappuccino.git
cd cappuccino
```

#### 2.2 安装依赖

```bash
pip install -r requirements.txt
```

#### 2.3 启动服务

```bash
cd app
python server.py
```
你将在控制台中看到你的 **本地 IP** 和随机生成的 **token**。下面的例子中 IP 为 192.168.0.100
```bash
Generated token: 854616
Chat WebSocket: ws://192.168.0.100:8000/chat
Screenshots WebSocket: ws://192.168.0.100:8001/screenshots
```

### 3. 发送指令

在另一台设备上运行以发起网络请求。当然，你也可以在被控制的终端上运行，但我们的设计理念是使用另一台设备发送指令，以避免影响计算机的操作执行。

#### 方法 1：Python 脚本

1. 修改 `request_demo.py` 中的 IP 和 token。例如，IP 为 192.168.0.100。
2. 填写 LLM 配置信息，如 API Key、供应商等。
3. 运行 Python 文件。
```bash
python request_demo.py
```

#### 方法 2：GUI 客户端

你可以在 🖥️ [cappuccino-client](https://github.com/GML-FMGroup/cappuccino-client) 中找到更详细的 GUI 客户端使用教程。

## 📖 指南

### 设计架构

我们将 **卡布奇诺** 分为三个部分：**模型、服务端、客户端**。

- **模型：** 你可以选择使用 dashscope、openai 等供应商，或者更安全的本地部署。
- **服务端：** GUI Agent，部署在被控制的计算机上，启用 websocket 网络服务以接收来自局域网的指令，并结合桌面截图与模型交互，使模型能够输出执行指令或计划。
- **客户端：** 用于通过 GUI 界面或 Python 脚本向服务器发送人类指令。

对于 GUI Agent 的设计，我们主要将其分为四部分：**🧠规划器、🤖分发器、✍️执行器、🔍校验器**。

- 🧠**规划器：** 将用户的复杂指令分解为多个任务，便于逐步执行。
- 🤖**分发器：** 结合桌面屏幕和执行器的功能，将任务拆解为多个子任务并分配给对应的执行器，每个子任务都是一个原子操作（人类操控电脑的最小动作单位，如：点击xx，输入xx）
- ✍️**执行器：** 结合桌面屏幕，基于原子操作生成可用于脚本执行的参数。
- 🔍**校验器：** 根据桌面屏幕判断是否完成了对应的任务。

### 支持的模型

| 规划器 - API       | 规划器 - 本地      | 分发器 & 校验器 - API    | 分发器 & 校验器 - 本地   | 执行器 - API        | 执行器 - 本地        |
|-------------------|------------------|------------------------|-----------------------|--------------------|---------------------|
| qwen-vl-max       | deepseek-v3      | qwen-vl-max            | qwen2.5-vl-72b        | qwen2.5-vl-7b      | qwen2.5-vl-7b       |
| gpt-4o            |                  | gpt-4o                 |                       |                    |                     |
| deepseek-v3       |                  |                        |                       |                    |                     |

### ⚠️ 注意事项

- 选择模型时，请确保名称正确且供应商支持该模型。
- 我们当前的接口基于 openai 库实现。请确保供应商或本地部署支持提供的模型。
- 由于模型输出带有不稳定性，若运行失败，可尝试再次运行或修改问题。
