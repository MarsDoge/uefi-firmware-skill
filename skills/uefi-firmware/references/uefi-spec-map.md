# UEFI Specification Map

Use this reference when the user needs standards boundaries, terminology, or a
path to official documentation.

## Source Hierarchy

- **UEFI Specification**: boot services, runtime services, protocols, device
  paths, variables, image loading, Secure Boot, HII, and Form Browser related
  interfaces.
- **PI Specification**: firmware phases and PI infrastructure such as SEC, PEI,
  DXE, SMM, PPIs, HOBs, FV/FFS, and dispatch models.
- **ACPI Specification**: OS-visible platform description, power management,
  processor/device description, AML, tables such as DSDT/SSDT/FADT/MADT/SRAT.
- **SMBIOS Specification**: inventory and management structures describing
  BIOS, system, board, chassis, CPU, memory, slots, and firmware metadata.
- **TCG PC Client / TPM specifications**: TPM measurement, event logs, PCRs,
  TCG2 protocol behavior, and measured boot concepts.

## How To Answer Standards Questions

- Say which spec family owns the concept.
- If a concept spans specs, describe the boundary. Example: Secure Boot policy
  is UEFI, TPM measurements are TCG, and OS table exposure may involve ACPI.
- Do not quote long spec text. Summarize and cite official sections when the
  exact version has been checked.
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

## Official Sources To Prefer

- UEFI Forum specifications: https://uefi.org/specifications
- TianoCore documentation and source: https://github.com/tianocore
- ACPI specification: https://uefi.org/specifications
- DMTF SMBIOS specification: https://www.dmtf.org/standards/smbios
- TCG specifications: https://trustedcomputinggroup.org/resource-library/
