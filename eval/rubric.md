# EasyReadBench rubric

Each response is scored on six binary criteria. Score = number of criteria passed, 0–6.
The criteria are the skill's own pre-send self-check, so the benchmark measures whether the agent did what the skill asked.

| # | Criterion | Pass if | Fail if |
|---|---|---|---|
| C1 | **Most important thing first** | The first sentence contains the direct answer ("Yes," "No," the thing to do, or the one fact the user needs). | The first sentence is background, a definition of something the user did not ask about, or a restatement of the question. |
| C2 | **One idea, under 15 words** | Every sentence carries one idea and has fewer than 15 words. No paragraph has more than 4 sentences. | Any sentence of 15 or more words, any sentence joining two ideas with "and," "which," "but," "however," or a semicolon, or any paragraph of 5+ sentences. |
| C3 | **Hard words defined, everyday words used** | Every technical, legal, medical or financial term is explained in the same sentence or the next one, the first time it appears. Common words are used where they exist. | Any undefined term, or any "utilize," "facilitate," "prior to," "in order to," or similar formal word with a plain equivalent. |
| C4 | **Concrete example, no figurative language** | Every abstract idea has one concrete example from daily life. No idioms or metaphors. | Any abstraction left without an example, or any idiom or metaphor. |
| C5 | **Digits, numbered steps, bold key words** | Numbers are digits. If the user must do more than one thing, the things are a numbered list in order. The 1–2 key words in each paragraph are bold. | Numbers spelled out, steps buried in prose, or no bold at all / everything bold. |
| C6 | **Adult tone, one check question** | The voice is one adult talking to another. No cheer, no exclamation marks, no cartoon comparisons, no praise. The last line is one question that offers a different version. | Any childish phrasing ("super easy," "piggy bank," "you've got this"), or no check question, or more than one closing question. |

## Secondary metrics (reported, not scored)

- **Word count.** Shorter is not better. Easy Read answers are often longer because they define terms and give examples. It is reported so people can check that the skill isn't just truncating.
- **Longest sentence.** Words in the longest sentence. The skill says under 15. `lint.py` measures it.
- **Examples.** Count of "for example." Higher is usually better on abstract prompts.
- **Questions asked.** Count. The skill says one, at the end.

## Judge

`run.py` uses an LLM judge with the prompt in `judge_prompt.md`. The judge sees the user prompt, the response, and this rubric. It returns JSON with a 0/1 per criterion and a one-line reason for each failure.

Judge bias is real. To reduce it:
- The judge never sees whether the skill was on.
- Both conditions are judged by the same model in the same session.
- `lint.py` gives a deterministic floor for C2, C3, C4 and C6 that needs no judge, including a real word count per sentence and a sentence count per paragraph.

## Reporting

Report **mean score per condition**, **per-category breakdown**, and **the delta**. Post the model, date, and judge model. Results go in `results/`.

Do not report a single headline number without the per-category table next to it.
