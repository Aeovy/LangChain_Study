import os
from langchain_openai import ChatOpenAI
class LLM_Model():
    def __init__(self, model_type: str="openai"):
        if model_type.lower()=="openai":
            api_key = os.getenv("OPENAI_API_KEY")
            model_name = os.getenv("MODEL_NAME")
            base_url = os.getenv("BASE_URL")
        elif model_type.lower()=="ollama":
            api_key = os.getenv("OLLAMA_API_KEY")
            model_name = os.getenv("OLLAMA_MODEL")
            base_url = os.getenv("OLLAMA_BASE_URL")
        

    def load_model(self, model_name: str):
        # Load the model using the specified model name
        pass

    def generate_response(self, prompt: str) -> str:
        # Generate a response from the model based on the prompt
        pass

    def fine_tune(self, training_data: list):
        # Fine-tune the model with the provided training data
        pass