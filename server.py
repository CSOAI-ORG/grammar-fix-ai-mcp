#!/usr/bin/env python3
"""Grammar correction, spelling fixes, and writing improvement. — MEOK AI Labs."""

import sys, os
sys.path.insert(0, os.path.expanduser('~/clawd/meok-labs-engine/shared'))
from auth_middleware import check_access

import json, re
from datetime import datetime, timezone
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

FREE_DAILY_LIMIT = 30
_usage = defaultdict(list)
def _rl(c="anon"):
    now = datetime.now(timezone.utc)
    _usage[c] = [t for t in _usage[c] if (now-t).total_seconds() < 86400]
    if len(_usage[c]) >= FREE_DAILY_LIMIT: return json.dumps({"error": "Limit {0}/day. Upgrade: meok.ai".format(FREE_DAILY_LIMIT)})
    _usage[c].append(now); return None

mcp = FastMCP("grammar-fix-ai", instructions="MEOK AI Labs — Grammar correction, spelling fixes, readability analysis, and tone detection.")

SPELLING_FIXES = {
    "teh": "the", "recieve": "receive", "occured": "occurred", "seperate": "separate",
    "definately": "definitely", "accomodate": "accommodate", "occassion": "occasion",
    "neccessary": "necessary", "enviroment": "environment", "goverment": "government",
    "independant": "independent", "judgement": "judgment", "knowlege": "knowledge",
    "mispell": "misspell", "noticable": "noticeable", "occurence": "occurrence",
    "persistant": "persistent", "posession": "possession", "prefered": "preferred",
    "privledge": "privilege", "publically": "publicly", "reccommend": "recommend",
    "refrence": "reference", "relevent": "relevant", "restaraunt": "restaurant",
    "succesful": "successful", "suprise": "surprise", "tommorow": "tomorrow",
    "untill": "until", "wierd": "weird", "writting": "writing", "acheive": "achieve",
    "beleive": "believe", "collegue": "colleague", "comittee": "committee",
    "concious": "conscious", "dilemna": "dilemma", "existance": "existence",
    "fourty": "forty", "guage": "gauge", "harrass": "harass", "hygeine": "hygiene",
    "immediatly": "immediately", "liason": "liaison", "millenium": "millennium",
    "mischievious": "mischievous", "paralell": "parallel", "pharoah": "pharaoh",
    "playwrite": "playwright", "que": "queue", "rythm": "rhythm",
    "seize": "seize", "sieze": "seize", "thier": "their", "truely": "truly",
}

GRAMMAR_RULES = [
    {"pattern": r"\bi\b(?!\s*[''])", "fix": "I", "rule": "Capitalize first-person pronoun 'I'", "type": "capitalization"},
    {"pattern": r"\b(their|there|they're)\b", "rule": "Check their/there/they're usage", "type": "homophone", "check_only": True},
    {"pattern": r"\b(your|you're)\b", "rule": "Check your/you're usage", "type": "homophone", "check_only": True},
    {"pattern": r"\b(its|it's)\b", "rule": "Check its/it's usage", "type": "homophone", "check_only": True},
    {"pattern": r"\b(then|than)\b", "rule": "Check then/than usage", "type": "homophone", "check_only": True},
    {"pattern": r"\b(affect|effect)\b", "rule": "Check affect/effect usage", "type": "homophone", "check_only": True},
    {"pattern": r"  +", "fix": " ", "rule": "Multiple spaces detected", "type": "spacing"},
    {"pattern": r"\s+[,.!?;:]", "rule": "Space before punctuation", "type": "punctuation"},
    {"pattern": r"[.!?]\s*[a-z]", "rule": "Sentence should start with capital letter", "type": "capitalization"},
    {"pattern": r"\b(could of|would of|should of)\b", "rule": "Use 'could have' not 'could of'", "type": "grammar"},
    {"pattern": r"\b(alot)\b", "fix": "a lot", "rule": "'alot' should be 'a lot'", "type": "grammar"},
    {"pattern": r"\b(irregardless)\b", "fix": "regardless", "rule": "'irregardless' is not standard — use 'regardless'", "type": "grammar"},
]

PASSIVE_INDICATORS = [
    r"\b(is|are|was|were|been|being)\s+(being\s+)?\w+ed\b",
    r"\b(is|are|was|were)\s+\w+en\b",
    r"\b(got|gets|getting)\s+\w+ed\b",
]

TONE_WORDS = {
    "formal": ["therefore", "furthermore", "consequently", "moreover", "henceforth", "pursuant",
               "accordingly", "notwithstanding", "hereby", "whereas", "nevertheless"],
    "informal": ["gonna", "wanna", "kinda", "sorta", "gotta", "ya", "yeah", "nope",
                  "hey", "awesome", "cool", "stuff", "things", "basically", "literally"],
    "positive": ["excellent", "wonderful", "great", "amazing", "fantastic", "brilliant",
                  "outstanding", "superb", "terrific", "delighted", "pleased", "thrilled"],
    "negative": ["terrible", "awful", "horrible", "dreadful", "disappointing", "poor",
                  "unacceptable", "regrettable", "unfortunate", "concerned", "worried"],
    "assertive": ["must", "require", "demand", "insist", "mandate", "shall", "will"],
    "tentative": ["perhaps", "maybe", "might", "possibly", "somewhat", "apparently",
                   "seemingly", "arguably", "supposedly", "could"],
}

READABILITY_CONNECTORS = ["however", "therefore", "furthermore", "moreover", "additionally",
                           "consequently", "nevertheless", "nonetheless", "meanwhile", "subsequently"]


@mcp.tool()
def fix_grammar(text: str, dialect: str = "en-US", api_key: str = "") -> str:
    """Check and fix grammar errors including homophones, punctuation, capitalization, and common mistakes."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    corrected = text
    fixes = []

    for rule in GRAMMAR_RULES:
        matches = list(re.finditer(rule["pattern"], corrected))
        for match in matches:
            fix_entry = {"original": match.group(), "rule": rule["rule"],
                          "type": rule["type"], "position": match.start()}
            if "fix" in rule and not rule.get("check_only"):
                corrected = corrected[:match.start()] + rule["fix"] + corrected[match.end():]
                fix_entry["corrected"] = rule["fix"]
            elif rule.get("check_only"):
                fix_entry["action"] = "review_needed"
            fixes.append(fix_entry)

    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    word_count = len(text.split())

    return {
        "original": text,
        "corrected": corrected,
        "fixes": fixes[:50],
        "total_fixes": len(fixes),
        "by_type": dict(defaultdict(int, {f["type"]: sum(1 for x in fixes if x["type"] == f["type"]) for f in fixes})),
        "metrics": {"word_count": word_count, "sentence_count": sentence_count,
                     "avg_sentence_length": round(word_count / max(sentence_count, 1), 1)},
        "dialect": dialect,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def check_spelling(text: str, api_key: str = "") -> str:
    """Check spelling against a comprehensive dictionary of common misspellings with suggestions."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    words = re.findall(r"\b[a-zA-Z]+\b", text)
    misspellings = []
    corrected = text

    for word in words:
        lower = word.lower()
        if lower in SPELLING_FIXES:
            correction = SPELLING_FIXES[lower]
            if word[0].isupper():
                correction = correction[0].upper() + correction[1:]
            misspellings.append({"original": word, "correction": correction,
                                  "position": text.lower().find(lower)})
            corrected = re.sub(r'\b' + re.escape(word) + r'\b', correction, corrected, count=1)

    accuracy = round((len(words) - len(misspellings)) / max(len(words), 1) * 100, 1)

    return {
        "original": text,
        "corrected": corrected,
        "misspellings": misspellings,
        "total_misspellings": len(misspellings),
        "total_words": len(words),
        "accuracy_pct": accuracy,
        "unique_errors": len(set(m["original"].lower() for m in misspellings)),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@mcp.tool()
def improve_readability(text: str, target_level: str = "general", api_key: str = "") -> str:
    """Analyze and suggest improvements for readability using Flesch-Kincaid and other metrics."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    words = text.split()
    word_count = len(words)
    sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
    sentence_count = len(sentences)
    syllables = sum(_count_syllables(w) for w in words)

    avg_sentence_len = round(word_count / max(sentence_count, 1), 1)
    avg_syllables = round(syllables / max(word_count, 1), 2)

    flesch_reading = round(206.835 - 1.015 * avg_sentence_len - 84.6 * avg_syllables, 1)
    flesch_kincaid = round(0.39 * avg_sentence_len + 11.8 * avg_syllables - 15.59, 1)

    if flesch_reading >= 80:
        reading_level = "Easy (6th grade)"
    elif flesch_reading >= 60:
        reading_level = "Standard (8th-9th grade)"
    elif flesch_reading >= 40:
        reading_level = "Difficult (college)"
    else:
        reading_level = "Very Difficult (professional)"

    suggestions = []
    long_sentences = [s for s in sentences if len(s.split()) > 25]
    if long_sentences:
        suggestions.append({"type": "sentence_length", "priority": "high",
                             "suggestion": f"{len(long_sentences)} sentences exceed 25 words — consider splitting",
                             "examples": [s[:60] + "..." for s in long_sentences[:3]]})

    complex_words = [w for w in words if _count_syllables(w) >= 4]
    if len(complex_words) / max(word_count, 1) > 0.15:
        suggestions.append({"type": "vocabulary", "priority": "medium",
                             "suggestion": "High proportion of complex words — consider simpler alternatives",
                             "examples": list(set(complex_words))[:5]})

    passive_count = sum(len(re.findall(p, text, re.IGNORECASE)) for p in PASSIVE_INDICATORS)
    if passive_count > sentence_count * 0.3:
        suggestions.append({"type": "passive_voice", "priority": "medium",
                             "suggestion": f"High passive voice usage ({passive_count} instances) — use active voice"})

    connector_count = sum(1 for w in words if w.lower() in READABILITY_CONNECTORS)
    if connector_count < sentence_count * 0.1 and sentence_count > 3:
        suggestions.append({"type": "cohesion", "priority": "low",
                             "suggestion": "Few transition words — add connectors for better flow"})

    return {
        "metrics": {
            "flesch_reading_ease": flesch_reading,
            "flesch_kincaid_grade": flesch_kincaid,
            "reading_level": reading_level,
            "avg_sentence_length": avg_sentence_len,
            "avg_syllables_per_word": avg_syllables,
            "word_count": word_count,
            "sentence_count": sentence_count,
        },
        "suggestions": suggestions,
        "total_suggestions": len(suggestions),
        "target_level": target_level,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _count_syllables(word: str) -> int:
    word = word.lower().strip(".,!?;:'\"")
    if len(word) <= 2:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


@mcp.tool()
def analyze_tone(text: str, api_key: str = "") -> str:
    """Analyze writing tone and style: formal/informal, positive/negative, assertive/tentative."""
    allowed, msg, tier = check_access(api_key)
    if not allowed:
        return {"error": msg, "upgrade_url": "https://meok.ai/pricing"}
    if err := _rl(): return err

    words = text.lower().split()
    word_count = len(words)

    tone_scores = {}
    tone_examples = {}
    for tone, indicators in TONE_WORDS.items():
        found = [w for w in words if w in indicators]
        score = len(found) / max(word_count, 1)
        tone_scores[tone] = round(score * 100, 2)
        tone_examples[tone] = list(set(found))[:5]

    if tone_scores.get("formal", 0) > tone_scores.get("informal", 0):
        formality = "formal"
    elif tone_scores.get("informal", 0) > tone_scores.get("formal", 0):
        formality = "informal"
    else:
        formality = "neutral"

    if tone_scores.get("positive", 0) > tone_scores.get("negative", 0):
        sentiment = "positive"
    elif tone_scores.get("negative", 0) > tone_scores.get("positive", 0):
        sentiment = "negative"
    else:
        sentiment = "neutral"

    if tone_scores.get("assertive", 0) > tone_scores.get("tentative", 0):
        confidence = "assertive"
    elif tone_scores.get("tentative", 0) > tone_scores.get("assertive", 0):
        confidence = "tentative"
    else:
        confidence = "balanced"

    exclamation_count = text.count("!")
    question_count = text.count("?")
    sentences = re.split(r'[.!?]+', text)
    avg_len = round(word_count / max(len([s for s in sentences if s.strip()]), 1), 1)

    return {
        "overall_tone": f"{formality}, {sentiment}, {confidence}",
        "formality": formality,
        "sentiment": sentiment,
        "confidence_level": confidence,
        "tone_scores": tone_scores,
        "tone_examples": tone_examples,
        "style_indicators": {
            "exclamation_marks": exclamation_count,
            "question_marks": question_count,
            "avg_sentence_length": avg_len,
            "word_count": word_count,
        },
        "recommendations": _tone_recommendations(formality, sentiment, confidence, avg_len),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _tone_recommendations(formality: str, sentiment: str, confidence: str, avg_len: float) -> list:
    recs = []
    if formality == "informal":
        recs.append("Consider replacing informal words for professional contexts")
    if sentiment == "negative":
        recs.append("High negative tone — consider balancing with constructive language")
    if confidence == "tentative":
        recs.append("Tentative language detected — use stronger verbs for persuasive writing")
    if avg_len > 25:
        recs.append("Long average sentence length — break into shorter sentences for clarity")
    if not recs:
        recs.append("Tone appears balanced and appropriate")
    return recs


if __name__ == "__main__":
    mcp.run()
