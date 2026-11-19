import base64
from PIL import Image

def generate_avatar_svg(png_path, svg_path):
    with open(png_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
        
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" width="100%" role="img">
  <title>Aditya Mohan Nair — Profile Avatar</title>
  <defs>
    <clipPath id="circleAvatar">
      <circle cx="250" cy="250" r="236"/>
    </clipPath>
    <filter id="avatarGlow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="6" stdDeviation="12" flood-color="#000000" flood-opacity="0.25"/>
    </filter>
    <linearGradient id="avatarRing" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#3b82f6"/>
      <stop offset="50%" stop-color="#8b5cf6"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>

  <!-- Ambient background glow & subtle ring -->
  <circle cx="250" cy="250" r="244" fill="#0f172a" filter="url(#avatarGlow)"/>
  <circle cx="250" cy="250" r="240" fill="none" stroke="url(#avatarRing)" stroke-width="3" stroke-dasharray="16 8" opacity="0.85"/>
  <circle cx="250" cy="250" r="236" fill="#fcf9f2"/>

  <!-- Portrait image clipped in circle -->
  <image href="data:image/png;base64,{encoded}" x="14" y="14" width="472" height="472" clip-path="url(#circleAvatar)" preserveAspectRatio="xMidYMid meet"/>

  <!-- Outer subtle tech accent ticks -->
  <circle cx="250" cy="250" r="248" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="2 18"/>
</svg>
'''
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generated circular avatar SVG: {svg_path}")

if __name__ == "__main__":
    generate_avatar_svg(
        "d:/Project/github profile/A2ZCoder404/source-photo.png",
        "d:/Project/github profile/A2ZCoder404/assets/profile-avatar.svg"
    )
