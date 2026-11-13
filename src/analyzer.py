import re
import pymorphy3


_morph = pymorphy3.MorphAnalyzer(lang="uk")

Pos_translation = {
    "NOUN": "іменник",
    "ADJF": "прикметник",
    "ADJS": "прикметник",
    "VERB": "дієслово",
    "INFN": "дієслово",
    "PRTF": "дієслово", # дієприкметник
    "PRTS": "дієслово",
    "GRND": "дієслово", # дієприслівник
    "NUMR": "числівник",
    "ADVB": "прислівник",
    "NPRO": "займенник",
    "PRED": "предикатив",
    "PREP": "прийменник",
    "CONJ": "сполучник",
    "PRCL": "частка",
    "INTJ": "вигук",
}

class ValidationError(ValueError):
    pass

def validate_text(text: str) -> str:
    if not text or not text.strip():
        raise ValidationError("Поле порожнє. Введіть текст.")

    stripped = text.strip()

    if re.fullmatch(r"[\d\s]+", stripped):
        raise ValidationError("Текст не може містити лише цифри.")

    if re.fullmatch(r"[A-Za-z\s]+", stripped):
        raise ValidationError("Текст не може містити лише латиницю.")

    if not re.search(r"[A-Za-zА-Яа-яЄєІіЇїҐґ0-9]", stripped):
        raise ValidationError("Текст не може містити лише розділові знаки.")

    return stripped


def analyze_text(text: str) -> list[list[str]]:

    validated_text = validate_text(text)

    tokens = re.findall(r"\b[А-Яа-яЄєІіЇїҐґ]+(?:-[А-Яа-яЄєІіЇїҐґ]+)*\b", validated_text)

    results = []
    seen = set()

    for token in tokens:
        parsed_list = _morph.parse(token)

        if not parsed_list:
            lemma_status = "не знайдено"
        else:
            best_parse = parsed_list[0]

        if "UNKN" in best_parse.tag:
            lemma_status = "не знайдено"
        else:
            lemma = best_parse.normal_form
            lemma_status = lemma

        pair = (token, lemma_status)
        if pair not in seen:
            seen.add(pair)
            results.append([token, lemma_status])

    return results


def analyze_sentence_by_index(text: str, sentence_index: int) -> tuple[str, str]:
    
    validated_text = validate_text(text)

    sentences = re.split(r'(?<=[.!?])\s+', validated_text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return "Не знайдено речень.", ""

    idx = int(sentence_index) - 1
    if idx < 0 or idx >= len(sentences):
        raise ValidationError(f"Введіть коректний номер речення (від 1 до {len(sentences)}).")

    selected_sentence = sentences[idx]

    words = re.findall(r"\b[А-Яа-яЄєІіЇїҐґ]+(?:-[А-Яа-яЄєІіЇїҐґ]+)*\b", selected_sentence)
   
    replaced_sentence = selected_sentence
    
    for word in words:
        parsed_list = _morph.parse(word)
        pos_ukr = "невідомо"
        if parsed_list:
            tag = parsed_list[0].tag
            pos_code = tag.POS
            if pos_code in Pos_translation:
                pos_ukr = Pos_translation[pos_code]
            else:
                pos_ukr = str(pos_code).lower()
        
        replaced_sentence = re.sub(rf"\b{word}\b", pos_ukr, replaced_sentence, count=1)

    return selected_sentence, replaced_sentence