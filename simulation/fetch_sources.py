"""Fetch research inspection material separately from the offline simulation.

With no arguments, print the exact sources and do not access the network.
With --refresh, curl each successful primary-source URL and regenerate inspection
text and the source manifest. Do not run this during or after a recorded analysis
without creating a new receipt for any changed declared inputs. Bibliography and
parameter choices are never edited by this script. Failed historical attempts
remain distinguishable from inspected full texts.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
DEST = ROOT / "data" / "source_evidence"
CODE_COMMIT = "759d6a9f2002ab7367791c65118500091749d75e"
DOIS = {
    "longden2017": "10.1038/nn.4533",
    "moshkforoush2020": "10.1073/pnas.2000151117",
    "isaacs2024": "10.1073/pnas.2405965121",
    "longden2026": "10.1152/ajpcell.00065.2026",
    "kapela2018": "10.1111/micc.12429",
    "behringer2012": "10.1161/CIRCRESAHA.111.262592",
    "rivers1997": "10.1152/ajpheart.1997.273.1.H310",
    "postnov2015": "10.1007/s11538-014-0058-0",
    "hariharan2022": "10.1016/j.celrep.2022.111872",
}
URLS = {f"{name}.crossref.json": "https://api.crossref.org/works/" + doi.replace("/", "%2F") for name, doi in DOIS.items()}
URLS.update({
    "longden2017.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC5404963/fullTextXML",
    "isaacs2024.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11648664/fullTextXML",
    "postnov2015.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC4303742/fullTextXML",
    "hariharan2022.xml": "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10187957/fullTextXML",
    "moshkforoush2020.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7368319/",
    "longden2026.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC13186272/",
    "kapela2018.fulltext.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC5809195/",
    "behringer2012.fulltext.html": "https://pmc.ncbi.nlm.nih.gov/articles/PMC3467972/?report=xml",
    "moshk_Fig4C.m": f"https://raw.githubusercontent.com/ntsoukias/Capillary-Kir-Model/{CODE_COMMIT}/scripts/Fig4/Fig4C.m",
    "moshk_Fig3AB.m": f"https://raw.githubusercontent.com/ntsoukias/Capillary-Kir-Model/{CODE_COMMIT}/scripts/Fig3/Fig3AB.m",
    "moshk_LICENSE.txt": f"https://raw.githubusercontent.com/ntsoukias/Capillary-Kir-Model/{CODE_COMMIT}/LICENSE.txt",
    "moshk_code_tree.json": f"https://api.github.com/repos/ntsoukias/Capillary-Kir-Model/git/trees/{CODE_COMMIT}?recursive=1",
    "moshk_code_commit.json": f"https://api.github.com/repos/ntsoukias/Capillary-Kir-Model/commits/{CODE_COMMIT}",
})

class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)
    def handle_endtag(self, tag):
        if tag in {"p", "h2", "h3", "table", "tr"}:
            self.parts.append("\n")

def extract(path):
    if path.suffix == ".xml":
        root = ET.parse(path).getroot()
        lines = [" ".join("".join(el.itertext()).split()) for el in root.iter() if el.tag in {"p", "title", "table", "table-wrap"}]
        path.with_suffix(".txt").write_text("\n".join(lines))
    elif path.suffix == ".html":
        parser = TextOnly()
        parser.feed(path.read_text())
        path.with_suffix(".txt").write_text("".join(parser.parts))

def write_manifest():
    files = []
    for path in sorted(DEST.iterdir()):
        if not path.is_file() or path.name == "manifest.json":
            continue
        failed = "failed-response" in path.name or path.name == "moshk_SI_response.html"
        files.append({
            "file": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
            "url": URLS.get(path.name),
            "role": "failed-fetch-not-evidence" if failed else "registry-identity" if path.name.endswith("crossref.json") else "source-inspection-or-retrieval-aid",
            "inspected": path.name in URLS and not failed,
        })
    record = {"schema": 1, "created_utc": datetime.now(timezone.utc).isoformat(), "code_commit": CODE_COMMIT,
              "note": "Raw sources are inspection material, not analyzed empirical data. Text extraction aids retain the source license. No fulltext inspection is asserted for Rivers1997 or failed requests.", "files": files}
    (DEST / "manifest.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="explicitly repeat online retrieval")
    parser.add_argument("--manifest-only", action="store_true", help="hash current local files without networking")
    args = parser.parse_args()
    if args.manifest_only:
        write_manifest()
        return
    if not args.refresh:
        print(json.dumps(URLS, indent=2))
        return
    DEST.mkdir(parents=True, exist_ok=True)
    for name, url in URLS.items():
        target = DEST / name
        temporary = target.with_name(target.name + ".download")
        subprocess.run(["curl", "--fail", "--location", "--silent", "--show-error", "--retry", "3", "--max-time", "60", url, "--output", str(temporary)], check=True)
        if temporary.stat().st_size == 0:
            raise RuntimeError(f"Empty response: {url}")
        if name.endswith("crossref.json"):
            assert json.loads(temporary.read_text())["status"] == "ok"
        elif name.endswith(".xml"):
            ET.parse(temporary)
        temporary.replace(target)
        if target.suffix in {".xml", ".html"}:
            extract(target)
    write_manifest()

if __name__ == "__main__":
    main()
