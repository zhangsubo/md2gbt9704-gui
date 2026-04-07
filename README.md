# md2gbt9704 GUI

按照 GB/T 9704-2012（党政机关公文格式）标准将 Markdown 转换为 DOCX 的图形化工具，支持格式检查和标准化。

## 功能特性

### 1. Markdown → DOCX 转换
- 将 Markdown 文档按照 GB/T 9704-2012 标准转换为标准公文格式
- 自动识别标题层级（一、/（一）/ 1. /（1））
- 自动处理落款格式（单位名称和日期右对齐）
- 自动生成符合标准的页码格式

### 2. DOCX 格式检查
- 检查页面设置（A4、边距）
- 检查字体规范
- 检查标题层级
- 检查正文格式（行距、加粗等）
- 检查表格格式
- 生成详细的检查报告

### 3. DOCX 格式标准化
- 自动格式化 Word 文档为标准公文格式
- 统一页面设置
- 统一字体和字号
- 统一标题格式
- 添加标准页码

### 4. 设置中心
- 页边距自定义配置
- 字体自定义配置
- 预设管理（GB/T 9704-2012 / 国家行政机关公文格式）
- 配置持久化保存

## 安装

### 依赖

- Python 3.8+
- PySide6 >= 6.6.0
- python-docx >= 1.1.0

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/zhangsubo/md2gbt9704-gui.git
cd md2gbt9704-gui
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 运行程序
```bash
python main.py
```

## 系统要求

### Windows
- Windows 10/11 (x64)

### macOS
- macOS 11+ (Intel & Apple Silicon)

## 字体要求

系统需安装以下中文字体：

| 字体 | Windows | macOS |
|------|---------|-------|
| 方正小标宋简体 | 方正小标宋简体 | 方正小标宋简体 |
| 仿宋 | 仿宋_GB2312 | 仿宋 |
| 黑体 | 黑体 | STHeiti |
| 楷体 | 楷体_GB2312 | 楷体 |

> 注意：缺少字体时会自动回退到系统可用字体

## GB/T 9704-2012 标准规格

| 项目 | 规格 |
|------|------|
| 纸张 | A4 |
| 上边距 | 37mm |
| 下边距 | 35mm |
| 左边距 | 27mm |
| 右边距 | 27mm |
| 行间距 | 固定值 28 磅 |

## 字体规范

| 元素 | 字体 | 字号 | 加粗 |
|------|------|------|------|
| 主标题 | 方正小标宋简体 | 2号（22pt） | 否 |
| 一级标题（一、） | 黑体 | 3号（16pt） | 是 |
| 二级标题（（一）） | 楷体 | 3号（16pt） | 是 |
| 三级标题（1.） | 仿宋 | 3号（16pt） | 是 |
| 四级标题（（1）） | 仿宋 | 3号（16pt） | 否 |
| 正文 | 仿宋 | 3号（16pt） | 否 |
| 表头 | 仿宋 | 小四号（12pt） | 是 |

## 项目结构

```
md2gbt9704-gui/
├── main.py                      # 应用入口
├── gui/
│   ├── __init__.py
│   ├── main_window.py           # 主窗口
│   ├── settings_widget.py       # 设置组件
│   ├── theme.py                 # 主题配置
│   └── widgets/
│       ├── __init__.py
│       ├── file_drop.py         # 文件拖拽组件
│       ├── preview.py           # 预览组件
│       └── report.py            # 报告组件
├── converter/
│   ├── __init__.py
│   ├── config.py                # 配置管理
│   ├── fonts.py                 # 字体检测
│   ├── md2docx.py               # Markdown转DOCX
│   ├── checker.py               # 格式检查器
│   └── formatter.py             # 格式标准化
├── utils/
│   └── fonts.py                 # 工具函数
├── requirements.txt
└── README.md
```

## 使用方法

### 方式一：命令行
```bash
# MD转DOCX
python -m converter.md2docx input.md [output.docx]

# 格式检查
python -m converter.checker input.docx

# 格式标准化
python -m converter.formatter input.docx [output.docx]
```

### 方式二：图形界面
```bash
python main.py
```

## 打包分发

### Windows
```bash
pip install pyinstaller
pyinstaller --name="md2gbt9704" --onefile main.py
```

### macOS
```bash
pip install pyinstaller
pyinstaller --name="md2gbt9704" --onefile --osx-bundle-identifier="com.md2gbt9704" main.py
```

## 许可证

MIT License

## 作者

张小璋
