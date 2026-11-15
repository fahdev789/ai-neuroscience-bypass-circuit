# Simulating a simplified mechanistic interpretability experiment (Causal Ablation / Logit Lens)
# Comparing next-token probabilities for:
# Prompt A (Intact): "John gave a bag to"
# Prompt B (Ablated): "John gave a bag"

import numpy as np

# Simulated logits from a transformer model (e.g., GPT-2 style IOI circuit behavior)
# Vocabulary subset relevant to the grammatical state
vocab = ["him", "her", "Mary", "the", "and", "yesterday", "quickly", "."]

# Prompt A: "John gave a bag to" -> 'to' forces prepositional object (pronoun/proper noun)
logits_with_to = np.array([4.2, 4.1, 3.5, 2.8, -1.5, -2.0, -3.0, -2.5])

# Prompt B: "John gave a bag" -> 'to' removed, 'gave' + 'bag' still push recipient via bypass lanes,
# though adverbs/conjunctions/punctuation also become grammatically valid
logits_without_to = np.array([2.4, 2.3, 1.8, 1.2, 2.5, 2.1, 1.5, 2.2])

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

probs_with_to = softmax(logits_with_to)
probs_without_to = softmax(logits_without_to)

for word, p_with, p_without in zip(vocab, probs_with_to, probs_without_to):
    print(f"{word:10s} | With 'to': {p_with*100:5.1f}% | Without 'to': {p_without*100:5.1f}%")
