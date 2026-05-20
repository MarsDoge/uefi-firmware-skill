# Upstreaming Firmware Changes

Use this reference for edk2/UEFI patch review, commit messages, and upstream
communication.

## Review Priorities

- Correctness against UEFI/PI/edk2 contracts.
- Compatibility with existing platforms and architectures.
- Scope: avoid unrelated refactors in bug fixes.
- Build impact across supported toolchains and architectures.
- Tests or reproduction steps that reviewers can run.
- Clear failure mode before and after the patch.

## Commit Message Shape

- Subject: concise subsystem prefix plus change.
- Body: explain the bug or limitation, why the current behavior is wrong, and
  why the fix is safe.
- Include concrete error text or reproduction details when helpful.
- Avoid overclaiming; prefer "can fail", "may dereference", or "is not accepted
  by Clang X" when evidence is scoped.
- Preserve author and sign-off unless explicitly changing ownership.

## Firmware Review Language

- Separate "spec requires", "edk2 currently does", and "this platform needs".
- When discussing compiler flags, name the compiler version and command line.
- When discussing memory allocation, name the allocation type, memory map state,
  and phase.
- When discussing HII/UI behavior, say whether semantics come from FormBrowser
  or rendering comes from DisplayEngine.

## Copyright And License

- Keep existing file headers when modifying upstream files.
- New edk2-compatible code usually follows the destination repository's license
  and copyright conventions.
- Do not copy vendor UI assets, fonts, logos, or private documentation into open
  firmware projects without explicit compatible licensing.

## Suggested Evidence Checklist

- Build command and target.
- Failing log or compiler diagnostic.
- Source files and functions involved.
- Before/after behavior.
- Regression surface: architecture, platform, toolchain, and QEMU or hardware.
