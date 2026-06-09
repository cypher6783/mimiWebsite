import bs4, re
with open('mimis-stitches.html', 'r', encoding='utf-8') as f:
    html = f.read()
soup = bs4.BeautifulSoup(html, 'html.parser')
panel = soup.find('div', class_='hero-panel')
if panel:
    clean_panel = re.sub(r'src="data:image/[^"]+"', 'src="..."', str(panel))
    print(clean_panel.encode('ascii', 'ignore').decode('ascii'))
