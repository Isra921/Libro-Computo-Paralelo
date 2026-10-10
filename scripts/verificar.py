from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
R=Path(__file__).resolve().parents[1]
errors=[]
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key not in ('src','href') or not value:continue
            parsed=urlsplit(value)
            if parsed.scheme or parsed.netloc or not parsed.path:continue
            target=(self.path.parent/unquote(parsed.path)).resolve()
            if not target.exists(): errors.append(f'{self.path.relative_to(R)} -> {value}')
for p in R.rglob('*.html'):
    parser=Links();parser.path=p;parser.feed(p.read_text(encoding='utf-8-sig'))
for p in R.rglob('*.json'):json.loads(p.read_text(encoding='utf-8-sig'))
catalog=json.loads((R/'assets/data/unidades-data.json').read_text(encoding='utf-8'))
topics=activities=0
for uid in catalog['unidades']:
    u=json.loads((R/f'assets/data/unidades/{uid}.json').read_text(encoding='utf-8'))
    topics+=len(u['temas']);activities+=len(u['temas'])+1
    for t in u['temas']:
        for url in (t['url'],t['actividad']['url']):
            if url and not (R/url).is_file():errors.append(url)
    final=u['actividad_final']['url']
    if final and not (R/final).is_file():errors.append(final)
print(f'{len(catalog["unidades"])} unidades, {topics} temas, {activities} actividades. JSON válidos.')
print('\n'.join(errors) if errors else 'Sin enlaces locales rotos en HTML ni en el catálogo.')
raise SystemExit(bool(errors))
