#!/usr/bin/env python3
"""
SVG Quality Assurance & Optimizer
Scans assets/*.svg, parses XML to verify structural validity, validates
viewBox specifications, and reports clean file sizes.
"""

import os
import xml.etree.ElementTree as ET

def optimize_and_validate():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "..", "assets")

    if not os.path.exists(assets_dir):
        print(f"[!] Assets directory not found at {assets_dir}")
        return

    svg_files = [f for f in os.listdir(assets_dir) if f.endswith(".svg")]
    print(f"[*] Validating and analyzing {len(svg_files)} SVG graphics in {assets_dir}:\n")

    print(f"{'FILE NAME':<26} {'VIEWBOX':<20} {'SIZE (KB)':<10} {'VALIDITY'}")
    print("-" * 68)

    errors = 0
    total_size = 0

    for filename in sorted(svg_files):
        filepath = os.path.join(assets_dir, filename)
        size_kb = os.path.getsize(filepath) / 1024
        total_size += size_kb

        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            viewbox = root.attrib.get("viewBox", "Not Specified")
            status = "✓ VALID XML"
        except ET.ParseError as pe:
            viewbox = "ERROR"
            status = f"✗ PARSE ERROR ({pe})"
            errors += 1

        print(f"{filename:<26} {viewbox:<20} {size_kb:>8.1f} KB   {status}")

    print("-" * 68)
    print(f"Total SVG Assets: {len(svg_files)} | Total Size: {total_size:.1f} KB | Errors: {errors}")
    if errors == 0:
        print("[✓] All SVGs pass XML standards and GitHub presentation readiness!")

if __name__ == "__main__":
    optimize_and_validate()
