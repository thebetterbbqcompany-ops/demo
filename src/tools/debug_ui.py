import gradio as gr
import httpx
import json

# CONFIGURATION
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"

def query_ollama(prompt, system_prompt, temp):
    """
    Direct Uplink to the Neural Core.
    """
    full_prompt = f"SYSTEM: {system_prompt}\nUSER: {prompt}"
    
    payload = {
        "model": MODEL,
        "prompt": full_prompt,
        "stream": False,
        "options": {"temperature": temp}
    }
    
    try:
        # Synchronous call for UI simplicity
        response = httpx.post(OLLAMA_URL, json=payload, timeout=30.0)
        if response.status_code == 200:
            data = response.json()
            return data.get("response", "No response from Cortex.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Connection Failed: {str(e)}"

# UI LAYOUT
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    gr.Markdown("# 🧠 CORTEX DEBUGGER // NEURAL PITMASTER")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ PARAMETERS")
            system_input = gr.Textbox(
                label="System Prompt (Personality)", 
                lines=5, 
                value="You are a rugged, obsession-driven Texas BBQ Pitmaster. You speak in short, technical bursts. You care only about fire management, airflow, and clean smoke."
            )
            temp_slider = gr.Slider(0.0, 1.0, value=0.7, label="Temperature (Creativity)")
            
        with gr.Column(scale=2):
            gr.Markdown("### 🧪 TEST CHAMBER")
            user_input = gr.Textbox(label="Simulated Telemetry / User Input", placeholder="E.g., Status: HEATING, Temp: 180F")
            output_box = gr.Textbox(label="Cortex Response", interactive=False)
            submit_btn = gr.Button("GENERATE THOUGHT", variant="primary")

    # WIRING
    submit_btn.click(
        fn=query_ollama, 
        inputs=[user_input, system_input, temp_slider], 
        outputs=output_box
    )

if __name__ == "__main__":
    print("🚀 LAUNCHING DEBUGGER ON http://localhost:7860")
    demo.launch(server_name="0.0.0.0", server_port=7860)
