# 🐾 AI小新 —— 桌面互动AI宠物

一个住在电脑桌面上的可爱AI宠物，基于 Python + Tkinter + Ollama 本地AI打造，支持**语音对话**（MOSS-TTS-Nano 音色克隆）。

> 运行 `python main.py`，桌面就会出现一只小新，可以拖动、点击、双击聊天，还能把聊天内容用真人音色朗读出来！

## ✨ 功能特性

- 🖱️ **桌面互动**：拖动、单击随机说话、双击打开聊天
- 🤖 **本地 AI 对话**：基于 Ollama 运行自定义模型 `xiaoxin`，完全离线
- 🔊 **文字转语音（TTS）**：聊天气泡旁一键播放语音，使用 MOSS-TTS-Nano 进行音色克隆（克隆 `蜂医新年快乐.wav` 的音色）
- ⚡ **语音缓存**：相同文本秒播，TTS 模型常驻内存无需重复加载
- 🎞️ **精灵图动画**：9 种状态动画（待机/走路/挥手/跳跃/开心/难过等）

---

## 📦 环境准备

### 1. 安装 Python

本项目需要 **Python 3.8 或以上版本**（推荐 Python 3.10+）。

打开终端（PowerShell 或 CMD），输入：

```bash
python --version
```

如果显示 `Python 3.x.x`（x ≥ 8），说明已安装。如果没有，请前往 [python.org](https://www.python.org/) 下载并安装。

> ⚠️ 安装时请务必勾选 **"Add Python to PATH"**，否则后续 `pip` 命令可能无法识别。

---

### 2. 安装项目依赖

进入项目目录，执行：

```bash
cd pet-ai
pip install -r requirements.txt
```

这会安装 `ollama` SDK、Pillow（图片加载）和 numpy（精灵图帧检测），三个都是必需的。

---

### 3. 安装并启动 Ollama

前往 [ollama.com](https://ollama.com/) 下载并安装 Ollama（Windows 版）。

安装完成后，打开终端，输入：

```bash
ollama --version
```

如果显示版本号，说明安装成功。

---

### 4. 下载基础模型

```bash
ollama pull qwen3:1.7b
```

> 首次下载需要一定时间，请耐心等待。qwen3:1.7b 约 1GB。

---

### 5. 使用 Modelfile 创建自定义模型

本项目已经为你准备好了 `Modelfile`，里面写好了小新的性格设定。

在终端中执行：

```bash
ollama create xiaoxin -f Modelfile
```

执行成功后，可以用以下命令测试小新：

```bash
ollama run xiaoxin
```

试试输入：`你好`、`你是谁？`、`你今天干嘛了？`

看到有趣回复后，输入 `/exit` 退出测试。

---

### 6. （可选）配置 TTS 语音合成

如果想让小新"开口说话"，需要准备 MOSS-TTS-Nano 环境：

**① 获取 MOSS-TTS-Nano**

> 注意：`MOSS-TTS-Nano-main/` 目录体积较大（含 ONNX 模型），不包含在本仓库中，需要单独下载：

```bash
git clone https://github.com/OpenMOSS/MOSS-TTS-Nano.git MOSS-TTS-Nano-main
```

将下载的目录放在项目根目录下。

**② 创建 conda 环境**

```bash
conda create -n moss-tts-nano python=3.12 -y
conda activate moss-tts-nano
cd MOSS-TTS-Nano-main
pip install -r requirements.txt
pip install -e .
```

> 环境名必须是 `moss-tts-nano`，程序会自动在常见 conda 安装路径下查找该环境。

**③ 确认 ONNX 模型文件**

程序使用 ONNX CPU 版本推理，模型应位于 `MOSS-TTS-Nano-main/models/` 目录下（`MOSS-TTS-Nano-100M-ONNX` 和 `MOSS-Audio-Tokenizer-Nano-ONNX`），缺失时首次运行会自动下载。

**④ 参考音频**

音色克隆使用项目根目录下的 `蜂医新年快乐.wav` 作为参考音频。可以替换成任意 5~10 秒的清晰人声 wav 文件，并同步修改 `tts_bridge.py` 中的 `REFERENCE_AUDIO` 路径。

> 💡 不配置 TTS 也能正常运行，只是聊天窗口不会显示语音播放按钮。

---

### 7. 运行桌面宠物

一切就绪后，在项目目录下运行：

```bash
python main.py
```

🎉 桌面上会出现一个 🧒 小新！

---

## 🖥️ 运行步骤总结（快速版）

```bash
# ① 安装依赖
pip install -r requirements.txt

# ② 下载基础模型
ollama pull qwen3:1.7b

# ③ 创建自定义模型
ollama create xiaoxin -f Modelfile

# ④ 测试模型（可选）
ollama run xiaoxin

# ⑤ 启动桌面宠物
python main.py
```

---

## 🎮 使用方法

| 操作 | 效果 |
|------|------|
| **鼠标拖动** | 把小新拖到桌面任意位置 |
| **单击小新** | 随机说一句话 |
| **双击小新** | 打开 AI 聊天窗口 |
| **点击气泡旁的 ▶** | 将该条消息转为语音播放（⏳ 合成中 → 🔊 播放中）|
| **右键小新** | 弹出菜单（聊天 / 说句话 / 换一句 / 关于 / 退出）|
| **关闭聊天窗口** | 小新继续留在桌面 |

> 🔊 语音按钮说明：首次点击需等待 10~40 秒（启动 TTS 子进程并加载模型），之后新文本几秒内完成，相同文本命中缓存即时播放。

---

## 📝 项目文件说明

```
pet-ai/
├── main.py                # 主程序（桌面宠物 + 聊天窗口 + 语音播放）
├── tts_bridge.py          # TTS 桥接子进程（MOSS-TTS-Nano 语音合成，由 main.py 自动启动）
├── Modelfile              # Ollama自定义模型配置文件
├── requirements.txt       # Python依赖清单
├── 蜂医新年快乐.wav        # TTS 音色克隆参考音频
├── README.md              # 本说明文档
├── .tts_cache/            # （运行时生成）语音缓存目录，可随时删除
├── MOSS-TTS-Nano-main/    # MOSS-TTS-Nano 模型与运行时（TTS 引擎）
└── assets/
    └── shinchan/          # 小新精灵图素材（sprite.webp）
```

---

## 🔊 TTS 工作原理（给初学者）

```
点击 ▶ 按钮
   ↓
main.py 的 TtsWorker 懒启动 tts_bridge.py 子进程（conda 环境 moss-tts-nano）
   ↓
MOSS-TTS-Nano (ONNX CPU) 常驻内存加载完成（约 12 秒）
   ↓
文字 + 参考音频（蜂医新年快乐.wav）→ 音色克隆合成 wav
   ↓
wav 缓存到 .tts_cache/（按文本 md5 命名），winsound 播放
```

主程序与 TTS 子进程通过 **stdin/stdout JSON 行协议**通信，互不阻塞，Ollama 对话与语音合成可以并行进行。

---

## 🔧 Modelfile 详解（给初学者）

`Modelfile` 是 Ollama 用来创建自定义模型的配置文件，类比"给模型写一份人设说明书"。

### FROM：基于哪个模型制作

```
FROM qwen3:1.7b
```
表示我们在 `qwen3:1.7b` 这个基础模型之上进行定制，不重新训练，只是改变它的说话风格。

### SYSTEM：告诉AI它是谁，以及应该怎么说话

```
SYSTEM """
你是住在用户电脑桌面上的可爱AI宠物小新。
...
"""
```
这段文字就是小新的"人设"，Ollama 会在每次对话时把这段文字作为背景提示发给模型。

### PARAMETER：调整模型运行参数

```
PARAMETER temperature 0.7
PARAMETER num_ctx 4096
```
- `temperature`：控制回答的"随机性"。0.2 = 很稳定，1.0 = 很天马行空。
- `num_ctx`：上下文长度，决定能记住多少对话内容。

---

## 🧪 课堂实践任务

### 实践1：改变小新性格

打开 `Modelfile`，把 SYSTEM 部分修改为：

```
你是是一只傲娇的猫咪。
```

保存后，重新执行：

```bash
ollama create xiaoxin -f Modelfile
```

再运行 `python main.py`，看看聊天效果有什么变化。

---

### 实践2：改变名字

把 Modelfile 和 `main.py` 中的 `"xiaoxin"` 改成其他名字，比如：

- `xiaodou`（小豆包）
- `xiaolan`（小蓝）
- `xiaobai`（小白）

记得同步修改 `MODEL_NAME` 变量，并重新创建模型。

---

### 实践3：改变语言风格

在 Modelfile 的 SYSTEM 中加入风格要求，例如：

```
每次回答最多两句话。
回答问题时偶尔使用emoji。
```

重新创建模型后测试效果。

---

### 实践4：改变 temperature

把 Modelfile 中的：

```
PARAMETER temperature 0.7
```

分别改为 `0.2` 和 `1.0`，每次改完后重新 `ollama create`，对比回答风格的变化。

---

## ⚠️ 常见错误解决方法

### 错误1："找不到 ollama 模块"
```
ModuleNotFoundError: No module named 'ollama'
```
**解决：** 执行 `pip install ollama`

---

### 错误2：Ollama 服务没有启动
```
ConnectionError: Cannot connect to host ...
```
**解决：** 确保 Ollama 正在运行。在终端执行：
```bash
ollama serve
```
（另开一个终端窗口运行，不要关闭）

---

### 错误3：找不到 xiaoxin 模型
```
error: model 'xiaoxin' not found
```
**解决：** 执行：
```bash
ollama create xiaoxin -f Modelfile
```

---

### 错误4： tkinter 窗口闪退
**解决：** 检查是否完整复制了所有代码，特别是 `if __name__ == "__main__":` 这一行不能漏。

---

### 错误5：Ollama 返回 "context length exceeded"
**解决：** 说明对话历史太长，超过了模型上下文限制。暂时清空聊天窗口重新开始即可。

---

### 错误6：点击 ▶ 长时间停在 ⏳，或变成 ⚠
**解决：** 说明 TTS 子进程启动/合成失败。查看项目目录下的 `.tts_cache/tts_stderr.log` 获取详细错误。常见原因：
- conda 环境 `moss-tts-nano` 不存在 → 参考「配置 TTS 语音合成」一节创建
- `MOSS-TTS-Nano-main/models/` 下缺少 ONNX 模型文件 → 在 conda 环境中运行一次 `python infer_onnx.py --text "测试"` 触发自动下载
- 参考音频 `蜂医新年快乐.wav` 被移动或删除 → 恢复文件或修改 `tts_bridge.py` 中的 `REFERENCE_AUDIO`

---

## 🗺️ 教学目标

学完这个项目，你应该能够：

1. 理解 **Ollama** 是什么，以及如何本地运行 AI 模型
2. 学会使用 **Modelfile** 定制自己的 AI 人格
3. 掌握用 **Python + Tkinter** 创建简单的桌面窗口
4. 了解如何用 Python 调用本地 AI 模型进行对话
5. 明白 AI 对话中的 **消息历史**（messages）是如何工作的
6. 能够在此基础上做出自己的 AI 桌面宠物！

---

## 📌 注意事项

- 本程序**不需要互联网**（Ollama 完全本地运行）
- 本程序**不修改 Windows 注册表**，不设置开机自启
- 聊天历史随窗口关闭而清空，不会保存到磁盘
- 第一版宠物使用 emoji 🧒 占位，后续可替换为真实 spritesheet

---

**祝你和小新玩得开心！** 🐾
