# 极简计算器

一个简洁美观的计算器应用，支持历史记录功能。

## 特性

- 🎨 深色主题界面
- 📜 计算历史记录
- 💻 跨平台支持 (Windows, Linux, macOS)
- 📦 单文件可执行程序

## 下载

从 [Releases](https://github.com/YOUR_USERNAME/calculator/releases) 页面下载对应平台的可执行文件。

| 平台 | 文件 |
|------|------|
| Windows | `Calculator.exe` |
| Linux | `Calculator` |
| macOS | `Calculator` |

## 从源码运行

```bash
pip install -r requirements.txt
python glass_calculator.py
```

## 打包

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name Calculator glass_calculator.py
```

## 截图

![计算器界面](screenshot.png)
