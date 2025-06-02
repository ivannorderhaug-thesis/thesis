import json
import logging
import os
import re
from textwrap import dedent
from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict, List, Optional, Type, Literal

PROVIDERS: Dict[str, Dict[str, Any]] = {
    "openai": {
        "imports": ["openai"],
        "client_ctor": lambda key: __import__("openai").OpenAI(api_key=key),
        "default_model": "gpt-4.1-2025-04-14",
        "api_key_env": "OPENAI_API_KEY",
    },
    "deepseek": {
        "imports": ["openai"],
        "client_ctor": lambda key: __import__("openai").OpenAI(
            api_key=key, base_url="https://api.deepseek.com"
        ),
        "default_model": "deepseek-reasoner",
        "api_key_env": "DEEPSEEK_API_KEY",
    },
    "gemini": {
        "imports": ["google.genai"],
        "client_ctor": lambda key: __import__("google.genai", fromlist=["Client"]).Client(
            api_key=key
        ),
        "default_model": "gemini-2.0-flash",
        "api_key_env": "GEMINI_API_KEY",
    },
    "claude": {
        "imports": ["anthropic"],
        "client_ctor": lambda key: __import__("anthropic").Anthropic(api_key=key),
        "default_model": "claude-3-opus-20240229",
        "api_key_env": "ANTHROPIC_API_KEY",
    },
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LLMConfig(BaseModel):
    provider: Literal["openai", "deepseek", "gemini", "claude"] = "openai"
    model: Optional[str] = None
    temperature: float = Field(0.0, ge=0.0, le=2.0)
    timeout: int = Field(15, gt=0)

    class Config:
        extra = "allow"

class LLMInterface:
    def __init__(
        self,
        *,
        config: LLMConfig,
        api_key: Optional[str] = None,
        **provider_kwargs: Any,
    ):
        """
        Initializes the LLMInterface.

        Args:
            config: LLMConfig instance (provider, model, temperature, timeout).
            api_key: Optional override for the provider API key.
            provider_kwargs: Any additional provider-specific parameters.
        """
        self.config = config
        self.provider = config.provider

        # Lookup provider info
        info = PROVIDERS.get(self.provider)
        if info is None:
            raise ValueError(f"Unsupported provider: {self.provider!r}")

        # Ensure required package(s) are installed
        for pkg in info["imports"]:
            try:
                __import__(pkg)
            except ImportError as e:
                raise ImportError(f"'{pkg}' is required for provider '{self.provider}'.") from e

        # Determine API key
        key = api_key or os.getenv(info["api_key_env"])
        if not key:
            raise ValueError(
                f"No API key provided for {self.provider!r}; set '{info['api_key_env']}'."
            )

        # Instantiate client
        self.client = info["client_ctor"](key)
        # Resolve model
        self.model = config.model or info["default_model"]
        self.provider_kwargs = provider_kwargs

        logger.info("Initialized LLMInterface(provider=%s, model=%s)", self.provider, self.model)

    def run(
        self,
        user_prompt: str,
        system_prompt: str,
        response_model: Type[BaseModel],
        runs: int = 1,
        lo_prompt: Optional[str] = None,         
        **call_overrides: Any,
    ) -> List[BaseModel]:
        """
        Send chat‐completions (and optional LO pass) and return validated models.
        """
        out: List[BaseModel] = []
        attempts = 0

        temperature = call_overrides.get("temperature", self.config.temperature)
        timeout     = call_overrides.get("timeout", self.config.timeout)

        # Initialize here
        lo_input: Optional[str] = None
        raw_lo: Optional[str] = None

        while len(out) < runs:
            attempts += 1
            try:
                raw = self._chat_call(system_prompt, user_prompt, temperature, timeout)
                if not raw.strip():
                    print(user_prompt)
                    raise json.JSONDecodeError("Empty response", raw, 0)
                data = self._extract_json(raw)

                if lo_prompt:
                    lo_input = f"Input: {user_prompt}\n{data}"
                    raw_lo = self._chat_call(lo_prompt, lo_input, temperature, timeout)
                    data = self._extract_json(raw_lo)

                validated = response_model.model_validate(data)
                out.append(validated.to_dict())

            except (json.JSONDecodeError, ValidationError) as err:
                logger.warning("Parse error on attempt %d: %s\nRaw Output:\n%s", attempts, err, raw)
                if lo_prompt and raw_lo is not None:
                    logger.warning("LO Pass Output:\n%s", raw_lo)
                if attempts >= runs * 10:
                    raise RuntimeError("Too many failed attempts parsing LLM output.") from err
                continue
            except Exception:
                logger.exception("LLM call failed")
                raise

        return out

    def _chat_call(
        self, system_prompt: str, user_prompt: str, temperature: float, timeout: int
    ) -> str:
        """Dispatch to provider-specific implementation."""
        method = getattr(self, f"_call_{self.provider}")
        return method(system_prompt, user_prompt, temperature, timeout)

    def _call_openai(
        self, system_prompt: str, user_prompt: str, temperature: float, timeout: int
    ) -> str:
        """Call OpenAI API with the given prompts and parameters."""
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": dedent(system_prompt)},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                timeout=timeout,
                seed=0,
                max_completion_tokens=2048,
                **self.provider_kwargs,
            )
            return resp.choices[0].message.content
        except Exception as e:
            raise RuntimeError("OpenAI API error") from e

    def _call_deepseek(
        self, system_prompt: str, user_prompt: str, temperature: float, timeout: int
    ) -> str:
        """Call DeepSeek API with the given prompts and parameters."""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": dedent(system_prompt)},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            **self.provider_kwargs,
        )
        return resp.choices[0].message.content

    def _call_gemini(
        self, system_prompt: str, user_prompt: str, temperature: float, timeout: int
    ) -> str:
        """Call Gemini API with the given prompts and parameters."""
        from google.genai import types
        try:
            resp = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    max_output_tokens=2048,
                    temperature=temperature,
                    seed=0,
                    system_instruction=dedent(system_prompt),
                ),
                contents=[user_prompt],
                **self.provider_kwargs,
            )
            if not resp or not resp.text:
                raise ValueError("Empty response from Gemini API")
            return resp.text
        except Exception as e:
            raise RuntimeError("Gemini API error") from e
        
    def _call_claude(
        self, system_prompt: str, user_prompt: str, temperature: float, timeout: int
    ) -> str:
        """Call Claude API with the given prompts and parameters."""
        try:
            resp = self.client.messages.create(
                model=self.model,
                system=dedent(system_prompt),
                messages=[
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                timeout=timeout,
                max_tokens=2048,
                **self.provider_kwargs,
            )
            return resp.content[0].text
        except Exception as e:
            raise RuntimeError("Claude API error") from e

    @staticmethod
    def _extract_json(raw: str) -> Any:
        """
        Attempt to find and parse the first valid JSON object in the given string,
        ignoring surrounding junk like markdown fences or trailing tokens.
        """
        if not raw.strip():
            raise json.JSONDecodeError("Empty input", raw, 0)

        # Remove markdown fencing if any
        raw = re.sub(r"^```json\s*", "", raw.strip(), flags=re.IGNORECASE)
        raw = re.sub(r"```$", "", raw.strip())

        # Try direct parse
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass  # Fall back to more aggressive search

        # Try to locate the first JSON object manually
        brace_stack = []
        json_start = None

        for idx, ch in enumerate(raw):
            if ch == '{':
                if not brace_stack:
                    json_start = idx
                brace_stack.append(ch)
            elif ch == '}':
                if brace_stack:
                    brace_stack.pop()
                    if not brace_stack:
                        # Found a full JSON object
                        json_str = raw[json_start:idx + 1]
                        try:
                            return json.loads(json_str)
                        except json.JSONDecodeError:
                            pass  # Keep scanning

        # If no valid JSON found
        raise json.JSONDecodeError("No valid JSON object found in output", raw, 0)