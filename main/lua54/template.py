pkgname = "lua54"
_mver = "5.4"
pkgver = f"{_mver}.3"
pkgrel = 0
build_style = "makefile"
make_check_target = "test"
hostmakedepends = ["pkgconf"]
makedepends = ["libedit-devel"]
pkgdesc = "Lua scripting language (5.4.x)"
maintainer = "q66 <q66@chimera-linux.org>"
license = "MIT"
url = "https://lua.org"
source = f"https://www.lua.org/ftp/lua-{pkgver}.tar.gz"
sha256 = "f8612276169e3bfcbcfb8f226195bfc6e466fe13042f1076cbde92b7ec96bbfb"
tool_flags = {"CFLAGS": ["-fPIC"]}

def init_configure(self):
    _bins = [
        f"lua{_mver}",
        f"luac{_mver}",
    ]
    # do not install the symlinks as BSD install(1) resolves those
    _libs = [
        f"liblua{_mver}.a",
        f"liblua{_mver}.so.{pkgver}",
    ]

    self.make_build_args += [
        "MYCFLAGS=" + self.get_cflags(shell = True),
        "MYLDFLAGS=" + self.get_ldflags(shell = True),
    ]
    self.make_install_args += [
        "INSTALL_TOP=" + str(self.chroot_destdir / "usr"),
        "TO_BIN=" + " ".join(_bins),
        "TO_LIB=" + " ".join(_libs),
        "INSTALL_INC=" + str(self.chroot_destdir / f"usr/include/lua{_mver}"),
        "INSTALL_MAN=" + str(self.chroot_destdir / "usr/share/man/man1")
    ]

def post_install(self):
    self.install_file(self.files_path / f"lua{_mver}.pc", "usr/lib/pkgconfig")
    self.install_license("doc/readme.html")

    self.mv(
        self.destdir / "usr/share/man/man1/lua.1",
        self.destdir / f"usr/share/man/man1/lua{_mver}.1"
    )
    self.mv(
        self.destdir / "usr/share/man/man1/luac.1",
        self.destdir / f"usr/share/man/man1/luac{_mver}.1"
    )

    self.install_link(f"lua{_mver}.1", "usr/share/man/man1/lua.1")
    self.install_link(f"luac{_mver}.1", "usr/share/man/man1/luac.1")

    _libf = f"liblua{_mver}.so.{pkgver}"
    self.install_link(_libf, f"usr/lib/liblua{_mver}.so")
    self.install_link(_libf, f"usr/lib/liblua{_mver}.so.{_mver}")

    # this is the primary lua
    self.install_link(f"lua{_mver}", "usr/bin/lua")
    self.install_link(f"luac{_mver}", "usr/bin/luac")
    self.install_link(f"lua{_mver}.pc", "usr/lib/pkgconfig/lua.pc")

@subpackage("lua54-devel")
def _devel(self):
    return self.default_devel(man = True)
