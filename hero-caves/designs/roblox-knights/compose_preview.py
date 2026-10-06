from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).parent
names=['Stahlritter','DunklerRitter','Sonnenpaladin','Frostritter']
labels=['1  Stahlritter','2  Dunkler Ritter','3  Sonnenpaladin','4  Frostritter']
canvas=Image.new('RGB',(1680,2076),(14,19,26));draw=ImageDraw.Draw(canvas)
path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
font=ImageFont.truetype(path,30);small=ImageFont.truetype(path,21)
draw.text((40,22),'Vier Ritter – tatsächliche Roblox-Modellgeometrie',font=font,fill=(237,232,220))
draw.text((40,64),'Aus den exportierten Teilen gerendert · Studio-Ausstellung liegt bei',font=small,fill=(153,170,185))
for i,name in enumerate(names):
 image=Image.open(P/(name+'.png')).convert('RGB')
 image.save(P/(name+'.jpg'),quality=94)
 x=(i%2)*840;y=106+(i//2)*985
 canvas.paste(image.resize((840,920),Image.Resampling.LANCZOS),(x,y))
 draw.text((x+420,y+946),labels[i],anchor='mm',font=font,fill=(236,231,219))
canvas.save(P/'Ritter-Roblox-Vorschau.jpg',quality=94)
print('JPG previews assembled from model renders.')
