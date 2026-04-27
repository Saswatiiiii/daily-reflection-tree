# Design Explanation – Daily Reflection Tree

## Approach

I approached this as a **behavioral system design problem**, not just a questionnaire.

Instead of asking generic questions, I structured the flow to:
1. Anchor the user in a real moment (OPEN_Q)
2. Split based on emotional direction (positive vs negative)
3. Progress through three axes of reflection

---

## Why Deterministic?

A deterministic system ensures:
- Consistency across users
- Traceable reasoning
- No hallucination

Every outcome is explainable based on:
- user choices
- predefined logic

---

## Tree Design Strategy

### 1. Progressive Depth
Each axis increases abstraction:

| Axis | Focus | Depth |
|------|------|------|
| A1 | Control | Immediate behavior |
| A2 | Contribution | Motivation |
| A3 | Radius | Perspective |

---

### 2. Decision Nodes
Each decision node uses:

- `matchSource`: where answer came from  
- `matchValues`: what to match  
- `target`: next node  

This ensures:
→ zero ambiguity  
→ full determinism  

---

### 3. Reflection Nodes
Reflections are:
- non-judgmental
- observational
- slightly open-ended

Goal:
→ not to “correct” the user  
→ but to **surface awareness**

---

## Handling AI Usage

I used AI to:
- brainstorm phrasing
- explore variations of questions

But I did NOT:
- blindly accept outputs
- generate the full tree automatically

---

## Where I Disagreed with AI

- AI tended to:
  - oversimplify questions
  - make reflections too generic
  - remove nuance

I manually:
- rewrote reflections to sound more human
- introduced ambiguity where needed
- preserved emotional realism

---

## Negative Prompting

To control AI outputs, I used constraints like:
- “avoid generic motivational tone”
- “do not give advice”
- “do not conclude the user’s state”
- “focus on observation, not correction”

---

## Final Thought

This system is not about giving answers.

It is about:
→ structuring attention  
→ guiding awareness  
→ enabling reflection  
