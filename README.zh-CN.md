<div align="center">

# easy-read

### 让你的 AI 用易读体写作。

**为智力和发展障碍成人设计。对所有人更好。**

12 条规则。0 行代码。支持 16 个代理宿主。10 秒安装。

[English](README.md) · [安装](#安装) · [12 条规则](#12-条规则)

```bash
npx skills add rosenhub/easy-read
```

<img src="assets/before-after.png" width="100%" alt="before / after">

</div>

---

智力和发展障碍成人用的聊天机器人和所有人一样。那个机器人写得像律师：一句话 30 个词、塞进三个意思；"利用""促进""为了""在此之前"；一个术语用四次、一次也不解释；抽象概念没有一个生活里的例子；步骤埋在段落里而不是按顺序列出来。你要求简单一点，它就换成卡通腔："把它想成一个魔法存钱罐！"

这不是智力障碍的问题，是写作的问题。把写作改好，每个人都能第一次读就照着做。

易读体（Easy Read）是一个成熟的标准。英国和欧盟的自我倡导组织几十年来一直用它写政府表格、健康手册和投票指南。本技能遵循其中的写作部分，不是认证。

## 安装

把 `SKILL.md` 复制到你的宿主对应位置（完整表格见 [English README](README.md#install)）：

| 宿主 | 位置 |
|---|---|
| Claude Code | `~/.claude/skills/easy-read/SKILL.md` |
| Codex CLI | 追加到 `AGENTS.md` |
| Cursor | `.cursor/rules/easy-read.mdc` |
| Gemini CLI | 追加到 `GEMINI.md` |
| OpenClaw | `~/.openclaw/skills/easy-read/SKILL.md` |
| ChatGPT | 设置 → 个性化 → 自定义指令 |

或者：`curl -fsSL https://raw.githubusercontent.com/rosenhub/easy-read/main/install.sh | sh`

## 12 条规则

| # | 规则 |
|---|---|
| 1 | 一句话只说一个意思。 |
| 2 | 每句少于 15 个词。 |
| 3 | 用日常词汇。"用"而不是"利用"。 |
| 4 | 每个难词在出现的地方就解释。 |
| 5 | 每个概念配一个具体例子。 |
| 6 | 数字用阿拉伯数字，不用汉字。 |
| 7 | 步骤用编号列表，按顺序。 |
| 8 | 最重要的事放第一句。 |
| 9 | 每段的关键词加粗。 |
| 10 | 不用习语和比喻。 |
| 11 | 简单不等于幼稚。永远用成人的语气。 |
| 12 | 结尾只问一个确认问题："要我换一种说法吗？" |

完整内容：[SKILL.md](SKILL.md)。基准测试：[eval/](eval/)。

## 许可

MIT。
