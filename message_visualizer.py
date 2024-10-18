import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import base64

def visualize_history(messages):
    window = tk.Tk()
    window.title("Message History")
    window.geometry("600x400")

    canvas = tk.Canvas(window)
    scrollbar = ttk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for message in messages:
        frame = ttk.Frame(scrollable_frame)
        frame.pack(fill="x", expand=True, padx=5, pady=5)

        role_label = ttk.Label(frame, text=f"Role: {message['role']}", font=("Arial", 10, "bold"))
        role_label.pack(anchor="w")

        content = message['content']
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and 'type' in item:
                    if item['type'] == 'text':
                        content_label = ttk.Label(frame, text=item['text'], wraplength=550)
                        content_label.pack(anchor="w")
                    elif item['type'] in ['image_url', 'image']:
                        image_data = _get_image_data(item)
                        if image_data:
                            image = Image.open(io.BytesIO(image_data))
                            image.thumbnail((200, 200))
                            photo = ImageTk.PhotoImage(image)
                            image_label = ttk.Label(frame, image=photo)
                            image_label.image = photo
                            image_label.pack(anchor="w")
                else:
                    content_label = ttk.Label(frame, text=str(item), wraplength=550)
                    content_label.pack(anchor="w")
        else:
            content_label = ttk.Label(frame, text=str(content), wraplength=550)
            content_label.pack(anchor="w")

        ttk.Separator(scrollable_frame, orient='horizontal').pack(fill='x', padx=5, pady=5)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    window.mainloop()

def _get_image_data(item):
    if 'image_url' in item:
        if item['image_url'].startswith('data:image'):
            return base64.b64decode(item['image_url'].split(',')[1])
        else:
            # Handle external URLs if needed
            pass
    elif 'image' in item:
        return item['image']
    return None

def test_visualizer():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."},
        {"role": "user", "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": "download.jpeg"}
        ]},
        {"role": "assistant", "content": "The image shows a beautiful landscape with mountains and a lake."}
    ]
    visualize_history(messages)

if __name__ == "__main__":
    test_visualizer()

