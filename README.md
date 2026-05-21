# Caelune — AI Study Assistant

Transform lecture notes into exam-ready summaries using free Hugging Face inference.

## Features

- **3 output formats** — Bullet Points, Flashcards Q&A, Structured Study Guide
- **File uploads** — PDF, Word (.docx), PowerPoint (.pptx), plain text, images (PNG/JPG)
- **Image OCR** — Upload a photo of handwritten notes or a textbook page; text is extracted automatically
- **Key terms extractor** — Auto-generates a glossary after every summary
- **12 subjects** — General, Biology, Chemistry, Physics, Maths, CS, Medicine, Law, Economics, Psychology, History, Literature
- **3 difficulty levels** — Beginner, Intermediate, Expert
- **3 response lengths** — Concise, Standard, Detailed
- **10 languages** — English, Spanish, French, German, Hindi, Portuguese, Arabic, Japanese, Korean, Mandarin
- **Session history** — Browse and restore previous summaries
- **Download** — Save summaries and key terms as plain text

## Quick Start (local)

```bash
git clone https://github.com/YOUR_USERNAME/caelune.git
cd caelune
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```toml
HF_TOKEN = "hf_your_token_here"
```

Get a free token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).

```bash
streamlit run streamlit_app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub (make sure `.streamlit/secrets.toml` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app → select this repo
3. In **Secrets**, add: `HF_TOKEN = "hf_your_token_here"`
4. Deploy

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit 1.35+ |
| LLM | Hugging Face Inference API (free serverless tier) |
| Default model | Qwen 2.5 7B Instruct |
| Vision/OCR | Llama 3.2 11B Vision Instruct |
| PDF parsing | pdfplumber |
| Word parsing | python-docx |
| PPT parsing | python-pptx |
| Markdown rendering | Markdown (Python) |

## Models

| Name | Use |
|---|---|
| Qwen 2.5 7B Instruct | Default summarisation |
| Zephyr 7B Beta | Alternative |
| Phi-3.5 Mini Instruct | Lightweight |
| Gemma 2 2B Instruct | Lightweight |
| Llama 3.2 11B Vision | Image OCR (auto-selected) |

## License

Apache 2.0
