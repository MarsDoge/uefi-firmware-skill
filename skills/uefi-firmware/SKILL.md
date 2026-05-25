---
name: uefi-firmware
version: 0.2.0
author: MarsDoge (Dongyan Qian)
license: MIT
description: Use when working on UEFI firmware architecture, specifications, edk2 development, HII/VFR/IFR/FormBrowser, ACPI/SMBIOS/TCG/Secure Boot concepts, QEMU firmware debugging, or upstream-friendly firmware patch review. Provides bilingual Chinese and English guidance, source-first debugging habits, and reference routing without copying full specifications.
metadata:
  hermes:
    tags: [uefi, firmware, edk2, bios, qemu, secure-boot, hii, vfr, debugging]
    related_skills: []
  domain: firmware
  languages: [en, zh]
  topics: [UEFI, PI, edk2, HII, VFR, IFR, ACPI, SMBIOS, TCG, TPM, Secure Boot, QEMU]
---

# UEFI Firmware

## Overview

Use this skill as a UEFI firmware navigation layer. It helps explain concepts,
locate the right standards or edk2 source areas, debug firmware symptoms, and
review firmware patches while preserving the boundary between standard behavior,
edk2 implementation behavior, and platform/vendor policy.

Prefer bilingual answers when useful: Chinese explanations are welcome, but keep
official English terms such as `Protocol`, `Handle`, `HOB`, `DXE`, `HII`, `VFR`,
`IFR`, `FormBrowser`, `ConfigAccess`, `Secure Boot`, and `SMBIOS` intact.

## Distillation Approach / 蒸馏方法

This skill is explicitly built as a distilled firmware-engineer operating model,
not a copied specification bundle. The distilled behavior is: classify firmware
phase first, separate spec/edk2/platform/tool layers, inspect source and logs
before guessing, preserve compatibility evidence, and answer with a verification
path.

The detailed method lives in `references/distillation-method.md`. Keep the
Nuwa-style skill distillation inspiration visible in the README and reference
file, but adapt it to domain reasoning rather than personality imitation.

## When to Use / 适用场景

Use this skill for:

- UEFI, PI, ACPI, SMBIOS, TCG/TPM, Secure Boot terminology and boundary questions.
- edk2 source orientation, package/module/library patterns, and build triage.
- HII/VFR/IFR/FormBrowser setup UI analysis and debugging.
- QEMU/OVMF firmware debug, serial logs, ASSERTs, and EFI status investigation.
- Firmware patch review where evidence, compatibility, and upstream wording matter.

## When Not to Use / 不适用场景

Do not rely on this skill alone for:

- Vendor-private behavior, unreleased platform policy, or NDA documentation.
- Exact current spec wording/version claims without checking official sources.
- Hardware-specific diagnosis without logs, board details, toolchain, and build data.
- Replacing edk2 maintainers' guidance, platform owners' documentation, or security review.

## First Decision

Classify the request before answering:

- **Concept explanation**: explain the term, boot phase, and where it appears in
  UEFI/PI/edk2.
- **Specification lookup**: use official specs or project docs first, then cite
  exact sections when browsing is available or requested.
- **Code orientation**: inspect the local tree first; do not guess file names
  when a repository is available.
- **Debugging**: start from symptoms, logs, platform, architecture, toolchain,
  and the exact phase where behavior changes.
- **Patch/review**: separate correctness, compatibility, coding style, tests,
  and upstream wording.

## Core Workflows

1. Identify phase and owner: SEC, PEI, DXE, BDS, SMM/MM, boot loader, or OS handoff.
2. Separate layers: specification contract, edk2 implementation, platform policy,
   and toolchain/QEMU/hardware behavior.
3. Gather evidence: source path, GUID/protocol, EFI status, log line, build
   command, spec section, or test result.
4. Route to focused references before expanding the answer.
5. Explain the practical consequence and the verification path.

For command-level templates, read `references/workflows.md`.

## Reference Routing

Load only the reference needed for the current task:

- For practical command-level templates and evidence collection, read
  `references/workflows.md`.
- For the distilled reasoning model behind this skill, read
  `references/distillation-method.md`.
- For UEFI/PI/ACPI/SMBIOS/TCG/Secure Boot standard boundaries and official links,
  read `references/uefi-spec-map.md`.
- For edk2 packages, build files, firmware phases, HII, protocols, and library
  patterns, read `references/edk2-map.md`.
- For QEMU, serial logs, ASSERTs, build failures, EFI status values, and setup UI
  debugging, read `references/debugging-map.md`.
- For patch review, commit messages, copyright, sign-off, and mailing-list or PR
  wording, read `references/upstreaming.md`.

## Common Pitfalls

- Treating vendor/platform policy as if it were required by the UEFI specification.
- Mixing UEFI Secure Boot with TCG measured boot or TPM policy without stating the boundary.
- Guessing edk2 file paths instead of searching the local tree.
- Debugging HII setup UI only at the visual layer while ignoring VFR/IFR,
  `ConfigAccess`, varstore, and FormBrowser behavior.
- Reviewing firmware patches without architecture, firmware volume size, variable
  store, QEMU/hardware, and toolchain compatibility evidence.

## Working Rules

- Do not present vendor-private behavior as UEFI standard behavior.
- Distinguish standard contracts from edk2 implementation choices and platform policy.
- For current versions, URLs, issue state, mailing-list state, or exact spec text,
  verify with official sources instead of relying on memory.
- When a local repo exists, prefer `search_files`, `rg`, `git grep`, build logs,
  and actual source inspection over broad explanations.
- Avoid rewriting `FormBrowser`/HII semantics unless the user explicitly wants a
  replacement; for edk2 setup UI work, prefer preserving native HII/FormBrowser
  semantics and changing the display layer.
- For high-risk firmware changes, include the test surface: architecture,
  platform, boot phase, QEMU/real hardware, toolchain, and regression cases.

## Verification Checklist

Before finalizing an answer or review, check:

- Is the claim labeled as spec, edk2 implementation, platform policy, or tool behavior?
- Is there a source path, log line, GUID/protocol, command, test, or spec link as evidence?
- Are architecture, platform, boot phase, toolchain, and QEMU/hardware scope clear?
- Are security-sensitive topics such as Secure Boot, TPM, SMM/MM, and variables treated conservatively?
- Is any remaining uncertainty stated with a concrete next verification step?

## Useful Answer Shape

For most UEFI questions:

1. State the direct answer.
2. Identify whether it is UEFI spec, PI spec, edk2 implementation, or platform policy.
3. Point to the relevant source/spec area.
4. Give the practical debug or implementation consequence.
5. Mention remaining uncertainty and how to verify it.
