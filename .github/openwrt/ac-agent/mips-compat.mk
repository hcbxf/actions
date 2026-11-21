# ac-agent supports a pure-Go build. Avoid the CGO assembler failures on
# 32-bit MIPS (including mt7621), and remove the forced external linker too.
ifneq ($(filter mips mipsle,$(GO_ARCH)),)
  GO_PKG_TARGET_VARS += CGO_ENABLED=0
  GO_PKG_DEFAULT_LDFLAGS = -buildid '$(SOURCE_DATE_EPOCH)'
endif
