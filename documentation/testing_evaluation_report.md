# RODIC InfraAI Innovation Challenge 2026
# Testing & Evaluation Report

**Project:** AI-Assisted Infrastructure Visual Inspection
**Report Type:** Model Testing, Evaluation & Performance Report
**Generated:** 2026-10-07T23:42:14.393064

---

## 1. Executive Summary

This report documents the quantitative evaluation of the two domain-trained
computer vision models used in the RODIC infrastructure inspection POC:

1. **CODEBRIM** — multi-label infrastructure defect classification.
2. **SDNET2018** — binary concrete crack classification.

The evaluation uses the trained checkpoints produced by the POC training
pipeline and evaluates them on held-out validation data.

The evaluation is intended to establish technical performance of the
computer-vision components. It does **not** establish structural safety,
structural capacity, remaining structural life, engineering certification,
or repair requirements.

---

## 2. Evaluation Scope

### 2.1 CODEBRIM

**Task:** Multi-label visual defect classification

**Classes:**

- background
- crack
- spallation
- efflorescence
- exposed_bars
- corrosion_stain

**Validation samples:** 616

**Decision threshold:** 0.5

Because CODEBRIM is a multi-label problem, each image can contain multiple
defect labels simultaneously.

Therefore, conventional single-label accuracy is not used as the primary
performance indicator.

---

### 2.2 SDNET2018

**Task:** Binary concrete crack classification

**Classes:**

- no_crack
- crack

**Total dataset samples:** 56092

**Training samples:** 47679

**Evaluation samples:** 8413

**Split method:** random_split

**Evaluation split seed:** 42

The SDNET2018 evaluation was performed on a reconstructed deterministic
evaluation split because the original training checkpoint did not preserve
the original validation indices.

**Split note:** This is a reconstructed deterministic evaluation split. The original training checkpoint did not contain validation indices.

---

## 3. CODEBRIM Results

### 3.1 Overall Metrics

| Metric | Result |
|---|---:|
| Subset accuracy | 69.16% |
| Micro precision | 85.98% |
| Micro recall | 79.84% |
| Micro F1 | 82.80% |
| Macro precision | 86.60% |
| Macro recall | 79.70% |
| Macro F1 | 82.56% |

### Interpretation

The **macro F1 score is 82.56%** and the
**micro F1 score is 82.80%** on the
616-image validation set.

The reported subset accuracy of 69.16%
means that all six labels were simultaneously correct for that proportion
of validation images at the selected threshold. It should therefore **not**
be interpreted as conventional single-label classification accuracy.

---

### 3.2 CODEBRIM Per-Class Performance

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| background | 87.50% | 98.00% | 92.45% | 150 |
| crack | 93.75% | 70.47% | 80.46% | 149 |
| spallation | 84.80% | 75.71% | 80.00% | 140 |
| efflorescence | 78.40% | 69.50% | 73.68% | 141 |
| exposed_bars | 98.28% | 80.28% | 88.37% | 142 |
| corrosion_stain | 76.88% | 84.25% | 80.39% | 146 |

---

### 3.3 CODEBRIM Confusion Matrices

The following one-vs-rest confusion-matrix counts were produced for each
class.


## 4. CODEBRIM Training Observations

**Training epochs:** 10

**Best epoch:** 6

**Best validation loss:** 0.2069

The best validation loss was achieved at epoch
6. Subsequent training epochs showed
lower training loss but degradation in validation loss. This is consistent
with an emerging overfitting pattern and is recorded as a model-development
observation rather than evidence of generalization beyond the validation
dataset.

---

## 5. SDNET2018 Results

### 5.1 Overall Metrics

| Metric | Result |
|---|---:|
| Accuracy | 95.28% |
| Precision | 87.87% |
| Recall | 79.60% |
| F1 | 83.53% |
| ROC-AUC | 0.9650 |
| PR-AUC | 0.9060 |

### Interpretation

The SDNET2018 model achieved:

- **Accuracy:** 95.28%
- **Precision:** 87.87%
- **Recall:** 79.60%
- **F1:** 83.53%
- **ROC-AUC:** 0.9650
- **PR-AUC:** 0.9060

These results describe performance on the reconstructed deterministic
evaluation split of 8413 images and should not be presented
as an estimate of performance on all infrastructure imagery.

---

### 5.2 SDNET2018 Per-Class Performance

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| no_crack | 96.45% | 98.06% | 97.25% | 7148 |
| crack | 87.87% | 79.60% | 83.53% | 1265 |

---

### 5.3 SDNET2018 Confusion Matrix

| | Predicted no_crack | Predicted crack |
|---|---:|---:|
| **Actual no_crack** | 7009 | 139 |
| **Actual crack** | 258 | 1007 |

The crack class achieved a recall of **79.60%**,
indicating that the model detected that proportion of crack-labelled samples
within this evaluation split.

---

## 6. Runtime and Performance

### CODEBRIM

- Total evaluation time: 87.06 seconds
- Samples evaluated: 616
- Throughput: 7.08 images/sec
- Pipeline time: 141.34 ms/image
- Device: cpu

### SDNET2018

- Total evaluation time: 1484.04 seconds
- Samples evaluated: 8413
- Throughput: 5.67 images/sec
- Pipeline time: 176.40 ms/image
- Device: cpu

### Runtime Interpretation

The measured SDNET2018 throughput was
**5.67 images/sec**
(**176.40 ms/image**) on CPU.

This measurement represents the **end-to-end validation pipeline**, including
data loading and preprocessing. It should therefore not be interpreted as
isolated neural-network inference latency or as a claim of real-time
production performance.

Production deployment benchmarking should separately measure warm-up,
model-only inference latency, preprocessing/postprocessing latency, and
hardware-specific throughput.

---

## 7. Model Checkpoints

| Model | Checkpoint |
|---|---|
| CODEBRIM | `outputs/best_codebrim.pt` |
| SDNET2018 | `outputs/best_sdnet.pt` |

The evaluation pipeline reported zero missing and zero unexpected checkpoint
parameters for the evaluated model state dictionaries.

---

## 8. Evaluation Limitations

The following limitations apply to interpretation of these results:

1. Evaluation is based on held-out dataset samples rather than field
   infrastructure imagery collected under deployment conditions.
2. Dataset-domain performance does not guarantee equivalent performance under
   changes in camera type, illumination, weather, viewpoint, surface
   contamination, compression, occlusion, or infrastructure geometry.
3. CODEBRIM is evaluated as a multi-label classification problem and its
   subset accuracy should not be treated as conventional classification
   accuracy.
4. SDNET2018 uses a reconstructed deterministic evaluation split because the
   original training checkpoint did not preserve the original validation
   indices.
5. Confidence scores are not claimed to be calibrated probabilities.
6. No single image should be treated as sufficient evidence for structural
   safety or engineering certification.
7. The current performance measurements do not establish fleet-scale,
   edge-device, GPU, or real-time production throughput.
8. Additional field validation and domain-specific benchmarking are required
   before operational deployment.

---

## 9. Responsible AI and Engineering Decision Boundary

### Confidence Interpretation

Model output scores are treated as model confidence scores and are not claimed to be calibrated probabilities.

### Engineering Boundary

The system does not determine structural safety, structural capacity, remaining life, repair requirements, or engineering certification.

### Human Validation

Consequential engineering decisions require qualified human validation.

### Evidence-Based Operation

The intended system architecture uses model predictions as visual evidence
rather than treating an individual model output as an autonomous engineering
decision.

The broader POC combines domain-trained computer vision with multimodal
reasoning and evidence arbitration. Where evidence is insufficient or
conflicting, the system should preserve uncertainty rather than fabricate a
definitive conclusion.

---

## 10. Reproducibility and Evidence Provenance

The evaluation artifacts are stored under:

`rodic-poc-project/outputs/`

Relevant evidence files:

- `codebrim_evaluation.json`
- `sdnet_evaluation.json`
- `sdnet_evaluation_split.json`
- `best_codebrim.pt`
- `best_sdnet.pt`

The submission packaging manifest is stored under:

`rodic-poc-project/submission/submission_manifest.json`

The evaluation report was generated automatically from the persisted JSON
evidence to minimize manual metric transcription.

---

## 11. Overall Technical Assessment

The evaluation demonstrates that the POC's two computer-vision components
can provide useful domain-specific visual evidence for infrastructure
inspection scenarios.

The results support the technical feasibility of the CV layer, while the
reported limitations establish an explicit boundary between **model-level
visual recognition** and **qualified engineering judgment**.

The intended production direction is therefore:

**Domain-trained CV → Multimodal Reasoning → Evidence Arbitration →
Structured Inspection Record → Human Validation**

rather than autonomous structural decision-making.

---

## 12. Submission Statement

This report is intended as the quantitative testing and evaluation evidence
for the RODIC InfraAI Innovation Challenge 2026 POC submission.

All reported metrics are derived from the persisted evaluation artifacts
generated by the project evaluation pipeline.
