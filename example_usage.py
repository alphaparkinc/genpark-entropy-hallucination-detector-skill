"""Example usage for Entropy Hallucination Detector."""
from client import EntropyHallucinationDetector
import json

response_sample = """
Machine learning models generalize through inductive bias.
Convolutional layers capture spatial localities, whereas transformer self-attention computes dense pairwise affinities.
"""

audit = EntropyHallucinationDetector.audit_text(response_sample)
print(json.dumps(audit, indent=2))
