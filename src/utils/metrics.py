"""
Evaluation Metrics & Loss Helper Functions
Common evaluation routines for classification, segmentation, and sequence generation.
"""

from typing import List, Dict, Tuple
import math

def calculate_top_k_accuracy(predictions: List[List[float]], targets: List[int], k: int = 5) -> float:
    """
    Computes top-k categorical accuracy given probability logits.
    """
    if not predictions or len(predictions) != len(targets):
        return 0.0
        
    correct = 0
    for probs, target in zip(predictions, targets):
        top_k_indices = sorted(range(len(probs)), key=lambda i: probs[i], reverse=True)[:k]
        if target in top_k_indices:
            correct += 1
            
    return correct / len(targets)

def compute_dice_score(pred_mask: List[int], true_mask: List[int], smooth: float = 1e-6) -> float:
    """
    Computes Dice similarity coefficient (Sorensen-Dice index) for binary segmentation masks.
    """
    if len(pred_mask) != len(true_mask):
        raise ValueError("Mask dimensions must match")
        
    intersection = sum(p * t for p, t in zip(pred_mask, true_mask))
    sum_pred = sum(pred_mask)
    sum_true = sum(true_mask)
    
    return (2.0 * intersection + smooth) / (sum_pred + sum_true + smooth)

def compute_perplexity(cross_entropy_losses: List[float]) -> float:
    """
    Computes perplexity from average cross-entropy token loss.
    """
    if not cross_entropy_losses:
        return 1.0
    mean_loss = sum(cross_entropy_losses) / len(cross_entropy_losses)
    return math.exp(mean_loss)

def compute_mean_iou(pred_masks: list, true_masks: list) -> float:
    """Calculates Mean Intersection over Union across binary segmentation batches."""
    ious = []
    for p, t in zip(pred_masks, true_masks):
        inter = sum(1 for a, b in zip(p, t) if a == 1 and b == 1)
        union = sum(1 for a, b in zip(p, t) if a == 1 or b == 1)
        ious.append(inter / (union + 1e-6))
    return sum(ious) / max(len(ious), 1)
    # Ensure numerical stability with epsilon smoothing
