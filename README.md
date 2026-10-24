# Homebrew Tap

Homebrew formulas for command-line tools.

## Available packages

| Package | Upstream |
| --- | --- |
| `cryptomator-cli` | [Cryptomator CLI](https://github.com/cryptomator/cli) |

## Installation

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

## Updates

```bash
brew update
brew upgrade evgenijrenke/tap/cryptomator-cli
```

## Package notes

### Cryptomator CLI

The formula supports macOS on Apple Silicon (ARM64), Linux ARM64, and
Linux x86_64. Intel Macs are not supported.

The formula was initially pinned to [release 0.6.1](https://github.com/cryptomator/cli/releases/tag/0.6.1),
which provides all three required platform artifacts.
[Release 0.6.2](https://github.com/cryptomator/cli/releases/tag/0.6.2)
does not publish a macOS Apple Silicon artifact.

The `--version` check verifies CLI startup, not vault mounting.
Filesystem integration requires a separately installed backend such as macFUSE
or FUSE-T on macOS, or libfuse on Linux. A WebDAV fallback is also available.
See the [upstream usage and mounting instructions](https://github.com/cryptomator/cli/blob/0.6.1/README.md).

## Source attribution

The Cryptomator CLI formula closely follows
[dominikplsek/homebrew-cryptomator-cli](https://github.com/dominikplsek/homebrew-cryptomator-cli).
Its original MIT copyright and permission notice are preserved in [LICENSE](LICENSE).
The formula code's license is separate from Cryptomator CLI's
`AGPL-3.0-only` license declared in the formula.

## Automation

Formula changes run Homebrew style, audit, installation, and formula tests on
macOS ARM64, Linux ARM64, and Linux x86_64 runners. These checks do
not exercise vault mounting.

A weekly or manually triggered release check proposes a formula update in a
pull request only when the latest stable release contains all three required
platform archives, including macOS ARM64. Missing assets are reported in the workflow summary; platform support
is never silently dropped. Updates are not automatically merged.

The updater uses `GITHUB_TOKEN`, with no additional secrets. Repository policy
must allow GitHub Actions to create pull requests. If that is disabled, the
workflow reports the failure rather than changing repository permissions.
The updater also has permission to dispatch formula checks on its update branch,
because PRs created with `GITHUB_TOKEN` do not trigger PR workflows automatically.
