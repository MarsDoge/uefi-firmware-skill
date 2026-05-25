# UEFI Firmware Skill

A bilingual agent skill for UEFI firmware architecture, specifications, edk2
development, and debugging guidance.

This repository packages an installable UEFI Firmware Skill for AI agents, local
assistants, and firmware development workflows. It is intentionally broad enough
for UEFI/PI/edk2/HII/ACPI/SMBIOS/Secure Boot/QEMU questions, while keeping the
loaded skill small through reference files.

The skill includes a distilled reasoning reference for firmware work: classify
the phase, separate specification contracts from edk2 implementation details,
inspect source and logs before guessing, and keep compatibility evidence visible.

## Included Reasoning Reference / 推理参考

This skill includes a Nuwa-inspired distilled reasoning note in
`references/distillation-method.md`. It takes inspiration from
[alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill), but adapts one
reference method from personality/perspective distillation into domain-expert
firmware reasoning: phase-first classification, standards-boundary discipline,
source-first debugging, and evidence-based review.

The loaded `SKILL.md` contains the compact operating model; agents can load the
distilled reasoning reference only when needed. No vendor firmware assets or
private documentation are included.

## Install

Use `skills/uefi-firmware/` as the installable skill directory. Any compatible
agent runtime can load the `SKILL.md` file and progressively read the reference
files as needed.

For Hermes Agent local installs, copy the full skill directory into your local
skills directory, then reload skills or restart Hermes:

```sh
mkdir -p ~/.hermes/skills
cp -R skills/uefi-firmware ~/.hermes/skills/
# In an active Hermes session, run /reload-skills if available; otherwise restart.
```

If your Hermes install uses a different skill directory, copy the entire
`skills/uefi-firmware/` directory there. Do not copy only `SKILL.md`; the
reference files are part of the skill.

For Codex-compatible environments:

```sh
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo MarsDoge/uefi-firmware-skill \
  --path skills/uefi-firmware
```

Restart the agent runtime after installation if it only loads skills at startup.

## What It Covers

- UEFI and PI architecture navigation
- edk2 package and build concepts
- HII, VFR, IFR, FormBrowser, and DisplayEngine relationships
- ACPI, SMBIOS, TCG/TPM, and Secure Boot orientation
- QEMU firmware debugging and serial-log triage
- Upstream-friendly firmware patch review and commit wording
- Firmware expert reasoning patterns included as a reusable reference

## What It Does Not Do

- It does not copy UEFI, PI, ACPI, SMBIOS, or TCG specifications.
- It does not replace platform documentation or source inspection.
- It does not encode vendor-private firmware behavior as standard behavior.
- It does not provide a complete UEFI tutorial book in the loaded skill body.

## Layout

```text
skills/uefi-firmware/
|-- SKILL.md
|-- agents/openai.yaml        # optional OpenAI/Codex-compatible metadata
`-- references/
    |-- debugging-map.md
    |-- distillation-method.md
    |-- edk2-map.md
    |-- uefi-spec-map.md
    |-- upstreaming.md
    `-- workflows.md
```

## Reference Files

- `references/workflows.md`: command-level templates for edk2 builds, source
  search, QEMU/OVMF debug, HII/VFR/IFR triage, and patch-review evidence.
- `references/uefi-spec-map.md`: official UEFI/PI/ACPI/SMBIOS/TCG/TPM and edk2
  documentation links plus standards-boundary guidance.
- `references/edk2-map.md`, `debugging-map.md`, `upstreaming.md`, and
  `distillation-method.md`: focused routing for implementation, debug, review,
  and reasoning behavior.

## Author

MarsDoge (Dongyan Qian)

## License

MIT
