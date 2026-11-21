#
# Host-only stand-in for OpenWrt's golang package.
#
# Used when the selected source tree ships a Go older than 1.21 (22.03 has
# Go 1.19). ac-agent's go.mod declares "go 1.26", which Go 1.19 cannot even
# parse, and GOTOOLCHAIN=auto only exists since Go 1.21.
#
# Instead of building Go from source (which needs a 1.4 -> 1.17 -> 1.21
# bootstrap chain), unpack the official prebuilt linux-amd64 toolchain into
# the layout expected by feeds/packages/lang/golang: staging_dir/hostpkg/
# lib/go-cross, plus staging_dir/hostpkg/bin/go.
#
# The package is named "golang" so ac-agent's PKG_BUILD_DEPENDS:=golang/host
# resolves to it; the workflow removes the feed's golang package first.
#
include $(TOPDIR)/rules.mk

PKG_NAME:=golang
PKG_VERSION:=1.26.0
PKG_RELEASE:=1

PKG_SOURCE:=go$(PKG_VERSION).linux-amd64.tar.gz
PKG_SOURCE_URL:=https://go.dev/dl/ \
	https://mirrors.ustc.edu.cn/golang/ \
	https://mirrors.nju.edu.cn/golang/
# sha256 of the official go1.26.0.linux-amd64.tar.gz release archive.
PKG_HASH:=aac1b08a0fb0c4e0a7c1555beb7b59180b05dfc5a3d62e40e9de90cd42f88235

PKG_LICENSE:=BSD-3-Clause
PKG_MAINTAINER:=OpenWrt AC CI

HOST_BUILD_DIR:=$(BUILD_DIR_HOST)/go-$(PKG_VERSION)

include $(INCLUDE_DIR)/host-build.mk
include $(INCLUDE_DIR)/package.mk

HOST_UNPACK:=$(HOST_TAR) -C "$(HOST_BUILD_DIR)" --strip-components=1 -xzf "$(DL_DIR)/$(PKG_SOURCE)"

define Package/golang
  SECTION:=lang
  CATEGORY:=Languages
  TITLE:=Go programming language (prebuilt host toolchain)
  URL:=https://go.dev/
endef

# The target package is never selected; it only exists so the package shows
# up in the build metadata next to its host variant.
define Package/golang/install
	$(INSTALL_DIR) $(1)/usr/lib/go-$(PKG_VERSION)
endef

define Host/Compile
endef

define Host/Install
	$(INSTALL_DIR) "$(STAGING_DIR_HOSTPKG)/lib/go-cross"
	$(CP) "$(HOST_BUILD_DIR)/." "$(STAGING_DIR_HOSTPKG)/lib/go-cross/"
	$(INSTALL_DIR) "$(STAGING_DIR_HOSTPKG)/bin"
	$(LN) ../lib/go-cross/bin/go "$(STAGING_DIR_HOSTPKG)/bin/go"
	$(LN) ../lib/go-cross/bin/gofmt "$(STAGING_DIR_HOSTPKG)/bin/gofmt"
endef

$(eval $(call HostBuild))
$(eval $(call BuildPackage,golang))
