# UEFI Firmware Skill

A bilingual Codex skill for UEFI firmware architecture, specifications, edk2
development, and debugging guidance.

This repository packages a reusable skill for agents that work on UEFI firmware
topics. It is intentionally broad enough for UEFI/PI/edk2/HII/ACPI/SMBIOS/Secure
Boot/QEMU questions, while keeping the loaded skill small through reference
files.

## Install

Install the skill into Codex:

```sh
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo MarsDoge/uefi-firmware-skill \
  --path skills/uefi-firmware
```

Restart Codex after installation.

## What It Covers

- UEFI and PI architecture navigation
- edk2 package and build concepts
- HII, VFR, IFR, FormBrowser, and DisplayEngine relationships
- ACPI, SMBIOS, TCG/TPM, and Secure Boot orientation
- QEMU firmware debugging and serial-log triage
- Upstream-friendly firmware patch review and commit wording

## What It Does Not Do

- It does not copy UEFI, PI, ACPI, SMBIOS, or TCG specifications.
- It does not replace platform documentation or source inspection.
- It does not encode vendor-private firmware behavior as standard behavior.
- It does not provide a complete UEFI tutorial book in the loaded skill body.

## Layout

```text
skills/uefi-firmware/
|-- SKILL.md
|-- agents/openai.yaml
`-- references/
    |-- debugging-map.md
    |-- edk2-map.md
    |-- uefi-spec-map.md
    `-- upstreaming.md
```

## Author

MarsDoge (Dongyan Qian)

## License

MIT
