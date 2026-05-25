# UEFI Firmware Workflows

Practical templates for UEFI/edk2 work. Use these as starting points and adjust
for the user's repo, platform, architecture, and toolchain. Prefer local evidence
over memory.

## 1. edk2 Build Orientation

Goal: identify platform, packages, toolchain, build target, and generated artifacts.

```sh
# From edk2 workspace root
pwd
git status --short
git branch --show-current

# Common setup; exact commands vary by platform docs
source edksetup.sh
build -l build.log -a X64 -t GCC5 -b DEBUG -p OvmfPkg/OvmfPkgX64.dsc

# Inspect the build result
rg -n "(error|warning|ASSERT|FATAL|GenFds|FV|FD)" build.log
```

What to collect:

- Workspace root, commit, branch, and local modifications.
- DSC/FDF/INF involved: `*.dsc`, `*.fdf`, `*.inf`.
- Architecture (`IA32`, `X64`, `AARCH64`, `RISCV64`), toolchain, target
  (`DEBUG`/`RELEASE`).
- Failing command, first error, and generated FV/FD paths.

## 2. Source Search Patterns

Use the fastest available local search. In agent environments, `search_files` is
preferred when available; in a shell, use `rg` or `git grep`.

```sh
# Locate GUIDs, protocols, PPIs, library classes, and PCDs
rg -n "gEfi.*ProtocolGuid|EFI_.*_PROTOCOL|Pcd[A-Za-z0-9_]+" .
git grep -n "EFI_HII_CONFIG_ACCESS_PROTOCOL"

# Find module ownership and build inclusion
rg -n "MODULE_TYPE|LIBRARY_CLASS|DEPEX|INF" --glob '*.inf' .
rg -n "SomeDriver.inf|SomeLibraryClass|SomePcd" --glob '*.{dsc,fdf,dec,inf}' .

# Trace HII/VFR/IFR paths
rg -n "VfrCompile|\.vfr|HiiAddPackages|HiiSetString|ExtractConfig|RouteConfig" .

# Trace error/status handling
rg -n "EFI_(NOT_FOUND|UNSUPPORTED|INVALID_PARAMETER|OUT_OF_RESOURCES|ACCESS_DENIED)" .
```

Evidence to report:

- Exact file paths and line numbers.
- Producer/consumer relationship for protocols, PPIs, HOBs, variables, or PCDs.
- Whether behavior is common edk2 code, platform package code, or
  vendor/platform policy.

## 3. QEMU/OVMF Debug Template

Goal: reproduce firmware behavior with serial logs and debuggable OVMF artifacts.

```sh
# Example OVMF DEBUG build
source edksetup.sh
build -a X64 -t GCC5 -b DEBUG -p OvmfPkg/OvmfPkgX64.dsc

# Typical QEMU serial-log run; adjust paths for your build tree
qemu-system-x86_64 \
  -machine q35,accel=tcg \
  -m 2048 \
  -drive if=pflash,format=raw,readonly=on,file=Build/OvmfX64/DEBUG_GCC5/FV/OVMF_CODE.fd \
  -drive if=pflash,format=raw,file=Build/OvmfX64/DEBUG_GCC5/FV/OVMF_VARS.fd \
  -serial file:serial.log \
  -display none

rg -n "(ASSERT|ERROR|WARNING|Security|Bds|DXE|PEI|SMM|Status|EFI_)" serial.log
```

Useful variations:

- Add `-debugcon file:debug.log -global isa-debugcon.iobase=0x402` when the
  platform supports debugcon.
- Use `-s -S` for GDB attach when symbols and debug setup are available.
- Preserve both `OVMF_CODE.fd` and a fresh writable `OVMF_VARS.fd` for
  reproducibility.

Report:

- QEMU command, OVMF build target/toolchain, serial/debug log excerpts.
- First failure point by phase, not just the last visible symptom.
- Whether failure depends on variable store contents, disk image, Secure Boot
  state, or architecture.

## 4. HII/VFR/IFR Triage

Goal: separate VFR source, compiled IFR, strings, varstore, browser behavior, and
platform display policy.

```sh
# Locate HII package production and form callbacks
rg -n "HiiAddPackages|HiiRemovePackages|EFI_HII_CONFIG_ACCESS_PROTOCOL" .
rg -n "ExtractConfig|RouteConfig|Callback|ConfigAccess" .

# Locate VFR, strings, and varstores
rg -n "formset|varstore|oneof|numeric|checkbox|suppressif|grayoutif" --glob '*.vfr' .
rg -n "STRING_TOKEN|\.uni|HiiSetString|HiiGetString" .

# Locate generated/build references
rg -n "VfrCompile|IFR|FormBrowser|DisplayEngine" Build .
```

Checklist:

- Which driver calls `HiiAddPackages()`?
- Which VFR formset/class GUID and varstore own the question?
- Is the issue in VFR logic (`suppressif`/`grayoutif`), string resources,
  `ConfigAccess`, variable defaults, or FormBrowser rendering?
- Is the requested change standard HII behavior, edk2 browser implementation,
  or platform UI policy?

## 5. Firmware Patch Review Evidence

Use this structure for review comments and summaries:

```text
Scope: package/module/phase/architecture
Claim: spec vs edk2 implementation vs platform policy
Evidence: file:line, build log, serial log, spec URL/section if verified
Risk: compatibility, security, FV size, variable migration, boot path, rollback
Verification: build commands, QEMU/hardware tests, negative cases
Recommendation: accept/change/request data
```

Commands that usually help:

```sh
git status --short
git diff --stat
git diff --check
git diff -- '*.c' '*.h' '*.inf' '*.dsc' '*.fdf' '*.dec' '*.vfr' '*.uni'
rg -n "TODO|FIXME|ASSERT\(|DEBUG\(|EFI_ERROR|CopyMem|AsciiStr|StrCpy|PcdGet" .
```

Review conservatively for:

- SMM/MM, variable services, capsule update, Secure Boot, TPM/measured boot,
  cryptography, and authentication paths.
- Firmware volume size, alignment, PCD defaults, variable store compatibility,
  and mixed architecture behavior.
- Upstream style: minimal patch scope, clear commit message, `Signed-off-by`
  when required, and no vendor-private claims or leaked identifiers.
