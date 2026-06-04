# 2026 世界杯预测 - 大模型对比分析

本项目记录各大AI模型对2026年FIFA世界杯小组出线结果的预测，并自动生成淘汰赛晋级图。

## 📊 项目目标

- 让多个大模型预测各小组 **第1名** 和 **第2名**
- 自动构建淘汰赛对阵并生成可视化晋级图
- 对比不同模型的预测差异

## 📁 数据结构

### 1. **比赛数据** (`matches/matches_sample.json`)

基于2026世界杯真实分组（48队，12组），含完整的72场小组赛对阵：

```json
{
  "tournament": "2026 FIFA World Cup",
  "group_stage": {
    "groups": {
      "A": {
        "group_name": "A组",
        "teams_display": ["墨西哥", "南非", "韩国", "捷克"],
        "matches": [...]
      },
      ...
    }
  }
}
```

### 2. **模型预测格式** (`predictions/[model_name].json`)

每个模型只预测 **每组第1名和第2名**：

```json
{
  "model_name": "GPT-4",
  "predictions": {
    "A": { "1st": "墨西哥", "2nd": "韩国" },
    "B": { "1st": "瑞士", "2nd": "加拿大" },
    "C": { "1st": "巴西", "2nd": "摩洛哥" },
    ...
  }
}
```

## 🔄 工作流程

### 第一步：准备提示词

打开 `prompts/prompt.md`，里面包含完整的12个分组球队名单和输出格式要求。

### 第二步：提交给大模型

把 `prompts/prompt.md` 的内容复制给不同的大模型（GPT-4、Claude、Gemini、DeepSeek 等）。模型会返回 JSON 格式的预测结果。

### 第三步：保存预测结果

将每个模型的返回结果保存为 `predictions/[模型名].json`，格式如上所示。

### 第四步：生成可视化

```bash
python3 show_predictions.py predictions/gpt4.json
```

脚本会自动：
- 解析各组第1/第2名
- 按球队实力补全8个成绩最好的小组第三
- 模拟淘汰赛32强→16强→8强→4强→决赛对阵
- 生成 HTML 晋级图仪表盘

打开 `predictions_dashboard.html` 查看结果。

## 🏆 2026世界杯分组（真实）

| 组别 | 球队 |
|------|------|
| A组 | 墨西哥、南非、韩国、捷克 |
| B组 | 加拿大、波黑、卡塔尔、瑞士 |
| C组 | 巴西、摩洛哥、海地、苏格兰 |
| D组 | 美国、巴拉圭、澳大利亚、土耳其 |
| E组 | 德国、库拉索、科特迪瓦、厄瓜多尔 |
| F组 | 荷兰、日本、瑞典、突尼斯 |
| G组 | 比利时、埃及、伊朗、新西兰 |
| H组 | 西班牙、佛得角、沙特阿拉伯、乌拉圭 |
| I组 | 法国、塞内加尔、伊拉克、挪威 |
| J组 | 阿根廷、阿尔及利亚、奥地利、约旦 |
| K组 | 葡萄牙、刚果民主共和国、乌兹别克斯坦、哥伦比亚 |
| L组 | 英格兰、克罗地亚、加纳、巴拿马 |

淘汰赛规则：每组前2名（24队）+ 8个成绩最好的小组第3 → 32强淘汰赛

## 📋 目录结构

```
├── README.md
├── prompts/
│   └── prompt.md              # 发给大模型的提示词
├── matches/
│   ├── matches_sample.json     # 分组数据
│   └── matches.json           # matches_sample的副本
├── predictions/
│   ├── gpt4.json              # 示例预测
│   └── gpt4_sample.json       # 旧格式示例
├── show_predictions.py        # 生成仪表盘脚本
├── generate_predictions.py    # 自动生成预测（实力评分法）
├── generate_matches.py        # 生成分组数据
└── predictions_dashboard.html # 生成的仪表盘
```

## 🎯 快速开始

1. **查看提示词** → `prompts/prompt.md`
2. **发给大模型** → 复制提示词内容给任意AI
3. **保存结果** → 存入 `predictions/[模型名].json`
4. **生成视图** → `python3 show_predictions.py predictions/[模型名].json`
5. **打开对比** → `predictions_dashboard.html`

---

*最后更新：2026年6月*
