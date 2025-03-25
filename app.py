import gradio as gr
from utils import (
    custom_theme, TRANSLATIONS, INSURANCE_TYPES, CURRENCY_MAP,
    chat_with_bot_stream, process_input, generate_policy_recommendation,
    update_budget_slider, update_ui_language, use_example
)
from static import JS_ANIMATE, JS_THEME, STYLE, THEME_RESET_SCRIPT

# ----------------------------------------------------------------------------- 
# UI Construction 
# -----------------------------------------------------------------------------

def create_ui():
    """Build the Gradio interface and layout."""
    with gr.Blocks(js=JS_ANIMATE, theme=custom_theme) as demo:
        gr.HTML(STYLE)
        gr.HTML(THEME_RESET_SCRIPT)
        
        # Language selection
        with gr.Row(elem_id="language-container"):
            language_dropdown = gr.Dropdown(
                choices=["🇬🇧 English", "🇫🇷 Français"],
                value="🇬🇧 English",
                label="Language",
                elem_id="language-dropdown",
                container=False,
                scale=8
            )
            theme_toggle = gr.Button("☼", elem_id="theme-toggle-btn", scale=2)
            theme_toggle.click(
                fn=lambda: None,
                inputs=[],
                outputs=[],
                js=JS_THEME
            )
            
        with gr.Tabs() as tabs:
            # Chat Tab
            with gr.TabItem("💬 Chat") as chat_tab:
                insurance_html = gr.HTML("""
                    <h1>🏦 Insurance Advisor Chatbot</h1>
                    <h3 class="subtitle">Discuss your insurance needs and get personalized policy recommendations!</h3>
                """)
                
                chatbot = gr.Chatbot(label="Insurance Advisor Chatbot")
                user_input = gr.MultimodalTextbox(
                    interactive=True,
                    file_count="multiple",
                    placeholder="Enter your question or upload voice or file to consult your insurance advisor...",
                    show_label=False,
                    sources=["microphone", "upload"],
                )
                
                with gr.Row():
                    audio_button = gr.Checkbox(
                        value=False, 
                        elem_id="checkbox", 
                        container=False, 
                        label="Enable Text-to-Speech"
                    )
                
                # Custom examples implementation with buttons
                examples_header = gr.HTML("<div class='examples-header'>Examples</div>", elem_id="examples-header")
                
                # English examples - visible by default
                with gr.Column(visible=True, elem_id="english-examples", elem_classes="lang-examples") as english_examples:
                    en_ex_row1 = gr.Row()
                    with en_ex_row1:
                        en_ex1 = gr.Button("I need help finding a comprehensive car insurance policy.", elem_classes="example-btn")
                        en_ex2 = gr.Button("What are the benefits of term life insurance?", elem_classes="example-btn")
                    en_ex_row2 = gr.Row()
                    with en_ex_row2:
                        en_ex3 = gr.Button("Can you recommend a home insurance policy for a new homeowner?", elem_classes="example-btn")
                        en_ex4 = gr.Button("What should I consider for a health insurance plan?", elem_classes="example-btn")
                
                # French examples - hidden by default
                with gr.Column(visible=False, elem_id="french-examples", elem_classes="lang-examples") as french_examples:
                    fr_ex_row1 = gr.Row()
                    with fr_ex_row1:
                        fr_ex1 = gr.Button("J'ai besoin d'aide pour trouver une police d'assurance automobile complète.", elem_classes="example-btn")
                        fr_ex2 = gr.Button("Quels sont les avantages de l'assurance vie temporaire?", elem_classes="example-btn")
                    fr_ex_row2 = gr.Row()
                    with fr_ex_row2:
                        fr_ex3 = gr.Button("Pouvez-vous recommander une police d'assurance habitation pour un nouveau propriétaire?", elem_classes="example-btn")
                        fr_ex4 = gr.Button("Que dois-je considérer pour un régime d'assurance maladie?", elem_classes="example-btn")
                
                # Set up the example button click events
                en_ex1.click(fn=use_example, inputs=[en_ex1], outputs=[user_input])
                en_ex2.click(fn=use_example, inputs=[en_ex2], outputs=[user_input])
                en_ex3.click(fn=use_example, inputs=[en_ex3], outputs=[user_input])
                en_ex4.click(fn=use_example, inputs=[en_ex4], outputs=[user_input])
                
                fr_ex1.click(fn=use_example, inputs=[fr_ex1], outputs=[user_input])
                fr_ex2.click(fn=use_example, inputs=[fr_ex2], outputs=[user_input])
                fr_ex3.click(fn=use_example, inputs=[fr_ex3], outputs=[user_input])
                fr_ex4.click(fn=use_example, inputs=[fr_ex4], outputs=[user_input])
                
                # Chain of functions to process user input and produce responses
                user_input.submit(
                    fn=lambda _: gr.update(interactive=False, submit_btn=False),
                    inputs=[],
                    outputs=user_input
                ).then(
                    fn=chat_with_bot_stream,
                    inputs=[user_input, audio_button, language_dropdown, chatbot],
                    outputs=chatbot,
                    api_name="bot_response"
                ).then(
                    fn=lambda _: "",
                    inputs=None,
                    outputs=user_input
                ).then(
                    fn=lambda _: gr.update(interactive=True, submit_btn=True),
                    inputs=[],
                    outputs=user_input
                )
    
            # Policy Finder Tab
            with gr.TabItem("🔍 Policy Finder") as policy_tab:
                policy_html = gr.HTML("""
                    <h1>🔍 Policy Finder</h1>
                    <h3 class="subtitle">Enter your requirements to receive tailored insurance policy recommendations.</h3>
                """)
                
                with gr.Row():
                    with gr.Column():
                        policy_details_input = gr.Textbox(
                            label="📝 Policy Details (Describe your needs)",
                            placeholder="E.g., I need comprehensive car insurance with roadside assistance",
                            lines=4
                        )
                        insurance_type_dropdown = gr.Dropdown(
                            choices=INSURANCE_TYPES["🇬🇧 English"],
                            value=INSURANCE_TYPES["🇬🇧 English"][0],
                            label="Insurance Type"
                        )
                        coverage_input = gr.Textbox(
                            label="Coverage Amount (optional)",
                            placeholder="E.g., $50,000",
                            interactive=True
                        )
                    with gr.Column():
                        with gr.Row():
                            currency_dropdown = gr.Dropdown(
                                choices=list(CURRENCY_MAP.keys()),
                                value="USD",
                                label="Select Currency",
                                scale=2
                            )
                            budget_slider = gr.Slider(
                                minimum=50,
                                maximum=2000,
                                step=10,
                                value=None,
                                label="Premium Budget ($) (optional)",
                                interactive=True,
                                scale=8
                            )
                            
                        num_people_slider = gr.Slider(
                            minimum=1,
                            maximum=10,
                            step=1,
                            value=1,
                            label="Number of Insured Individuals (optional)",
                            interactive=True
                        )
                        policy_term_input = gr.Textbox(
                            label="Policy Term (optional)",
                            placeholder="E.g., 1 year, 5 years",
                            interactive=True
                        )
                
                generate_btn = gr.Button("Generate Recommendation")
                recommendation_output = gr.Markdown(label="Recommendation")
                
                # Update budget slider when currency changes
                currency_dropdown.change(
                    fn=update_budget_slider, 
                    inputs=[currency_dropdown, language_dropdown], 
                    outputs=[budget_slider]
                )
                
                # Generate recommendation when button is clicked
                generate_btn.click(
                    fn=lambda lang: TRANSLATIONS[lang]["generating_text"],
                    inputs=[language_dropdown],
                    outputs=recommendation_output
                ).then(
                    fn=generate_policy_recommendation,
                    inputs=[
                        policy_details_input,
                        insurance_type_dropdown,
                        coverage_input,
                        budget_slider,
                        policy_term_input,
                        num_people_slider,
                        currency_dropdown,
                        language_dropdown
                    ],
                    outputs=recommendation_output
                )
                
        # Language dropdown change handler - update UI elements
        language_dropdown.change(
            fn=update_ui_language,
            inputs=[language_dropdown],
            outputs=[
                chat_tab,
                policy_tab,
                insurance_html,
                policy_html,
                user_input,
                audio_button,
                policy_details_input,
                insurance_type_dropdown,
                coverage_input,
                currency_dropdown,
                budget_slider,
                num_people_slider,
                policy_term_input,
                generate_btn,
                recommendation_output,
                english_examples,
                french_examples,
                examples_header
            ]
        )
    
    return demo

# ----------------------------------------------------------------------------- 
# Main Entry Point 
# -----------------------------------------------------------------------------

def main():
    demo = create_ui()
    demo.launch()

if __name__ == "__main__":
    main()