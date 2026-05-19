import json
import jmespath
from collections import Counter
from typing import List, Dict, Any
from . import utils


def extract_topics(messages: List[str], num_topics: int = 5) -> List[Dict[str, Any]]:
    """
    Extract topics from messages using simple keyword clustering.
    Returns a list of topics with their keywords and frequency.
    """
    if not messages:
        return []
    
    # Clean and tokenize all messages
    all_words = []
    for msg in messages:
        cleaned = utils.remove_emojis(str(msg))
        cleaned = utils.remove_chars_from_text(cleaned)
        words = cleaned.lower().split()
        # Filter out short words and stopwords
        words = [w for w in words if len(w) > 3 and w not in utils.stopword_set]
        all_words.extend(words)
    
    if not all_words:
        return []
    
    # Get word frequencies
    word_freq = Counter(all_words)
    
    # Group words into simple topics based on co-occurrence
    # This is a simplified approach - for production, use LDA or BERTopic
    top_words = word_freq.most_common(num_topics * 3)
    
    topics = []
    for i in range(0, len(top_words), 3):
        topic_words = top_words[i:i+3]
        if topic_words:
            total_freq = sum(count for _, count in topic_words)
            topics.append({
                "keywords": [word for word, _ in topic_words],
                "frequency": total_freq,
                "weight": total_freq / len(all_words) * 100
            })
    
    return topics[:num_topics]


def analyze_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate simple similarity between two texts using Jaccard similarity.
    Returns a value between 0 and 1.
    """
    if not text1 or not text2:
        return 0.0
    
    # Tokenize and clean
    words1 = set(utils.remove_chars_from_text(utils.remove_emojis(text1.lower())).split())
    words2 = set(utils.remove_chars_from_text(utils.remove_emojis(text2.lower())).split())
    
    # Remove stopwords
    words1 = {w for w in words1 if w not in utils.stopword_set and len(w) > 2}
    words2 = {w for w in words2 if w not in utils.stopword_set and len(w) > 2}
    
    if not words1 or not words2:
        return 0.0
    
    # Jaccard similarity
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    
    return intersection / union if union > 0 else 0.0


def extract_key_phrases(text: str, min_length: int = 2, max_phrases: int = 10) -> List[str]:
    """
    Extract key phrases from text using simple n-gram approach.
    """
    if not text:
        return []
    
    cleaned = utils.remove_chars_from_text(utils.remove_emojis(text.lower()))
    words = cleaned.split()
    words = [w for w in words if w not in utils.stopword_set and len(w) > 2]
    
    if not words:
        return []
    
    # Extract bigrams and trigrams
    phrases = []
    
    # Bigrams
    for i in range(len(words) - 1):
        phrase = f"{words[i]} {words[i+1]}"
        phrases.append(phrase)
    
    # Trigrams
    for i in range(len(words) - 2):
        phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
        phrases.append(phrase)
    
    # Count phrase frequencies
    phrase_freq = Counter(phrases)
    
    # Return top phrases
    return [phrase for phrase, _ in phrase_freq.most_common(max_phrases)]


def analyze_semantic_coherence(messages: List[str]) -> Dict[str, Any]:
    """
    Analyze the semantic coherence of a conversation.
    Returns metrics about how related the messages are to each other.
    """
    if len(messages) < 2:
        return {"coherence_score": 0.0, "avg_similarity": 0.0}
    
    similarities = []
    
    # Compare each message with the next one
    for i in range(len(messages) - 1):
        sim = analyze_text_similarity(messages[i], messages[i + 1])
        similarities.append(sim)
    
    if not similarities:
        return {"coherence_score": 0.0, "avg_similarity": 0.0}
    
    avg_similarity = sum(similarities) / len(similarities)
    
    # Coherence score based on consistency of similarities
    coherence = avg_similarity * 100
    
    return {
        "coherence_score": round(coherence, 2),
        "avg_similarity": round(avg_similarity, 3),
        "message_pairs_analyzed": len(similarities)
    }


def semantic_analysis_from_file(filepath: str) -> Dict[str, Any]:
    """
    Perform semantic analysis on a Telegram export file.
    """
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)
    
    messages = jmespath.search('messages[*].text', data) or []
    
    # Extract text from messages
    text_messages = []
    for msg in messages:
        if isinstance(msg, str):
            text_messages.append(msg)
        elif isinstance(msg, list):
            for item in msg:
                if isinstance(item, str):
                    text_messages.append(item)
    
    if not text_messages:
        return {"error": "No text messages found for semantic analysis"}
    
    # Perform various semantic analyses
    topics = extract_topics(text_messages)
    coherence = analyze_semantic_coherence(text_messages)
    
    # Extract key phrases from all messages combined
    all_text = " ".join(text_messages)
    key_phrases = extract_key_phrases(all_text)
    
    return {
        "topics": topics,
        "coherence": coherence,
        "key_phrases": key_phrases,
        "total_messages_analyzed": len(text_messages)
    }
