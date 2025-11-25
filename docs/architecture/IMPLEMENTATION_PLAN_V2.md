# Campaign Generator Improvement Plan v2

## Executive Summary

Transform the campaign generator from a working prototype to production-grade code in **4 phases, ~40-50 hours** of development.

**Current State:** 2,344 lines in single file, B+ grade
**Target State:** Modular, resilient, fast, production-ready

---

## Phase 1: Quick Wins (6-8 hours)
**Goal:** Immediate reliability and visibility improvements

### 1.1 Extract JSON Utility (1 hour)
**File:** `tools/utils/json_parser.py`

Create reusable JSON extraction that handles:
- Markdown code blocks
- Balanced brace finding
- Common fixes (trailing commas, quotes)

**Replaces:** 5+ duplicate patterns at lines 360-363, 401-404, 971-977

### 1.2 Add Token Tracking (1 hour)
**File:** `tools/generate_campaign.py` lines 138-164

Track `response.usage.total_tokens` for cost visibility.

### 1.3 Fix Retry Logic (3 hours)
**File:** `tools/generate_campaign.py` lines 138-164

Error-specific handling:
- `AuthenticationError` → Don't retry
- `RateLimitError` → Exponential backoff + jitter
- `APIError 5xx` → Retry with backoff
- `BadRequestError` → Don't retry

### 1.4 Actually Regenerate Duplicate Ideas (1 hour)
**File:** `tools/generate_campaign.py` lines 1430-1433

Change from warning to action - regenerate similar ideas.

### 1.5 Config Validation (2 hours)
**File:** `tools/utils/config.py`

Dataclass-based validation with clear error messages.

---

## Phase 2: Core Architecture (8-10 hours)
**Goal:** Modular, testable, maintainable code

### 2.1 Create Module Structure (2 hours)

```
tools/
├── generate_campaign.py (orchestrator, ~200 lines)
├── core/
│   ├── __init__.py
│   ├── context.py          # CampaignContext class
│   ├── config.py           # Configuration management
│   └── client.py           # API client setup
├── phases/
│   ├── __init__.py
│   ├── research.py         # generate_research()
│   ├── ideas.py            # generate_ideas()
│   ├── scoring.py          # score_idea_independently()
│   └── production.py       # generate_production_guide()
├── integrations/
│   ├── __init__.py
│   ├── openai_client.py    # OpenAI API wrapper
│   └── veo3.py             # Veo 3 video generation
├── utils/
│   ├── __init__.py
│   ├── json_parser.py      # JSON extraction
│   ├── markdown.py         # Markdown generation
│   └── validation.py       # Document/idea validation
└── outputs/
    ├── __init__.py
    └── formatters.py       # Output formatting
```

### 2.2 Create CampaignContext (2 hours)
Central context object with:
- Config
- Stats (api_calls, tokens_used, tokens_by_phase)
- Client
- Output directory
- Current phase tracking

### 2.3 Refactor Main Orchestrator (2 hours)
Clean orchestrator that imports and calls phase modules.

### 2.4 Extract Phase Functions (4 hours)
Move each major function to its own module.

---

## Phase 3: Quality & Resilience (8-10 hours)
**Goal:** Reliable error handling and recovery

### 3.1 Implement Checkpoint Resume (3 hours)
**File:** `tools/core/checkpoint.py`

- Atomic writes (temp file then rename)
- Get resume point from checkpoint
- Skip completed phases

### 3.2 Robust JSON Parsing with Retry (2 hours)
**File:** `tools/utils/json_parser.py`

- Multiple extraction strategies
- Auto-retry with stricter prompt
- Proper error raising

### 3.3 Better Similarity Detection (2 hours)
**File:** `tools/utils/similarity.py`

- TF-IDF or n-gram based similarity
- Configurable threshold
- Actually reject/regenerate duplicates

### 3.4 Validation with Auto-Fix (3 hours)
**File:** `tools/utils/validation.py`

- Validate idea structure
- Auto-fix common issues
- Reject if still invalid

---

## Phase 4: Performance (4-6 hours)
**Goal:** Speed and efficiency improvements

### 4.1 Async File I/O (2 hours)
**Dependency:** `pip install aiofiles`

Non-blocking file writes for 15-25% speedup.

### 4.2 Rate Limiting (2 hours)
**File:** `tools/core/rate_limiter.py`

- RPM/TPM tracking
- Semaphore for max concurrent
- Auto-wait when limits approached

### 4.3 Prompt Caching (Optional, 2 hours)
**File:** `tools/utils/cache.py`

Cache responses for repeated prompts.

---

## Implementation Schedule

### Week 1: Foundation (Days 1-3)
| Day | Tasks | Hours |
|-----|-------|-------|
| 1 | 1.1 JSON utility, 1.2 Token tracking | 2 |
| 2 | 1.3 Retry logic (error-specific handling) | 3 |
| 3 | 1.4 Duplicate regeneration, 1.5 Config validation | 3 |

### Week 2: Architecture (Days 4-7)
| Day | Tasks | Hours |
|-----|-------|-------|
| 4 | 2.1 Create module structure | 2 |
| 5 | 2.2 CampaignContext class | 2 |
| 6 | 2.3 Refactor orchestrator | 2 |
| 7 | 2.4 Extract phase functions | 4 |

### Week 3: Quality (Days 8-10)
| Day | Tasks | Hours |
|-----|-------|-------|
| 8 | 3.1 Checkpoint resume capability | 3 |
| 9 | 3.2 Robust JSON parsing, 3.3 Similarity | 4 |
| 10 | 3.4 Validation with auto-fix | 3 |

### Week 4: Performance (Days 11-12)
| Day | Tasks | Hours |
|-----|-------|-------|
| 11 | 4.1 Async file I/O, 4.2 Rate limiting | 4 |
| 12 | 4.3 Caching (optional), testing, polish | 4 |

---

## Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Generation time | ~16 min | <12 min |
| API cost visibility | None | Full tracking |
| Duplicate ideas | Allowed | Auto-regenerated |
| Resume capability | None | Full checkpoint |
| Error recovery | Generic | Error-specific |
| Code maintainability | 2,344 lines/1 file | ~200 lines/file |

---

## Dependencies to Add

```txt
# requirements.txt additions
aiofiles>=23.0.0        # Async file I/O
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Breaking existing functionality | Keep original file as backup, test incrementally |
| Module import issues | Use relative imports, clear __init__.py |
| Token tracking overhead | Minimal - just reading response.usage |

---

**Created:** November 2024
**Status:** Ready for implementation
