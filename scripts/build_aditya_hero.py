import os
import re
import numpy as np
from PIL import Image, ImageOps, ImageEnhance
import xml.sax.saxutils as saxutils

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

def get_font_and_css_block():
    css_path = os.path.join(ROOT, 'data', 'hero_fonts.css')
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    hero_path = os.path.join(ROOT, 'cards', 'hero.svg')
    if os.path.exists(hero_path):
        with open(hero_path, 'r', encoding='utf-8') as f:
            content = f.read()
        m = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
        if m:
            return m.group(1)
    raise ValueError("Could not find hero_fonts.css or cards/hero.svg for style block")

def generate_ascii_rows(photo_path=None, cols=180, rows=96):
    if photo_path is None:
        photo_path = os.path.join(ROOT, 'source-photo.png')
    img = Image.open(photo_path).convert('RGB')
    
    # 1120x1120 square crop centered on face
    # Center X: 623, Y: 60 to 1180
    crop_box = (63, 60, 1183, 1180)
    cropped = img.crop(crop_box)
    
    gray = cropped.convert('L')
    
    # Increase sharpness and contrast for crisp facial features
    gray = ImageEnhance.Contrast(gray).enhance(1.3)
    gray = ImageEnhance.Sharpness(gray).enhance(1.4)
    
    arr = np.array(gray, dtype=np.float32)
    
    # Clean background: in source-photo.png, background is warm off-white (>216)
    bg_mask = arr > 216
    arr[bg_mask] = 255.0
    
    # Non-background face and body
    face_mask = ~bg_mask
    if np.any(face_mask):
        # Stretch face tones between 0 and 215
        min_v = arr[face_mask].min()
        max_v = arr[face_mask].max()
        # Normalization
        norm = (arr[face_mask] - min_v) / (max_v - min_v + 1e-5) * 215.0
        # Gentle curve: boost contrast between skin and dark features (hair, eyes, beard/stubble, clothes)
        # Values under 80 get pulled darker (towards 0), values above 140 stay bright
        norm = np.where(norm < 85, norm * 0.75, norm)
        arr[face_mask] = norm
        
    cleaned_img = Image.fromarray(arr.astype(np.uint8))
    small = cleaned_img.resize((cols, rows), Image.Resampling.LANCZOS)
    small_arr = np.array(small, dtype=np.float32)
    
    # Density ramp from Avi's hero:
    # ' ' (light/empty) -> . ` : - = + * c s # % @ (dark/dense)
    RAMP = " .`:-=+*cs#%@"
    
    ascii_rows = []
    y_start = 43.2
    y_step = 8.333
    delay_start = 0.250
    delay_step = (1.960 - 0.250) / (rows - 1)
    
    for r in range(rows):
        line_chars = []
        for c in range(cols):
            p = small_arr[r, c]
            if p >= 210:
                line_chars.append(' ')
            else:
                # 0 (darkest) -> 1.0, 210 (lightest) -> 0.0
                ratio = (210.0 - p) / 210.0
                # Using 13 bins so the top range cleanly maps to '@' and '%'
                idx = int(ratio * len(RAMP))
                idx = max(1, min(len(RAMP) - 1, idx))
                line_chars.append(RAMP[idx])
                
        raw_str = ''.join(line_chars)
        safe_str = saxutils.escape(raw_str)
        
        y_val = y_start + r * y_step
        delay = delay_start + r * delay_step
        
        row_svg = f'<text class="f" style="animation-delay:{delay:.3f}s;animation-duration:.35s" xml:space="preserve" x="20" y="{y_val:.1f}" fill="#111111" font-size="7.2" textLength="800" lengthAdjust="spacing">{safe_str}</text>'
        ascii_rows.append(row_svg)
        
    return '\n  '.join(ascii_rows)

def build_hero_svg(output_path=None):
    if output_path is None:
        output_path = os.path.join(ROOT, 'cards', 'hero.svg')
    css_content = get_font_and_css_block()
    ascii_markup = generate_ascii_rows()
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="880.000" height="432" viewBox="0 0 880.000 432" role="img" aria-label="Aditya Nair. Computer Engineering Student and Fullstack AI Developer at Team Pixel Nova."><title>Aditya Nair. Computer Engineering Student and Fullstack AI Developer at Team Pixel Nova.</title><style>{css_content}</style>
<defs>
  <linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0">
    <stop offset="0" stop-color="#111111"/><stop offset=".42" stop-color="#111111"/>
    <stop offset=".5" stop-color="#2f55ff"/><stop offset=".58" stop-color="#111111"/>
    <stop offset="1" stop-color="#111111"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;600 0"
      keyTimes="0;.45;1" dur="7s" begin="1.6s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<rect width="880" height="420" rx="14" fill="#f3f3f1"/>
<g class="f" style="animation-delay:0.00s">
  <rect class="live" x="48" y="49" width="8" height="8" rx="2" fill="#2f55ff"/>
  <text x="66" y="57" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="12" letter-spacing="1" fill="#6e6e73">COMPUTER ENGINEERING · FULLSTACK &amp; AI</text>
</g>
<text class="r" style="animation-delay:0.15s" x="44" y="190" font-family="'Instrument Serif', Georgia, serif" font-size="116" letter-spacing="-2.5" fill="#111111">Aditya</text>
<text class="r" style="animation-delay:0.30s" x="44" y="290" font-family="'Instrument Serif', Georgia, serif" font-style="italic" font-size="116" letter-spacing="-2.5" fill="url(#shine)">Nair</text>
<g class="r" style="animation-delay:0.55s">
  <text x="48" y="338" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="18" fill="#3a3a3c">Core builder at Team Pixel Nova. I build AI systems,</text>
  <text x="48" y="365" font-family="Geist, system-ui, -apple-system, sans-serif" font-size="18" fill="#3a3a3c">autonomous agents &amp; teach people to do the same.</text>
</g>
<g class="f" style="animation-delay:0.80s">
  <a href="https://striveforexcellence.in/" target="_blank">
    <text x="48" y="396" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#111111">striveforexcellence.in</text>
    <text class="nu" x="232" y="396" font-family="'Geist Mono', ui-monospace, SFMono-Regular, Menlo, monospace" font-size="13" fill="#2f55ff">&#8599;</text>
  </a>
</g>
<g transform="translate(520 46) scale(0.41) translate(-20 -37)" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">
  {ascii_markup}
</g>
</svg>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f"Successfully generated {output_path} (length: {len(svg)})")

if __name__ == '__main__':
    build_hero_svg()
