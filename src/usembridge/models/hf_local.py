from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass
class HuggingFaceJSONTranslator:
    """Lazy local Hugging Face adapter; heavy dependencies are imported only when used."""

    model_id: str
    max_new_tokens: int = 2048
    temperature: float = 0.0

    def __post_init__(self) -> None:
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Install the optional LLM stack with pip install -e '.[llm]'") from exc
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            device_map="auto",
            torch_dtype="auto",
        )

    def translate(self, source_text: str, *, seed: int | None = None) -> dict:
        import torch

        if seed is not None:
            torch.manual_seed(seed)
        prompt = (
            "Convert the following rules, facts, and query into the U-SemBridge CIR JSON. "
            "Do not infer missing facts. Distinguish explicit negation from absence of evidence. "
            "Return JSON only.\n\n" + source_text
        )
        messages = [{"role": "user", "content": prompt}]
        text = self._tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )
        inputs = self._tokenizer(text, return_tensors="pt").to(self._model.device)
        do_sample = self.temperature > 0
        kwargs = {
            "max_new_tokens": self.max_new_tokens,
            "do_sample": do_sample,
        }
        if do_sample:
            kwargs["temperature"] = self.temperature
        with torch.no_grad():
            out = self._model.generate(**inputs, **kwargs)
        generated = out[0][inputs["input_ids"].shape[1] :]
        raw = self._tokenizer.decode(generated, skip_special_tokens=True).strip()
        return json.loads(raw)
