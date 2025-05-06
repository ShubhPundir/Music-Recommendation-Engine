from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from collections import defaultdict
# from pprint import pprint

# Load GoEmotions BERT model
goemotions_model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_pipeline = pipeline("text-classification", model=goemotions_model, tokenizer=goemotions_tokenizer, return_all_scores=True)


def analyze_with_goEmotions(text):
    max_len = goemotions_tokenizer.model_max_length - 2  # account for [CLS], [SEP]
    tokens = goemotions_tokenizer.tokenize(text)
    
    chunks = []
    for i in range(0, len(tokens), max_len):
        chunk = tokens[i:i + max_len]
        chunk_text = goemotions_tokenizer.convert_tokens_to_string(chunk)
        chunks.append(chunk_text)

    aggregated_scores = defaultdict(float)

    for i, chunk in enumerate(chunks):
        # print(f"\n--- Chunk {i + 1} ---")
        scores = goemotions_pipeline(chunk)[0]
        # pprint(scores)

        for emotion in scores:
            aggregated_scores[emotion['label']] += emotion['score']

    # Normalize or sort if needed
    sorted_scores = sorted(
        [{"label": label, "score": score} for label, score in aggregated_scores.items()],
        key=lambda x: x["score"],
        reverse=True
    )

    return sorted_scores

# x = analyze_with_goEmotions(lyrics)
# pprint("*******"*10)
# pprint(x)