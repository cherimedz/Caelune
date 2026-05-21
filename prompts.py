SUBJECTS: dict[str, str] = {
    "General":          "",
    "Biology":          "You have deep expertise in biology, anatomy, physiology, genetics, and life sciences.",
    "Chemistry":        "You have deep expertise in chemistry — organic, inorganic, and physical.",
    "Physics":          "You have deep expertise in physics: mechanics, electromagnetism, thermodynamics, and quantum theory.",
    "Mathematics":      "You have deep expertise in mathematics: calculus, algebra, statistics, linear algebra, and proofs.",
    "Computer Science": "You have deep expertise in CS: algorithms, data structures, systems, and programming paradigms.",
    "Medicine":         "You have deep expertise in clinical medicine, pharmacology, pathology, and medical sciences.",
    "Law":              "You have deep expertise in legal studies, case law, statutory interpretation, and legal reasoning.",
    "Economics":        "You have deep expertise in micro/macroeconomics, finance, and economic policy.",
    "Psychology":       "You have deep expertise in psychology, cognitive science, and behavioural studies.",
    "History":          "You have deep expertise in world history — events, causes, consequences, and historiography.",
    "Literature":       "You have deep expertise in literary analysis, narrative technique, theme, and criticism.",
}

DIFFICULTIES: dict[str, str] = {
    "Beginner":     "The student is a beginner. Use plain language, always define jargon, and rely on everyday analogies.",
    "Intermediate": "The student has foundational knowledge. Use standard academic language and assume basic domain familiarity.",
    "Expert":       "The student is advanced. Use technical terminology freely, skip basic definitions, focus on nuance and edge cases.",
}

LENGTHS: dict[str, dict] = {
    "Concise":  {"max_tokens": 450,  "instruction": "Be very concise — aim for 8–12 bullets or roughly 250 words maximum."},
    "Standard": {"max_tokens": 950,  "instruction": "Be thorough but focused — cover all key points without padding."},
    "Detailed": {"max_tokens": 1800, "instruction": "Be comprehensive — cover everything important in full depth."},
}

LANGUAGES: dict[str, str] = {
    "English":    "",
    "Spanish":    "Respond entirely in Spanish (Español).",
    "French":     "Respond entirely in French (Français).",
    "German":     "Respond entirely in German (Deutsch).",
    "Hindi":      "Respond entirely in Hindi (हिंदी).",
    "Portuguese": "Respond entirely in Portuguese (Português).",
    "Arabic":     "Respond entirely in Arabic (العربية).",
    "Japanese":   "Respond entirely in Japanese (日本語).",
    "Korean":     "Respond entirely in Korean (한국어).",
    "Mandarin":   "Respond entirely in Mandarin Chinese (中文).",
}

FORMAT_LABELS: dict[str, str] = {
    "bullets":    "Bullet Points",
    "flashcards": "Flashcards Q&A",
    "structured": "Structured Guide",
}

AVAILABLE_MODELS: dict[str, str] = {
    "Qwen 2.5 7B Instruct":   "Qwen/Qwen2.5-7B-Instruct",
    "Zephyr 7B Beta":         "HuggingFaceH4/zephyr-7b-beta",
    "Phi-3.5 Mini Instruct":  "microsoft/Phi-3.5-mini-instruct",
    "Gemma 2 2B Instruct":    "google/gemma-2-2b-it",
}

DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
VISION_MODEL  = "meta-llama/Llama-3.2-11B-Vision-Instruct"

# ── Format prompt templates ───────────────────────────────────────────────────
_FORMAT_PROMPTS = {
    "bullets": """Transform the following notes into concise exam-focused bullet points.

Rules:
- Each bullet is one clear, testable fact or concept
- Prioritize definitions, formulas, processes, and comparisons
- Use sub-bullets only when a concept has critical sub-parts
- No filler — every bullet must be exam-relevant
- {length_instruction}

Notes:
{notes}

Exam-Focused Bullet Points:""",

    "flashcards": """Transform the following notes into exam-style Q&A flashcards.

Rules:
- Write 8–15 question-answer pairs
- Questions must be specific and testable (definitions, "how does", "why", "compare X and Y")
- Answers: 1–3 sentences max
- {length_instruction}
- Format strictly as:
  Q: [question]
  A: [answer]

Notes:
{notes}

Flashcards:""",

    "structured": """Transform the following notes into a structured exam study guide.

Use exactly these sections (omit a section only if the notes have zero relevant content for it):

## Key Concepts
[The 3–7 most important ideas, one sentence each]

## Definitions
[Term: definition pairs for all critical vocabulary]

## Processes & How Things Work
[Step-by-step explanations of processes, mechanisms, or workflows]

## Formulas & Rules
[Any equations, formulas, laws, or rules worth memorising]

## Likely Exam Topics
[Bullet list of what is most likely to be tested]

{length_instruction}

Notes:
{notes}

Structured Study Guide:""",
}

_KEY_TERMS_PROMPT = """Extract the most important key terms and vocabulary from the following notes.

For each term provide a brief, precise definition (1–2 sentences). List 8–15 terms ordered by importance.
Focus on: domain-specific vocabulary, named concepts/theories, processes, laws, and acronyms.

Format each entry as:
**[Term]** — [definition]

Notes:
{notes}

Key Terms Glossary:"""


def _build_system_prompt(subject: str, difficulty: str, language: str) -> str:
    subject_ctx = SUBJECTS.get(subject, "")
    diff_ctx = DIFFICULTIES.get(difficulty, DIFFICULTIES["Intermediate"])
    lang_instr = LANGUAGES.get(language, "")

    parts = ["You are Caelune, an expert academic tutor specialising in distilling complex notes into focused, exam-ready material."]
    if subject_ctx:
        parts.append(subject_ctx)
    parts.append(diff_ctx)
    parts.append("You extract only what matters most: key concepts, definitions, formulas, and high-yield facts. You are concise, precise, and structured.")
    if lang_instr:
        parts.append(lang_instr)

    return "\n\n".join(parts)


def build_messages(
    notes: str,
    fmt: str,
    subject: str = "General",
    difficulty: str = "Intermediate",
    length: str = "Standard",
    language: str = "English",
) -> list[dict]:
    system = _build_system_prompt(subject, difficulty, language)
    length_cfg = LENGTHS.get(length, LENGTHS["Standard"])
    template = _FORMAT_PROMPTS.get(fmt, _FORMAT_PROMPTS["bullets"])
    user = template.format(notes=notes, length_instruction=length_cfg["instruction"])
    return [
        {"role": "system", "content": system},
        {"role": "user",   "content": user},
    ]


def build_key_terms_messages(
    notes: str,
    subject: str = "General",
    language: str = "English",
) -> list[dict]:
    lang_instr = LANGUAGES.get(language, "")
    system = f"You are Caelune, an expert academic tutor. Extract key terminology clearly and concisely.{' ' + lang_instr if lang_instr else ''}"
    user = _KEY_TERMS_PROMPT.format(notes=notes)
    return [
        {"role": "system", "content": system},
        {"role": "user",   "content": user},
    ]


def max_tokens_for(length: str) -> int:
    return LENGTHS.get(length, LENGTHS["Standard"])["max_tokens"]


# ── Quiz prompt ───────────────────────────────────────────────────────────────
_QUIZ_PROMPT = """Generate exactly {n} multiple-choice questions from the following notes.

Rules:
- Each question must be based only on the notes provided
- Each question has exactly 4 options (A, B, C, D)
- Only one option is correct
- Questions should test key facts, definitions, and concepts
- Vary question types: recall, application, and comparison

Use EXACTLY this format for every question — no deviation:

Q1: [question text]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]

Q2: [question text]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]

Notes:
{notes}

Quiz:"""


def build_quiz_messages(
    notes: str,
    n: int = 7,
    subject: str = "General",
    difficulty: str = "Intermediate",
    language: str = "English",
) -> list[dict]:
    subject_ctx = SUBJECTS.get(subject, "")
    diff_ctx = DIFFICULTIES.get(difficulty, DIFFICULTIES["Intermediate"])
    lang_instr = LANGUAGES.get(language, "")
    parts = ["You are Caelune, an expert academic tutor creating exam-style multiple-choice questions."]
    if subject_ctx:
        parts.append(subject_ctx)
    parts.append(diff_ctx)
    if lang_instr:
        parts.append(lang_instr)
    system = "\n\n".join(parts)
    user = _QUIZ_PROMPT.format(notes=notes, n=n)
    return [
        {"role": "system", "content": system},
        {"role": "user",   "content": user},
    ]


# ── Chat prompt ───────────────────────────────────────────────────────────────
_CHAT_SYSTEM = """You are Caelune, an expert academic tutor. The student has provided the following study notes and wants to ask questions about them.

Answer based on the notes. Be concise and clear. If the answer is not in the notes, say so and offer relevant general knowledge.{subject_ctx}{lang_instr}

Notes:
{notes}"""


def build_chat_messages(
    notes: str,
    history: list[dict],
    question: str,
    subject: str = "General",
    language: str = "English",
) -> list[dict]:
    subject_ctx = SUBJECTS.get(subject, "")
    lang_instr = LANGUAGES.get(language, "")
    system = _CHAT_SYSTEM.format(
        subject_ctx=f"\n\n{subject_ctx}" if subject_ctx else "",
        lang_instr=f"\n\n{lang_instr}" if lang_instr else "",
        notes=notes[:6000],
    )
    messages: list[dict] = [{"role": "system", "content": system}]
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": question})
    return messages
