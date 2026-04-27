# Daily Reflection Tree – Deterministic Design

## Overview
This project implements a **deterministic decision tree** for daily reflection.  
The goal is to guide a user through structured self-reflection using **fixed choices**, **clear branching**, and **no generative output**.

The system is designed around three psychological axes:
1. **Agency (Internal vs External)**
2. **Contribution (Contribution vs Entitlement)**
3. **Radius (Self vs Others / Alto)**

Each axis builds on the previous one, moving from:
- “What did I control?”
→ “What did I give?”
→ “Who else was impacted?”

---

## Structure

### 1. Tree (JSON)
- File: `tree/reflection-tree.json`
- Fully deterministic
- Each node has:
  - `id`
  - `type` (start / question / decision / reflection / bridge / summary / end)
  - `options` (fixed choices only)
  - `routing` (explicit branching rules)

### 2. Engine (Python)
- File: `agent/app.py`
- Loads JSON and executes the tree
- Tracks:
  - user responses
  - axis signals
- Produces a final structured summary

---

## Deterministic Design Principles

- No free text input
- No LLM used at runtime
- Every path is predefined
- Every decision is traceable
- No randomness

---

## Guardrails Against Hallucination

- JSON is treated as the **single source of truth**
- No dynamic generation of text
- All transitions use:
  - `matchSource`
  - `matchValues`
  - `target`
- Summary uses predefined templates (`summarySegments`)

---

## Design Thinking

### Axis 1 – Agency
Focus: control vs reaction  
Goal: shift attention from outcome → choice

### Axis 2 – Contribution
Focus: giving vs expecting  
Goal: reveal motivation behind actions

### Axis 3 – Radius
Focus: self vs others  
Goal: expand awareness beyond individual experience

---

## Key Insight
The tree is not just a questionnaire—it is a **progressive narrowing of attention**:
- From events → to behavior → to perspective

---

## How to Run

```bash
cd agent
python app.py --tree ../tree/reflection-tree.json
```
---

## Output
- Interactive CLI reflection
- Final summary based on dominant axis signals

---

## Notes
This system was designed using AI as a tool, but:
- All structure was manually verified
- All branching logic was explicitly controlled
- All outputs are deterministic