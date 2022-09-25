from transformers import pipeline, set_seed
import gradio as grad, random, re


gpt2_pipe = pipeline('text-generation', model='Gustavosta/MagicPrompt-Stable-Diffusion', tokenizer='gpt2')
with open("ideas.txt", "r") as f:
    line = f.readlines()


def generate(starting_text):
    for count in range(4):
        seed = random.randint(100, 1000000)
        set_seed(seed)

        if starting_text == "":
            starting_text: str = line[random.randrange(0, len(line))].replace("\n", "").lower().capitalize()
            starting_text: str = re.sub(r"[,:\-–.!;?_]", '', starting_text)
            print(starting_text)
    
        response = gpt2_pipe(starting_text, max_length=(len(starting_text) + random.randint(60, 90)), num_return_sequences=4)
        response_list = []
        for x in response:
            resp = x['generated_text'].strip()
            if resp != starting_text and len(resp) > (len(starting_text) + 4) and resp.endswith((":", "-", "—")) is False:
                response_list.append(resp+'\n')
    
        response_end = "\n".join(response_list)
        response_end = re.sub('[^ ]+\.[^ ]+','', response_end)
        response_end = response_end.replace("<", "").replace(">", "")

        if response_end != "":
            return response_end
        if count == 4:
            return response_end


txt = grad.Textbox(lines=1, label="Initial Text", placeholder="English Text here")
out = grad.Textbox(lines=4, label="Generated Prompts")

examples = []
for x in range(8):
    examples.append(line[random.randrange(0, len(line))].replace("\n", "").lower().capitalize())

title = "Stable Diffusion Prompt Generator"
description = 'This is a demo of the model series: "MagicPrompt", in this case, aimed at: Stable Diffusion. To use it, simply submit your text or click on one of the examples.<b><br><br>To learn more about the model, go to the link: https://huggingface.co/Gustavosta/MagicPrompt-Stable-Diffusion<br>'
article = "<div><center><img src='https://visitor-badge.glitch.me/badge?page_id=magicprompt_Stable Diffusion' alt='visitor badge'></center></div>"

grad.Interface(fn=generate,
               inputs=txt,
               outputs=out,
               examples=examples,
               title=title,
               description=description,
               article=article,
               allow_flagging='never',
               cache_examples=False,
               theme="default").launch(enable_queue=True, debug=True)


