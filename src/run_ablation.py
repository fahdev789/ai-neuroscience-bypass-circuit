import torch
import pandas as pd
from transformer_lens import HookedTransformer

def run_traffic_ablation_experiment():
    # Load GPT-2 Small (standard benchmark model in AI Neuroscience)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = HookedTransformer.from_pretrained("gpt2-small", device=device)
    model.eval()

    prompt_with_to = "John gave a bag to"
    prompt_without_to = "John gave a bag"

    candidate_tokens = [" him", " her", " Mary", " the", " and", " yesterday", " quickly", "."]
    candidate_ids = [model.to_single_token(tok) for tok in candidate_tokens]

    # Run forward passes with cache to inspect internal layers
    with torch.no_grad():
        logits_a, cache_a = model.run_with_cache(prompt_with_to)
        logits_b, cache_b = model.run_with_cache(prompt_without_to)

    probs_a = torch.softmax(logits_a[0, -1, :], dim=-1)
    probs_b = torch.softmax(logits_b[0, -1, :], dim=-1)

    # 1. Compare Final Output Probabilities
    results = []
    for tok, tok_id in zip(candidate_tokens, candidate_ids):
        results.append({
            "Candidate Token": tok.strip(),
            "With 'to' (%)": round(probs_a[tok_id].item() * 100, 2),
            "Without 'to' (%)": round(probs_b[tok_id].item() * 100, 2),
        })

    df = pd.DataFrame(results)
    print("\n=== FINAL LAYER PROBABILITY COMPARISON ===")
    print(df.to_string(index=False))

    # 2. Logit Lens: Trace top prediction across layers for Run B (Without 'to')
    print("\n=== LOGIT LENS TRACE (WITHOUT 'to') ===")
    for layer in range(model.cfg.n_layers):
        # Project intermediate residual stream directly to vocabulary space
        resid_post = cache_b[f"blocks.{layer}.hook_resid_post"][0, -1, :]
        layer_logits = model.unembed(model.ln_final(resid_post))
        top_token_id = torch.argmax(layer_logits).item()
        top_token = model.to_string(top_token_id)
        print(f"Layer {layer:02d}: Top predicted next token -> '{top_token}'")

if __name__ == "__main__":
    run_traffic_ablation_experiment()
