# UX Writing Intake Guide

**`ui-studio-onboard/templates` · Phase 5 manual intake · March 2026**

*Use this guide when UX writing guidelines are not available in Supernova or Figma documentation frames. Walk through each slot with the designer or product owner. Each answer populates one slot in `ux_writing` in the brand config.*

---

## How to Use This Guide

1. Share this document with the designer or product owner before the session
2. Walk through each slot — ask the question, capture the pattern
3. For each populated slot, note the source (style guide page, design spec, verbal confirmation)
4. After filling in all slots, paste the answers into the `ux_writing` block in the config

Not every slot needs an answer immediately. Incomplete slots can be filled later — they affect the completeness score but don't block Mode B builds.

---

## Slot 1: Empty States

**What to ask:**
When a user sees a screen with no content yet — an empty list, zero results, a first-time state — what should the message say?

**Things to understand:**
- Should the message state what's missing, or invite action, or both?
- Is there a specific verb style for the action (e.g., "Create your first project" vs "No projects yet. Add one to get started.")?
- What's the tone — encouraging, neutral, instructional?
- Are there specific phrases this brand avoids in empty states?

**Capture:**
```
Pattern: [how the message is structured]
Example: [a real or sample empty state message from the brand]
Avoid: [any patterns this brand explicitly won't use]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Slot 2: Error Messages

**What to ask:**
When something goes wrong — a failed network request, a validation error, a system error — what should the message say?

**Things to understand:**
- Should the message always include a next step, or sometimes just explain what happened?
- What's the tone — apologetic, matter-of-fact, calm, urgent?
- Is there a maximum length for error messages?
- Does the brand avoid "Oops," "Sorry," or similar words?
- How should validation errors differ from system errors?

**Capture:**
```
Pattern: [overall approach to error messages]
Tone: [how they should sound]
Structure: [sentence format, e.g., "[What failed]. [Next step]."]
Example: [a real or sample error message]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Slot 3: Tooltips

**What to ask:**
When a user hovers or focuses on an element and sees a tooltip — what should it say and how long can it be?

**Things to understand:**
- Is there a character or word limit?
- Should tooltips describe what a UI element does, or explain why someone would use it?
- Should they start with a verb ("Exports the current view as CSV") or a noun phrase ("CSV export")?
- Are there specific patterns to avoid (e.g., restating the button label)?

**Capture:**
```
Max length: [characters or "none specified"]
Tone: [terse, friendly, instructional]
Structure: [e.g., "Verb + what it does" or "Noun phrase"]
Avoid: [specific patterns not to use]
Example: [a real or sample tooltip]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Slot 4: Buttons and CTAs

**What to ask:**
What verbs and patterns does this brand use for buttons and primary calls to action?

**Things to understand:**
- Does the brand prefer generic verbs (Submit, Save, Continue) or specific outcome verbs (Deploy, Connect, Archive)?
- Should CTAs describe the action or the outcome?
- Is there a house style for button capitalization (sentence case, title case, ALL CAPS)?
- Are there any words or patterns this brand explicitly avoids on buttons?

**Capture:**
```
Verb preference: [specific vs. generic; examples of preferred verbs]
Style: [how CTAs sound — commanding, inviting, descriptive]
Capitalization: [sentence case, title case, ALL CAPS]
Examples: [3-5 real or sample button labels]
Avoid: [words or patterns not to use]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Slot 5: Form Labels

**What to ask:**
How does this brand write the labels and helper text for form fields?

**Things to understand:**
- What's the capitalization rule for field labels (sentence case, title case)?
- Does the brand use helper text? If so, is it instructional or format guidance only?
- What's the policy on placeholder text — is it used as a label substitute, a format example, or not at all?
- How are validation messages styled (e.g., "This field is required" vs "Required" vs "Please fill in your name")?

**Capture:**
```
Label case: [sentence case, title case, ALL CAPS]
Helper text style: [format guidance only / instructional / none]
Placeholder policy: [format example / never / sparingly]
Validation style: [how validation messages sound]
Examples: [2-3 real or sample form labels with helper text]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Slot 6: Notifications

**What to ask:**
When the system sends a toast or banner notification — success, error, warning, info — what should each type say and how should it sound?

**Things to understand:**
- Should success notifications confirm the action (past tense: "Saved") or celebrate it ("Your file is saved!")?
- Should error notifications just describe what failed, or include a path forward?
- Is there a maximum length for toast notifications?
- What's the tone difference between these four types for this brand?

**Capture:**
```
Success: [structure and tone for success messages]
Error: [structure and tone for error messages]
Warning: [structure and tone for warning messages]
Info: [structure and tone for info messages]
Examples: [one real or sample message per type]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Slot 7: Loading States

**What to ask:**
When the system is processing something and the user is waiting — what should the message say?

**Things to understand:**
- Should loading messages be action-specific ("Saving your work...") or generic ("Loading...")?
- Does the brand use an ellipsis in loading messages?
- Are there any loading message patterns this brand explicitly avoids?
- Should messages change if loading takes longer than expected?

**Capture:**
```
Pattern: [general approach — action-specific vs. generic]
Ellipsis: [yes / no / sometimes]
Examples: [3-5 real or sample loading messages]
Avoid: [patterns not to use]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Slot 8: Onboarding

**What to ask:**
When a new user is going through the onboarding or setup flow — what's the tone and structure of the copy?

**Things to understand:**
- Is the tone encouraging and hand-holding, or confident and efficient?
- Is there a preferred step structure (one action per step, or multiple tasks per step)?
- Should step titles be imperatives ("Connect your account") or descriptive ("Step 1: Account connection")?
- Does the brand use progress indicators, and if so, what language accompanies them?
- Are there specific phrases this brand uses to mark milestones or completion?

**Capture:**
```
Tone: [how onboarding copy sounds]
Structure: [one action per step / multi-task / other]
Step format: [imperative / descriptive / other]
Progress language: [how progress is communicated]
Completion language: [what happens when a step or the whole flow is done]
Examples: [2-3 real or sample onboarding steps]
Source: [style guide page, verbal confirmation, etc.]
```

---

## Additional Custom Slots

If the brand has UX writing patterns not covered by the eight standard slots, document them here:

```
Slot name: [describe what context this covers]
Pattern: [the rule or approach]
Examples: [real or sample copy]
Source: [where this comes from]
```

---

*HeyHi Internal Use Only. Created March 25, 2026.*
