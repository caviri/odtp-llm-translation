import gradio as gr
import tempfile
import os
from app import translate_file
import argparse

def translate_interface(input_file, input_text, model, language, endpoint, api_key):
    # Determine input source
    if input_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8', suffix='.txt') as temp_in:
            temp_in.write(input_file.read().decode('utf-8'))
            temp_in.flush()
            input_path = temp_in.name
    elif input_text:
        with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8', suffix='.txt') as temp_in:
            temp_in.write(input_text)
            temp_in.flush()
            input_path = temp_in.name
    else:
        return "No input provided.", None

    with tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8', suffix='.txt') as temp_out:
        output_path = temp_out.name

    translate_file(
        input_file=input_path,
        output_file=output_path,
        model_name=model,
        language=language,
        endpoint=endpoint,
        api_key=api_key
    )

    with open(output_path, 'r', encoding='utf-8') as f:
        translated = f.read()

    return translated, output_path

def download_file(file_path):
    return file_path

with gr.Blocks() as demo:
    gr.Markdown("# File/Text Translator with OpenAI Endpoint")
    with gr.Row():
        input_file = gr.File(label="Upload File", file_types=['.txt'])
        input_text = gr.Textbox(label="Or Paste Text Here", lines=10)
    model = gr.Textbox(label="Model Name", value="google/gemini-2.0-flash-exp:free")
    language = gr.Textbox(label="Target Language", value="Spanish")
    endpoint = gr.Textbox(label="OpenAI Endpoint", value="https://openrouter.ai/api/v1")
    api_key = gr.Textbox(label="API Key", type="password")
    translate_btn = gr.Button("Translate")
    output_text = gr.Textbox(label="Translated Output", lines=10)
    download_btn = gr.File(label="Download Translated File")

    def run_translation(input_file, input_text, model, language, endpoint, api_key):
        translated, file_path = translate_interface(input_file, input_text, model, language, endpoint, api_key)
        return translated, file_path

    translate_btn.click(
        run_translation,
        inputs=[input_file, input_text, model, language, endpoint, api_key],
        outputs=[output_text, download_btn]
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch Gradio app with optional sharing.")
    parser.add_argument('--share', action='store_true', help="Enable sharing the app with a public URL.")
    args = parser.parse_args()

    demo.queue().launch(
        server_name="0.0.0.0",  # More secure default for development
        server_port=7860,         # Default Gradio port
        share=args.share,              # Disable temporary public URL
        show_error=True,          # Show detailed error messages
        debug=True               # Enable debug mode for development
    )
