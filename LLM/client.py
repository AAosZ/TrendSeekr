import json
import os
from typing import Any

from config import Config
from llama_cpp import Llama

from .prompts import Prompts


class Client:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.model = None

    def load_llm(self) -> Llama:
        if not os.path.exists(self.config.MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found: {self.config.MODEL_PATH}. Set NEWS_LLM_MODEL_PATH to a GGUF model."
            )

        self.model = Llama(
            model_path=self.config.MODEL_PATH,
            n_ctx=self.config.N_CTX,
            n_gpu_layers=self.config.N_GPU_LAYERS,
            n_threads=self.config.N_THREADS,
            verbose=False,
        )
        return self.model

    def classify_batch(
        self,
        prompts: Prompts,
        headline_payload: list[dict[str, Any]],
    ) -> str:
        if not self.model:
            self.load_llm()

        response = self.model.create_chat_completion(
            messages=[
                {"role": "system", "content": prompts.SYSTEM_PROMPT.strip()},
                {
                    "role": "user",
                    "content": prompts.USER_PROMPT_TEMPLATE.format(
                        headlines_json=json.dumps(headline_payload, ensure_ascii=True)
                    ).strip(),
                },
            ],
            temperature=self.config.TEMPERATURE,
            max_tokens=self.config.MAX_TOKENS,
        )

        return response["choices"][0]["message"]["content"]
