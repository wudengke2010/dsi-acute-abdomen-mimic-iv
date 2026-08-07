"""
SVG Optimization Pipeline (Inkscape-compatible publication output)
====================================================================
Optimizes matplotlib-generated SVGs using scour to:
  - Remove metadata, comments, and unnecessary attributes
  - Simplify path data and reduce precision
  - Compact IDs and CSS
  - Reduce file size while preserving visual quality

Output: figures_publication/optimized/
"""

from pathlib import Path
from scour import scour

SRC_DIR = Path('figures_publication')
OPT_DIR = SRC_DIR / 'optimized'
OPT_DIR.mkdir(exist_ok=True)

options = scour.generateDefaultOptions()
options.enable_viewboxing = True
options.strip_xml_prolog = True
options.remove_titles = True
options.remove_descriptions = True
options.remove_metadata = True
options.strip_ids = True
options.shorten_ids = True
options.embed_rasters = False
options.keep_defs = False
options.strip_comments = True
options.simple_colors = True
options.style_to_xml = True
options.group_collapse = True
options.renderer_workaround = True
options.digits = 5

print('=' * 60)
print('SVG Optimization Pipeline')
print(f'Input:  {SRC_DIR}/')
print(f'Output: {OPT_DIR}/')
print('=' * 60)

svg_files = sorted(SRC_DIR.glob('Fig*.svg'))
print(f'Found {len(svg_files)} SVG files to optimize.')

for svg in svg_files:
    opt_svg = OPT_DIR / svg.name
    with open(svg, 'r', encoding='utf-8') as f:
        input_string = f.read()
    output_string = scour.scourString(input_string, options)
    with open(opt_svg, 'w', encoding='utf-8') as f:
        f.write(output_string)
    original_size = svg.stat().st_size
    optimized_size = opt_svg.stat().st_size
    reduction = (1 - optimized_size / original_size) * 100
    print(f'{svg.name:30s} {original_size/1024:6.1f} KB -> {optimized_size/1024:6.1f} KB ({reduction:5.1f}% reduction)')

print('\n' + '=' * 60)
print('Optimization complete.')
print('=' * 60)
