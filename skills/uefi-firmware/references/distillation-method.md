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

## Engineering Rules and Examples / 工程规则与例子

These rules apply across architectures and platforms. Examples illustrate the
reasoning, not universal implementation requirements or claims of completed tests.
Keep incident-specific commands and project history out of the core model.

### 1. Choose Evidence for the Question / 按问题选择证据

**Rule:** There is no universal evidence ranking. Use the applicable specification
version and section for normative requirements, exact source and configuration
for implementation behavior, and execution evidence for observed results. History
and review discussions explain intent; label inference separately.

**Example:** Linux accepting an ACPI record demonstrates behavior of that consumer
on the tested path. Check the applicable ACPI record and method constraints before
calling the encoding compliant.

**Limit:** Consumer acceptance does not establish specification compliance or
prove that a related operation such as hotplug works.

### 2. Trace the Complete Chain / 检查完整链路

**Rule:** Follow data from producer through interface to consumer. Check identity,
availability, lifetime, build inclusion, packaging, and actual runtime use before
claiming a feature is integrated.

**Example:** After building an ACPI generator, check that the platform supplies its
inputs, the generator is registered in the running image, the generated table is
installed, and the OS receives the intended data.

**Limit:** A schema that can express the data is not a platform integration.
Equivalent consumer-visible behavior is also a different claim from byte identity.

### 3. Fix the Owning Layer / 在职责所属层修复

**Rule:** Identify ownership before editing. Prefer the smallest change that fully
repairs the relevant contract, rather than the fewest changed lines. Keep unrelated
policy changes and hardening separate.

**Example:** A Setup layout defect may belong to rendering, while an incorrect
hidden or disabled state may come from form expressions or current configuration.
Trace the cause instead of forcing visibility in the drawing code.

**Limit:** This is not a blanket preference for display-layer fixes; preserve the
configuration owner's validation and writeback responsibilities.

### 4. Verify the Artifact Being Run / 确认实际运行产物

**Rule:** Connect the source revision and build configuration to the generated
artifact and actual load path. Preserve enough information to repeat the test.

**Example:** Rebuilding firmware may leave a standalone UEFI application on the ESP
unchanged. Confirm or refresh the loaded application before attributing a changed
result to the patch.

**Limit:** A successful build or a new timestamp alone does not prove that the
running image contains the change. Track the relevant image, inputs, and logs.

### 5. Test the Promised Behavior / 按目标行为验收

**Rule:** Test the consumer-visible outcome, not just an intermediate success code.
Cover relevant boundaries, error propagation, and cleanup according to the
interface contract.

**Example:** For a setting, verify modification, save, reread, and the intended
visible effect. Reboot if persistence across reboot is required. A failed write
must not be presented as a successful save.

**Limit:** Persistence is not required for every setting; acceptance follows the
declared behavior, not a checklist copied from another feature.

### 6. Bound Conclusions by Evidence / 结论不超出证据

**Rule:** Separate static reasoning, reproduced failures, compilation, executed
tests, and platform compatibility. Report a finding's trigger, impact, evidence,
and smallest complete remedy. A missing test is not itself a demonstrated bug.

**Example:** A host test checking an ACPI generator's serialized fields supports
that serialization claim. It does not establish firmware integration or OS boot
on the target board.

**Limit:** Static analysis can prove a defect without reproduction when the input
and control flow establish it. State that basis explicitly instead of inventing a
failed run or treating every hypothetical edge case as a blocker.

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
