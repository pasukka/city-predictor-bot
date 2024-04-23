import yaml


class Config:
    llm: str
    huggingface_hub_token: str
    prompt_template: str
    key: str

    def __init__(
            self,
            llm: str,
            token: str,
            prompt_template: str,
            key_path: str
    ):
        self.llm = llm
        self.huggingface_hub_token = token
        self.prompt_template = prompt_template
        self.key = extract_key(key_path)


def extract_key(key_path: str) -> str:
    with open(key_path, 'r', encoding='utf-8') as file:
        key = file.read()
    return key


def load_config(file_path: str) -> Config:
    with open(file_path, 'r', encoding='utf-8') as stream:
        config_dict = yaml.safe_load(stream)['app-config']

    return Config(
        config_dict['llm'],
        config_dict['huggingface-hub-token'],
        config_dict['prompt_template'],
        config_dict['key_path']
    )
