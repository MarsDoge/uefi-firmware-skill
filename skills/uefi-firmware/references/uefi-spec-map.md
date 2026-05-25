# UEFI Specification Map

Use this reference when the user needs standards boundaries, terminology, or a
path to official documentation. Prefer official URLs and cite exact versions or
sections only after checking them. Do not copy specification text.

## Source Hierarchy

- **UEFI Specification**: boot services, runtime services, protocols, device
  paths, variables, image loading, Secure Boot, HII, and Form Browser interfaces.
- **PI Specification**: firmware phases and PI infrastructure such as SEC, PEI,
  DXE, SMM/MM, PPIs, HOBs, FV/FFS, and dispatch models.
- **ACPI Specification**: OS-visible platform description, power management,
  processor/device description, AML, and tables such as DSDT/SSDT/FADT/MADT/SRAT.
- **SMBIOS Specification**: inventory and management structures describing BIOS,
  system, board, chassis, CPU, memory, slots, and firmware metadata.
- **TCG PC Client / TPM specifications**: TPM measurements, event logs, PCRs,
  TCG2 protocol usage, and measured boot concepts.
- **edk2 documentation/source**: implementation behavior, package conventions,
  build tools, maintainers, and coding practices.

## Official Sources To Prefer

### UEFI Forum

- UEFI specifications landing page: https://uefi.org/specifications
- UEFI specification documents landing page: https://uefi.org/specs/UEFI
- Platform Initialization (PI) specification documents: https://uefi.org/specs/PI
- ACPI specification documents hosted by UEFI Forum: https://uefi.org/specs/ACPI
- UEFI Forum Learning Center and white papers: https://uefi.org/learning_center

### DMTF

- SMBIOS standard landing page: https://www.dmtf.org/standards/smbios
- DMTF published documents index: https://www.dmtf.org/dsp/DSP0134

### Trusted Computing Group (TCG)

- TCG resource library: https://trustedcomputinggroup.org/resource-library/
- TCG PC Client Platform Firmware Profile specification family:
  https://trustedcomputinggroup.org/resource/pc-client-specific-platform-firmware-profile-specification/
- TCG EFI Protocol specification family:
  https://trustedcomputinggroup.org/resource/tcg-efi-protocol-specification/
- TPM 2.0 Library specification landing page:
  https://trustedcomputinggroup.org/resource/tpm-library-specification/

### TianoCore / edk2

- edk2 source repository: https://github.com/tianocore/edk2
- edk2 documentation repository: https://github.com/tianocore/tianocore.github.io/wiki/EDK-II
- edk2 build specification: https://tianocore-docs.github.io/edk2-BuildSpecification/release-1.28/
- edk2 DSC specification: https://tianocore-docs.github.io/edk2-DscSpecification/release-1.28/
- edk2 INF specification: https://tianocore-docs.github.io/edk2-InfSpecification/release-1.27/
- edk2 DEC specification: https://tianocore-docs.github.io/edk2-DecSpecification/release-1.27/
- edk2 FDF specification: https://tianocore-docs.github.io/edk2-FdfSpecification/release-1.28/
- edk2 VFR specification: https://tianocore-docs.github.io/edk2-VfrSpecification/release-1.91/
- edk2 Module Writer's Guide: https://tianocore-docs.github.io/edk2-ModuleWriteGuide/draft/
- edk2 Driver Writer's Guide: https://tianocore-docs.github.io/edk2-UefiDriverWritersGuide/draft/
- TianoCore contribution guidelines: https://github.com/tianocore/tianocore.github.io/wiki/EDK-II-Development-Process

## Secure Boot / Measured Boot Boundary

- UEFI owns Secure Boot variables, image authentication, signature databases, and
  the boot service/runtime service interfaces around image loading and variables.
- TCG owns measured boot concepts, PCR semantics, TPM event log formats, and TPM
  command/library specifications.
- edk2 implements both UEFI-facing and TCG-facing pieces, but platform policy
  determines defaults, key enrollment flows, setup UI, and deployment constraints.
- ACPI may expose TPM devices and related platform tables to the OS, but ACPI is
  not the Secure Boot policy specification.

## How To Answer Standards Questions

- Say which spec family owns the concept.
- If a concept spans specs, describe the boundary. Example: Secure Boot policy is
  UEFI, TPM measurements are TCG, and OS table exposure may involve ACPI.
- Do not quote long spec text. Summarize and cite official sections only after
  the exact version has been checked.
- If the user asks for latest behavior, verify the current spec version or
  official project source.

## Common Boundaries

- `EFI_BOOT_SERVICES` exists before `ExitBootServices()` and is not available to
  the OS after boot services exit.
- `EFI_RUNTIME_SERVICES` are designed to remain callable after
  `ExitBootServices()` where the OS preserves mappings and calling convention.
- `LoadImage()` and `StartImage()` are UEFI image lifecycle services; platform
  boot policy is usually BDS or platform boot manager logic.
- `AllocatePages()` supports allocation by type, maximum address, or fixed
  address, but allocator choice and memory map state are firmware behavior.
- HII and Form Browser define setup UI data and interaction contracts; visual
  styling is implementation-specific.
- ACPI describes platform hardware to the OS; it is not a firmware setup UI
  mechanism.
- SMBIOS is inventory/management data; it is generally not a configuration
  control path by itself.
