# Changelog

All notable changes to **IntlQ** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Dual NLP scoring: TF-IDF cosine similarity + keyword coverage
- 8 job role question banks
- Confidence interval scoring with percentile benchmarks
- Pytest test suite for scoring algorithms

### Fixed
- Fixed stopword removal causing false negatives in technical terms

### Changed
- Keyword matching now uses stemmed token comparison

---

## [1.0.0] - 2025-01-01

### Added
- Initial public release of IntlQ.
- Core feature implementation.
- README and project documentation.
- GitHub Actions CI pipeline.

[Unreleased]: https://github.com/LAKSHYA-NIGAM/IntlQ/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/LAKSHYA-NIGAM/IntlQ/releases/tag/v1.0.0
