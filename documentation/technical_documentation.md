# RODIC InfraAI Innovation Challenge 2026

# Technical Documentation

**Solution:** AI-Assisted Infrastructure Visual Inspection POC

**Generated:** 2026-10-07 23:54:45

> An evidence-grounded multimodal AI system that transforms
> infrastructure images into traceable, uncertainty-aware
> inspection intelligence by combining domain-trained computer
> vision, multimodal reasoning and explicit evidence arbitration
> while keeping consequential engineering decisions human-validated.


# 1. Executive Summary

The proposed solution is an AI-assisted infrastructure visual
inspection Proof of Concept designed to support inspection teams
by converting infrastructure imagery into structured, traceable
inspection evidence.

The system combines two complementary evidence sources:

1. Domain-trained computer vision models trained/evaluated using
   CODEBRIM and SDNET2018.
2. Gemini-based multimodal visual reasoning for contextual image
   interpretation.

The system does not treat either model as an autonomous engineering
decision maker.

Instead, model outputs are retained as source-specific evidence and
passed through an evidence-arbitration layer.

The resulting inspection record can contain:

- detected visual observations
- model-specific evidence
- source/provenance information
- uncertainty indicators
- agreement/conflict states
- inspection findings
- human-review flags

The final consequential decision remains with a qualified
engineer/inspector.

# 2. Business Problem

Infrastructure inspection often requires review of large volumes
of visual evidence collected from bridges, roads, tunnels,
buildings and construction environments.

A conventional workflow can involve:

- manual image review
- repetitive documentation
- inconsistent terminology
- difficulty comparing large image collections
- limited traceability between observations and source evidence
- delayed escalation of potentially important observations

The business opportunity is not simply to replace inspectors with
image classification.

The objective is to create an AI-assisted inspection layer that:

- accelerates visual evidence review
- standardizes defect observations
- organizes evidence
- identifies uncertainty and model disagreement
- produces structured inspection records
- supports human inspection workflows
- preserves traceability from finding back to visual evidence

# 3. Solution Objective

The objective of the POC is to demonstrate an evidence-grounded
multimodal infrastructure inspection workflow.

The system should:

1. ingest infrastructure imagery;
2. extract domain-specific visual evidence;
3. obtain complementary multimodal reasoning;
4. preserve source-specific evidence and provenance;
5. identify agreement, conflict or insufficient evidence;
6. generate a structured inspection record;
7. expose uncertainty and review flags;
8. keep consequential engineering decisions under qualified
   human validation.

## 3.1 End-to-End Architecture

    INFRASTRUCTURE IMAGE
             |
       +-----+-----+
       |           |
       v           v
    DOMAIN CV    GEMINI VLM
       |        Visual Reasoning
       |           |
       +-----+-----+
             |
             v
    SOURCE-SPECIFIC EVIDENCE
             |
       +-----+-----+
       |           |
       v           v
    CV Evidence  VLM Evidence
       |           |
       +-----+-----+
             |
             v
    EVIDENCE ARBITRATION
             |
       +-----+-----+
       |     |     |
       v     v     v
    Agreement Conflict Insufficient
       |     |     |
       +-----+-----+
             |
             v
    EVIDENCE-GROUNDED
    INSPECTION ANALYST
             |
             v
    STRUCTURED INSPECTION RECORD
             |
             v
    HUMAN VALIDATION
             |
             v
    QUALIFIED ENGINEER / INSPECTOR
        REVIEW & DECISION

## 3.2 Architectural Interpretation

The architecture deliberately separates:

- visual detection/classification evidence;
- multimodal reasoning;
- evidence arbitration;
- inspection interpretation;
- human engineering judgment.

The system does not collapse different model outputs into a single
unexplained confidence value.

# 4. Evidence Arbitration

Evidence arbitration is a central innovation of the proposed
inspection architecture.

Rather than blindly selecting the output of one model, the system
compares source-specific observations.

| Evidence State | Meaning |
|---|---|
| HIGH_AGREEMENT | Independent evidence sources support a consistent observation |
| PARTIAL_AGREEMENT | Evidence sources overlap but differ in scope or confidence |
| MODEL_CONFLICT | Evidence sources materially disagree |
| INSUFFICIENT_EVIDENCE | Available visual evidence is inadequate for a reliable conclusion |

These are operational evidence states rather than calibrated
probabilities.

The system should not mathematically average CV confidence and VLM
confidence and label the result as a calibrated probability.

# 5. Computer Vision Implementation

The current computer vision implementation uses ResNet18
classification architectures.

The implementation is intentionally compact and reproducible for
the POC.

| Parameter | Current POC |
|---|---|
| Backbone | ResNet18 |
| Image size | 224 × 224 |
| Optimizer | Adam |
| Loss | BCEWithLogitsLoss |
| CODEBRIM task | Multi-label classification |
| SDNET2018 task | Binary classification |
| Primary evaluation threshold | 0.50 |

# 6. Dataset Description

The POC uses two public infrastructure/concrete visual datasets.

## CODEBRIM

- Total discovered images: 7,717
- Validation samples: 616
- Task: multi-label defect classification
- Local project path:
  `data/codebrim_raw/classification_dataset`

Primary classes:

- background
- crack
- spallation
- efflorescence
- exposed_bars
- corrosion_stain

## SDNET2018

- Total indexed images: 56,092
- Training portion: 47,679
- Evaluation portion: 8,413
- Task: binary crack/no-crack classification
- Local project path:
  `data/sdnet2018`


# 7. Training Methodology

The POC training pipeline uses a pretrained ResNet18 backbone
followed by a task-specific classification head.

The architecture is implemented in:

`src/model.py`

Training configuration is defined in:

`src/config.py`

Training logic is implemented in:

`src/train.py`

The current configuration uses:

- ResNet18
- Adam
- BCEWithLogitsLoss
- 224 × 224 input images
- configurable batch size
- configurable learning rate
- configurable training epochs

The CODEBRIM training run used 6,481 training samples and
616 validation samples.

The best observed CODEBRIM validation loss was approximately
0.2069 at epoch 6.

Later epochs showed increasing validation loss, indicating
emerging overfitting.

# 8. Model Checkpoints

The current project contains the following trained checkpoints:

- `outputs/best_codebrim.pt`
- `outputs/best_sdnet.pt`

The checkpoints are generated from the project training pipeline
and are used by the evaluation workflow.

The project does not claim that these checkpoints represent
production-grade engineering certification models.

# 9. Evaluation Methodology

Evaluation is performed separately for CODEBRIM and SDNET2018
because the tasks have different label structures.

CODEBRIM is evaluated as a multi-label classification problem.

SDNET2018 is evaluated as a binary classification problem.

Evaluation outputs are persisted as JSON evidence under:

`outputs/`

This documentation is generated from those saved evaluation
artifacts rather than manually entering the reported metrics.

# 10. CODEBRIM Evaluation Results

## 10.1 Overall Metrics

| Metric | Result |
|---|---:|
| Subset accuracy | 69.16% |
| Micro precision | 85.98% |
| Micro recall | 79.84% |
| Micro F1 | 82.80% |
| Macro precision | 86.60% |
| Macro recall | 79.70% |
| Macro F1 | 82.56% |

The primary jury-facing aggregate metrics are:

- Macro F1: 82.56%
- Micro F1: 82.80%

The reported subset accuracy of 69.16% should not be described
as ordinary classification accuracy.

In a multi-label setting, subset accuracy means that all labels for
an individual sample must be correct simultaneously.

## 10.2 CODEBRIM Per-Class Results

| Class | Precision | Recall | F1 |
|---|---:|---:|---:|
| background | 87.50% | 98.00% | 92.45% |
| crack | 93.75% | 70.47% | 80.46% |
| spallation | 84.80% | 75.71% | 80.00% |
| efflorescence | 78.40% | 69.50% | 73.68% |
| exposed_bars | 98.28% | 80.28% | 88.37% |
| corrosion_stain | 76.88% | 84.25% | 80.39% |

The strongest precision is observed for exposed bars.

Crack detection shows high precision but lower recall.

Efflorescence has the lowest F1 among the principal defect
classes in this evaluation and should receive additional
validation attention.

# 11. SDNET2018 Evaluation Results

## 11.1 Evaluation Provenance

The original training checkpoint did not preserve the original
validation indices.

Therefore, the reported evaluation was performed on a reconstructed
deterministic evaluation split:

- Total indexed images: 56,092
- Training portion: 47,679
- Evaluation portion: 8,413
- Split seed: 42

This provenance is explicitly documented to avoid presenting the
reconstructed split as the original dataset validation split.

## 11.2 SDNET2018 Metrics

| Metric | Result |
|---|---:|
| Accuracy | 95.28% |
| Precision | 87.87% |
| Recall | 79.60% |
| F1 | 83.53% |
| ROC-AUC | 0.9650 |
| PR-AUC | 0.9060 |

## 11.3 SDNET2018 Runtime

The recorded evaluation throughput was approximately:

- 5.67 images/second
- 176.398 ms/image
- approximately 1,484 seconds total

These measurements represent the recorded end-to-end evaluation
pipeline, including data loading and preprocessing.

The POC therefore does not claim that 176.398 ms represents
isolated neural-network inference latency or real-time production
performance.

# 12. Error Analysis

The error analysis is treated as an engineering diagnostic rather
than merely a model leaderboard.

## CODEBRIM

- Crack precision is high while recall is lower.
- Efflorescence remains comparatively difficult.
- Exposed bars demonstrate strong precision.
- Corrosion staining achieves comparatively strong recall.
- Multi-label interactions require continued evaluation on
  real-world infrastructure imagery.

## SDNET2018

The binary evaluation shows:

- strong no-crack recognition;
- lower recall for the crack class than no-crack recognition;
- false-negative crack cases remain operationally important.

In an infrastructure inspection workflow, false negatives may
deserve additional human review because failure to surface a visible
defect can be more consequential than generating an additional
review candidate.


# 13. Multimodal Reasoning Layer

The POC architecture includes Gemini-based multimodal visual
reasoning as a complementary evidence source.

The VLM is intended to provide contextual visual interpretation such
as:

- visible infrastructure observations
- contextual description
- possible defect characteristics
- visible environmental/contextual information
- uncertainty or ambiguity

The VLM output is not treated as ground truth.

The system preserves the distinction between:

1. learned CV evidence;
2. multimodal visual reasoning;
3. engineering interpretation.

# 14. Structured Inspection Intelligence

The output of the inspection workflow is intended to be represented
as a structured inspection record.

A conceptual record can contain:

| Field | Purpose |
|---|---|
| image_id | Source image identifier |
| observation | Visual observation |
| defect_type | Standardized defect category |
| CV_evidence | Model-derived evidence |
| VLM_evidence | Multimodal reasoning evidence |
| provenance | Evidence source |
| agreement_state | Evidence arbitration result |
| uncertainty | Ambiguity indicator |
| review_required | Human-review flag |
| inspector_decision | Human validation result |

The schema is designed so that evidence can be traced back to the
source image and model that produced it.

# 15. Responsible AI Framework

Responsible AI is treated as an architectural requirement rather
than a documentation-only activity.

## 15.1 Human Oversight

The system does not make autonomous consequential engineering
decisions.

The final review and decision remain with a qualified
engineer/inspector.

## 15.2 Uncertainty

Where visual evidence is inadequate, the system should preserve
uncertainty rather than fabricate a confident conclusion.

The intended behavior is:

insufficient evidence → uncertainty / review flag

rather than:

insufficient evidence → guessed defect

## 15.3 Evidence Traceability

Inspection findings should retain:

- source image;
- model/source;
- model output;
- reasoning evidence;
- arbitration state;
- human-review status.

## 15.4 No Unsupported Safety Claims

The current POC does not determine:

- structural safety;
- structural capacity;
- failure probability;
- remaining useful life;
- engineering certification;
- repair authorization;
- structural health diagnosis from a single image.

## 15.5 Privacy

The system should minimize collection and retention of unnecessary
personal information.

Images and inspection records should be handled according to the
deployment organization's data governance requirements.

## 15.6 Auditability

Persisted evaluation artifacts and provenance information support
reproducibility and auditability of model performance.

# 16. Security and Data Governance

For production deployment, the following controls are recommended:

- authenticated application access;
- role-based access control;
- encrypted transport;
- encrypted storage;
- controlled model/API credentials;
- secrets stored outside source code;
- image retention policies;
- audit logging;
- model/version traceability;
- dataset provenance;
- controlled access to inspection records.

The current POC should not be interpreted as a complete production
security implementation.

# 17. Technology Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Deep learning | PyTorch |
| Computer vision | torchvision / ResNet18 |
| CODEBRIM model | ResNet18 multi-label classifier |
| SDNET2018 model | ResNet18 binary classifier |
| Multimodal reasoning | Gemini VLM |
| Evaluation | Python evaluation pipeline |
| Data format | Image files + JSON evaluation artifacts |
| Documentation | Markdown |
| Development environment | Google Colab / Google Drive |

The architecture is intentionally modular so model components can
be replaced independently in future iterations.

# 18. APIs and External Services

The current POC uses a multimodal Gemini VLM as an external
reasoning component.

Production deployment should isolate API credentials from source
code and use secure secret management.

External model/API usage should also be governed by:

- request logging;
- privacy policy;
- data retention requirements;
- API quota controls;
- cost monitoring;
- latency monitoring;
- failure handling;
- fallback behavior.

The computer vision models themselves are locally executable
PyTorch models and do not inherently require an external inference
API.


# 19. Current POC vs Future Roadmap

It is important to distinguish implemented capabilities from future
architectural opportunities.

## Implemented / Evaluated

- CODEBRIM dataset processing
- SDNET2018 dataset processing
- ResNet18 model training
- CODEBRIM multi-label evaluation
- SDNET2018 binary evaluation
- evaluation metrics
- confusion/error analysis
- saved model checkpoints
- evidence/provenance documentation
- Responsible AI boundaries
- technical documentation and QA

## POC Architecture / Demonstration

- Gemini multimodal visual reasoning
- evidence-source separation
- evidence arbitration concept
- structured inspection intelligence
- human validation workflow

## Future / Planned

The following are not presented as current POC capabilities:

- V-JEPA / JEPA world models
- Mamba / State Space Models
- reinforcement learning
- drone autonomy
- LiDAR/radar sensor fusion
- CARLA-scale autonomous simulation
- TensorRT optimization
- ONNX edge deployment
- fleet-scale deployment
- automated engineering certification
- autonomous infrastructure maintenance decisions

# 20. Recommended Production Architecture

    Browser / Inspection UI
              |
              v
         FastAPI Service
              |
              v
    +-----------------------------+
    | AI Inspection Inference     |
    |                             |
    | CODEBRIM ResNet18           |
    | SDNET2018 ResNet18          |
    | Gemini VLM                  |
    +-----------------------------+
              |
              v
       Evidence Arbitration
              |
              v
     Structured Inspection JSON
              |
        +-----+-----+
        |           |
        v           v
    Evidence    Human Validation
      Store           |
                      v
             Qualified Engineer /
                 Inspector

# 21. Production Roadmap

## Phase 1 — POC Hardening

- freeze evaluation protocol;
- expand infrastructure-domain validation data;
- improve minority-class recall;
- improve provenance;
- formalize structured inspection schema;
- add repeatable inference tests.

## Phase 2 — Pilot Deployment

- deploy inference API;
- introduce secure image storage;
- introduce role-based access;
- implement inspection workflow UI;
- collect qualified inspector feedback;
- establish model monitoring.

## Phase 3 — Domain Expansion

Expand toward broader infrastructure inspection categories:

- roads;
- bridges;
- tunnels;
- construction progress;
- visible water/dampness indicators;
- joints and surface deterioration.

## Phase 4 — Advanced AI

Potential future research directions include:

- multimodal world models;
- temporal reasoning;
- V-JEPA/JEPA-style representation learning;
- efficient state-space architectures;
- sensor fusion;
- edge inference;
- active learning;
- human-in-the-loop reinforcement learning.

These capabilities require additional datasets, validation,
engineering controls and domain-specific testing before production
deployment.

# 22. Business Impact

The primary business value is not simply automated defect
classification.

The proposed system can support:

## Inspection Productivity

Reduce repetitive visual review and organize large image
collections.

## Standardization

Provide consistent defect terminology and structured records.

## Traceability

Maintain a relationship between findings and the underlying
visual evidence.

## Prioritization

Surface potentially important observations for human review.

## Decision Support

Give inspectors structured evidence rather than an opaque single
model score.

## Scalability

Create a software layer that can be expanded to additional
infrastructure categories and inspection modalities.

# 23. Current Limitations

## Dataset limitations

Public datasets may not fully represent:

- local infrastructure conditions;
- regional construction materials;
- lighting variation;
- weather;
- camera variability;
- image quality;
- operational inspection conditions.

## Model limitations

The current classifiers are visual recognition models and should
not be interpreted as structural engineering models.

## Evaluation limitations

SDNET2018 evaluation uses a reconstructed deterministic split
because the original checkpoint did not preserve the original
validation indices.

## VLM limitations

Multimodal foundation models can produce plausible but incorrect
interpretations.

Therefore VLM output must remain evidence rather than unquestioned
ground truth.

## Engineering limitations

A single image generally cannot establish structural safety or
structural condition.

Human engineering validation remains essential.

# 24. Reproducibility

The project keeps model checkpoints, evaluation artifacts and source
code within the project structure.

Important locations include:

- `rodic-poc-project/data/`
- `rodic-poc-project/src/`
- `rodic-poc-project/outputs/`
- `rodic-poc-project/submission/`

Important model checkpoints:

- `outputs/best_codebrim.pt`
- `outputs/best_sdnet.pt`

Important evaluation artifacts:

- `outputs/codebrim_evaluation.json`
- `outputs/sdnet_evaluation.json`
- `outputs/sdnet_evaluation_split.json`

The evaluation artifacts used to generate this documentation are
persisted as JSON.

This document is generated incrementally from those artifacts and
the project source configuration.


# 25. Innovation Quotient

The innovation is positioned at the system-architecture level.

The proposed solution does not rely solely on a defect classifier.

Instead it combines:

1. domain-specific CV evidence;
2. multimodal contextual reasoning;
3. explicit evidence arbitration;
4. uncertainty handling;
5. provenance;
6. structured inspection intelligence;
7. human validation.

This transforms the role of AI from:

image classifier

into:

evidence-grounded inspection assistant

while preserving the engineering decision boundary.

# 26. Human Decision Boundary

    AI SYSTEM
        |
        | observes visual evidence
        v
    AI INSPECTION ASSISTANT
        |
        | produces findings + uncertainty
        v
    EVIDENCE / REVIEW FLAG
        |
        v
    QUALIFIED ENGINEER / INSPECTOR
        |
        | validates and decides
        v
    ENGINEERING DECISION

# 27. Final Technical Assessment

The current POC demonstrates a technically reproducible foundation
for AI-assisted infrastructure visual inspection.

The strongest demonstrated components are:

- domain-specific computer vision;
- multi-label infrastructure defect recognition;
- binary crack detection;
- saved model checkpoints;
- quantitative evaluation;
- explicit evaluation provenance;
- multimodal reasoning architecture;
- evidence arbitration;
- structured inspection intelligence;
- human validation;
- Responsible AI boundaries.

The current evidence supports positioning the system as an
AI-assisted inspection intelligence POC, not as an autonomous
engineering certification or structural-safety system.

The architecture is suitable for subsequent pilot development
provided that additional real-world infrastructure data,
domain-expert validation, operational testing and production
security controls are introduced.

# 28. Submission Readiness

The technical documentation supports the following challenge
submission requirements:

- technical implementation description;
- data source and dataset description;
- model architecture;
- evaluation methodology;
- quantitative testing results;
- runtime information;
- Responsible AI framework;
- data privacy considerations;
- technology stack;
- APIs/external services;
- current POC scope;
- future roadmap;
- reproducibility;
- business impact;
- innovation positioning.

The hosted application URL and demonstration video remain separate
submission artifacts and should be added when finalized.

# 29. Evidence Artifacts

The primary machine-readable evidence artifacts are:

- `outputs/codebrim_evaluation.json`
- `outputs/sdnet_evaluation.json`
- `outputs/sdnet_evaluation_split.json`
- `outputs/best_codebrim.pt`
- `outputs/best_sdnet.pt`

The implementation source files are:

- `src/config.py`
- `src/model.py`
- `src/dataset.py`
- `src/train.py`
- `src/evaluator.py`

These artifacts provide the evidence base for the reported model
configuration, evaluation results and reproducibility information.

# 30. Document Control

| Field | Value |
|---|---|
| Project | RODIC InfraAI Innovation Challenge 2026 |
| Document | Technical Documentation |
| Generation method | Incremental section builder |
| Generated automatically | Yes |
| Source directory | `rodic-poc-project/src/` |
| Evidence directory | `rodic-poc-project/outputs/` |
| Submission directory | `rodic-poc-project/submission/` |

