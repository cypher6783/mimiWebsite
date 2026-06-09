import re

with open('mimis-stitches.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find Bridal Inspiration card
search_str = '<span class="garment-name">Bridal Inspiration</span>'
idx = html.find(search_str)

if idx == -1:
    print("Could not find Bridal Inspiration card")
    exit()

card_start = html.rfind('<div class="garment-card', 0, idx)

# Find the end of this div. We know it ends after the </a>
end_idx = html.find('</div>', html.find('</div>', html.find('</a>', idx)) + 6) + 6

card_html = html[card_start:end_idx]

# Extract src
src_match = re.search(r'src="(data:image/jpeg;base64,.*?)"', card_html)
if not src_match:
    print("Could not find src in card")
    exit()

new_src = src_match.group(1)

# Remove card from html
html = html[:card_start] + html[end_idx:]

# Find the first hero-panel-img
first_hero_idx = html.find('class="hero-panel-img"')
src_start = html.find('src="', first_hero_idx) + 5
src_end = html.find('"', src_start)

html = html[:src_start] + new_src + html[src_end:]

with open('mimis-stitches.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully moved wedding ideas to hero section.")
