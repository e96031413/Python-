import re
import requests
from rich import print

from .base_translator import Base


class GPT3(Base):
    def __init__(
        self,
        key,
        language,
        api_base=None,
        prompt_template=None,
        temperature=1.0,
        **kwargs,
    ) -> None:
        super().__init__(key, language)
        self.api_url = (
            f"{api_base}v1/completions"
            if api_base
            else "https://api.openai.com/v1/completions"
        )
        self.headers = {
            "Content-Type": "application/json",
        }
        # TODO support more models here
        self.data = {
            "prompt": "",
            "model": "text-davinci-003",
            "max_tokens": 1024,
            "temperature": temperature,
            "top_p": 1,
        }
        self.session = requests.session()
        self.language = language
        self.prompt_template = (
            prompt_template or "Please help me to translate, `{text}` to {language}"
        )

    def rotate_key(self):
        self.headers["Authorization"] = f"Bearer {next(self.keys)}"

    def translate(self, text):
        print(text)
        self.rotate_key()
        self.data["prompt"] = self.prompt_template.format(
            text=text,
            language=self.language,
        )
        r = self.session.post(self.api_url, headers=self.headers, json=self.data)
        if not r.ok:
            return text
        t_text = r.json().get("choices")[0].get("text", "").strip()
        print("[bold green]" + re.sub("\n{3,}", "\n\n", t_text) + "[/bold green]")
        return t_text
