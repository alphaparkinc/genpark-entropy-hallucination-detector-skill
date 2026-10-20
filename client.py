"""Entropy Hallucination Detector.
100% Python Standard Library.
"""
import re
import math

class EntropyHallucinationDetector:
    """N-gram repetition and Shannon token entropy hallucination detector."""

    @staticmethod
    def calculate_token_entropy(text: str) -> float:
        tokens = re.findall(r'\b[a-zA-Z0-9_-]+\b', text.lower())
        if not tokens:
            return 0.0
        n = len(tokens)
        counts = {}
        for t in tokens:
            counts[t] = counts.get(t, 0) + 1

        entropy = 0.0
        for count in counts.values():
            p = count / n
            entropy -= p * math.log2(p)
        return round(entropy, 4)

    @classmethod
    def audit_text(cls, text: str, min_entropy: float = 2.5, max_repeat_ratio: float = 0.35) -> dict:
        tokens = re.findall(r'\b[a-zA-Z0-9_-]+\b', text.lower())
        if len(tokens) < 10:
            return {"is_hallucinating": False, "reason": "Text too short to evaluate"}

        entropy = cls.calculate_token_entropy(text)

        tri_grams = [tuple(tokens[i:i+3]) for i in range(len(tokens) - 2)]
        tri_counts = {}
        for tg in tri_grams:
            tri_counts[tg] = tri_counts.get(tg, 0) + 1

        max_tri_repeat = max(tri_counts.values()) if tri_counts else 0
        repeat_ratio = (max_tri_repeat * 3) / len(tokens) if tri_grams else 0.0

        is_degenerate = (entropy < min_entropy) or (repeat_ratio > max_repeat_ratio)
        reasons = []
        if entropy < min_entropy:
            reasons.append(f"Low vocabulary entropy ({entropy} < {min_entropy}), indicating token collapse")
        if repeat_ratio > max_repeat_ratio:
            reasons.append(f"Severe n-gram repetition loop (ratio {round(repeat_ratio, 2)} > {max_repeat_ratio})")

        return {
            "is_hallucinating": is_degenerate,
            "entropy": entropy,
            "max_repeat_ratio": round(repeat_ratio, 4),
            "reasons": reasons
        }
