# UEFI Debugging Map

Use this reference for firmware build failures, boot hangs, QEMU symptoms,
setup UI issues, and logs.

## First Data To Collect

- Platform and architecture: x86, AArch64, RISC-V, LoongArch, or other.
- Environment: QEMU version, accelerator, machine type, firmware image, variable
  store, disk image, and command line.
- Toolchain: GCC/Clang version, target triple, build target, architecture.
- Phase where it fails: SEC, PEI, DXE dispatch, BDS, setup UI, boot loader, OS
  kernel handoff.
- Exact log line, ASSERT, EFI status, or crash address.

## Build Failures

- Check the first compiler or linker diagnostic, not only the final make error.
- For edk2, inspect the module being built, selected toolchain, selected library
  instances, and generated AutoGen paths.
- Clang and GCC flags are not interchangeable; verify architecture-specific
  flags against the exact compiler version.
- If a BaseTools utility fails, separate input file corruption from tool logic.

## QEMU Firmware Hangs

- Compare acceleration modes: for example `tcg` vs `hvf` or `kvm`.
- Compare machine options that affect interrupt controllers, timer devices,
  memory map, firmware volumes, and graphics devices.
- Capture serial logs and identify the last successful firmware phase.
- For BDS waits or boot manager stalls, check boot options, device connection,
  variable store freshness, and input/display availability.

## Setup UI Debugging

- If a native HII page is wrong, decide whether the bug is in the HII producer,
  SetupBrowser/FormBrowser, DisplayEngine, GraphicsConsole, font rendering, or
  GOP mode selection.
- Missing glyphs are a renderer/font problem unless HII strings are corrupt.
- Incorrect hidden/grayed state is usually FormBrowser/IFR expression or current
  configuration state, not pure drawing.
- Failed writes should be traced through `ConfigAccess.RouteConfig()` and the
  owning driver.

## EFI Status Interpretation

- Always preserve the exact `EFI_STATUS` value and symbolic name if available.
- `EFI_NOT_FOUND` often means missing protocol, variable, handle, package, or
  target object; it is not specific enough without call-site context.
- `EFI_UNSUPPORTED` can be a deliberate platform/driver policy.
- `EFI_INVALID_PARAMETER` often indicates contract mismatch, buffer size/state,
  or wrong optional field assumptions.

## Controlled Validation / 受控验证

**Rule:** Compare baseline and patched behavior with the relevant environment held
constant. Record the revision, build configuration, loaded image, boot media, and
initial variable-store state. Preserve the failing state before testing a fresh
store, and change one relevant factor at a time.

**Example:** If a changed Setup page still looks identical, confirm the loaded
application first, then navigate to that page, exercise the affected interaction,
and inspect both the display and exception/ASSERT logs.

**Limit:** Reaching the boot menu is not validation of a changed page. A screenshot
proves appearance at that moment, not persistence or successful configuration
writeback. Use the acceptance behavior to choose the additional checks.

## Build-to-Run Trace / 从构建追到运行

**Rule:** Check each relevant boundary: source and configuration, build tool,
generated module, packaged firmware, deployed boot media, and actual load path.
Record artifact identities and logs. After changing a conversion or packaging tool,
verify that downstream images were regenerated with it, not merely that the tool
itself was rebuilt.

**Example:** After a GenFw change, regenerate the affected EFI images and firmware,
then confirm that QEMU loads that firmware. If the application is loaded from an
ESP, update and verify that copy separately. Use a clean rebuild when incremental
dependency tracking cannot establish which tool produced the image.

**Limit:** Full rebuilds are not required for every edit. A hash identifies bytes,
not correctness or proof of execution; connect it to the configured and observed
load path. Do not reset the variable store as a side effect of refreshing code.

## Cross-Architecture Fault Localization / 跨架构异常定位

**Rule:** Identify the faulting module and exact build before symbolizing an
address. Distinguish runtime addresses, PE RVAs, ELF virtual addresses, and file
offsets; derive conversions from the loader and section layout. Use target-aware
disassembly to inspect the failing instruction, relocation target, and stack frame.

**Example:** For a crash near a rendering function, map the fault to the matching
debug image and inspect the generated prologue and callees for large stack
allocations or inlining. For a bad relocated pointer, trace its original target
and transformed section address instead of substituting an RVA into an ELF formula.

**Limit:** Subtracting the runtime image base gives an image-relative address, not
a universally valid input to an ELF symbolizer. Large stack frames are a hypothesis,
not a diagnosis by themselves. Exception names, relocation rules, and generated
code differ by architecture and toolchain; an X64 build does not validate another
target's link or runtime behavior.

## Device Visibility versus Boot Entries / 设备可见与启动项分开排查

**Rule:** Trace discovery, driver connection, filesystem or loader access, boot
policy, and persistent boot-entry updates as separate steps. Inspect the relevant
Boot#### and BootOrder operations and their exact status before blaming device
enumeration or changing boot policy.

**Example:** If Shell exposes a filesystem but Setup has no corresponding boot
entry, inspect the boot-option creation path and variable-write results. A failed
write may explain the missing entry even though filesystem discovery succeeded.

**Limit:** A visible filesystem proves neither a valid loader nor eligibility under
platform boot policy. A missing entry does not prove variable-store exhaustion.
Preserve the failing store for diagnosis; do not automatically delete user boot
entries or substitute a fresh store and call the original problem fixed.

## Good Debug Answer Pattern

1. Identify the phase and component.
2. State the most likely ownership boundary.
3. Show the source/log evidence.
4. Propose the smallest comparison test.
5. Avoid changing unrelated firmware policy while debugging display or parser
   symptoms.
