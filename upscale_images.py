import os, glob, base64
from PIL import Image
from io import BytesIO

files = glob.glob('assets/*.*')
files.sort(key=os.path.getmtime, reverse=True)
latest_images = files[:3]

html_file = 'mimis-stitches.html'
with open(html_file, 'r', encoding='utf-8') as f:
    html = f.read()

start_tag = '<div class="bridal-grid">'
start_idx = html.find(start_tag)
idx = start_idx + len(start_tag)
div_count = 1
end_idx = -1

while idx < len(html):
    next_open = html.find('<div', idx)
    next_close = html.find('</div', idx)
    
    if next_close == -1:
        break
        
    if next_open != -1 and next_open < next_close:
        div_count += 1
        idx = next_open + 4
    else:
        div_count -= 1
        idx = next_close + 6
        if div_count == 0:
            end_idx = next_close
            break

if end_idx == -1:
    print('Could not find closing div')
    exit()

new_html = ''
names = ['Contemporary Bridal', 'Royal White Gown', 'Bridal Inspiration']
for i, img_path in enumerate(latest_images):
    img = Image.open(img_path)
    # Upscale 2x using LANCZOS
    new_size = (img.width * 2, img.height * 2)
    upscaled = img.resize(new_size, Image.Resampling.LANCZOS)
    
    buffer = BytesIO()
    fmt = img.format if img.format else 'JPEG'
    if fmt == 'MPO': fmt = 'JPEG'
    # Use RGB for JPEG to avoid errors
    if upscaled.mode != 'RGB' and fmt == 'JPEG':
        upscaled = upscaled.convert('RGB')
        
    upscaled.save(buffer, format=fmt)
    b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
    mime = f'image/{fmt.lower()}'
    src = f'data:{mime};base64,{b64_str}'
    
    card = f'''
    <div class="garment-card bridal-card-sm reveal">
      <img class="garment-img" src="{src}">
      <div class="garment-caption">
        <span class="garment-tag">Bridal Couture</span>
        <span class="garment-name">{names[i]}</span>
        <a href="#contact" class="garment-link">Enquire about this piece ✧</a>
      </div>
    </div>
    '''
    new_html += card

html = html[:end_idx] + new_html + html[end_idx:]

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(html)

print('Successfully upscaled images and added to HTML.')
