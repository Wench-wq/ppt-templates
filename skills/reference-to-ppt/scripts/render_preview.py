import argparse,subprocess,tempfile,shutil
from pathlib import Path
import fitz
from PIL import Image,ImageDraw

def render(file,out):
 out.mkdir(parents=True,exist_ok=True);exe=shutil.which('soffice')
 if not exe:raise RuntimeError('LibreOffice soffice required')
 with tempfile.TemporaryDirectory() as tmp:subprocess.run([exe,'-env:UserInstallation='+Path(tmp).as_uri(),'--headless','--convert-to','pdf','--outdir',str(out.resolve()),str(file.resolve())],check=True,timeout=120)
 pdf=out/(file.stem+'.pdf')
 if not pdf.exists():raise RuntimeError('PDF not generated')
 doc=fitz.open(pdf);grid=Image.new('RGB',(1500,((len(doc)+2)//3)*305),'#ddd5c4')
 for i,page in enumerate(doc):
  pix=page.get_pixmap(matrix=fitz.Matrix(1.25,1.25));f=out/f'{i+1:02d}.png';pix.save(f);im=Image.open(f).convert('RGB');im.thumbnail((480,270));x=(i%3)*500;y=(i//3)*305;grid.paste(im,(x+10,y+10));ImageDraw.Draw(grid).text((x+15,y+285),str(i+1),fill='#343a24')
 grid.save(out/'contact-sheet.jpg');print('Rendered',len(doc),'pages')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('file');a.add_argument('--output',required=True);v=a.parse_args();render(Path(v.file),Path(v.output))
