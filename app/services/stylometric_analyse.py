import re
import math
from collections import Counter
from typing import List, Dict, Any
from . import utils


def calculate_lexical_diversity(text: str) -> float:
    """
    Calculate lexical diversity (unique words / total words).
    Higher values indicate more diverse vocabulary.
    """
    if not text:
        return 0.0
    
    cleaned = utils.remove_chars_from_text(utils.remove_emojis(text.lower()))
    words = cleaned.split()
    words = [w for w in words if len(w) > 2]
    
    if not words:
        return 0.0
    
    unique_words = len(set(words))
    total_words = len(words)
    
    return (unique_words / total_words) * 100 if total_words > 0 else 0.0


def calculate_average_word_length(text: str) -> float:
    """
    Calculate average word length.
    """
    if not text:
        return 0.0
    
    cleaned = utils.remove_chars_from_text(utils.remove_emojis(text))
    words = cleaned.split()
    words = [w for w in words if w.isalpha()]
    
    if not words:
        return 0.0
    
    total_chars = sum(len(word) for word in words)
    return total_chars / len(words)


def calculate_sentence_length_stats(text: str) -> Dict[str, float]:
    """
    Calculate statistics about sentence lengths.
    """
    if not text:
        return {"avg_length": 0.0, "min_length": 0, "max_length": 0}
    
    # Split into sentences (simple approach)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return {"avg_length": 0.0, "min_length": 0, "max_length": 0}
    
    lengths = [len(s.split()) for s in sentences]
    
    return {
        "avg_length": sum(lengths) / len(lengths),
        "min_length": min(lengths),
        "max_length": max(lengths),
        "total_sentences": len(sentences)
    }


def count_punctuation_usage(text: str) -> Dict[str, int]:
    """
    Count usage of different punctuation marks.
    """
    if not text:
        return {}
    
    punctuation = {
        'exclamation': text.count('!'),
        'question': text.count('?'),
        'comma': text.count(','),
        'period': text.count('.'),
        'ellipsis': text.count('...'),
        'dash': text.count('-'),
        'semicolon': text.count(';'),
        'colon': text.count(':')
    }
    
    return punctuation


def analyze_emotional_tone(text: str) -> Dict[str, Any]:
    """
    Analyze emotional tone based on punctuation and word patterns.
    """
    if not text:
        return {"dominant_tone": "neutral", "confidence": 0.0}
    
    punctuation = count_punctuation_usage(text)
    
    # Simple heuristics for tone detection
    exclamations = punctuation.get('exclamation', 0)
    questions = punctuation.get('question', 0)
    total_punct = sum(punctuation.values())
    
    if total_punct == 0:
        return {"dominant_tone": "neutral", "confidence": 0.5}
    
    excl_ratio = exclamations / total_punct
    quest_ratio = questions / total_punct
    
    if excl_ratio > 0.4:
        return {"dominant_tone": "excited", "confidence": excl_ratio}
    elif quest_ratio > 0.4:
        return {"dominant_tone": "inquisitive", "confidence": quest_ratio}
    elif excl_ratio > 0.2:
        return {"dominant_tone": "enthusiastic", "confidence": excl_ratio}
    else:
        return {"dominant_tone": "neutral", "confidence": 0.5}


def calculate_readability_score(text: str) -> float:
    """
    Calculate a simple readability score (similar to Flesch-Kincaid).
    Lower scores indicate easier reading.
    """
    if not text:
        return 0.0
    
    cleaned = utils.remove_chars_from_text(utils.remove_emojis(text))
    sentences = re.split(r'[.!?]+', cleaned)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    words = cleaned.split()
    words = [w for w in words if w.isalpha()]
    
    if not sentences or not words:
        return 0.0
    
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables = sum(count_syllables(word) for word in words) / len(words)
    
    # Simplified Flesch-Kincaid formula
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
    
    return max(0, min(100, score))


def count_syllables(word: str) -> int:
    """
    Estimate syllable count in a word (simplified).
    """
    word = word.lower()
    if len(word) <= 3:
        return 1
    
    vowels = 'aeiouy'
    count = 0
    prev_is_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_is_vowel:
            count += 1
        prev_is_vowel = is_vowel
    
    if word.endswith('e'):
        count -= 1
    
    return max(1, count)


def detect_writing_patterns(messages: List[str]) -> Dict[str, Any]:
    """
    Detect writing patterns across multiple messages.
    """
    if not messages:
        return {}
    
    all_text = " ".join(messages)
    
    patterns = {
        "uses_emojis": any(utils.remove_emojis(msg) != msg for msg in messages),
        "avg_message_length": sum(len(msg.split()) for msg in messages) / len(messages),
        "short_messages_ratio": sum(1 for msg in messages if len(msg.split()) < 10) / len(messages),
        "long_messages_ratio": sum(1 for msg in messages if len(msg.split()) > 50) / len(messages),
    }
    
    return patterns


def stylometric_analysis_from_messages(messages: List[str]) -> Dict[str, Any]:
    """
    Perform comprehensive stylometric analysis on a list of messages.
    """
    if not messages:
        return {"error": "No messages for stylometric analysis"}
    
    all_text = " ".join(messages)
    
    # Calculate various metrics
    lexical_diversity = calculate_lexical_diversity(all_text)
    avg_word_length = calculate_average_word_length(all_text)
    sentence_stats = calculate_sentence_length_stats(all_text)
    punctuation_usage = count_punctuation_usage(all_text)
    emotional_tone = analyze_emotional_tone(all_text)
    readability = calculate_readability_score(all_text)
    writing_patterns = detect_writing_patterns(messages)
    
    return {
        "lexical_diversity": round(lexical_diversity, 2),
        "average_word_length": round(avg_word_length, 2),
        "sentence_stats": sentence_stats,
        "punctuation_usage": punctuation_usage,
        "emotional_tone": emotional_tone,
        "readability_score": round(readability, 2),
        "writing_patterns": writing_patterns,
        "total_messages_analyzed": len(messages)
    }
