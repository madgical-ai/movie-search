import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained('intfloat/multilingual-e5-large')
model = AutoModel.from_pretrained('intfloat/multilingual-e5-large')

# Define a function to compute the average pooling of embeddings
def average_pool(last_hidden_states: Tensor,
                    attention_mask: Tensor) -> Tensor:
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

def convertTextToVectors(text):

    # print(type(text))

    if isinstance(text, str):

        # Create input texts for the tokenizer
        input_texts = [f'query: {text}']
        # print(input_texts)

        # Tokenize the input texts
        batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

        # Encode the input texts to obtain embeddings
        with torch.no_grad():
            outputs = model(**batch_dict)
            embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
            embeddings = F.normalize(embeddings, p=2, dim=1)
        
        # Return the vector 
        return embeddings.tolist()

    else:
        input_texts = ['query: ' + item["text"] for item in text]
        batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

        # Encode the input texts to obtain embeddings
        with torch.no_grad():
            outputs = model(**batch_dict)
            embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
            embeddings = F.normalize(embeddings, p=2, dim=1)
        
        # Split your data into batches
        batch_size = 3
        # data_batches = [json_data[i:i + batch_size] for i in range(0, len(json_data), batch_size)]

        data_batches = [text[i:i + batch_size] for i in range(0, len(text), batch_size)]
        print("No")
        return embeddings,data_batches

# convertTextToVectors("steam will rotate a turbine and that's a mechanical energy right there and then this trubin will detect a generator which converts that energy into electrical energy see that just by knowing this law you can do so much and that's it this is easy engineering see again for our other easy and fun engineering topics is engineering engineering topics made easy and fun for you [Music] you")