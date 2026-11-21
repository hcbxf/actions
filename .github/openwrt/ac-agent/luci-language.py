#!/usr/bin/env python3
"""Keep LuCI's selected language, with Chinese fallback for the agent view."""

import gettext
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


def main():
    package = Path(sys.argv[1])
    language_dir = package / "po/zh_Hans"
    view = package / "htdocs/luci-static/resources/view/ac-agent/overview.js"
    source = view.read_text(encoding="utf-8")
    marker = "// AC agent: follow LuCI language, with Chinese fallback."
    if marker in source:
        return

    # Keep LuCI's require directives ahead of executable JavaScript.
    directives = list(re.finditer(r"^['\"]require [^'\"\n]+['\"];[ \t]*$", source, re.M))
    if not directives:
        raise ValueError("Cannot find the ac-agent view's LuCI require directives")

    shutil.copyfile(Path(__file__).with_name("zh-cn.po"), language_dir / "ac-agent-ci.po")
    merged = subprocess.run(
        ["msgcat", "--use-first", str(language_dir / "ac-agent.po"),
         str(language_dir / "ac-agent-ci.po")],
        check=True, stdout=subprocess.PIPE,
    )
    compiled = subprocess.run(
        ["msgfmt", "-o", "-", "-"], input=merged.stdout,
        check=True, stdout=subprocess.PIPE,
    )
    translations = gettext.GNUTranslations(io.BytesIO(compiled.stdout))
    catalog = {
        key: value for key, value in translations._catalog.items()
        if isinstance(key, str) and key and value
    }
    fallback = """

%s
var _ = (function(translate) {
    var chinese = %s;
    return function(message, context) {
        var translated = translate(message, context);
        var language = document.documentElement.lang || '';
        if (translated !== message || /^en(?:[-_]|$)/i.test(language))
            return translated;
        return Object.prototype.hasOwnProperty.call(chinese, message)
            ? chinese[message] : translated;
    };
})(window._);
""" % (marker, json.dumps(catalog, ensure_ascii=False, sort_keys=True))
    position = directives[-1].end()
    view.write_text(source[:position] + fallback + source[position:], encoding="utf-8")


if __name__ == "__main__":
    main()
