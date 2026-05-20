# edk2 Map

Use this reference when the user asks how edk2 is structured, where a feature
lives, or how UEFI concepts map to source code.

## Repository Concepts

- `*.dec`: package declarations, GUIDs, PPIs, protocols, PCDs, and library class
  declarations exported by a package.
- `*.dsc`: platform build description, module list, library class resolutions,
  PCD settings, architectures, and build options.
- `*.fdf`: firmware device layout, firmware volumes, files, sections, capsules,
  and image placement.
- `*.inf`: module metadata, sources, packages, library classes, protocols, PPIs,
  GUIDs, PCDs, and depex.
- `*.vfr`: Visual Forms Representation source for HII setup forms.
- `*.uni`: localized strings used by HII packages or module UI text.

## Firmware Phases In edk2

- **SEC**: earliest entry, temporary execution environment, handoff to PEI.
- **PEI**: memory discovery, PPIs, HOB construction, PEIM dispatch.
- **DXE**: driver dispatch, protocols, boot services, runtime services drivers.
- **BDS**: boot policy, boot options, front page, boot manager, shell, OS loader.
- **SMM/MM**: privileged management mode, SMI/MM handlers and isolated services.

## Package Orientation

- `MdePkg`: UEFI/PI base types, protocols, GUIDs, library interfaces.
- `MdeModulePkg`: common UEFI drivers, SetupBrowser, HII database, UI app,
  variable services, boot manager libraries.
- `UefiCpuPkg`: CPU initialization and CPU-related drivers.
- `SecurityPkg`: Secure Boot, TPM/TCG, crypto and security modules.
- `NetworkPkg`: UEFI network stack and network configuration.
- `ShellPkg`: UEFI Shell.
- `ArmVirtPkg`, `OvmfPkg`, `EmulatorPkg`: common virtual platform examples.

## HII/FormBrowser Orientation

- HII database stores packages: strings, forms, fonts, images, keyboard layout,
  and related data.
- VFR compiles into IFR bytecode carried in HII form packages.
- `SetupBrowserDxe`/FormBrowser interprets IFR, evaluates conditions, calls
  `EFI_HII_CONFIG_ACCESS_PROTOCOL`, and manages question semantics.
- Display engines render already-interpreted form state. Prefer changing display
  engines for UI modernization instead of reimplementing IFR semantics.
- `ConfigAccess.ExtractConfig()` reads current configuration and
  `RouteConfig()` writes configuration back through the owning driver.

## Source Inspection Habits

- Use `rg` or `git grep` for GUID names, protocol names, PCDs, INF module names,
  and error strings.
- For behavior questions, inspect both the library class declaration and the
  platform's library instance resolution in the DSC.
- For setup UI issues, distinguish: HII producer driver, HII database,
  SetupBrowser/FormBrowser, DisplayEngine, graphics console, and GOP.
- For architecture-specific bugs, compare the same code path on another
  architecture before assigning ownership.
