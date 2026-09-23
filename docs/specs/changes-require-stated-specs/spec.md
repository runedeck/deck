# Spec Presence Attestation Specification

## Purpose

A pull request that touches a protected path carries a specification change or a labelled reason. This specification defines what the `spec/presence` check accepts.

## Requirements

### Requirement: Canonical delta specification

The spec gate MUST accept canonical delta specifications under `docs/changes/<change>/specs/`.

#### Scenario: A protected change includes a delta specification

- **WHEN** a pull request changes a protected path
- **AND** it changes a file under `docs/changes/<change>/specs/`
- **THEN** the spec gate accepts the specification
