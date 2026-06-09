with open('mimis-stitches.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the first hero-panel-caption
start_idx = html.find('class="hero-panel-caption"')
if start_idx == -1:
    print("Could not find hero-panel-caption")
    exit()

end_idx = html.find('</div>', start_idx)
caption_html = html[start_idx:end_idx]

# Replace "Bridal Couture" with "Bridal & Bespoke"
new_caption_html = caption_html.replace('Bridal Couture', 'Bridal & Bespoke')
# Replace "Gowns for" with "Attire for"
new_caption_html = new_caption_html.replace('Gowns for', 'Attire for')

html = html[:start_idx] + new_caption_html + html[end_idx:]

with open('mimis-stitches.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Caption updated successfully.")
