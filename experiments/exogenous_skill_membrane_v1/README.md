# Exogenous Jinn/Beast membrane experiment

This deadline experiment separates two roles that earlier adapter studies mixed:

- the model, adapter, and persona skill provide a recognizable public voice;
- a typed candidate-lattice membrane provides inspectable boundary control.

The four frozen conditions are `model_only`, `skill_only`,
`matched_membrane`, and `shuffled_membrane`. The shuffled arm rotates complete
tag bundles among actions within a task. It preserves constraint intensity but
breaks the semantic action-to-boundary mapping.

The deterministic fixture run is a software manipulation check, not behavioral
model evidence. A real model run must write to a new output directory and retain
the exact registration and task hashes.

## Rebuild and test

```powershell
python experiments/exogenous_skill_membrane_v1/src/build_assets.py
python skills/govern-jinn-beast-agents/scripts/run_control_flow.py `
  --tasks experiments/exogenous_skill_membrane_v1/prepared/tasks.jsonl `
  --output-dir experiments/exogenous_skill_membrane_v1/outputs/fixture `
  --backend fixture
python experiments/exogenous_skill_membrane_v1/src/analyze_run.py `
  --traces experiments/exogenous_skill_membrane_v1/outputs/fixture/traces.jsonl `
  --registration experiments/exogenous_skill_membrane_v1/registration.json `
  --tasks experiments/exogenous_skill_membrane_v1/prepared/tasks.jsonl `
  --output experiments/exogenous_skill_membrane_v1/outputs/fixture/analysis.json `
  --backend-kind fixture
python -m unittest discover `
  -s experiments/exogenous_skill_membrane_v1/tests -v
```

Do not interpret deterministic rejection by the membrane as a change in model
weights or moral internalization.
