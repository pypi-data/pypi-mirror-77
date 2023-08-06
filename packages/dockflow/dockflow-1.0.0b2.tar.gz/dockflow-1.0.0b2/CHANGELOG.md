# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## [Unreleased]

## [1.0.0beta2] - 2020-08-20
### Added
- Mount GCP Credentials

## [1.0.0beta1] - 2020-08-07
### Updated
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