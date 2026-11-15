## Residual Traffic Circuits: Mechanistic Interpretability of Grammatical Bypass Paths

An **AI Neuroscience (Mechanistic Interpretability)** experiment exploring how transformer language models track grammar, route information through the residual stream, and preserve directional intent even when front-line grammatical tokens are removed.

## 🧠 The Core Intuition: The Traffic Intersection Model
Think of a transformer's **Residual Stream** as a multi-lane road stopped at a red light:
* **Content Tokens (`John`, `gave`, `bag`) = Cars behind the line:** They carry heavy semantic features and already have their "turn signals" on (e.g., `gave` activates a *ditransitive verb frame* expecting a recipient).
* **Function Tokens (`to`) = Cyclists in the front box:** They take up very little semantic space, sit at the front line, and act as grammatical gatekeepers.
* **Parallel Attention Heads = Open Bypass Lanes:** Even if you remove the front-line cyclist (`to`), the cars behind (`gave` + `bag`) still know where they are going and route their directional momentum straight through the bypass lanes.

---

## 🔬 Experiment: Causal Ablation of the Front-Line Token

We compare the model's next-token probability distribution and layer-by-layer predictions (**Logit Lens**) across two prompts:
* **Run A (Intact Traffic):** `"John gave a bag to"`
* **Run B (Ablated Cyclist):** `"John gave a bag"`

### Key Findings
1. **Bypass Signal Persistence:** Removing `to` does not erase recipient prediction—`him`, `her`, and `Mary` still retain **42.1%** of total probability mass.
2. **Circuit Modularity:** The internal ratio between top recipients remains virtually frozen (`him:her` is **1.10:1** with `to` vs. **1.11:1** without `to`), proving that *semantic entity selection* and *syntactic gating* operate on separate circuits.
3. **Gatekeeper Effect:** The true role of `to` is suppression—it blocks non-recipient continuations (`.`, `and`, `yesterday`, `quickly`) from **52.8%** down to **0.2%**.

---

## 🛡️ Why This Matters for Responsible AI
* **Surface Filtering Fails:** Blocking or editing a single trigger token at the end of a prompt does not stop earlier context tokens from broadcasting biased or unsafe intent down the residual bypass lanes.
* **Upstream Intervention is Required:** Effective AI safety and debiasing must target the middle layers where content tokens write their directional representations into the residual stream.

---

## 🚀 Quickstart

```bash
git clone https://github.com
cd residual-traffic-circuits
pip install -r requirements.txt
python src/run_ablation.py
```
