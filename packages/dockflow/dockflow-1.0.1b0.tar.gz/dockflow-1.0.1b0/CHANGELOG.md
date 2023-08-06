# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]
### Added
### Changed
### Removed

## [1.0.1beta] - 2020-08-24
### Added
- dockflow is now published to PyPi
- `dockflow start` will initially create a `dockflow` bridge network, following containers will be added to this network.
    - Allows for easier communication between containers.

### Changed
- `dockflow stop --rm` is now able to remove containers that have already been stopped.
- `dockflow start` will delete previously created container if it did not start successfully.
- On initial start, dockflow will prompt the user for the container repo URL if not set using `dockflow config`.
- `dockflow test` spins up an ephemeral test container to run tests in a fresh environment

## [1.0.0beta2] - 2020-08-20
### Added
- Mount GCP Credentials

## [1.0.0beta1] - 2020-08-07
### Changed
- Default version changed to `composer-1.10.6-airflow-1.10.6`

## [1.0.0beta] - 2020-07-27
### Added
- Python docker SDK to manage docker containers
- Feedback to terminal
- Basic error handling for `dockflow start` command

### Fixed
- `dockflow reset` no longer kills the scheduler

## [0.0.1] - 2020-07-01
### Added
- Basic dockflow CLI tool to ease the Airflow DAG development process.
- Current Composer-Airflow version: composer-1.7.2-airflow-1.10.2