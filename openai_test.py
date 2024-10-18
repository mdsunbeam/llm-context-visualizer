import base64
import os
from openai import OpenAI
from message_visualizer import visualize_history

class OpenAIModel:
    def __init__(self):
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.messages = []

    def add_system_message(self, content):
        self.messages.append({"role": "system", "content": content})

    def add_user_message(self, content, image_path=None):
        message = {"role": "user", "content": content}
        if image_path:
            message["content"] = [
                {"type": "text", "text": content},
                {"type": "image_url", "image_url": self._encode_image(image_path)}
            ]
        self.messages.append(message)

    def add_assistant_message(self, content):
        self.messages.append({"role": "assistant", "content": content})

    def get_completion(self, model="chatgpt-4o-latest"):
        response = self.client.chat.completions.create(
            model=model,
            messages=self.messages,
            max_tokens=300
        )
        return response.choices[0].message.content

    def _encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"

    def visualize_history(self):
        visualize_history(self.messages)

# Test function
def test_openai_model():
    model = OpenAIModel()
    
    # Test text completion
    model.add_system_message("You are a helpful assistant.")
    model.add_user_message("What is the capital of France?")
    text_response = model.get_completion()
    print("Text completion response:", text_response)
    model.add_assistant_message(text_response)
    
    # Test image completion
    model.add_system_message("You are an image analysis assistant.")
    model.add_user_message("What's in this image?", "mountains.jpg")
    image_response = model.get_completion()
    print("Image completion response:", image_response)
    model.add_assistant_message(image_response)

    # Visualize message history
    model.visualize_history()

if __name__ == "__main__":
    test_openai_model()
