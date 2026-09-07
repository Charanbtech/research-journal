# 🔬 AI Research Journal & Experiment Notes

Personal research notes on model architectures, memory optimization, and algorithmic insights.

---

### LoRA Rank Scaling vs Downstream Perplexity
- **Observations:** Evaluated alpha/rank scaling factors when fine-tuning quantized 7B backbones. Found that `r=16` with `alpha=32` maintains optimal downstream accuracy while keeping parameter footprint bounded.
- **Key finding:** Scaling alpha proportionally to rank stabilizes initial gradient norms during adapter warmups.

---

### FlashAttention-2 Memory Tiling
- **Observations:** Reviewed GPU kernel SRAM tiling patterns. Minimizing roundtrips between High Bandwidth Memory (HBM) and local SRAM reduces memory bus saturation on long-context attention heads.
- **Next steps:** Test sliding window attention blocks for sequence lengths exceeding 8k tokens.

---

### Differential Privacy Gradient Clipping Thresholds
- **Observation:** Evaluated Renyi DP budgets when training with DP-SGD. Clipping gradient norms to C=1.0 yielded the best empirical trade-off between privacy leakage and model accuracy.
- **Takeaway:** Fixed clipping thresholds require adaptive learning rate dampening in early iterations.
