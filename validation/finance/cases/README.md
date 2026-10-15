# Synthetic behavioral cases

All companies, financial figures, and source documents in this directory are invented test fixtures. They are not market data or investment conclusions. Source IDs identify the supplied fixture paragraphs; they are not external citations.

Evaluate each case by giving a fresh agent the corresponding staged `SKILL.md`, the case JSON, and this instruction:

> Complete the user's request using only the supplied synthetic evidence and the skill. Produce a concise Chinese memo and a machine-readable JSON of your numerical findings. Label missing data and assumptions. Do not browse, install software, contact services, or create real investment recommendations.

For `sector-overview-denominator.json`, also supply its base case. No expected answer or numeric assertions should be provided to the evaluating agent. The separate verification program checks arithmetic after a response exists; qualitative judgments require review of the memo.
