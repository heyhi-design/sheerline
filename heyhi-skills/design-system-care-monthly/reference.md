# Design System Care Monthly: Reference

*Companion to SKILL.md. Contains the report template, baseline schema, drift log format, and scoring quick reference. Load this when generating outputs.*

---

## Monthly Report Template

---

**[Client Name] / Design System Care / [Month Year]**
*HeyHi / Month [N] of [N]*

---

### This Month

*One paragraph. What happened in the system this month. What's healthy. What needs attention. Written so someone who reads only this paragraph understands the state of the system.*

> Example (Month 1): "This is your first Design System Care cycle. We've inventoried the full system: 47 tokens across color, spacing, and typography; 23 components in the Figma library and 19 in code. The four-component gap between Figma and code is the headline finding. Your token naming is solid in the color category but inconsistent in spacing. Documentation covers about 60% of the active library. This report establishes the baseline that every future month measures against."

> Example (Month 3): "Quiet month for the system, which is good. Two new components were added (Tooltip and Badge), both in Figma and code with matching props. Token drift is minimal: one new spacing token was added with a non-semantic name that we've flagged. The Button component's focus state was updated in code but not in Figma. Documentation is current for both new components."

**Trajectory:** [Improving / Stable / Declining] since last month. [One sentence of evidence.]

---

### Token Health

**Summary:**
- Tokens added: [N] ([list names if <=5, or categories if >5])
- Tokens removed: [N]
- Tokens with changed values: [N]
- Naming violations found: [N]
- New hardcoded values found: [N] across [N] components

**Details:**

*Include only items that need attention. Don't list things that are fine.*

[For each finding worth noting:]

**[Token name or category]:** [What happened.] [Why it matters.] [Recommended action.]

**Trend:** [Is drift increasing, decreasing, or stable month-over-month? Include the last 3 months if available.]

| Month | Added | Removed | Changed | Violations | Hardcoded |
|-------|-------|---------|---------|-----------|-----------|
| [M-2] | | | | | |
| [M-1] | | | | | |
| [Current] | | | | | |

---

### Component Health

**Summary:**
- Components added: [N] ([list names])
- Components modified: [N]
- Components deprecated: [N]
- Shadow components identified: [N]
- Figma-code alignment: [N]/[total] fully aligned

**Changes this month:**

[For each changed component:]

**[Component name]:** [What changed.] [Alignment status: aligned / Figma-only / code-only / props mismatch.] [Action needed, if any.]

**Shadow components:** [List any components built outside the system. For each: where it was built, what it does, and whether it should be promoted to the library.]

---

### Documentation Status

**Coverage:** [N]% of active components have current documentation.

**Gaps identified this month:**

[For each gap:]
- **[Component or token]:** [What's missing or stale.] [Recommended action.]

**Governance adherence:** [Were the documented contribution and review processes followed for this month's changes? If not, note what was bypassed and why it matters.]

---

### Care+ Sections

*Include only for Care+ tier engagements.*

#### Figma Sync

- Last successful sync: [date]
- Pending Figma changes not yet in code: [N]
- Pending code changes not yet in Figma: [N]
- Code Connect status: [current / stale / not configured]

#### Accessibility Spot-Check

Components checked: [list the 3-5 components]

| Component | Contrast | Touch targets | Focus states | Labels | Status |
|-----------|----------|--------------|-------------|--------|--------|
| | | | | | |

[Note any regressions. If significant issues found, recommend a dedicated accessibility review.]

#### Maturity Profile

| Dimension | Score | Change | Note |
|-----------|-------|--------|------|
| Token Architecture | [1-5] | [+/-/=] | |
| Component Coverage | [1-5] | [+/-/=] | |
| Documentation & Governance | [1-5] | [+/-/=] | |
| Figma-Code Sync | [1-5] | [+/-/=] | |
| Accessibility | [1-5] | [+/-/=] | |
| Team Relationship | [1-5] | [+/-/=] | |

**Advisory warnings active:** [List any warning combinations that apply. See maturity model for definitions.]

---

### Recommendations

**This month (prioritized):**

1. [Most important action.] [Why it's first.]
2. [Second priority.] [Why.]
3. [Third priority, if applicable.]

**Looking ahead:** [What to anticipate next month based on the client's product roadmap or upcoming changes.]

**Escalations:** [Any findings that exceed monthly care scope. What they are, why they matter, and what the recommended next step is.]

---

*Prepared by HeyHi / [Date]*
*Questions: [Care lead contact]*

---

## Baseline JSON Schema

The baseline file captures the system's state at the end of each care cycle. It is the comparison point for next month.

```json
{
  "meta": {
    "client": "",
    "month": "YYYY-MM",
    "cycle_number": 1,
    "tier": "care | care+",
    "generated": "YYYY-MM-DDTHH:mm:ssZ",
    "generated_by": "design-system-care-monthly"
  },
  "tokens": {
    "total_count": 0,
    "by_category": {
      "color": { "count": 0, "names": [] },
      "spacing": { "count": 0, "names": [] },
      "typography": { "count": 0, "names": [] },
      "elevation": { "count": 0, "names": [] },
      "motion": { "count": 0, "names": [] },
      "border": { "count": 0, "names": [] }
    },
    "naming_violations": [],
    "hardcoded_values_found": 0,
    "hardcoded_locations": []
  },
  "components": {
    "total_count": 0,
    "in_figma": 0,
    "in_code": 0,
    "fully_aligned": 0,
    "figma_only": [],
    "code_only": [],
    "props_mismatch": [],
    "inventory": [
      {
        "name": "",
        "in_figma": true,
        "in_code": true,
        "alignment": "aligned | figma-only | code-only | props-mismatch",
        "props_figma": [],
        "props_code": [],
        "variants_figma": [],
        "variants_code": [],
        "documentation_status": "current | stale | missing",
        "last_modified_figma": "YYYY-MM-DD",
        "last_modified_code": "YYYY-MM-DD"
      }
    ],
    "shadow_components": []
  },
  "documentation": {
    "coverage_percent": 0,
    "components_documented": 0,
    "components_undocumented": [],
    "stale_docs": [],
    "governance_deviations": []
  },
  "maturity": {
    "token_architecture": 0,
    "component_coverage": 0,
    "documentation_governance": 0,
    "figma_code_sync": 0,
    "accessibility": 0,
    "team_relationship": 0,
    "advisory_warnings": []
  },
  "figma_sync": {
    "last_sync": "",
    "pending_figma_to_code": 0,
    "pending_code_to_figma": 0,
    "code_connect_status": "current | stale | not-configured"
  },
  "accessibility": {
    "components_checked": [],
    "regressions_found": [],
    "full_audit_recommended": false
  }
}
```

**Notes on the schema:**
- `maturity` section is populated only for Care+ tier.
- `figma_sync` and `accessibility` sections are populated only for Care+ tier.
- `shadow_components` in the components section stores components found outside the library that are candidates for promotion.
- `hardcoded_locations` stores file paths and line numbers where hardcoded values were found.
- All date fields use ISO 8601 format.

---

## Drift Log Format

The drift log captures the raw comparison between this month and last month. It is the working data that feeds the report.

```json
{
  "meta": {
    "client": "",
    "current_month": "YYYY-MM",
    "previous_month": "YYYY-MM or null if Month 1",
    "generated": "YYYY-MM-DDTHH:mm:ssZ",
    "is_baseline": false
  },
  "tokens": {
    "added": [
      { "name": "", "category": "", "value": "", "semantic": true }
    ],
    "removed": [
      { "name": "", "category": "", "previous_value": "" }
    ],
    "changed": [
      { "name": "", "category": "", "previous_value": "", "current_value": "", "intentional": null }
    ],
    "naming_violations": [
      { "name": "", "violation": "", "suggested_name": "" }
    ],
    "new_hardcoded": [
      { "file": "", "line": 0, "value": "", "should_be_token": "" }
    ]
  },
  "components": {
    "added": [
      { "name": "", "in_figma": true, "in_code": true, "documented": false }
    ],
    "modified": [
      { "name": "", "what_changed": "", "figma_updated": true, "code_updated": true }
    ],
    "deprecated": [
      { "name": "", "still_in_use": true, "usage_count": 0 }
    ],
    "shadow_components": [
      { "name": "", "location": "", "purpose": "", "promote_candidate": true }
    ],
    "alignment_changes": [
      { "name": "", "previous_status": "", "current_status": "" }
    ]
  },
  "documentation": {
    "newly_stale": [],
    "newly_documented": [],
    "gaps_from_last_month_closed": [],
    "gaps_from_last_month_still_open": []
  }
}
```

**Month 1 drift log notes:**
- Set `previous_month` to `null` and `is_baseline` to `true`.
- The `tokens.added` array contains ALL tokens (since everything is "new" relative to nothing).
- The `tokens.removed` and `tokens.changed` arrays are empty.
- The `components.added` array contains ALL components.
- The `documentation.gaps_from_last_month_closed` and `gaps_from_last_month_still_open` arrays are empty.
- This drift log is the inventory, not a diff. The report should frame it accordingly.

**`compute_drift.py` output (MCP code path).** When the MCP path runs the deterministic diff (SKILL.md § Step 2), `scripts/compute_drift.py` emits this structured month-over-month token delta. It is the machine-generated core that feeds the `tokens.added` / `tokens.removed` / `tokens.changed` arrays above; the model adds the `category`, `semantic`, and intent fields the diff cannot infer.

```json
{
  "drift_detected": true,
  "total_current": 247,
  "total_baseline": 244,
  "changed": [{ "key": "color/brand/primary/default", "previous": "...", "current": "..." }],
  "added":   [{ "key": "spacing/component/card-padding-compact", "value": "8px" }],
  "removed": [{ "key": "color/feedback/warning-subtle", "previous": "..." }]
}
```

Keys are slash-joined paths from the flattened variable manifest, sorted for stable month-over-month diffs. Pass this delta to the report step; do not load both manifests into context.

---

## Component Change Log Format

Use this format when documenting component changes in the report. One entry per component that changed.

```
### [Component Name]

**Change:** [What happened]
**When:** [Date or date range]
**Figma:** [Updated / Not updated / N/A]
**Code:** [Updated / Not updated / N/A]
**Props alignment:** [Aligned / Mismatch: (describe)]
**Documentation:** [Updated / Needs update / Missing]
**Action:** [None needed / Update Figma / Update code / Update docs / Review needed]
```

---

## Month-Over-Month Comparison Template

Include this starting in Month 2 (with Month 1 baseline + Month 2 current). Expand to a 3-month view when Month 3 data is available. Month 1 reports do not include this section.

```
### System Trend (Last 3 Months)

| Metric | [M-2] | [M-1] | [Current] | Direction |
|--------|-------|-------|-----------|-----------|
| Total tokens | | | | |
| Naming violations | | | | |
| Hardcoded values | | | | |
| Total components | | | | |
| Fully aligned | | | | |
| Shadow components | | | | |
| Doc coverage % | | | | |

Overall: [The system is {improving/stable/declining}. {One sentence explaining the trend.}]
```

---

## Maturity Dimension Scoring Quick Reference

Score each dimension 1-5 using the Design System Maturity Model definitions. This is a condensed reference for monthly scoring. For the full dimension descriptions and level definitions, see `ai-services/design-intelligence/design-system-maturity-model.md`.

| Score | Level | One-line summary |
|-------|-------|-----------------|
| 1 | Ad Hoc | No systematic approach. Local decisions, no shared standards. |
| 2 | Established | Foundation exists. Basic, centralized, some documentation. |
| 3 | Systematic | Semantic, governed, consistent. Treated as infrastructure. |
| 4 | Automated | Tooling validates. Measured in CI/CD. Data-informed decisions. |
| 5 | Intelligent | Machine-queryable. Agents validate against rules. |

**Advisory warning pairs to check each month:**
- Token/Component at 5, Governance at 1-2: generation without governance
- Token/Sync at 4, Accessibility at 1-2: automation without accessibility
- Any dimension at 5, Sync/Token below 4: intelligent tooling without measurement
- Token/Component at 3+, Team Relationship at 1-2: strong infrastructure, weak adoption

---

## Shadow Component Promotion Criteria

A shadow component is a "promote candidate" if it meets these conditions:
- Used in two or more feature areas (not a one-off)
- Meets the accessibility baseline (contrast, touch targets, focus states, labels)
- Ready for documentation (purpose and usage are clear enough to write up)
- Team consensus exists on the design (no active debate about whether this is the right approach)

If all four conditions are met, recommend promotion in the monthly report. If conditions are partially met, note what's needed before promotion.

---

## Escalation Criteria

Use these thresholds to decide when a finding exceeds monthly care scope.

| Condition | Action |
|-----------|--------|
| Maturity dimension drops 2+ levels in one month | Flag for client conversation. May indicate team or organizational change. |
| Token architecture needs structural rebuild | Scope a Build engagement. Monthly care can't fix foundational issues. |
| Shadow components exceed 30% of library | The system isn't meeting the team's needs. Scope a component coverage Build. |
| Team relationship signals active workaround | Discuss with client. May need Org Consulting before more system work. |
| 3+ accessibility regressions in one month | Recommend a dedicated accessibility audit. |
| Figma-code sync has been broken for 2+ consecutive months | Escalate pipeline repair as a separate scoped task. |

---

## File Naming Conventions

All care deliverables follow this pattern:

```
<engagement folder>/deliverables/care/
  care-report-YYYY-MM.md          (or .docx)
  baseline-YYYY-MM.json
  drift-log-YYYY-MM.json
```

Example for a client called "acme-corp" in March 2026:
```
<engagement folder for acme-corp>/deliverables/care/
  care-report-2026-03.md
  baseline-2026-03.json
  drift-log-2026-03.json
```

Previous months' files are never overwritten. The accumulation is the value.

---

*Companion to design-system-care-monthly/SKILL.md*
*Cross-reference: ai-services/design-intelligence/design-system-maturity-model.md, recurring-revenue/productized-services.md, heyhi-design-intelligence-audit/reference.md*

*HeyHi Confidential*
