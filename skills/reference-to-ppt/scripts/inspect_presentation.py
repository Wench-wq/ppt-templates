import argparse,json,zipfile
from pathlib import Path
from pptx import Presentation
from lxml import etree

def inspect(file):
 p=Presentation(file);r={'slides':len(p.slides),'editable_textboxes':0,'native_charts':0,'transitions':0,'internal_links':0,'errors':[],'limits':['Text overflow and overlap require visual inspection','WPS playback unverified']}
 with zipfile.ZipFile(file) as z:
  if z.testzip():r['errors'].append('CRC failure')
  for n in z.namelist():
   if n.endswith('.xml'):etree.fromstring(z.read(n))
 for i,s in enumerate(p.slides,1):
  for q in s.shapes:
   if q.left<0 or q.top<0 or q.left+q.width>p.slide_width+10000 or q.top+q.height>p.slide_height+10000:r['errors'].append(f'Slide {i}: shape {q.shape_id} outside canvas')
   r['editable_textboxes']+=int(q.has_text_frame and bool(q.text.strip()));r['native_charts']+=int(q.has_chart)
  r['transitions']+=len(s._element.xpath('./p:transition'));r['internal_links']+=len(s._element.xpath('.//a:hlinkClick'))
 return r
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('file');a.add_argument('--output',required=True);v=a.parse_args();r=inspect(v.file);Path(v.output).write_text(json.dumps(r,ensure_ascii=False,indent=2));print(r);raise SystemExit(bool(r['errors']))
