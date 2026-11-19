import numpy as np
from PIL import Image, ImageOps, ImageEnhance

def generate_halftone_face(input_path, output_svg_path, cols=90):
    img = Image.open(input_path).convert('L')
    
    # Crop tightly around head/shoulders if necessary, or use as is (it's already a square centered portrait)
    # Enhance contrast for clean editorial look
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.25)
    img = ImageOps.autocontrast(img, cutoff=1)
    
    # Calculate aspect ratio
    rows = int(cols * (img.height / img.width))
    img_small = img.resize((cols, rows), Image.Resampling.LANCZOS)
    pixels = np.array(img_small)
    
    view_width = 450
    view_height = int(view_width * (rows / cols))
    cell_w = view_width / cols
    cell_h = view_height / rows
    
    svg_circles = []
    
    # Cream background like Avi reference and editorial prints
    bg_color = "#f8f9fa"
    border_color = "#e2e8f0"
    
    for y in range(rows):
        for x in range(cols):
            val = float(pixels[y, x])
            # The background in source-photo.png is ~240-255
            if val < 238:
                # 0 = darkest (hair, eyes, beard), 238 = lightest skin highlight
                darkness = (238.0 - val) / 238.0
                # Non-linear scaling to preserve subtle facial features
                r = (cell_w / 2.0) * (darkness ** 0.8) * 0.98
                if r >= 0.35:
                    cx = x * cell_w + cell_w / 2.0
                    cy = y * cell_h + cell_h / 2.0
                    
                    # Subtle tonal coloring: deepest blacks for hair/beard, muted charcoal for midtones
                    if darkness > 0.7:
                        fill = "#0f172a"
                        op = 0.95
                    elif darkness > 0.4:
                        fill = "#334155"
                        op = 0.85
                    else:
                        fill = "#64748b"
                        op = 0.65
                    
                    svg_circles.append(f'  <circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" opacity="{op:.2f}"/>')
    
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_width} {view_height}" width="100%" role="img">
  <title>Aditya Mohan Nair — Halftone Portrait</title>
  <desc>Stylized editorial halftone stippled portrait generated from verified photograph.</desc>
  <defs>
    <filter id="portraitShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#000000" flood-opacity="0.12"/>
    </filter>
    <clipPath id="portraitClip">
      <rect x="0" y="0" width="{view_width}" height="{view_height}" rx="16" ry="16"/>
    </clipPath>
  </defs>
  
  <!-- Outer card with subtle border and cream background -->
  <rect x="0" y="0" width="{view_width}" height="{view_height}" rx="16" ry="16" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5" filter="url(#portraitShadow)"/>
  
  <!-- Halftone Dot Matrix -->
  <g clip-path="url(#portraitClip)">
{chr(10).join(svg_circles)}
  </g>
  
  <!-- Subtle Editorial Caption -->
  <g transform="translate(20, {view_height - 18})">
    <text font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, monospace" font-size="9" fill="#94a3b8" letter-spacing="1.5">ADITYA MOHAN NAIR · DEV IDENTITY</text>
  </g>
</svg>
'''
    with open(output_svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f"Generated halftone portrait with {len(svg_circles)} stippled elements: {output_svg_path}")

if __name__ == '__main__':
    generate_halftone_face(
        'd:/Project/github profile/A2ZCoder404/source-photo.png',
        'd:/Project/github profile/A2ZCoder404/assets/hero-face.svg'
    )
