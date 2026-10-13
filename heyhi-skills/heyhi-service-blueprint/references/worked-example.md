---
classification: confidential
title: "Worked example — Service Blueprint Pack (synthetic: white-glove furniture delivery)"
version: "0.1.0"
updated: "2026-09-07"
note: "SYNTHETIC input. No client content. Calibration only — read for register and depth of the free-prose surfaces; do not copy the findings."
---

# Worked example (synthetic) — white-glove furniture delivery + assembly

**Synthetic engagement. Invented service, no client content.** Read this to calibrate the register and the depth of the open-questions and near-misses surfaces, and to see the provenance discipline in action. Do not copy its findings.

**The journey the human brought (synthetic):** a customer buys a sofa online, chooses "white-glove delivery + assembly," gets a scheduling window, receives a reminder, is home for a two-person crew who deliver and assemble the sofa and remove the packaging, then gets a follow-up email asking for a review.

---

# Service Blueprint Pack — White-glove furniture delivery + assembly · as of [UNCONFIRMED — hypothesis]
Journey input: 5-step post-purchase delivery journey (order → schedule → reminder → delivery+assembly → follow-up)     Owner: ____     Ops confirmer: ____ (a delivery-operations lead — NOT YET NAMED)

## The scaffold (five swim-lanes + three separators, per the foundation's structure canon)

| Step → | 1. Order placed | 2. Window scheduled | 3. Reminder | 4. Delivery + assembly | 5. Follow-up |
|--------|-----------------|---------------------|-------------|------------------------|--------------|
| **Physical evidence** | order confirmation screen | scheduling email + calendar hold | SMS reminder | the sofa; crew uniforms; the assembled result | review-request email |
| **Customer actions (the journey)** | selects white-glove at checkout | picks a delivery window | confirms / reschedules | is home; lets crew in; inspects | reads email; maybe reviews |
| — line of interaction — |
| **Frontstage contact** | checkout UI | scheduling UI + auto-email | SMS | the two-person delivery crew | the review email `inferred` (who sends it?) |
| — line of visibility — (load-bearing) |
| **Backstage contact** | [candidate] order-routing clerk assigns to a regional hub `assumption` | [candidate] a dispatcher slots the crew `assumption` | [candidate] a system (or a person?) triggers the SMS `assumption` | [candidate] crew lead reports completion `assumption` | [candidate] a CRM enqueues the review email `assumption` |
| — line of internal interaction — |
| **Support processes** | warehouse inventory system `assumption` (the order screen hints at stock, but a customer-facing screen is not ops confirmation) | third-party logistics scheduling API `assumption` | SMS gateway vendor `assumption` | route/manifest system + assembly-crew staffing `assumption` | reviews platform integration `assumption` |

Frontstage rows are drafted from the journey; the follow-up sender is tagged `inferred` (the journey shows the email arrives, not who sends it).

## Provenance ledger (every cell is evidence-linked or assumption-marked)

| Cell | Lane | evidence-linked (source) / assumption | note |
|------|------|---------------------------------------|------|
| warehouse inventory (live-stock display) | Support (step 1) | `assumption` — the order screen shows "in stock, ships from [hub]", which is tempting, but a customer-facing screen is a frontstage cue, not ops confirmation of the backstage system | the discipline resists the tempting frontstage signal; ops confirms the backstage, the UI does not |
| order-routing clerk | Backstage (step 1) | `assumption` | could be fully automated; nobody confirmed a human is in this loop |
| third-party logistics scheduling API | Support (step 2) | `assumption` | the scheduling UI implies an integration; the vendor and its SLA are unconfirmed |
| dispatcher slots the crew | Backstage (step 2) | `assumption` | central dispatch vs. hub-local is unknown — a real fork for where a delay originates |
| SMS trigger (system or person) | Backstage (step 3) | `assumption` | if a person triggers it, the reminder has a staffing dependency the journey hides |
| assembly-crew staffing | Support (step 4) | `assumption` | the single biggest cost and failure driver, entirely below the line and entirely unconfirmed |
| CRM enqueues review email | Backstage (step 5) | `assumption` | and the `inferred` frontstage sender depends on it |

## Candidate backstage / support steps (ALL flagged `assumption` until confirmed)

Every below-the-line cell above is a candidate (the live-stock cue included — a frontstage signal does not exempt a backstage cell from confirmation). Named so the ops confirmer can strike, correct, or confirm each — not asserted.

## Open questions for ops (questions, not judgments)

- Is crew scheduling central or hub-local? (Where a missed window originates depends on the answer — a real root-cause fork.)
- Is the delivery step one team or two handoffs (a driver, then an assembler)? The journey shows one crew; the backstage may be two.
- Who owns the reschedule path when the customer moves the window — the logistics vendor's system, or a back-office queue nobody named?
- Is the review email transactional-automated, or does a marketing team send it? (Determines whether the `inferred` frontstage cell has a human dependency.)

## Near-misses and unchecked territory (the blueprint journey, made inspectable)

- Considered, set aside: assumed a nightly batch reconciled the logistics vendor's status back to the order system — **struck**, no evidence it exists; logged as an open question instead of a cell.
- Almost asserted: "a dispatcher slots the crew" read like a fact from the smooth scheduling UI — pulled back to `assumption`; a smooth UI is not evidence of the backstage behind it.
- Could not check: whether the assembly crew is employed or contracted (an SLA-vs-employment distinction that changes the whole support lane) — outside the journey.

## ⛔ Backstage confirmation — NEEDS OPS IN THE ROOM (the named gate; every `assumption` cell resolves here)
This slot is intentionally empty. All seven below-the-line cells are `assumption` — the human brought only a journey, so there is no operational source to evidence-link to, and even the tempting live-stock cue does not earn a confirmation. Until a delivery-operations lead confirms the real staffing, systems, and SLAs, **this blueprint is a hypothesis of the service, not a map of it** — and it says so in its own header ("as of [UNCONFIRMED — hypothesis]").

## ⛔ Line-of-visibility placement (where contested) — NEEDS HUMAN
(The delivery crew is frontstage; whether the crew *lead's completion report* is a backstage action or a frontstage courtesy — "we're done, here's your receipt" — is genuinely ambiguous and left for the human.)

## ⛔ Operational root-cause to fix — NEEDS HUMAN
## ⛔ The service verdict (is this service working; what to redesign) — NEEDS HUMAN

## Named gate
Ops confirmation (the person who owns the backstage reality): ____________  Date: ______
No backstage cell is recorded as fact, and no root-cause or verdict is rendered, until this line is signed.

---

*HeyHi Confidential. Synthetic worked example for `heyhi-service-blueprint`. No client content. Method canon: `sheerline/os/foundations/service-design/FOUNDATION.md`; recipe: `references/blueprint-canon.md`.*
