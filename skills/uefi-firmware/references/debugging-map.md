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

## Good Debug Answer Pattern

1. Identify the phase and component.
2. State the most likely ownership boundary.
3. Show the source/log evidence.
4. Propose the smallest comparison test.
5. Avoid changing unrelated firmware policy while debugging display or parser
   symptoms.
