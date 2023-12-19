pkgname = "shotman"
pkgver = "0.4.5"
pkgrel = 0
build_style = "cargo"
hostmakedepends = ["cargo", "pkgconf", "scdoc"]
makedepends = ["libxkbcommon-devel", "rust-std"]
depends = ["slurp"]
pkgdesc = "Screenshot GUI for Wayland"
maintainer = "triallax <triallax@tutanota.com>"
license = "ISC"
url = "https://sr.ht/~whynothugo/shotman"
source = f"https://git.sr.ht/~whynothugo/shotman/archive/v{pkgver}.tar.gz"
sha256 = "59ade23793294b5021d4aa6e4151cd3dc2063079011c67ab12e6c6b9d4031b2e"
env = {
    "SHOTMAN_VERSION": f"v{pkgver}",
}
# !check because no tests, and !cross because completions are generated by
# running a binary
options = ["!check", "!cross"]


def post_build(self):
    self.do("make", "shotman.1")

    with open(self.cwd / "shotman.bash", "w") as cf:
        self.do(
            f"target/{self.profile().triplet}/release/shotman_completions",
            "bash",
            stdout=cf,
        )

    with open(self.cwd / "shotman.fish", "w") as cf:
        self.do(
            f"target/{self.profile().triplet}/release/shotman_completions",
            "fish",
            stdout=cf,
        )

    with open(self.cwd / "shotman.zsh", "w") as cf:
        self.do(
            f"target/{self.profile().triplet}/release/shotman_completions",
            "zsh",
            stdout=cf,
        )


def post_install(self):
    self.install_license("LICENCE.md")
    self.install_man("shotman.1")

    self.install_completion("shotman.bash", "bash")
    self.install_completion("shotman.zsh", "zsh")
    self.install_completion("shotman.fish", "fish")
