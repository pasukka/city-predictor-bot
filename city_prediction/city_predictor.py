from huggingface_hub import InferenceClient
from city_prediction.config import load_config, Config


class CityPredictor:
    model: str
    huggingface_hub_token: str
    key : str

    def __init__(self):
        config = load_config('config.yml')
        self.model = config.llm
        self.huggingface_hub_token = config.huggingface_hub_token
        self.key = config.key
        self.prompt_template_path = config.prompt_template

    def create_llm_prompt(self, prompt_template: str, message: str) -> str:
        prompt = prompt_template
        prompt = prompt.replace('{message}', message)
        return prompt.strip()

    def get_response(self, prompt_template: str, message: str) -> str:
        prompt = self.create_llm_prompt(prompt_template, message)
        response = self.llm.text_generation(
            prompt, do_sample=False, max_new_tokens=30, stop_sequences=['.']).strip()
        response = response.replace("Ответ: ", "").replace(".", "").replace('"', '')
        prompt += response
        return prompt, response

    def predict_city(self, message) -> None:
        self.llm = InferenceClient(model=self.model,
                                   timeout=8,
                                   token=self.huggingface_hub_token)
        with open(self.prompt_template_path+'city_prediction.txt', 'r', encoding='utf-8') as f:
            prompt_template = f.read().strip()
        prompt, city = self.get_response(prompt_template, message)

        print(f'[City 1]: {city}')
        if city != 'None':
            with open(self.prompt_template_path+'chain.txt', 'r', encoding='utf-8') as f:
                prompt_template = f.read().strip()

            prompt += prompt_template
            
            _, city = self.get_response(prompt, city)
            print(f'[City 2]: {city}')

        return city

    def __call__(self, message):       
        city = self.predict_city(message)
        return city
