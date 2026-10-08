
"""Gemini VLM evidence extraction for the RODIC InfraAI POC."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from google import genai
from google.genai import types


DEFAULT_CONFIG_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "gemini_config.json"
)

DEFAULT_CONTRACT_PATH = (
    Path(__file__).resolve().parents[1]
    / "app"
    / "gemini_vlm_contract.json"
)


def _load_json(path: Path) -> dict[str, Any]:
    """Load a JSON configuration file."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _build_prompt(contract: dict[str, Any]) -> str:
    """Build a contract-aware visual evidence prompt."""

    output_schema = contract["output_schema"]

    return f"""
You are an infrastructure visual evidence extraction system.

Analyze the supplied infrastructure image only for observable
visual evidence relevant to infrastructure condition assessment.

Return ONLY valid JSON.

Do not provide a final engineering diagnosis.
Do not claim structural safety.
Do not invent measurements.
Do not infer hidden damage that is not visually supported.
If evidence is insufficient, explicitly report insufficient evidence.

Required JSON structure:

{json.dumps(output_schema, indent=2)}

The engineering_decision field MUST remain:

{{
  "status": "not_provided",
  "reason": "Engineering significance and final disposition require qualified human validation."
}}
"""


def _validate_result(
    result: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    """Validate and normalize Gemini evidence output."""

    required_fields = [
        "image_assessment",
        "observations",
        "negative_evidence",
        "limitations",
        "engineering_decision",
    ]

    missing_fields = [
        field for field in required_fields
        if field not in result
    ]

    if missing_fields:
        raise ValueError(
            f"Gemini response missing required fields: {missing_fields}"
        )

    if not isinstance(result["observations"], list):
        raise ValueError("Gemini observations must be a list.")

    if not isinstance(result["negative_evidence"], list):
        raise ValueError("Gemini negative_evidence must be a list.")

    if not isinstance(result["limitations"], list):
        raise ValueError("Gemini limitations must be a list.")

    engineering_decision = result["engineering_decision"]

    if not isinstance(engineering_decision, dict):
        raise ValueError(
            "Gemini engineering_decision must be an object."
        )

    if engineering_decision.get("status") != "not_provided":
        raise ValueError(
            "Gemini attempted to provide an engineering decision."
        )

    observation_fields = [
        "observation",
        "evidence_type",
        "location_description",
        "visual_confidence",
    ]

    for index, observation in enumerate(result["observations"]):

        if not isinstance(observation, dict):
            raise ValueError(
                f"Observation {index} must be an object."
            )

        missing = [
            field
            for field in observation_fields
            if field not in observation
        ]

        if missing:
            raise ValueError(
                f"Observation {index} missing fields: {missing}"
            )

    return {
        "source": "gemini_vlm",
        "model": None,
        "image_assessment": result["image_assessment"],
        "observations": result["observations"],
        "negative_evidence": result["negative_evidence"],
        "limitations": result["limitations"],
        "engineering_decision": {
            "status": "not_provided",
            "reason": (
                "Engineering significance and final disposition "
                "require qualified human validation."
            ),
        },
    }


def analyze_image_with_gemini(
    image_bytes: bytes,
    config_path: Path | None = None,
    contract_path: Path | None = None,
) -> dict[str, Any]:
    """
    Analyze an infrastructure image using Gemini.

    Returns source-specific visual evidence.
    No engineering decision is produced.
    """

    if not image_bytes:
        raise ValueError("image_bytes cannot be empty.")

    config_path = config_path or DEFAULT_CONFIG_PATH
    contract_path = contract_path or DEFAULT_CONTRACT_PATH

    config = _load_json(config_path)
    contract = _load_json(contract_path)

    api_key_name = config["api_key_environment_variable"]
    api_key = os.environ.get(api_key_name)

    if not api_key:
        raise RuntimeError(
            f"{api_key_name} is not available."
        )

    client = genai.Client(api_key=api_key)

    model_name = config["model"]

    prompt = _build_prompt(contract)

    response = client.models.generate_content(
        model=model_name,
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg",
            ),
            prompt,
        ],
        config=types.GenerateContentConfig(
            temperature=config["temperature"],
            max_output_tokens=config["max_output_tokens"],
            response_mime_type="application/json",
        ),
    )

    response_text = getattr(response, "text", None)

    if not response_text:
        raise RuntimeError(
            "Gemini returned no textual response."
        )

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Gemini response was not valid JSON."
        ) from exc

    validated = _validate_result(
        result=result,
        contract=contract,
    )

    validated["model"] = model_name

    return validated
