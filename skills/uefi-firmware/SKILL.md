---
name: uefi-firmware
description: Use when working on UEFI firmware architecture, specifications, edk2 development, HII/VFR/IFR/FormBrowser, ACPI/SMBIOS/TCG/Secure Boot concepts, QEMU firmware debugging, or upstream-friendly firmware patch review. Provides bilingual Chinese and English guidance, source-first debugging habits, and reference routing without copying full specifications.
---

# UEFI Firmware

## Overview

Use this skill as a UEFI firmware navigation layer. It helps explain concepts,
locate the right standards or edk2 source areas, debug firmware symptoms, and
review firmware patches while preserving the boundary between standard behavior,
edk2 implementation behavior, and platform/vendor policy.

Prefer bilingual answers: explain in Chinese when useful, keep official English
terms such as `Protocol`, `Handle`, `HOB`, `DXE`, `HII`, `VFR`, `IFR`,
`FormBrowser`, `ConfigAccess`, `Secure Boot`, and `SMBIOS` intact.

## First Decision

Classify the request before answering:

- **Concept explanation**: explain the term, the boot phase, and where it appears
  in UEFI/PI/edk2.
- **Specification lookup**: use official specs or project docs first, then cite
  exact sections when browsing is available or requested.
- **Code orientation**: inspect the local tree first; do not guess file names
  when a repository is available.
- **Debugging**: start from symptoms, logs, platform, architecture, toolchain,
  and the exact phase where behavior changes.
- **Patch/review**: separate correctness, compatibility, coding style, tests,
  and upstream wording.

## Reference Routing

Load only the reference needed for the current task:

- For UEFI/PI/ACPI/SMBIOS/TCG/Secure Boot standard boundaries, read
  `references/uefi-spec-map.md`.
- For edk2 packages, build files, firmware phases, HII, protocols, and library
  patterns, read `references/edk2-map.md`.
- For QEMU, serial logs, ASSERTs, build failures, EFI status values, and setup UI
  debugging, read `references/debugging-map.md`.
- For patch review, commit messages, copyright, sign-off, and mailing-list or PR
  wording, read `references/upstreaming.md`.

## Working Rules

- Do not present vendor-private behavior as UEFI standard behavior.
- Distinguish standard contracts from edk2 implementation choices and platform
  policy.
- For current versions, URLs, issue state, mailing-list state, or exact spec text,
  verify with official sources instead of relying on memory.
- When a local repo exists, prefer `rg`, `git grep`, build logs, and actual source
  inspection over broad explanations.
- Avoid rewriting `FormBrowser`/HII semantics unless the user explicitly wants a
  replacement; for edk2 setup UI work, prefer preserving native HII/FormBrowser
  semantics and changing the display layer.
- For high-risk firmware changes, include the test surface: architecture,
  platform, boot phase, QEMU/real hardware, toolchain, and regression cases.

## Useful Answer Shape

For most UEFI questions:

1. State the direct answer.
2. Identify whether it is UEFI spec, PI spec, edk2 implementation, or platform
   policy.
3. Point to the relevant source/spec area.
4. Give the practical debug or implementation consequence.
5. Mention remaining uncertainty and how to verify it.
