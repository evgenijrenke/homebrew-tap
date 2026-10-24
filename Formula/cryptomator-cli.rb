class CryptomatorCli < Formula
  desc "Command-line interface for Cryptomator vaults"
  homepage "https://github.com/cryptomator/cli"
  license "AGPL-3.0-only"

  depends_on arch: :arm64

  on_macos do
    on_arm do
      url "https://github.com/cryptomator/cli/releases/download/0.6.1/cryptomator-cli-0.6.1-mac-arm64.zip"
      sha256 "9252f8765db5068931d78f1ee74f7fe4d653605bf691d30e05c119eb5fa5d0d3"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/cryptomator/cli/releases/download/0.6.1/cryptomator-cli-0.6.1-linux-aarch64.zip"
      sha256 "f8c493abefafd1d55903e20cbec281587dc70d7a9d5c5817b33f777204dd80ed"
    end
  end

  def install
    if OS.mac?
      app_contents = Pathname("Contents")
      odie "Cryptomator CLI app contents were not found in the release archive" unless app_contents.directory?

      (libexec/"cryptomator-cli.app").install app_contents
      bin.write_exec_script libexec/"cryptomator-cli.app/Contents/MacOS/cryptomator-cli"
    else
      executable = Pathname("bin/cryptomator-cli")
      odie "Cryptomator CLI executable was not found in the release archive" unless executable.executable?

      libexec.install Dir["*"]
      bin.write_exec_script libexec/"bin/cryptomator-cli"
    end
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/cryptomator-cli --version")
  end
end
