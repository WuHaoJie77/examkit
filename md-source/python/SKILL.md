---
name: python-exam-prep
description: "Use when a user shares raw Python exam questions (from 超星/学习通 or similar platforms) and wants them condensed into a structured study guide with self-tests. Covers the full pipeline: receive raw questions → categorize by topic → produce condensed markdown with key points, trap tables, 15 self-test questions, answers with explanations, and a scoring rubric."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [python, exam-prep, study-guide, education, 超星, 学习通]
    related_skills: [pdf-design]
---

# Python Exam Prep — 题库浓缩技能

## Overview

Takes raw Python exam questions (typically from 超星/学习通 platforms), processes them into a structured, compact study guide. Each chapter guide follows a fixed 6-section format optimized for Chinese university students preparing for Python exams.

The output is a `.md` file saved to the user's Desktop, viewable in VS Code or any Markdown viewer.

## When to Use

- User pastes raw exam questions from 超星/学习通 or similar platforms
- User says "浓缩" / "整理题库" / "做速记卡" / "做复习资料"
- User sends questions in the format: `题号. (题型, 分值) 题干 + 选项`
- User wants a self-test section appended to an existing guide
- User explicitly mentions "Python题库" or "期末复习"

Do NOT use for:
- Questions in image/screenshot format (ask user to provide text)
- Non-Python subjects
- Single-question help (just answer directly)

## Fixed Output Format (6 Sections per Chapter)

Every chapter guide MUST include these sections in order:

### 1. Knowledge Condensation
- Group related questions into thematic modules
- **Each module MUST start with a 费曼例子 (Feynman example):** a 1-3 line analogy using everyday life that makes the abstract concept instantly intuitive. Use comparisons like: 变量=储物柜标签, 切片=切蛋糕, 循环=流水线, 函数=榨汁机, 列表=购物车, etc. The example goes BEFORE the technical content so the student "gets it" before seeing rules. A complete catalog of proven Feynman examples for all 13 chapters is in `references/feynman-catalog.md` — consult it first; invent new ones only for uncovered topics.
- Use markdown tables for quick reference
- Include code examples where applicable
- Prioritize rule tables over paragraph text

### 2. High-Frequency Trap Table
- One-line-per-trap format: `| 陷阱描述 | 正确答案 |`
- Extract the most commonly-missed questions from the batch
- Focus on "which is WRONG" / "which is CORRECT" type traps

### 3. Self-Test (15 Questions)
- Cover ALL modules in the chapter
- Mix question types: fill-in, code-output prediction, concept selection
- Each question tests a different knowledge point
- Format: number + stem + 4 options (A/B/C/D)

### 4. Answers with Explanations
- Table format: `| 题号 | 答案 | 解析 |`
- Each explanation states WHY the answer is correct
- For incorrect options, briefly explain why they're wrong

### 5. Scoring Rubric
- ≤3 wrong: can proceed to next chapter
- 3-6 wrong: re-read specific modules
- >6 wrong: re-read entire chapter

### 6. Memory Aids (where applicable)
- Mnemonics, comparison tables, or "one-sentence rules"
- E.g., "end不包含" for slicing, "append整体 extend拆开" for list methods

## Processing Workflow

### Step 1: Parse and Categorize
When questions arrive, silently:
1. Identify the chapter topic from question content
2. Group questions by sub-topic (e.g., "变量命名", "字符串切片", "分支结构")
3. Detect duplicate/near-duplicate questions and merge them
4. Assign a chapter number based on the content progression

### Step 2: Build Condensed Guide
1. Create the file at `Desktop/Python第X章_浓缩版.md`
2. Write all 6 sections using `write_file`
3. Use `patch` to append self-test section if doing it separately

### Step 3: Self-Test Generation Rules
- 15 questions, each covering a distinct topic
- Include at least 3 "code output prediction" questions
- Include at least 3 "which is WRONG/CORRECT" trap questions
- Include at least 2 "fill in the blank" questions
- Answer table must have `解析` column explaining reasoning
- Place self-test as the LAST major section before any appendices

## Key Design Principles

1. **Chinese-first:** All content in Chinese, code examples in English
2. **Table-heavy:** Student preference is for quick-reference tables, not paragraphs
3. **Trap-focused:** Each chapter's 最易错 points must be explicitly called out
4. **Self-contained:** Each chapter guide can be studied independently
5. **30-minute target:** Each chapter should take ~30 minutes to complete

## File Naming Convention

```
Desktop/Python第X章_浓缩版.md
```

Where X is the chapter number. Use Chinese numerals for consistency (第一章, 第二章, etc.).

## Common Chapter Topics (Reference)

| Chapter | Topic | Key Focus |
|---------|-------|-----------|
| 1 | 语言基础 | 发展史, Python特点, IDLE |
| 2 | 变量+切片 | 命名规则, 字符串切片基础 |
| 3 | 输入输出 | print/input/eval, 缩进, IPO |
| 4 | 数字类型 | 进制转换, 运算符, 内置函数 |
| 5 | 字符串深入 | 界定符, 切片步长, 字符串运算符 |
| 6 | 字符串方法 | find/count/split/join, is判断系列 |
| 7 | 关系逻辑 | 程序结构, 比较, and/or/not |
| 8 | 分支结构 | if/elif/else, 嵌套, 三元表达式 |
| 9 | for循环 | range, continue/break, for-else |
| 10 | while循环 | while True+break, 嵌套混用 |
| 11 | 列表基础 | 切片, sort/sorted/reverse |
| 12 | 列表增删改 | append/extend/insert/pop/remove/del |
| 13 | 函数基础 | def, return, 形参实参 |

## Common Pitfalls

1. **Answering questions individually instead of condensing.** The goal is a STUDY GUIDE, not an answer key. Merge similar questions, extract rules, don't answer one-by-one.

2. **Skipping the trap table.** This is the most valuable section for exam prep. Always include it.

3. **Making self-test questions too easy or too similar to original questions.** The self-test should test understanding, not memorization of the original questions.

4. **Forgetting the scoring rubric.** Every chapter must end with "错3题以内/错3-6题/错6题以上" guidance.

5. **Writing overly long explanations.** Each trap explanation should be one line. Each self-test explanation should be 1-2 sentences max.

6. **Not verifying answers.** For code-output questions, mentally trace the execution before writing the answer. Float precision, off-by-one, and immutable string traps are common.

## One-Shot Recipe

User says: "帮我浓缩这些Python题" and pastes a batch of questions.

1. Scan questions to identify chapter topic
2. Categorize into sub-topics
3. Write the full `Python第X章_浓缩版.md` to Desktop in one `write_file` call
4. If questions are too many (>100) or the user wants self-test separately, use `patch` to append
5. Report the file path, chapter number, and a 1-line summary of what each module covers
