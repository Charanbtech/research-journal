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

---

### Mixture of Experts (MoE) Load Balancing Loss
- **Observation:** Auxiliary loss coefficient of 0.01 successfully prevents routing collapse to top-2 experts during distributed pre-training.
- **Next steps:** Experiment with capacity factors under 1.25 to save peak VRAM.

---

### Vector Search: HNSW vs IVF-PQ Recall Tradeoffs
- **Observation:** At ef_search=64, HNSW maintains >98% recall at 1200 QPS on 1536-dim embeddings. IVF-PQ provides 3x smaller memory footprint with minor recall drop.
- **Decision:** Use HNSW for latency-critical agent retrievers and IVF-PQ for cold archives.
