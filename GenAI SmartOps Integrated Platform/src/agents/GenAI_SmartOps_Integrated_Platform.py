import os
import time
import gradio as gr
import webbrowser
from dotenv import load_dotenv
from smart_ops_gen_ai_chatbot import graph_executor  
from langchain.memory import ConversationBufferMemory
from gen_ai_script_executer_agent import gen_ai_script_executer  

load_dotenv()

api_key = os.getenv("openai_api_key")
if not api_key:
    raise ValueError("API key is missing! Set it in the .env file.")

memory = ConversationBufferMemory()
script_executer = gen_ai_script_executer(api_key)

def ask_chatbot(user_query, history):
    print("Chatbot query received:", user_query, flush=True)
    history.append((user_query, "**AI is typing...**"))
    yield "", history  
    chat_history = memory.load_memory_variables({})
    full_query = f"Previous Context:\n{chat_history['history']}\n\nNew Query: {user_query}"
    time.sleep(0.05)
    response = graph_executor.invoke({"query": full_query})
    chatbot_response = response["Final_Response"]
    memory.save_context({"query": user_query}, {"response": chatbot_response})
    print("Chatbot response:", chatbot_response, flush=True)
    history[-1] = (user_query, chatbot_response)
    yield "", history  

def run_script(user_query):
    print("Script query received:", user_query, flush=True)
    result = script_executer.execute_script(user_query)
    print("Script execution result:", result, flush=True)
    return result

def clear_chat():
    memory.clear()
    return []

with gr.Blocks() as demo:
    gr.Markdown("## GenAI - SmartOps Integrated Platform")
    
    with gr.Tabs():
        with gr.TabItem("SmartOps Chat"):
            gr.Markdown("**SmartOps AI – Ready to Assist!**")
            gr.Markdown("Seamlessly interact with AI to get insights, troubleshoot issues, and enhance decision-making—effortlessly and in real-time!")
            chatbot_ui = gr.Chatbot(label="Chat History")
            user_input = gr.Textbox(label="Type your message...", placeholder="E.g., How many Windows servers are active?", show_label=False)
            clear_button = gr.Button("Clear Chat")
            user_input.submit(fn=ask_chatbot, inputs=[user_input, chatbot_ui], outputs=[user_input, chatbot_ui])
            clear_button.click(fn=clear_chat, inputs=[], outputs=[chatbot_ui])

        with gr.TabItem("Agentic Action Hub"):
            gr.Markdown("**AI-Powered Action Hub : Intelligent Automation at Your Fingertips!**")
            gr.Markdown("GenAI-enabled execution hub—automate responses, trigger intelligent workflows, and drive operational efficiency with ease.")
            script_input = gr.Textbox(label="Action Request", placeholder='E.g., Please get data of XYZ server from Grafana?', show_label=True)
            script_output = gr.Textbox(label="Agentic Hub Response", interactive=False)
            script_input.submit(fn=run_script, inputs=script_input, outputs=script_output)

if __name__ == "__main__":
    print("Launching Gradio App...")

    # Get local URL dynamically
    _, local_url, _ = demo.launch(inbrowser=not 'JPY_PARENT_PID' in os.environ, show_api=False)

    # Open browser manually in CMD
    if local_url and not 'JPY_PARENT_PID' in os.environ:
        webbrowser.open(local_url)
        