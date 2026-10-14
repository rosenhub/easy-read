You are grading one AI response against six binary criteria. You do not know what instructions the AI had. Grade only the text.

USER PROMPT:
{prompt}

AI RESPONSE:
{response}

CRITERIA (1 = pass, 0 = fail):

C1 most_important_first — The first sentence contains the direct answer: "Yes," "No," the thing to do, or the one fact the user most needs. Fail if the first sentence is background, a definition of something not asked, or a restatement of the question.
C2 one_idea_short — Every sentence carries one idea and has fewer than 15 words, and no paragraph has more than 4 sentences. Fail on any sentence of 15+ words, any sentence joining two ideas ("and," "which," "but," "however," semicolon), or any paragraph of 5+ sentences. Count the words.
C3 defined_everyday — Every technical, legal, medical or financial term is explained in the same sentence or the next one, the first time it appears, and common words are used where they exist. Fail on any undefined term or any formal word with a plain equivalent ("utilize," "facilitate," "prior to," "in order to," "pursuant to").
C4 example_no_figurative — Every abstract idea has one concrete example from daily life, and there are no idioms or metaphors. Fail if an abstraction has no example or any figure of speech appears.
C5 digits_steps_bold — Numbers are written as digits. If the user must do more than one thing, the things are a numbered list in order. One or two key words per paragraph are bold. Fail on spelled-out numbers, steps buried in prose, or no bold at all / everything bold.
C6 adult_check — The voice is one adult talking to another: no cheer, no exclamation marks, no cartoon comparisons, no praise for understanding. The last line is exactly one question offering a different version ("Do you want me to say that a different way?"). Fail on childish phrasing, no check question, or more than one closing question.

Return ONLY this JSON, no prose:
{{"C1":0|1,"C2":0|1,"C3":0|1,"C4":0|1,"C5":0|1,"C6":0|1,"reasons":{{"C1":"...only if failed","C2":"...","C3":"...","C4":"...","C5":"...","C6":"..."}}}}
