"""Generate the code reference pages and navigation."""

from pathlib import Path
import mkdocs_gen_files



root = Path(__file__).parent.parent

mod_symbol = '<code class="doc-symbol doc-symbol-nav doc-symbol-module"></code>'


nav = mkdocs_gen_files.Nav()
src = Path("src/")

for path in sorted(src.rglob("*.py")):
    
    module_path = path.relative_to(src).with_suffix("")
    doc_path = path.relative_to(src).with_suffix(".md")
    full_doc_path = Path("reference", doc_path)
    parts = tuple(module_path.parts)

    # print(f"doc path: {doc_path}")
    # print(f"full doc path: {full_doc_path}")

    if parts[-1].startswith("__"):
        continue

    nav_parts = [f"{mod_symbol} {part}" for part in parts]
    nav[tuple(nav_parts)] = doc_path.as_posix()

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(parts)
        print("::: " + ident)
        fd.write(f"::: {ident}")

    mkdocs_gen_files.set_edit_path(full_doc_path, Path("../") / path)

with mkdocs_gen_files.open(f"reference/SUMMARY.md", "w") as nav_file: 
    nav_file.writelines(nav.build_literate_nav())
