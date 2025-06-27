from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from collections import defaultdict
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Load GoEmotions BERT model
goemotions_model = AutoModelForSequenceClassification.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_tokenizer = AutoTokenizer.from_pretrained("monologg/bert-base-cased-goemotions-original")
goemotions_pipeline = pipeline("text-classification", model=goemotions_model, tokenizer=goemotions_tokenizer, return_all_scores=True)


def analyze_with_goEmotions(text):
    if text == "" or text is None:
        return [{'label': 'anger', 'score': 0.0},
                {'label': 'fear', 'score': 0.0},   
                {'label': 'annoyance', 'score': 0.0},
                {'label': 'confusion', 'score': 0.0},
                {'label': 'surprise', 'score': 0.0},
                {'label': 'neutral', 'score': 0.0},
                {'label': 'curiosity', 'score': 0.0},
                {'label': 'embarrassment', 'score': 0.0},
                {'label': 'disgust', 'score': 0.0},
                {'label': 'love', 'score': 0.0},
                {'label': 'disappointment', 'score': 0.0},
                {'label': 'amusement', 'score': 0.0},
                {'label': 'nervousness', 'score': 0.0},
                {'label': 'optimism', 'score': 0.0},
                {'label': 'admiration', 'score':0.0},
                {'label': 'sadness', 'score': 0.0},
                {'label': 'disapproval', 'score': 0.0},
                {'label': 'excitement', 'score': 0.0},
                {'label': 'desire', 'score': 0.0},
                {'label': 'realization', 'score': 0.0},
                {'label': 'gratitude', 'score':0.0},
                {'label': 'caring', 'score':0.0},
                {'label': 'remorse', 'score':0.0},
                {'label': 'pride', 'score': 0.0},
                {'label': 'approval', 'score':0.0}]

    max_len = 256 - 2  # account for [CLS], [SEP]
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
            aggregated_scores[emotion['label']] += emotion['score'] / len(chunks)
            
    # Normalize or sort if needed
    sorted_scores = sorted(
        [{"label": label, "score": score} for label, score in aggregated_scores.items()],
        key=lambda x: x["score"],
        reverse=True
    )

    return sorted_scores


# x = analyze_with_goEmotions("")
# pprint("*******"*10)
# pprint(x)