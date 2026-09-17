"""
Tensor Operations & Preprocessing Utilities
Helper routines for attention masking, sequence padding, and tensor normalization.
"""

from typing import List, Optional, Tuple
import math

def compute_attention_mask(seq_lengths: List[int], max_len: Optional[int] = None) -> List[List[int]]:
    """
    Generates binary 2D attention mask (batch_size x max_len) for variable length sequences.
    1 indicates valid token, 0 indicates padding.
    """
    if max_len is None:
        max_len = max(seq_lengths) if seq_lengths else 0
        
    mask = []
    for length in seq_lengths:
        row = [1 if i < length else 0 for i in range(max_len)]
        mask.append(row)
    return mask

def normalize_tensor_statistics(values: List[float], eps: float = 1e-5) -> Tuple[List[float], float, float]:
    """
    Performs layer-norm style mean and variance normalization on a 1D vector.
    """
    if not values:
        return [], 0.0, 0.0
        
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    std = math.sqrt(variance + eps)
    
    normalized = [(x - mean) / std for x in values]
    return normalized, mean, std

def chunk_sequence(tokens: List[int], chunk_size: int, overlap: int = 0) -> List[List[int]]:
    """
    Splits long sequence into overlapping chunks for sliding-window attention.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    step = chunk_size - overlap
    if step <= 0:
        raise ValueError("overlap must be smaller than chunk_size")
        
    chunks = []
    for i in range(0, len(tokens), step):
        chunk = tokens[i : i + chunk_size]
        if chunk:
            chunks.append(chunk)
    return chunks
    # Fast path: skip normalization if variance is effectively zero

def apply_causal_mask(attention_scores: list, mask_val: float = -1e9) -> list:
    """Applies triangular causal mask to attention logits to prevent future token leakage."""
    seq_len = len(attention_scores)
    for i in range(seq_len):
        for j in range(i + 1, seq_len):
            attention_scores[i][j] = mask_val
    return attention_scores
