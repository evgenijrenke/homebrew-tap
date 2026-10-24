# Evgenijrenke Homebrew Tap

Homebrew formulas for Cryptomator CLI and other tools.

## Install Cryptomator CLI

Install directly from the tap:

```bash
brew install evgenijrenke/tap/cryptomator-cli
```

Or add the tap first:

```bash
brew tap evgenijrenke/tap
brew install cryptomator-cli
```

Verify the installation:

```bash
cryptomator-cli --version
```

## Formula layout

Formulas are stored under `Formula/` so additional tools can be added without
changing the tap or the installation path for existing formulas.

## Maintenance note

The current formula uses Cryptomator CLI 0.6.1 because that upstream release
provides macOS Apple Silicon, macOS Intel, Linux ARM64, and Linux x86_64
artifacts. The newer 0.6.2 release currently does not publish a macOS
Apple Silicon artifact.
