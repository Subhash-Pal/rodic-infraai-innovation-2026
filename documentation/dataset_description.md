# RODIC InfraAI Innovation Challenge 2026
# Dataset Description

**Project:** AI-Assisted Infrastructure Visual Inspection
**Report Type:** Dataset Description and Data Provenance
**Generated:** 2026-10-07T23:52:56.576780

---

## 1. Dataset Overview

The POC uses two publicly available computer-vision datasets to provide
domain-specific visual evidence for infrastructure inspection:

1. **CODEBRIM** — multi-label concrete defect classification.
2. **SDNET2018** — binary concrete crack classification.

The datasets are used as model-development and evaluation resources for the
computer-vision layer of the POC.

The datasets are **not treated as direct substitutes for field inspection
data**. Performance measured on these datasets does not establish equivalent
performance under real infrastructure operating conditions.

---

# 2. CODEBRIM

## 2.1 Source and Local Dataset Path

**Dataset:** CODEBRIM

**Local project path:**

`/content/drive/MyDrive/rodic-poc-project/data/codebrim_raw/classification_dataset`

**Filesystem status:** **Available**

**Images discovered recursively:** **7,717**

The dataset is indexed by the POC's `CodebrimDataset` loader.

---

## 2.2 POC Label Taxonomy

The CODEBRIM model uses the following six output classes:

| Class |
|---|
| background |
| crack |
| spallation |
| efflorescence |
| exposed_bars |
| corrosion_stain |

CODEBRIM is treated as a **multi-label classification task**, meaning that
an image may contain more than one applicable visual condition.

---

## 2.3 Dataset Structure Discovered

The following image-containing directories were detected directly from the
project filesystem:

| Directory | Image count |
|---|---:|
| `rodic-poc-project` | 63,836 |
| `test` | 628 |
| `test/background` | 150 |
| `test/defects` | 478 |
| `train` | 6,473 |
| `train/background` | 2,185 |
| `train/defects` | 4,288 |
| `val` | 616 |
| `val/background` | 150 |
| `val/defects` | 466 |

### Immediate Dataset Directories

| Directory | Image count |
|---|---:|
| `metadata` | 0 |
| `rodic-poc-project` | 63,836 |
| `test` | 628 |
| `train` | 6,473 |
| `val` | 616 |

The directory information above is generated from the actual files present
in the project rather than from manually entered counts.

---

## 2.4 POC Evaluation Split

The persisted CODEBRIM evaluation evidence records:

- Training samples: **6,481**
- Validation samples: **616**
- Validation task: multi-label classification

The validation set contains **616**
images and was used for the reported CODEBRIM model evaluation.

---

# 3. SDNET2018

## 3.1 Source and Local Dataset Path

**Dataset:** SDNET2018

**Local project path:**

`/content/drive/MyDrive/rodic-poc-project/data/sdnet2018`

**Filesystem status:** **Available**

**Images discovered recursively:** **56,092**

The dataset is indexed by the POC's `SdnetDataset` loader.

---

## 3.2 POC Label Taxonomy

The SDNET2018 model uses binary crack classification:

| Class | Meaning |
|---|---|
| `no_crack` | Image classified as not containing the target crack condition |
| `crack` | Image classified as containing the target crack condition |

The POC therefore treats SDNET2018 as a **binary classification task**.

---

## 3.3 Dataset Structure Discovered

The following image-containing directories were detected directly from the
project filesystem:

| Directory | Image count |
|---|---:|
| `D` | 13,620 |
| `D/CD` | 2,025 |
| `D/UD` | 11,595 |
| `P` | 24,334 |
| `P/CP` | 2,608 |
| `P/UP` | 21,726 |
| `W` | 18,138 |
| `W/CW` | 3,851 |
| `W/UW` | 14,287 |

### Immediate Dataset Directories

| Directory | Image count |
|---|---:|
| `D` | 13,620 |
| `P` | 24,334 |
| `W` | 18,138 |

The structure is reported from the actual project filesystem and is not
manually assumed by this document.

---

## 3.4 POC Evaluation Split

The persisted deterministic evaluation manifest records:

- Total samples: **56,092**
- Training samples: **47,679**
- Evaluation samples: **8,413**
- Split method: **random_split**
- Evaluation seed: **42**

The evaluation set contains **8,413**
images.

### Split Provenance

The SDNET2018 evaluation split was reconstructed deterministically using
seed **42** because the original model
checkpoint did not preserve the original validation indices.

This distinction is explicitly documented to avoid presenting the
reconstructed split as the original training-time validation split.

---

# 4. Dataset-to-Model Mapping

| Dataset | Task | Classes | Role in POC |
|---|---|---|---|
| CODEBRIM | Multi-label classification | 6 | Domain-specific concrete defect evidence |
| SDNET2018 | Binary classification | 2 | Crack-focused visual evidence |

The two models provide complementary evidence.

**CODEBRIM** provides a broader set of concrete defect categories, while
**SDNET2018** provides an additional crack/no-crack signal.

The POC architecture can subsequently combine these model outputs with
multimodal visual reasoning and evidence arbitration.

---

# 5. Infrastructure Inspection Relevance

The datasets support visual recognition of conditions relevant to
infrastructure inspection, particularly concrete surface conditions.

The POC uses the following operational vocabulary:

### Defect / Condition Evidence

- Crack
- Spallation
- Efflorescence
- Exposed reinforcement / bars
- Corrosion staining

These categories are treated as **visual observations**.

They are not themselves engineering conclusions about structural capacity,
remaining life, safety, repair requirements, or regulatory compliance.

---

# 6. Dataset Limitations

The datasets have important limitations when transferred to real-world
infrastructure inspection.

### Domain Shift

Field imagery may differ from benchmark datasets in:

- Camera hardware
- Resolution
- Viewing distance
- Viewing angle
- Illumination
- Weather
- Shadows
- Surface contamination
- Water or moisture
- Occlusion
- Compression
- Infrastructure geometry
- Background complexity

### Representation Limitations

Dataset labels describe the visual conditions represented in the source
datasets. They do not necessarily capture every condition encountered during
road, bridge, tunnel, or construction inspection.

### Engineering Interpretation

A visual classification result does not directly establish:

- Structural safety
- Structural capacity
- Remaining service life
- Failure probability
- Repair requirements
- Material strength
- Structural severity according to an engineering code
- Engineering certification

Such interpretations require appropriate engineering inspection,
measurements, context, and qualified professional judgment.

---

# 7. Data Privacy and Usage Boundary

The current POC uses dataset imagery as model-development and evaluation
evidence.

The POC does not require personal identity information to perform the
computer-vision classification task.

For future field deployment, data governance should address:

- Image provenance
- Access control
- Retention policy
- Metadata handling
- Potential personally identifiable information
- Site/location information
- Secure storage and transmission
- Auditability of inspection evidence

Field data should be processed according to the applicable organizational,
contractual, and legal requirements.

---

# 8. Reproducibility Artifacts

Relevant dataset and evaluation artifacts are maintained under:

`rodic-poc-project/outputs/`

Important files include:

- `codebrim_evaluation.json`
- `sdnet_evaluation.json`
- `sdnet_evaluation_split.json`
- `best_codebrim.pt`
- `best_sdnet.pt`

The deterministic SDNET2018 split manifest is retained separately so that
the reported evaluation set can be reconstructed consistently.

---

# 9. Responsible AI Data Interpretation

Dataset performance should be interpreted as **benchmark/model evidence**,
not as proof that the system can independently make engineering decisions.

The POC therefore maintains the following boundary:

> **AI observes and organizes visual evidence; qualified humans validate
> consequential engineering decisions.**

Where evidence is insufficient or conflicting, the intended system behavior
is to preserve uncertainty rather than fabricate a definitive engineering
conclusion.

---

# 10. Summary

The RODIC POC combines two complementary visual datasets:

- **CODEBRIM:** 7,717 images discovered in the
  project dataset structure and six-class multi-label defect taxonomy.
- **SDNET2018:** 56,092 images discovered in the project
  dataset structure and binary crack/no-crack taxonomy.

Together, these datasets support the domain-trained computer-vision layer
of the proposed infrastructure inspection intelligence pipeline:

**Infrastructure Image → Domain CV → Multimodal Reasoning →
Evidence Arbitration → Inspection Record → Human Validation**

The dataset results establish technical feasibility of the visual recognition
layer while the documented limitations prevent overclaiming field-level
engineering capability.
