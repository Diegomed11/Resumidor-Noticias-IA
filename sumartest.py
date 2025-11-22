import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, DataCollatorForSeq2Seq
# Загрузка модели и токенизатора
model_name = "data-silence/any-news-sum"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def generate_summary_with_special_tokens(text, max_length=512):
    inputs = tokenizer(text, return_tensors="pt", max_length=max_length, truncation=True).to(device)
    
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=4,
    )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=False)
    
    # Разделение на заголовок и резюме
    parts = generated_text.split('<title_resume_sep>')
    title = parts[0].replace("<pad> ", "").strip()
    resume = parts[1].replace("</s>", "").strip() if len(parts) > 1 else ""
    
    return title, resume

text= 'Normalmente cuando si te gusta cabrón una morra ya en un punto como que empiezas a todo el tiempo como que demostrarle que ya te tiene tipo ganado, bueno yo en mi pendeja llegaba a hacer eso y osea si está bien, porque si es una morra que vale la pena pues está bien que se sienta segura, pero igual no le dejes todo tipo tan facil de que sepa que tipo ya te gusta incondicionalmente o que ya te tiene ganado, osea que se siga esforzando haciendo cosas (tu también hazlo) para que tipo te siga gustando, porque si deja de hacer cosas y sigues igual o así ya te da por ganado y en primera ya deja de esforzarse y en segunda es como jugar un partido ganado y no está chido, es como si fueras a jugar basket y quieres jugar chido y ves que vas a jugar contra niños de 5 años entonces pues no te dejan tipo disfrutar el jugar o así'
title, resume = generate_summary_with_special_tokens(text)
print(title)  # Ученые показал, каким именно образом сердечные заболевания влияют на выработку гормона сна в шишковидной железе
print(resume)  # Ученые опубликовали статью, опубликованную в журнале Science, команда Мюнхенского технического университета (TUM) показывает, каким образом кардиальные заболевания влияет на выработку гормона сна в шишковидной железе.

