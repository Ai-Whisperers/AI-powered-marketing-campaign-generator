# Changelog

All notable changes to Marketing Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial release of Marketing Agent
- Automated research system with GPT Researcher
- Two-phase ideation generating 13 strategic fields
- Brand context service for Nestlé visual identity
- Batch video agent for Veo 3.1 integration
- Hybrid Groq/OpenAI AI provider system
- Intelligent caching (80%+ time savings)
- CLI interface with multiple commands
- Comprehensive documentation

### Features

- `generate` - Generate campaign ideas
- `generate-branded-videos` - Create Veo 3.1 videos with branding
- `score` - Score and rank ideas
- Dry-run mode for cost estimation
- Prompts-only mode for video generation

## [1.0.0] - 2024-11-26

### Added

- Core campaign generation workflow
- Multi-source research automation
- AI-powered ideation system
- Video generation integration
- Brand guidelines automation
- Cost optimization with Groq
- Professional documentation

### Changed

- Migrated from single-phase to two-phase ideation
- Switched from OpenAI-only to hybrid Groq/OpenAI
- Improved error handling and fallback logic

### Fixed

- JSON parsing errors with AI responses
- Critic node handling of list responses
- AIProviderError instantiation bugs

---

## Version History

- **1.0.0** - Initial release with core features
- **Unreleased** - Ongoing development

## Migration Guides

### From 0.x to 1.0

1. Update `.env` with new provider settings:

   ```bash
   AI_PRIMARY_PROVIDER=groq
   AI_FALLBACK_PROVIDER=openai
   ```

2. Add Groq API key:

   ```bash
   GROQ_API_KEY=your_key_here
   ```

3. Update CLI commands (if using old syntax)

## Deprecations

None yet.

## Security

See [SECURITY.md](SECURITY.md) for security-related changes.
