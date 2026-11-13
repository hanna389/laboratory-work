import gradio as gr
from analyzer import ValidationError, analyze_text, analyze_sentence_by_index

if __name__ == "__main__":
    print(analyze_text("Привіт"))


def process_input(text: str):
    try:
        data = analyze_text(text)
        return data
    except ValidationError as e:
        gr.Warning(str(e))
        return[]


def process_sentence_task(text: str, sentence_num):
    try:
        orig_sent, transformed_sent = analyze_sentence_by_index(text, sentence_num)
        return orig_sent, transformed_sent
    except ValidationError as e:
        gr.Warning(str(e))
        return "", ""

def clear_tab1():
    return "", []


def clear_tab2():
    return "", 1, "", ""

custom_theme = gr.themes.Base(
    primary_hue="zinc",
    neutral_hue="teal",
    )

with gr.Blocks(theme=custom_theme, title="Аналізатор слів та речень") as demo:
    gr.Markdown("Лематизація та аналіз частин мови у реченнях")

    with gr.Tabs():
        with gr.TabItem("Лематизація"):
            with gr.Row():
                with gr.Column(scale=2):
                    input_text = gr.Textbox(
                        lines=5,
                        placeholder="Введіть текст тут...",
                        label="Вхідний текст",
                    )
                    with gr.Row():
                        analyze_btn = gr.Button("Аналізувати", variant="primary")
                        clear_btn1 = gr.Button("Очистити")

                with gr.Column(scale=3):
                    output_table = gr.Dataframe(
                        headers=["Словоформа", "Початкова форма"],
                        datatype=["str", "str"],
                        label="Результати лематизації",
                        interactive=False,
                    )

        with gr.TabItem("Аналіз речення за номером"):
            with gr.Row():
                with gr.Column(scale=2):
                    input_text_sent = gr.Textbox(
                        lines=5,
                        placeholder="Введіть текст із кількома реченнями...",
                        label="Вхідний текст",
                    )
                    sent_number = gr.Number(
                        value=1, 
                        label="Номер речення", 
                        precision=0
                    )
                    with gr.Row():
                        analyze_sent_btn = gr.Button("Обробити речення", variant="primary")
                        clear_btn2 = gr.Button("Очистити")
                
                with gr.Column(scale=3):
                    out_original = gr.Textbox(label="Обране речення", interactive=False)
                    out_transformed = gr.Textbox(label="Речення із заміною на частини мови", interactive=False)

            analyze_btn.click(
                fn=process_input, inputs=input_text, outputs=output_table
            )
            clear_btn1.click(
                            fn=clear_tab1, inputs=None, outputs=[input_text, output_table],
            )
            analyze_sent_btn.click(
                fn=process_sentence_task,
                inputs=[input_text_sent, sent_number],
                outputs=[out_original, out_transformed],
            )
            clear_btn2.click(
                fn=clear_tab2, inputs=None, outputs=[input_text_sent, sent_number, out_original, out_transformed],
            )

if __name__ == "__main__":
    demo.launch()