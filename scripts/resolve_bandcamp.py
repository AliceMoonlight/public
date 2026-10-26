"""Resolve Bandcamp's public embed IDs for Night Index.

Runs on GitHub Actions; writes only safe IDs and presence flags, never lyrics.
"""
import json, re, html, time, os, datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
from urllib.parse import urlparse
from curl_cffi import requests

HORROR_WORDS = ['halloween','witch','witches','blood','bloody','ghost','ghosts','vampire','zombie','zombies','haunted','haunt','demon','devil','satan','curse','cursed','poison','grave','graveyard','cemetery','bones','skull','corpse','dead','death','fear','panic','nightmare','evil','monster','monsters','skeleton','shadow','darkness','ritual','magic','possession','possessed','coffin','horror','reaper','tomb','witchcraft','sorcery','slender','slaughter','kill','killer','murder','murderous','sacrifice','haunting']

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(ROOT, 'candidates.json'), encoding='utf-8'))['candidates']

class MetaParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.metas = []
    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            self.metas.append(dict(attrs))

def inspect(row):
    url = row['bandcamp_url']
    ans = {'status':'unavailable','url':url,'type':row['source_kind'],'has_published_lyrics':None}
    if row['source_kind'] != 'track' or not url.startswith('https://') or not urlparse(url).hostname.endswith('bandcamp.com'):
        ans['status'] = 'not_track_page'; return row['id'],ans
    for attempt in range(2):
      try:
        r = requests.get(url, timeout=28, impersonate='chrome', headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36','Accept-Language':'en-US,en;q=0.9'})
        ans['http_status'] = r.status_code
        if r.status_code != 200:
            ans['status'] = 'http_error'; time.sleep(attempt+1); continue
        body = r.text
        p=MetaParser(); p.feed(body[:200000]); props={}
        for m in p.metas:
            if m.get('name')=='bc-page-properties':
                try: props=json.loads(html.unescape(m['content']))
                except (ValueError, KeyError):pass
        id_ = props.get('item_id')
        if not id_:
            m = re.search(r'(?:"track_id"|&quot;track_id&quot;)\s*:\s*(\d+)',body)
            if m:id_=m.group(1)
        try: id_ = int(id_)
        except (TypeError, ValueError):id_=0
        if id_ <= 0 or id_ > 99999999999:
            ans['status']='id_not_found';ans['debug']={'head':body[:450],'meta':p.metas[:8],'bc_page_properties_found':'bc-page-properties' in body,'body_length':len(body),'track_id_seen':'track_id' in body};return row['id'],ans
        ans['status']='resolved';ans['track_id']=id_
        # Published Bandcamp lyrics are in a lyricsText block or tralbumData markup.
        try:
            from bs4 import BeautifulSoup
            soup=BeautifulSoup(body,'html.parser')
            node=soup.select_one('.lyricsText, .tralbumData.lyricsText, [itemprop="lyrics"]')
            if node:
                txt=node.get_text(' ',strip=True)
                ans['has_published_lyrics']=len(txt)>35 and 'lyrics' not in txt.lower()[:20]
                ans['lyric_word_count']=len(txt.split()) if ans['has_published_lyrics'] else 0
                if ans['has_published_lyrics']:
                    prompt = row['prompt'].lower()
                    text_lower=txt.lower()
                    ans['prompt_in_lyrics']=bool(re.search(r'(?<![a-z])'+re.escape(prompt)+r'(?![a-z])',text_lower))
                    found=[w for w in HORROR_WORDS if re.search(r'(?<![a-z])'+re.escape(w)+r'(?![a-z])',text_lower)]
                    ans['horror_words']=found[:12]
                    words=txt.split()
                    # Only a short excerpt (<= 8 words) is retained; never persist full lyrics.
                    sample_index=0
                    for i, word in enumerate(words):
                        norm=re.sub(r'[^a-z]','',word.lower())
                        if norm==prompt:
                            sample_index=i;break
                    else:
                        for i, word in enumerate(words):
                            norm=re.sub(r'[^a-z]','',word.lower())
                            if norm in found:
                                sample_index=i;break
                    start=max(0,sample_index-3)
                    ans['lyric_excerpt']=' '.join(words[start:start+8])

            else:
                # All pages contain the word lyrics in menus, so default to not verified.
                ans['has_published_lyrics']=False
                ans['lyric_word_count']=0
        except Exception as exc:
            ans['lyrics_audit_error']=str(exc)[:100]
        return row['id'],ans
      except Exception as e:
        ans['status']='request_error';ans['error']=str(e)[:160];time.sleep(attempt+1)
    return row['id'],ans

resolved={}
with ThreadPoolExecutor(max_workers=4) as pool:
    futs=[pool.submit(inspect,row) for row in rows]
    for f in as_completed(futs):
        ident,item=f.result();resolved[ident]=item
        print(f"{ident}: {item['status']} {item.get('track_id','')} lyrics={item.get('has_published_lyrics')} {item.get('http_status','')}", flush=True)
manifest={'source':'Bandcamp public track pages', 'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'tracks':resolved,
          'counts':{'resolved':sum(1 for v in resolved.values() if v['status']=='resolved'),'attempted':len(resolved), 'lyrics_verified':sum(1 for v in resolved.values() if v.get('has_published_lyrics') is True)}}
with open(os.path.join(ROOT,'player_manifest.json'),'w',encoding='utf-8') as f:json.dump(manifest,f,ensure_ascii=False,indent=2)
print('Final counts:',manifest['counts'],flush=True)