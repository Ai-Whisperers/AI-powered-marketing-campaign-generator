# Campaign Generator - Implementation Plan

## Overview

This document outlines the detailed implementation plan for improving the campaign generator tool. The improvements are organized into 4 phases, each building on the previous one.

**Estimated Total Time: 8-12 hours of development**

---

## Phase 1: Quick Wins (2-3 hours)
*Foundation improvements that provide immediate value*

### 1.1 Research Consolidation Document
**Goal:** Create a synthesized document that combines key insights from all research for idea generation

**Tasks:**
- [ ] Add `generate_research_consolidation()` function
- [ ] Extract key insights from each research document
- [ ] Create `CONSOLIDADO-PARA-IDEAS.md` with:
  - Top 10 consumer insights
  - 5 cultural tensions to leverage
  - 3 competitive opportunities
  - Key statistics summary
  - Recommended creative territories
- [ ] Generate this after all research documents are complete

**Code Location:** After research loop, before ideas generation

```python
async def generate_research_consolidation(research_docs: dict, brief_content: str) -> str:
    """Synthesize all research into actionable creative brief"""
    # Compile all research content
    # Generate consolidated insights
    # Return markdown document
```

### 1.2 Improved Idea Structure
**Goal:** Add territories, taglines, and better organization to ideas

**Tasks:**
- [ ] Update idea JSON schema to include:
  - `territory`: (e.g., "Humor", "Emocional", "Educativo")
  - `tagline`: Slogan or tagline for the idea
  - `key_visual`: Description of hero visual
  - `call_to_action`: Primary CTA
  - `hashtags`: Suggested hashtags
- [ ] Update idea prompt to request these fields
- [ ] Update markdown template for new fields

**New Idea Schema:**
```python
idea_schema = {
    "title": str,
    "territory": str,  # NEW
    "tagline": str,  # NEW
    "concept": str,
    "insight": str,
    "key_visual": str,  # NEW
    "execution": {
        "redes_sociales": str,
        "video": str,
        "activacion": str
    },
    "call_to_action": str,  # NEW
    "hashtags": list,  # NEW
    "why_it_works": str
}
```

### 1.3 Basic Quality Validation
**Goal:** Validate generated content before saving

**Tasks:**
- [ ] Add `validate_research_doc()` function:
  - Check minimum word count (800 words)
  - Verify headers are present
  - Check for placeholder text
- [ ] Add `validate_idea()` function:
  - Verify all required fields present
  - Check concept clarity (not too vague)
  - Verify insight is from research
- [ ] Log warnings for quality issues

---

## Phase 2: Core Improvements (3-4 hours)
*Major architectural improvements for better output quality*

### 2.1 Phased Research with Context Accumulation
**Goal:** Each research phase builds on previous phases for coherent output

**Tasks:**
- [ ] Define research phases:
  1. **Foundation:** Market + Brand (no context needed)
  2. **Competitive:** Competition (uses Foundation)
  3. **Consumer:** Target audience (uses Foundation + Competitive)
  4. **Cultural:** Local context (uses Consumer)
  5. **Creative:** References (uses all above)
- [ ] Modify generation loop to pass context between phases
- [ ] Create context summary for each phase

**Implementation:**
```python
research_phases = [
    {
        "name": "foundation",
        "categories": ["01-mercado-general", "02-marca"],
        "context_from": []
    },
    {
        "name": "competitive",
        "categories": ["03-competencia"],
        "context_from": ["foundation"]
    },
    {
        "name": "consumer",
        "categories": ["04-consumidor"],
        "context_from": ["foundation", "competitive"]
    },
    {
        "name": "cultural",
        "categories": ["05-cultura-local"],
        "context_from": ["consumer"]
    },
    {
        "name": "creative",
        "categories": ["06-estadisticas", "07-referencias", "08-investigacion-creativa"],
        "context_from": ["foundation", "consumer", "cultural"]
    }
]
```

### 2.2 Idea Scoring and Ranking
**Goal:** Score each idea and rank them for easy prioritization

**Tasks:**
- [ ] Define scoring criteria:
  - `relevancia_brief`: 0-10 (alignment with objectives)
  - `originalidad`: 0-10 (uniqueness in category)
  - `ejecutabilidad`: 0-10 (production feasibility)
  - `conexion_cultural`: 0-10 (local relevance)
  - `potencial_viral`: 0-10 (shareability)
- [ ] Add scoring to idea generation prompt
- [ ] Calculate weighted average (overall_score)
- [ ] Add tier classification:
  - Tier A (8.0+): Priority for presentation
  - Tier B (6.0-7.9): Strong alternates
  - Tier C (4.0-5.9): Development needed
- [ ] Sort ideas by score in output

**Scoring Weights:**
```python
scoring_weights = {
    "relevancia_brief": 0.25,
    "originalidad": 0.20,
    "ejecutabilidad": 0.20,
    "conexion_cultural": 0.20,
    "potencial_viral": 0.15
}
```

### 2.3 Ideas Comparison Matrix
**Goal:** Generate a visual comparison of all ideas

**Tasks:**
- [ ] Create `MATRIZ-COMPARATIVA.md`
- [ ] Table with all ideas and scores
- [ ] Quick-view of territories covered
- [ ] Highlight top 5 recommendations
- [ ] Show diversity of approaches

---

## Phase 3: Advanced Features (2-3 hours)
*Performance and quality enhancements*

### 3.1 Parallel Generation with asyncio.gather
**Goal:** Generate independent documents simultaneously for speed

**Tasks:**
- [ ] Identify parallelizable tasks:
  - Documents within same phase
  - Ideas within same territory
- [ ] Implement parallel generation:
  ```python
  async def generate_phase_parallel(phase_docs):
      tasks = [generate_doc(doc) for doc in phase_docs]
      results = await asyncio.gather(*tasks)
      return results
  ```
- [ ] Add rate limiting to avoid API limits
- [ ] Maintain order in output

### 3.2 Idea Refinement Sub-flow
**Goal:** Improve low-scoring ideas automatically

**Tasks:**
- [ ] For ideas scoring 4.0-6.0:
  - Identify weak areas from scores
  - Generate improvement prompt
  - Re-generate with specific feedback
- [ ] Limit to 2 refinement attempts per idea
- [ ] Track original vs refined versions
- [ ] Only keep refined if score improves

**Implementation:**
```python
async def refine_idea(idea: dict, feedback: str) -> dict:
    """Attempt to improve a weak idea"""
    prompt = f"""
    Esta idea necesita mejoras:
    {json.dumps(idea)}

    Áreas débiles: {feedback}

    Mejora la idea manteniendo el concepto central pero
    fortaleciendo las áreas débiles.
    """
    # Generate improved version
    # Score new version
    # Return better of two
```

### 3.3 Production Guide Generation
**Goal:** Create actionable production specifications

**Tasks:**
- [ ] Generate `GUIA-PRODUCCION.md` for top 5 ideas
- [ ] Include for each idea:
  - Talent requirements
  - Location suggestions
  - Props and wardrobe
  - Music/sound direction
  - Estimated budget tier (Low/Medium/High)
  - Timeline estimate
- [ ] Technical specifications per format

---

## Phase 4: Polish (1-2 hours)
*Final touches and user experience improvements*

### 4.1 Executive Summary Document
**Goal:** One-page overview for client presentation

**Tasks:**
- [ ] Create `RESUMEN-EJECUTIVO-FINAL.md`
- [ ] Include:
  - Campaign objective (1 sentence)
  - Strategic approach (3 bullets)
  - Top 3 idea recommendations with thumbnails
  - Key metrics to track
  - Next steps
- [ ] Keep under 500 words

### 4.2 Media Plan Skeleton
**Goal:** Basic media distribution plan

**Tasks:**
- [ ] Create `PLAN-MEDIOS-SUGERIDO.md`
- [ ] Platform recommendations by idea
- [ ] Suggested posting schedule
- [ ] Format specifications per platform
- [ ] Budget allocation suggestions

### 4.3 Progress Tracking
**Goal:** Real-time progress feedback during generation

**Tasks:**
- [ ] Add progress bar or percentage
- [ ] Show estimated time remaining
- [ ] Log each completed step with timestamp
- [ ] Summary at end with timing stats

### 4.4 Error Resilience
**Goal:** Handle API errors gracefully

**Tasks:**
- [ ] Add retry logic (3 attempts with backoff)
- [ ] Save partial progress on failure
- [ ] Generate placeholder for failed docs
- [ ] Error log with context for debugging
- [ ] Resume capability from last checkpoint

---

## Implementation Order

### Week 1: Foundation
1. **Day 1-2:** Phase 1 (Quick Wins)
   - Research consolidation
   - Improved idea structure
   - Basic validation

### Week 2: Core
2. **Day 3-4:** Phase 2.1 (Phased Research)
   - Context accumulation
   - Phase definitions

3. **Day 5:** Phase 2.2-2.3 (Scoring & Matrix)
   - Scoring system
   - Comparison matrix

### Week 3: Advanced & Polish
4. **Day 6:** Phase 3.1-3.2 (Parallel & Refinement)
   - Async optimization
   - Idea refinement

5. **Day 7:** Phase 3.3 + Phase 4 (Production + Polish)
   - Production guide
   - Executive summary
   - Progress tracking

---

## Success Metrics

After implementation, the generator should:

1. **Quality:** 80%+ of ideas score 6.0+ on first generation
2. **Speed:** Full campaign generated in <15 minutes
3. **Coherence:** Research themes appear in ideas
4. **Diversity:** At least 4 different territories covered
5. **Usability:** Output ready for client presentation

---

## File Structure After Implementation

```
campaign-{brand}-{date}/
├── README.md
├── investigacion/
│   ├── 01-mercado-general/
│   ├── 02-marca/
│   ├── 03-competencia/
│   ├── 04-consumidor/
│   ├── 05-cultura-local/
│   ├── 06-estadisticas/
│   ├── 07-referencias/
│   ├── 08-investigacion-creativa/
│   ├── CONSOLIDADO-PARA-IDEAS.md      # NEW
│   ├── RESUMEN-EJECUTIVO.md
│   └── INSIGHTS-CREATIVOS.md
├── ideas/
│   ├── idea-01-*.md
│   ├── idea-02-*.md
│   ├── ...
│   ├── 00-RESUMEN-IDEAS.md
│   └── MATRIZ-COMPARATIVA.md          # NEW
├── produccion/                         # NEW
│   ├── GUIA-PRODUCCION.md
│   └── PLAN-MEDIOS-SUGERIDO.md
└── RESUMEN-EJECUTIVO-FINAL.md         # NEW
```

---

## Next Steps

1. Review this plan and confirm priorities
2. Start with Phase 1 implementation
3. Test after each phase with sample brief
4. Iterate based on output quality

---

**Created:** November 2024
**Status:** Ready for implementation
