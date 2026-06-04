# 2026 世界杯预测 - 大模型对比分析

本项目记录各大AI模型对2026年FIFA世界杯比赛结果的预测，并与最终实际结果进行对比分析。

## 📊 项目目标

- 记录多个领先大模型的世界杯预测
- 对比不同模型的预测准确率
- 分析模型在不同赛段的表现差异

## 📁 数据结构

### 1. **比赛数据格式** (`matches/matches.json`)

```json
{
  "stage": "group",
  "matches": [
    {
      "match_id": "GRP_A_1",
      "round": "小组赛",
      "stage_name": "A组",
      "date": "2026-06-XX",
      "team_a": "国家A",
      "team_b": "国家B",
      "score_a": 2,
      "score_b": 1,
      "status": "completed",
      "actual_winner": "team_a"
    }
  ]
}
```

### 2. **模型预测数据格式** (`predictions/`)

单个模型预测文件结构 (`predictions/[model_name].json`):

```json
{
  "model_name": "GPT-4",
  "model_version": "20250601",
  "prediction_date": "2026-05-20",
  "predictions": [
    {
      "match_id": "GRP_A_1",
      "predicted_winner": "team_a",
      "predicted_score_a": 2,
      "predicted_score_b": 0,
      "confidence": 0.85
    }
  ]
}
```

### 3. **预测结果统计** (`results/evaluation.json`)

```json
{
  "evaluation_period": "2026 FIFA World Cup",
  "models": [
    {
      "model_name": "GPT-4",
      "total_predictions": 64,
      "correct_predictions": 48,
      "accuracy_rate": 0.75,
      "stage_breakdown": {
        "group_stage": {
          "total": 48,
          "correct": 38,
          "accuracy": 0.792
        },
        "knockout": {
          "total": 16,
          "correct": 10,
          "accuracy": 0.625
        }
      },
      "comparison": {
        "accuracy_vs_model_2": "+5%",
        "ranking": 1
      }
    }
  ],
  "overall_ranking": [
    {
      "rank": 1,
      "model_name": "GPT-4",
      "accuracy": 0.75
    }
  ]
}
```

## 🔄 工作流程

### 第一步：准备比赛清单
- 创建完整的64场比赛数据（小组赛48场 + 淘汰赛16场）
- 记录每场比赛的基本信息（对阵队伍、时间等）

### 第二步：提交给大模型
为每个模型创建统一的提示词模板，例如：

```
请根据球队的历史成绩、球员阵容、伤病情况等因素，预测以下2026年世界杯比赛的结果：

[比赛列表]

请以JSON格式返回你的预测，包括每场比赛的预测胜者和预测比分。
```

### 第三步：收集预测结果
- 将各模型的预测结果保存到 `predictions/` 目录
- 格式统一为上述JSON格式

### 第四步：统计分析
- 比赛结束后，更新比赛实际结果
- 运行评估脚本计算每个模型的准确率
- 生成对比报告

## 📈 评估指标

| 指标 | 说明 |
|------|------|
| **准确率** | 预测正确的比赛数 / 总比赛数 |
| **阶段精度** | 分别统计小组赛和淘汰赛的准确率 |
| **比分准确率** | 预测比分完全正确的占比 |
| **晋级预测** | 球队最终晋级情况的预测准确率 |

## 📋 目录结构

```
├── README.md
├── matches/
│   └── matches.json           # 完整的64场比赛数据
├── predictions/
│   ├── gpt4.json             # GPT-4的预测
│   ├── claude.json           # Claude的预测
│   ├── gemini.json           # Gemini的预测
│   └── deepseek.json         # DeepSeek的预测
├── results/
│   ├── evaluation.json       # 整体评估结果
│   ├── model_comparison.md   # 对比分析报告
│   └── detailed_analysis/    # 详细分析（可选）
└── scripts/
    └── evaluate.py           # 评估计算脚本（可选）
```

## 🎯 快速开始

1. **初始化比赛数据** → 创建 `matches/matches.json`
2. **准备提示词** → 设计统一的提示词模板
3. **收集预测** → 将各模型预测保存到 `predictions/`
4. **输入实际结果** → 完赛后更新 `matches/matches.json` 中的实际结果
5. **生成报告** → 运行评估生成结果统计

## 📝 示例数据

参考 `examples/` 目录获取样例JSON文件

---

*最后更新：2026年5月*
