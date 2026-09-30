import re

import streamlit as st


def correct_grammar(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Apply a few common, transparent English grammar and spacing rules."""
    corrections: list[tuple[str, str]] = []

    def substitute(pattern: str, replacement, value: str, flags: int = 0) -> str:
        def replace_match(match: re.Match) -> str:
            updated = replacement(match) if callable(replacement) else replacement
            if match.group(0) != updated:
                corrections.append((match.group(0), updated))
            return updated

        return re.sub(pattern, replace_match, value, flags=flags)

    text = substitute(r"\s{2,}", " ", text)
    text = substitute(r"\s+([,.!?;:])", lambda match: match.group(1), text)
    text = substitute(r"\bi\b", "I", text, flags=re.IGNORECASE)

    vowel_sound_exceptions = ("university", "unit", "user", "unique", "unicorn", "European", "one", "once")
    silent_h_words = ("hour", "honest", "honor", "heir")

    def fix_article(match: re.Match) -> str:
        article, word = match.group(1), match.group(2)
        lower_word = word.lower()
        use_an = lower_word.startswith(silent_h_words) or (
            word[0].lower() in "aeiou" and not lower_word.startswith(vowel_sound_exceptions)
        )
        corrected_article = "an" if use_an else "a"
        if article[0].isupper():
            corrected_article = corrected_article.capitalize()
        return f"{corrected_article} {word}"

    text = substitute(r"\b(a|an)\s+([A-Za-z]+)\b", fix_article, text, flags=re.IGNORECASE)

    verb_rules = [
        (r"\b(I)\s+is\b", "I am"),
        (r"\b(you|we|they)\s+is\b", lambda match: f"{match.group(1)} are"),
        (r"\b(he|she|it)\s+are\b", lambda match: f"{match.group(1)} is"),
        (r"\b(he|she|it)\s+have\b", lambda match: f"{match.group(1)} has"),
        (r"\b(I|you|we|they)\s+has\b", lambda match: f"{match.group(1)} have"),
        (r"\b(he|she|it)\s+do\b", lambda match: f"{match.group(1)} does"),
        (r"\b(he|she|it)\s+(go|like|want|need|play|work|eat)\b", lambda match: f"{match.group(1)} {match.group(2)}s"),
        (r"\b(I|you|we|they)\s+(go|likes|wants|needs|plays|works|eats)\b", lambda match: f"{match.group(1)} {match.group(2).rstrip('s')}"),
    ]
    for pattern, replacement in verb_rules:
        text = substitute(pattern, replacement, text, flags=re.IGNORECASE)

    text = substitute(
        r"(^|[.!?]\s+)([a-z])",
        lambda match: f"{match.group(1)}{match.group(2).upper()}",
        text,
    )
    return text, corrections


st.set_page_config(page_title="AI Grammar Correction Assistant", page_icon="✍️", layout="centered")
st.title("AI Grammar Correction Assistant")
st.caption("A lightweight, rule-based helper for common English grammar mistakes.")

with st.form("grammar_form"):
    input_text = st.text_area(
        "Enter English text",
        height=180,
        placeholder="For example: i has a apple. they is ready.",
    )
    submitted = st.form_submit_button("Correct Grammar", type="primary")

if submitted:
    if not input_text.strip():
        st.session_state.pop("grammar_result", None)
        st.warning("Enter some text to correct.")
    else:
        corrected_text, corrections = correct_grammar(input_text)
        st.session_state["grammar_result"] = {
            "original": input_text,
            "corrected": corrected_text,
            "corrections": corrections,
        }

result = st.session_state.get("grammar_result")
if result:
    st.subheader("Results")
    st.metric("Corrections detected", len(result["corrections"]))
    original_column, corrected_column = st.columns(2)
    with original_column:
        st.text_area("Original Text", value=result["original"], height=150, disabled=True)
    with corrected_column:
        st.text_area("Corrected Text", value=result["corrected"], height=150, disabled=True)

    st.subheader("Corrections")
    if result["corrections"]:
        for wrong, correct in result["corrections"]:
            st.write(f"{wrong} → {correct}")
    else:
        st.write("No supported corrections were needed.")

st.caption("This demo checks a small set of common patterns; it is not a full grammar checker.")