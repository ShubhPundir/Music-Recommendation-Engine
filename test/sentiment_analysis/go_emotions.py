from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from collections import defaultdict
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# Load GoEmotions model and tokenizer
MODEL_NAME = "monologg/bert-base-cased-goemotions-original"
goemotions_model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
goemotions_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
goemotions_pipeline = pipeline(
    "text-classification",
    model=goemotions_model,
    tokenizer=goemotions_tokenizer,
    return_all_scores=True
)

# Fetch all emotion labels from the model config
ALL_LABELS = list(goemotions_model.config.id2label.values())

def analyze_with_goEmotions(text):
    if not text:
        return [{"label": label, "score": 0.0} for label in ALL_LABELS]

    # Token chunking
    max_len = goemotions_tokenizer.model_max_length - 2  # reserve for [CLS] and [SEP]
    tokens = goemotions_tokenizer.tokenize(text)

    chunks = [
        goemotions_tokenizer.convert_tokens_to_string(tokens[i:i + max_len])
        for i in range(0, len(tokens), max_len)
    ]

    aggregated_scores = defaultdict(float)

    for chunk in chunks:
        try:
            scores = goemotions_pipeline(chunk)[0]
            for entry in scores:
                aggregated_scores[entry["label"]] += entry["score"] / len(chunks)
        except Exception as e:
            print(f"Error analyzing chunk: {e}")

    return sorted(
        [{"label": label, "score": aggregated_scores.get(label, 0.0)} for label in ALL_LABELS],
        key=lambda x: x["score"],
        reverse=True
    )


print("Length of all labels:",len(list(goemotions_model.config.id2label.values())))

print(len(analyze_with_goEmotions("Such a lovely day today")))