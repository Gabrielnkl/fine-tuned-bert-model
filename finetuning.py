
!pip install transformers datasets torch

# Importando as bibliotecas necessárias
#from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from transformers import BertTokenizer, BertForSequenceClassification, DistilBertForSequenceClassification, DistilBertTokenizer, Trainer, TrainingArguments
from datasets import load_dataset

# Carregar o dataset IMDB
dataset = load_dataset("imdb")

# Visualizar as primeiras entradas do dataset
dataset['train'][0]

# Carregar o tokenizer do BERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')

# Função para tokenizar os textos
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True)

# Tokenizar os dados de treino e teste
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Visualizar um exemplo tokenizado
tokenized_datasets['train'][0]

# Carregar o modelo BERT pré-treinado para classificação
# Carregar o modelo DistilBERT
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)


# Verificar a estrutura do modelo
model.config

# Definir os parâmetros de treinamento
training_args = TrainingArguments(
    output_dir='./results',          # Diretório para salvar os resultados
    evaluation_strategy="epoch",     # Avaliação por época
    learning_rate=2e-5,              # Taxa de aprendizado
    per_device_train_batch_size=4,  # Tamanho do batch
    per_device_eval_batch_size=16,   # Tamanho do batch para avaliação
    num_train_epochs=2,              # Número de épocas de treinamento
    weight_decay=0.01,               # Decaimento de peso
    logging_dir='./logs',            # Diretório para logs
)

# Exibir os parâmetros de treinamento
training_args

# Criar o Trainer
trainer = Trainer(
    model=model,                       # Modelo que será treinado
    args=training_args,                # Argumentos de treinamento
    train_dataset=tokenized_datasets['train'],   # Dataset de treino
    eval_dataset=tokenized_datasets['test'],    # Dataset de avaliação
    tokenizer=tokenizer,               # Tokenizer usado
)

# Iniciar o treinamento
trainer.train()

# Avaliar o modelo
results = trainer.evaluate()

# Exibir os resultados da avaliação
results

# Salvar o modelo e o tokenizer
model.save_pretrained('./fine_tuned_bert')
tokenizer.save_pretrained('./fine_tuned_bert')

# Função para fazer previsões
def predict(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=-1)
    return "Positivo" if prediction.item() == 1 else "Negativo"

# Testar a função de previsão
predict("I loved this movie! It was amazing.")

