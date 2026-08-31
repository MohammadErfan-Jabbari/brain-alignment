# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown>=3.5", "pymdown-extensions>=10"]
# ///
"""Render a teach-mode lesson markdown file to a self-contained HTML view.

Inline `$...$` and display `$$...$$` math render via KaTeX; ```mermaid blocks
render via Mermaid. Both load from a CDN, so open the output in a browser with
internet. The markdown lesson is the source of truth; this HTML is a disposable
view that solves the terminal's no-render problem.

Usage:
  uv run .claude/skills/teach/scripts/render_lesson.py <lesson.md> [out.html]
"""
import sys
from pathlib import Path

import markdown

KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist"
MERMAID = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"

TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="__KATEX__/katex.min.css">
<script defer src="__KATEX__/katex.min.js"></script>
<script defer src="__KATEX__/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body,{delimiters:[
    {left:'$$',right:'$$',display:true},
    {left:'$',right:'$',display:false},
    {left:'\\[',right:'\\]',display:true},
    {left:'\\(',right:'\\)',display:false}],throwOnError:false});"></script>
<style>
 body{max-width:820px;margin:2.5rem auto;padding:0 1.2rem;
   font:16px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1a1a1a}
 h1,h2,h3{line-height:1.25} h1{font-size:1.7rem} h2{font-size:1.3rem;margin-top:2rem}
 code{background:#f3f3f3;padding:.1em .35em;border-radius:3px;font-size:.9em}
 pre{background:#f6f8fa;padding:1rem;border-radius:6px;overflow-x:auto}
 pre code{background:none;padding:0}
 table{border-collapse:collapse;margin:1rem 0} th,td{border:1px solid #ddd;padding:.4rem .7rem}
 blockquote{border-left:3px solid #c9933a;margin:1rem 0;padding:.2rem 1rem;color:#444;background:#fffaf0}
 hr{border:none;border-top:1px solid #e0e0e0;margin:2rem 0}
 .banner{background:#fff3cd;border:1px solid #e0c97a;border-radius:6px;padding:.6rem 1rem;font-size:.9em}
</style></head><body>
__BODY__
<script type="module">
 import mermaid from "__MERMAID__";
 document.querySelectorAll('pre > code.language-mermaid').forEach(c=>{
   const d=document.createElement('div');d.className='mermaid';d.textContent=c.textContent;
   c.parentElement.replaceWith(d);});
 mermaid.initialize({startOnLoad:true});
</script></body></html>
"""


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: render_lesson.py <lesson.md> [out.html]")
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".html")
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists",
                    "pymdownx.arithmatex"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}},
    )
    body = md.convert(src.read_text(encoding="utf-8"))
    html = (TEMPLATE.replace("__TITLE__", src.stem).replace("__KATEX__", KATEX)
            .replace("__MERMAID__", MERMAID).replace("__BODY__", body))
    out.write_text(html, encoding="utf-8")
    print(f"rendered -> {out}")


if __name__ == "__main__":
    main()
