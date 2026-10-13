---
classification: confidential
title: "Module 3.2 — VALIDATE: the validator and the conformance lane"
track: 3
module: "3.2"
level: advanced
prereqs: ["3.1"]
est_minutes: 30
teaches: sheerline
opens_files:
  - heyhi-mcp/heyhi_mcp/core/validator.py
  - heyhi-mcp/heyhi_mcp/conformance/css_check.py
  - heyhi-mcp/heyhi_mcp/tools/validate.py
---

# Module 3.2 — VALIDATE: the validator and the conformance lane

## You are here

RETRIEVE handed the agent the design system. VALIDATE asks the reverse question: does this emitted output honor it? This module opens the checking layer, the part of the loop that runs outside the model and so costs no tokens and returns the same answer every time. The question underneath: what is the difference between checking the claim an agent makes and checking the code it emits? Previous: [`module-3-1.md`](module-3-1.md). Next: [`module-3-3.md`](module-3-3.md).

## Learning objectives

After this you can:

- Say why validation is deterministic and zero-token, and what that property buys the loop.
- Name the two lanes, the manifest validator and the conformance lane, and how one tool bridges them.
- Read a rule and name its finding, and state what a hardcoded hex triggers in each lane.
- Explain why the legal-token set is generated from the token file rather than written into the validator.

## Concept

The design value under this verb is the third invariant, evaluation before deployment, and the mechanism has one defining property: it runs outside the model. A model asked to check its own output returns a probability and a token bill; a validator returns the same verdict on every run, for free. That is why the loop's checking layer is code, not a prompt, and why it can run on every artifact without a budget conversation.

There are two lanes, and holding them apart is the whole module. The first is the manifest validator in `heyhi-mcp/heyhi_mcp/core/validator.py`: four artifact validators, for a component, a token-usage block, a copy string, and a full page, implementing nine rules on a Pydantic base. It reads the artifact an agent *reports*, the structured claim about what it built, and returns a result carrying validity, errors, warnings, suggestions, and a confidence score. Its set of legal tokens and contrast pairs is generated from the token file at import, so nothing is hardcoded: when the design system changes, the validator changes with it instead of drifting from it. A hardcoded value in a reported token trips Rule 1, the `token_compliance` rule.

The second lane reads the code itself, and its one-line brief is the whole idea: read the emitted stylesheet, not the claim about it. `heyhi-mcp/heyhi_mcp/conformance/css_check.py` is that lane. An agent can report a clean manifest and still emit a literal hex in its CSS; the manifest lane trusts the report, and the conformance lane checks the artifact. It reports four core finding kinds, `literal_color`, `off_scale_dimension`, `untokenised_font`, and `unknown_var`, with a later token-fidelity expansion adding three more of the same shape (`off_token_number`, `off_token_duration`, `off_token_easing`). Each fires whether or not a token exists for the literal, marking the two cases with `token_available`. A literal that matches a known token is the higher-severity, auto-fixable case; a literal with no token at all is a value that is simply not in the design system. A checker that reported only the first would be blind to the second, which is the worse problem.

The two lanes meet inside one tool. `validate_output` has a rendered-CSS path that delegates to the conformance engine, so a single call can check the claim and, when handed real CSS, check the code. This is the seam a smart reader connects forward: a correction carrying a machine-checkable predicate becomes a rule the conformance lane runs, which is 3.4, and every finding produced here becomes an input to the grade in 3.3. Notice, too, the honesty the conformance lane keeps about its own limits. It does not resolve the cascade, reading declarations as written, and an out-of-gamut color gets a verdict with a reason rather than a guessed token. A deterministic checker earns its trust by refusing to guess.

Two terms to carry. A *token* is the system's named value; a *literal* is a raw value written where a token belongs, a hex, a px length, a font stack. Every rule in this layer is one question asked in two places: is this a token, or a literal pretending to be one?

## Walkthrough

Open `heyhi-mcp/heyhi_mcp/core/validator.py` and read the Architecture block in the docstring: nine rules across four artifact validators, the legal-token set auto-generated from the token file, and the line "validation is deterministic and has no token cost." Skim the `rule_name` values through the file, `token_compliance`, `contrast`, `touch_target`, `label_coverage`, `focus_state`, `variant_legality`, `component_scope`, `copy_constraints`, and `output_format`, then match two of them to the failure they name.

Now open `heyhi-mcp/heyhi_mcp/conformance/css_check.py` and read the module header: the read-the-code brief, the finding kinds, and the `token_available` note that a finding fires with or without a matching token. Read to the bottom and find `check_class`, the exact-match presence check, `focus-visible:ring-2` is not satisfied by `ring-4`, which is the check that 3.4's factual predicates dispatch to. Then open `heyhi-mcp/heyhi_mcp/tools/validate.py`, the thin tool that delegates into the validator.

## Lab

Read the four finding-kind definitions at the top of `heyhi-mcp/heyhi_mcp/conformance/css_check.py` and pick `literal_color`. Then, in `heyhi-mcp/heyhi_mcp/core/validator.py`, find the Rule 1 `token_compliance` path. Write what a hardcoded hex triggers in each lane, and what decides the severity.

**Success looks like:** the conformance lane names a `literal_color` finding, the manifest lane names Rule 1 `token_compliance`, and one sentence stating that `token_available` distinguishes a literal that has a known token replacement (higher severity, auto-fixable) from a literal with no token at all (a value outside the system), so neither case is silently passed.

## Common misreads

- *"Validation asks a model to check the output."* No. It runs outside the model: the same answer every run, at no token cost. That determinism is the point.
- *"The manifest and the CSS are one check."* No. The manifest lane trusts the reported artifact; the conformance lane reads the emitted stylesheet. An agent can report clean and still emit a literal.
- *"The legal-token set is a list inside the validator."* No. It is generated from the token file at import, so the validator tracks the system instead of drifting from a stale copy.
- *"A finding fires only when a token exists for the literal."* No. It fires either way; `token_available` marks which case, so a value with no token at all is never quietly passed.

## Self-check

1. Why is validation deterministic and zero-token, and what does that buy the loop?
2. Name the two lanes and how `validate_output` bridges them.
3. What does a hardcoded hex trigger in each lane, and what does `token_available` decide?
4. From the Lab: your finding kind, your rule name, and the `token_available` sentence.

## Go deeper

- `heyhi-mcp/heyhi_mcp/core/validator.py`: the nine rules across four artifact validators, and the generated token set.
- `heyhi-mcp/heyhi_mcp/conformance/css_check.py`: the literal-versus-token finding kinds and the read-the-code brief.
- `heyhi-mcp/heyhi_mcp/tools/validate.py`: the tool that delegates into the validator.
- Architecture figure 4, [`../../docs/architecture.md`](../../docs/architecture.md), draws VALIDATE as the second verb.
- The conformance lane is where 3.4's factual predicates run, and every finding here feeds the grade in 3.3.

---

*HeyHi Confidential*
