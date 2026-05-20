# UEFI Firmware Skill Distillation Method

This reference describes what the skill is trying to preserve: not a database of
facts, but the working style of a careful UEFI firmware engineer.

The method is inspired by skill distillation projects such as
`alchaincyf/nuwa-skill`, but adapts the idea from "how a person thinks" to "how
a firmware expert should reason". Do not role-play a person. Run the workflow.

## Core Mental Models

### 1. Phase First

Every firmware symptom belongs to a phase or a phase boundary.

- SEC/PEI symptoms usually involve early entry, memory discovery, PPIs, HOBs, or
  firmware volume access.
- DXE symptoms usually involve driver dispatch, protocols, handles, variables,
  runtime drivers, or device connection.
- BDS symptoms usually involve boot policy, boot options, UI, shell, or OS
  loader handoff.
- OS handoff symptoms usually involve memory map, `ExitBootServices()`, ACPI,
  device tree, initrd/kernel placement, or runtime mappings.

If the phase is unknown, ask for or inspect serial logs before proposing a fix.

### 2. Four-Layer Separation

Classify every claim into one of four layers:

- **Specification contract**: UEFI, PI, ACPI, SMBIOS, TCG, or architecture ABI.
- **edk2 implementation**: the behavior of a concrete edk2 module or library.
- **Platform policy**: DSC/FDF choices, library instances, PCDs, boot policy,
  board/OEM decisions, or IBV custom behavior.
- **Tool behavior**: compiler, BaseTools, QEMU, accelerator, debugger, or host
  environment.

Do not turn an edk2 behavior into a spec rule. Do not turn a platform workaround
into a generic firmware rule.

### 3. Producer/Consumer Ownership

For every protocol, HII package, variable, ACPI table, SMBIOS record, or device
path, identify:

- who produces it,
- who consumes it,
- when it becomes available,
- whether it is required by standard contract or platform policy.

This prevents fixes in the wrong layer. For example, a setup UI visual issue may
belong to DisplayEngine, while a hidden/grayed condition belongs to FormBrowser
or the HII producer.

### 4. Compatibility Surface

A firmware answer is incomplete until it states where it was validated:

- architecture: IA32/X64, AArch64, RISC-V, LoongArch, or other;
- platform: QEMU virtual platform, reference board, server board, laptop, etc.;
- boot mode and variable-store state;
- toolchain and build target;
- relevant firmware volume size or memory-map constraint;
- real hardware vs emulator.

### 5. Minimal Semantic Change

For compatibility work, prefer the smallest change that preserves existing UEFI
semantics. In edk2 setup UI work, this often means:

- keep HII/VFR/IFR parsing in SetupBrowser/FormBrowser;
- keep `ConfigAccess` callbacks and variable writeback with the owning driver;
- change rendering through DisplayEngine/GOP only when the problem is visual;
- keep native fallback paths until enough forms are verified.

## Decision Heuristics

- If the question asks "what does this mean", first map the term to phase and
  spec family.
- If the question asks "why does this hang", first find the last log line and
  compare one variable at a time.
- If the question asks "should we change this", first identify the owner and
  compatibility blast radius.
- If the question asks "is this a bug", compare spec contract, edk2 behavior, and
  another platform or architecture.
- If the question asks for upstream wording, make claims narrow and evidence
  based.

## Evidence Ladder

Prefer evidence in this order:

1. Exact source code and build configuration in the user's tree.
2. Serial log, ASSERT, EFI status, compiler diagnostic, or QEMU command line.
3. Official specification or upstream project documentation.
4. Upstream commit history, issue, pull request, or mailing-list discussion.
5. Reasoned inference, clearly marked as inference.

## Answer DNA

Good answers should be direct, bounded, and operational:

- "This is spec behavior" vs "this is edk2's implementation".
- "The owner is likely this module because it produces this protocol/string."
- "The next comparison test is X vs Y."
- "This is safe only if these architectures/platforms still pass."
- "I am inferring this from source/logs; verify by checking this path."

Avoid:

- vague statements like "UEFI does this" when only one platform does;
- changing HII semantics to solve a rendering problem;
- suggesting broad refactors before isolating the phase;
- hiding uncertainty;
- copying vendor-private UI or policy as if it were open firmware practice.
