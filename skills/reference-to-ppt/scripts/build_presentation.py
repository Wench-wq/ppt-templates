import argparse,json,zipfile,random
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.oxml.xmlchemy import OxmlElement

def build(d,out,template=None):
 allowed={'cover','agenda','section','content','compare','process','chart','summary','closing'}
 for s in d['slides']:
  if s['type'] not in allowed or not s['title']:raise ValueError('Invalid page')
  if len(s.get('body',[]))>4 or any(len(x)>65 for x in s.get('body',[])):raise ValueError('Split long content')
  if s['type']=='chart' and (not s.get('source') or len(s['categories'])!=len(s['values'])):raise ValueError('Chart requires matching data and source')
 p=Presentation(template) if template else Presentation()
 for sid in list(p.slides._sldIdLst):p.part.drop_rel(sid.rId);p.slides._sldIdLst.remove(sid)
 p.slide_width=Inches(13.3333);p.slide_height=Inches(7.5);c=d['palette'];fonts=d['fonts'];out.parent.mkdir(parents=True,exist_ok=True)
 assets=out.parent/'assets';assets.mkdir(exist_ok=True);rng=random.Random(11)
 base=tuple(bytes.fromhex(c['bg']));im=Image.new('RGB',(1200,675));im.putdata([tuple(max(0,min(255,v+rng.randint(-2,2))) for v in base) for _ in range(1200*675)]);im.save(assets/'paper.png')
 def box(sl,x,y,w,h,k,oval=False):
  q=sl.shapes.add_shape(MSO_SHAPE.OVAL if oval else MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h));q.fill.solid();q.fill.fore_color.rgb=RGBColor.from_string(c[k]);q.line.fill.background();q._element.spPr.append(OxmlElement('a:effectLst'));return q
 def txt(sl,t,x,y,w,h,size=26,k='ink',title=False):
  q=sl.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h));tf=q.text_frame;tf.word_wrap=True
  tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
  for i,line in enumerate(t.split('\n')):
   a=tf.paragraphs[0] if i==0 else tf.add_paragraph();a.text=line;a.font.name=fonts['title' if title else 'body'];a.font.size=Pt(size);a.font.color.rgb=RGBColor.from_string(c[k]);a.space_after=Pt(8)
  return q
 def cup(sl,x,y,z):
  box(sl,x+.15*z,y+.3*z,3.2*z,2.35*z,'olive',True);box(sl,x,y,3.2*z,2.35*z,'paper',True);box(sl,x+.35*z,y+.28*z,2.5*z,1.8*z,'orange',True)
  box(sl,x+2.8*z,y+.4*z,.7*z,1*z,'paper',True);box(sl,x+2.98*z,y+.57*z,.32*z,.65*z,'bg',True)
  for i in range(10):
   q=box(sl,x+(.6+i*.16)*z,y+.8*z,.11*z,.025*z,'paper');q.rotation=i*13
 expanded=[]
 for logical,s in enumerate(d['slides']):
  for n in (range(1,len(s['body'])+1) if s['type']=='process' and s.get('reveal') else [len(s.get('body',[]))]):expanded.append((logical,s,n))
 first={};created=[];layout=next((x for x in p.slide_layouts if x.name.lower()=='blank'),p.slide_layouts[-1])
 for i,(logical,s,n) in enumerate(expanded):
  sl=p.slides.add_slide(layout);first.setdefault(logical,sl);created.append(sl);sl.shapes.add_picture(str(assets/'paper.png'),0,0,width=p.slide_width,height=p.slide_height)
  for j in range(6):box(sl,0,j*1.25,.22,1.18,'olive' if j%2 else 'orange')
  txt(sl,f'{i+1:02d}',12.1,7.0,.6,.3,13);t=s['type'];body=s.get('body',[])
  if t in {'cover','section','closing'}:
   for row in range(5):
    for col in range(4):box(sl,8.35+col*1.22,row*1.5,1.13,1.42,'olive' if (row+col)%2 else 'paper')
   cup(sl,8.55,2.25,1.08);txt(sl,'WARM CLASSROOM / 学习札记',.8,1.0,7,.5,17,'olive');txt(sl,s['title'],.8,2.05,7,2.15,42,title=True);txt(sl,'\n'.join(body),.85,4.7,6.8,1.6,24)
  else:
   txt(sl,s['title'],.8,.55,11.7,.8,34,title=True);box(sl,.82,1.55,.8,.07,'orange')
   if t in {'process','compare'}:
    w=(11.65-(len(body)-1)*.3)/len(body)
    for j,line in enumerate(body[:n]):
     x=.8+j*(w+.3);box(sl,x,2.15,w,3.9,'paper');box(sl,x+.25,2.45,.6,.6,'orange',True);txt(sl,str(j+1),x+.42,2.5,.3,.4,20,'paper');txt(sl,line,x+.3,3.4,w-.6,2.2,25)
   elif t=='chart':
    data=CategoryChartData();data.categories=s['categories'];data.add_series(s.get('series','人数'),s['values']);ch=sl.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED,Inches(1),Inches(2),Inches(8),Inches(4.35),data).chart;ch.has_legend=False
    for ax in [ch.category_axis,ch.value_axis]:ax.tick_labels.font.name=fonts['body'];ax.tick_labels.font.size=Pt(18)
    ch.series[0].format.fill.solid();ch.series[0].format.fill.fore_color.rgb=RGBColor.from_string(c['olive']);ch.plots[0].has_data_labels=True;ch.plots[0].data_labels.font.size=Pt(18)
    txt(sl,'\n'.join(body),9.35,2.6,3.05,2.8,23);txt(sl,s['source'],1,6.55,11,.4,16,'olive')
   else:
    for j,line in enumerate(body):box(sl,.85,2+j*1.02,.12,.55,'orange');txt(sl,line,1.25,1.95+j*1.02,10.8,.9,26)
    if len(body)<4:cup(sl,10.5,5.2,.52)
  sl.notes_slide.notes_text_frame.text=s.get('notes','')+f'\n预计 {s.get("minutes",1)} 分钟。'+(f'\n连续页揭示第 {n} 步，手动翻页。' if t=='process' else '')
  tr=OxmlElement('p:transition');tr.set('spd','med');tr.append(OxmlElement('p:fade'));sl._element.insert_element_before(tr,'p:timing','p:extLst')
 for j,s in enumerate(d['slides']):
  if s['type']=='agenda':
   for k,target in enumerate(s.get('targets',[])):
    q=txt(first[j],'→',11.7,2+k*1.02,.6,.5,25,'olive');q.click_action.target_slide=first[target]
 for sl in created:
  if 1 in first and sl!=first[1]:txt(sl,'目录',.8,7.03,.8,.28,13,'olive').click_action.target_slide=first[1]
 from lxml import etree
 for part in p.part.package.iter_parts():
  if str(part.partname).startswith('/ppt/theme/'):
   root=etree.fromstring(part.blob);ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
   for tag,font in [('majorFont',fonts['title']),('minorFont',fonts['body'])]:
    for q in root.xpath('//a:'+tag+'/a:latin|//a:'+tag+'/a:ea',namespaces=ns):q.set('typeface',font)
   for tag,key in [('accent1','olive'),('accent2','orange')]:
    for q in root.xpath('//a:clrScheme/a:'+tag+'/a:srgbClr',namespaces=ns):q.set('val',c[key])
   part._blob=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
 p.save(out);return len(expanded)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--input',required=True);a.add_argument('--output',required=True);a.add_argument('--potx');a.add_argument('--template');v=a.parse_args();d=json.loads(Path(v.input).read_text());n=build(d,Path(v.output),v.template)
 if v.potx:
  with zipfile.ZipFile(v.output) as src,zipfile.ZipFile(v.potx,'w',zipfile.ZIP_DEFLATED) as dst:
   for name in src.namelist():
    b=src.read(name)
    if name=='[Content_Types].xml':b=b.replace(b'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml',b'application/vnd.openxmlformats-officedocument.presentationml.template.main+xml')
    dst.writestr(name,b)
 print(f'{len(d["slides"])} logical / {n} physical slides')
