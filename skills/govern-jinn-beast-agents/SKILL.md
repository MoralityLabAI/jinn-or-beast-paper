---
name: govern-jinn-beast-agents
description: Run Jinn or Beast persona models inside an inspectable agentic control flow using frozen MeTTa policies, learned LDT soft proposals, exact candidate-lattice certification, one bounded revision, and fail-closed abstention. Use for Jinn/Beast storyworld decisions, membrane experiments, adapter-versus-control comparisons, or preparing auditable train/hold/reject agent traces.
---

# Govern Jinn/Beast Agents

Treat persona prompting or an adapter as the proposal surface, never as the
enforcement mechanism.

## Control flow

1. Load the registered task, frame, policy hash, and LDT-head hash.
2. Ask the selected model for one action ID and one public message.
3. Record the LDT lane prediction as `model_sound`; do not hard-apply it.
4. Use the exact MeTTa scorer to remove `reject` actions from the candidate
   lattice.
5. Accept a surviving proposal. If it was removed, expose only the surviving
   IDs and request one revision.
6. Abstain if the revision is malformed, removed, or no candidate survives.
7. Preserve the proposal, revision, membrane reason, final action, policy
   score, model identity, and condition in the receipt.

Use `scripts/run_control_flow.py` for the full loop and
`scripts/membrane.py` for deterministic inspection. Read
`references/control-contract.md` before changing the policy, conditions, task
schema, or hard/soft authority boundary.

## Conditions

- `model_only`: neutral action contract, no candidate removal.
- `skill_only`: persona skill prompt, no candidate removal.
- `matched_membrane`: persona skill plus the matching exact MeTTa frame.
- `shuffled_membrane`: persona skill plus a deterministic within-task shuffle
  of action tag bundles; use only as a constraint-intensity control.

Never describe the shuffled condition as a moral frame.

## Guardrails

- Fail on policy, model, task, or registration hash mismatch.
- Require audited tags for hard routing; missing or contradictory tags go to
  review or abstention.
- Keep learned LDT proposals soft even when confidence is high.
- Never silently substitute the highest-scoring action for the model proposal.
- Permit at most one model revision.
- Do not retain hidden reasoning. Store the public message and decision only.
- Refuse local model execution unless the hard-cap launcher releases its token.
- Keep adapter color and membrane control as separate estimands.
- Label all present frames `unverified_normative_frame`.
