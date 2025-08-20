# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Common Changelog](https://common-changelog.org/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

- update grouping algorithm to use day in US Central as the first part of unique grouping identifier ([#177](https://github.com/nasa/batchee/pull/177))([**@ank1m**](https://github.com/ank1m))

## [1.3.0] - 2024-11-19

### Changed

- update pre commit: to autoupdate and with gitleaks ([#147](https://github.com/nasa/batchee/pull/147))([**@danielfromearth**](https://github.com/danielfromearth))

## [1.2.0] - 2024-06-27

### Changed

- Increase continuous integration/unit test coverage ([#128](https://github.com/nasa/batchee/issues/128))([**@danielfromearth**](https://github.com/danielfromearth))

### Added

- Group dependabot updates into fewer PRs ([#127](https://github.com/nasa/batchee/issues/127))([**@danielfromearth**](https://github.com/danielfromearth))
- Add autoupdate schedule for pre-commit ([#129](https://github.com/nasa/batchee/issues/129))([**@danielfromearth**](https://github.com/danielfromearth))

## [1.1.0] - 2024-05-01

### Added

- Add badges to the readme ([#114](https://github.com/nasa/batchee/issues/114))([**@danielfromearth**](https://github.com/danielfromearth))

## [1.0.0] - 2024-04-23

### Changed

- Rename from concat_batcher to batchee ([#11](https://github.com/nasa/batchee/issues/11))([**@danielfromearth**](https://github.com/danielfromearth))
- Improve CICD workflows ([#21](https://github.com/nasa/batchee/issues/21))([**@danielfromearth**](https://github.com/danielfromearth))
- Change Adapter output from single to multiple STAC Catalogs ([#41](https://github.com/nasa/batchee/issues/41))([**@danielfromearth**](https://github.com/danielfromearth))

### Added

- Create Adapter code that processes a Harmony Message and STAC Catalog ([#6](https://github.com/nasa/batchee/issues/6))([**@danielfromearth**](https://github.com/danielfromearth))
- Create working Docker image ([#7](https://github.com/nasa/batchee/issues/7))([**@danielfromearth**](https://github.com/danielfromearth),[**@hpatel426**](https://github.com/hpatel426))
- Add simple command line interface for testing ([#13](https://github.com/nasa/batchee/issues/13))([**@danielfromearth**](https://github.com/danielfromearth))
- Add a logo ([#16](https://github.com/nasa/batchee/issues/16))([**@danielfromearth**](https://github.com/danielfromearth))
- Add Docker build steps to GitHub Actions workflow ([#75](https://github.com/nasa/batchee/pull/75))([**@danielfromearth**](https://github.com/danielfromearth))
- Add readme badges ([#84](https://github.com/nasa/batchee/pull/84))([**@danielfromearth**](https://github.com/danielfromearth))
- Add license ([#100](https://github.com/nasa/batchee/pull/100))([**@danielfromearth**](https://github.com/danielfromearth))
- Add codecov to CI pipeline ([#111](https://github.com/nasa/batchee/pull/111))([**@danielfromearth**](https://github.com/danielfromearth))
- Add SNYK and PyPI to CI pipeline ([#112](https://github.com/nasa/batchee/pull/111))([**@danielfromearth**](https://github.com/danielfromearth))
