from pathlib import Path
import json, math
from PIL import Image, ImageDraw, ImageFont
P=Path(__file__).parent
models=json.loads((P/'character_geometry.json').read_text())
img=Image.new('RGB',(1600,850),(17,24,36)); d=ImageDraw.Draw(img)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(fontpath,25); title=ImageFont.truetype(fontpath,40); small=ImageFont.truetype(fontpath,17)
d.text((45,25),'HERO CAVES  /  CHARACTER MODELS',font=title,fill=(236,236,224))
d.text((46,82),'Geometrievorschau der erstellten Roblox-Modelle',font=small,fill=(146,165,185))
def projection(v,base):
 x,y,z=v
 return (base+.84*x*71+.55*z*71,465-(.24*x+.88*y-.36*z)*71)
def depth(v): return .5*v[0]+.35*v[1]-.8*v[2]
sub=['Stahlrüstung · Schwert & Schild','Fellrüstung · Doppelaxt','Violette Robe · Kristallstab','Goldrüstung · Schwert & Schild']
for idx,(name,parts) in enumerate(models.items()):
 base=210+idx*393
 d.rounded_rectangle((base-183,130,base+183,796),radius=18,fill=(27,37,51),outline=(48,62,78),width=2)
 d.ellipse((base-135,645,base+135,695),fill=(16,23,33))
 faces=[]
 for p in parts:
  x,y,z=p['pos']; sx,sy,sz=[v/2 for v in p['size']]
  vertices=[(x+dx*sx,y+dy*sy,z+dz*sz) for dx,dy,dz in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]]
  for ids,shade in [([0,1,2,3],1),([1,5,6,2],.74),([3,2,6,7],1.13)]:
   face=[vertices[i] for i in ids]; center=tuple(sum(v[a] for v in face)/4 for a in range(3)); col=tuple(min(255,int(v*shade)) for v in p['color'])
   faces.append((depth(center),face,col))
 for _,face,col in sorted(faces,key=lambda f:f[0]):
  poly=[projection(v,base) for v in face]; d.polygon(poly,fill=col); d.line(poly+[poly[0]],fill=tuple(int(c*.68) for c in col),width=1)
 d.text((base,721),name,anchor='mm',font=font,fill=(242,237,219))
 d.text((base,760),sub[idx],anchor='mm',font=small,fill=(154,173,191))
img.save(P/'Charaktere.png')
