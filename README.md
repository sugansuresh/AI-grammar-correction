# AI Grammar Correction Assistant

A small Streamlit app that corrects a few common English grammar and spacing mistakes using local rules. It does not download a model or send text to an external service.

## Setup

Create and activate a virtual environment if desired, then install the dependency:

```bash
pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Enter English text and select **Correct Grammar** to see the original text, corrected text, number of corrections, and a list of changes. The rules cover examples such as capitalization of “I”, basic article use, selected subject-verb agreement patterns, and spacing around punctuation. This beginner-friendly demo is not a full grammar checker.