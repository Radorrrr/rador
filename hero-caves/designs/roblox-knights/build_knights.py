from pathlib import Path
import math,json,xml.etree.ElementTree as E
import numpy as np
P=Path(__file__).parent
I=np.eye(3)
def rotate(x=0,y=0,z=0):
 x,y,z=map(math.radians,(x,y,z));cx,sx=math.cos(x),math.sin(x);cy,sy=math.cos(y),math.sin(y);cz,sz=math.cos(z),math.sin(z)
 return np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])@np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]])@np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]])
models={}
styles=[
 dict(name='Stahlritter',metal=(159,179,197),trim=(219,172,68),cloth=(24,65,139),secondary=(41,51,65),light=(228,232,230)),
 dict(name='DunklerRitter',metal=(43,48,59),trim=(151,35,39),cloth=(81,21,29),secondary=(22,25,33),light=(255,58,55)),
 dict(name='Sonnenpaladin',metal=(207,155,51),trim=(246,211,116),cloth=(234,226,202),secondary=(125,91,34),light=(255,241,173)),
 dict(name='Frostritter',metal=(125,148,171),trim=(181,205,223),cloth=(30,49,74),secondary=(46,55,68),light=(95,206,255))]
def add(a,name,size,pos,color,material='SmoothPlastic',group='Body',shape='Block',rotation=None):
 a.append(dict(name=name,size=list(size),pos=list(pos),color=list(color),material=material,group=group,shape=shape,rotation=(I if rotation is None else rotation).tolist()))
def bar(a,name,point0,point1,width,depth,color,z=-.72,group='Body',material='Metal'):
 p0=np.array(point0,float);p1=np.array(point1,float);v=p1-p0;mid=(p0+p1)/2
 # +Y axis rotated to segment direction in the front XY plane.
 angle=math.degrees(math.atan2(-v[0],v[1]))
 add(a,name,(width,float(np.linalg.norm(v)),depth),(mid[0],mid[1],z),color,material,group,rotation=rotate(z=angle))
TRI=np.array([[0,1,0],[0,0,1],[1,0,0]])
def triangle(a,name,w,h,t,pos,color,side='right',group='Body',material='Metal'):
 add(a,name,(t,w,h),pos,color,material,group,'Wedge',TRI if side=='right' else rotate(y=180)@TRI)
def sun(a,cx,cy,z,r,trim,group='Body'):
 add(a,'SunDisc',(r*1.15,r*1.15,.10),(cx,cy,z),trim,'Metal',group,'Ball')
 for j in range(8):
  angle=2*math.pi*j/8
  x0=cx+math.cos(angle)*r*.73;y0=cy+math.sin(angle)*r*.73
  x1=cx+math.cos(angle)*r*1.3;y1=cy+math.sin(angle)*r*1.3
  bar(a,'SunRay',(x0,y0),(x1,y1),r*.14,.055,trim,z,group)
def fleur(a,x,y,z,scale,trim,group='Body'):
 bar(a,'EmblemStem',(x,y-.45*scale),(x,y+.45*scale),.11*scale,.07,trim,z,group)
 for side in [-1,1]:
  bar(a,'EmblemBranch',(x,y),(x+side*.30*scale,y+.25*scale),.09*scale,.07,trim,z,group)
  add(a,'EmblemPetal',(.20*scale,.28*scale,.07),(x+side*.30*scale,y+.30*scale,z),trim,'Metal',group,rotation=rotate(z=-side*28))
  bar(a,'EmblemFoot',(x,y-.26*scale),(x+side*.17*scale,y-.38*scale),.08*scale,.07,trim,z,group)
 add(a,'EmblemLily',(.17*scale,.30*scale,.07),(x,y+.51*scale,z),trim,'Metal',group,rotation=rotate(z=45))
def rune(a,x,y,z,scale,color,group='Body'):
 for p0,p1 in [((0,-.4),(0,.4)),((-.28,.25),(.28,-.25)),((-.28,-.25),(.28,.25))]:
  bar(a,'Rune',(x+p0[0]*scale,y+p0[1]*scale),(x+p1[0]*scale,y+p1[1]*scale),.075*scale,.055,color,z,group)
for style in styles:
 a=[]; name=style['name'];models[name]=a
 metal,trim,cloth,dark,light=[style[k] for k in ['metal','trim','cloth','secondary','light']]
 skin=(235,188,137)
 add(a,'Torso',(2,2.15,1.05),(0,0,0),dark,'Fabric')
 add(a,'Head',(1.42,1.42,1.32),(0,1.88,0),skin)
 add(a,'NeckGuard',(1.76,.28,1.26),(0,1.15,0),metal,'Metal')
 for side,x in [('Left',-1.38),('Right',1.38)]:
  group='Body' if side=='Left' else 'Arm'
  add(a,side+'Arm',(.7,1.7,.78),(x,.1,0),dark,'Fabric',group)
  handgroup='Body' if side=='Left' else 'Hand'
  add(a,side+'Hand',(.72,.55,.74),(x,-.92,0),dark,'Metal',handgroup)
  for y in [-.76,-.92,-1.08]: add(a,side+'GloveFinger',(.60,.105,.10),(x,y,-.41),metal,'Metal',handgroup)
  fore='Body' if side=='Left' else 'Forearm'
  add(a,side+'Bracer',(.8,.65,.87),(x,-.39,0),metal,'Metal',fore)
  for y in [-.1,-.36,-.62]: add(a,side+'BracerBand',(.86,.075,.93),(x,y,0),trim,'Metal',fore)
  # Large layered low-poly shoulder caps.
  for j,(w,h,dep) in enumerate([(1.2,.5,1.23),(1.08,.35,1.12),(.9,.25,1.02)]):
   add(a,side+'PauldronLayer',(w,h,dep),(x,.76+j*.23,.02+j*.03),metal,'Metal',group)
   add(a,side+'PauldronEdge',(w+.025,.075,.055),(x,.58+j*.23,-dep/2-.015),trim,'Metal',group)
  for dx in [-.36,.36]: add(a,'ShoulderStud',(.115,.115,.08),(x+dx,.95,-.59),trim,'Metal',group,'Ball')
  add(a,side+'UpperPlate',(.70,.45,.11),(x,.27,-.46),metal,'Metal',group)
 for side,x in [('Left',-.54),('Right',.54)]:
  add(a,side+'Leg',(.88,1.7,.83),(x,-1.91,0),dark,'Fabric')
  add(a,side+'ThighPlate',(.82,.61,.12),(x,-1.26,-.49),metal,'Metal')
  add(a,side+'Knee',(.92,.42,.22),(x,-1.78,-.55),metal,'Metal')
  add(a,side+'KneeInset',(.40,.25,.045),(x,-1.78,-.684),trim,'Metal',rotation=rotate(z=45))
  add(a,side+'ShinPlate',(.78,.7,.18),(x,-2.26,-.49),metal,'Metal')
  add(a,side+'ShinRidge',(.13,.62,.075),(x,-2.26,-.62),trim,'Metal')
  add(a,side+'Boot',(.99,.45,1.35),(x,-2.67,-.2),metal,'Metal')
  add(a,side+'Sole',(1.02,.13,1.40),(x,-2.90,-.2),dark)
  for y,z in [(-2.60,-.89),(-2.75,-.90)]: add(a,side+'BootBand',(.94,.07,.06),(x,y,z),trim,'Metal')
 # Torso: front armor, cloth inset, framed seams, belt and skirt lames.
 add(a,'Breastplate',(2.07,1.36,.24),(0,.28,-.62),metal,'Metal')
 add(a,'Tabard',(1.18,1.60,.075),(0,.12,-.78),cloth,'Fabric')
 for x in [-.67,.67]: add(a,'ChestPiping',(.055,1.5,.07),(x,.12,-.83),trim,'Metal')
 for x in [-.92,.92]:
  for y in [-.05,.45,.80]: add(a,'ChestRivet',(.07,.07,.075),(x,y,-.77),trim,'Metal','Body','Ball')
 add(a,'Belt',(2.19,.24,1.2),(0,-.64,0),(63,43,33),'Wood')
 add(a,'Buckle',(.42,.34,.11),(0,-.64,-.77),trim,'Metal')
 add(a,'BuckleInset',(.25,.17,.035),(0,-.64,-.84),dark,'Metal')
 for x in [-.77,-.52,.52,.77]: add(a,'BeltRivet',(.075,.075,.075),(x,-.64,-.66),trim,'Metal','Body','Ball')
 for side,x in [('Left',-.82),('Right',.82)]:
  for j in range(3):
   add(a,'SkirtArmor',(.55,.22,.18),(x,-.87-j*.20,-.62),metal,'Metal',rotation=rotate(z=(-1 if x>0 else 1)*12))
   add(a,'SkirtArmorEdge',(.52,.04,.055),(x,-.96-j*.20,-.74),trim,'Metal',rotation=rotate(z=(-1 if x>0 else 1)*12))
 add(a,'TabardTail',(.82,1.12,.12),(0,-1.40,-.61),cloth,'Fabric')
 for x in [-.39,.39]: add(a,'TabardTailBorder',(.055,1.12,.045),(x,-1.40,-.70),trim,'Fabric')
 # Cape panels overlap into a shallow flowing shape.
 cape=cloth
 for j in range(5):
  x=(j-2)*.37; length=2.50+(abs(j-2)*.15)
  add(a,'CapePanel',(.41,length,.085),(x,-.45,.84+abs(j-2)*.13),cape,'Fabric',rotation=rotate(x=10,z=(j-2)*-3))
  add(a,'CapeHem',(.41,.065,.09),(x,-.45-length/2,.84+abs(j-2)*.13+length*.085),trim if name!='DunklerRitter' else dark,'Fabric')
 # Eye and eyebrow geometry: square Roblox face, visible through open helmet.
 for x in [-.29,.29]:
  add(a,'Eye',(.13,.22,.055),(x,1.97,-.681),(28,26,24))
  add(a,'Eyebrow',(.31,.085,.075),(x,2.20,-.69),(54,34,27),rotation=rotate(z=(-15 if x>0 else 15)))
 add(a,'Mouth',(.28,.05,.055),(0,1.60,-.68),(76,43,30))
 add(a,'HelmetCap',(1.67,.42,1.54),(0,2.51,.05),metal,'Metal')
 add(a,'HelmetBrow',(1.72,.17,.12),(0,2.35,-.79),trim,'Metal')
 for x in [-.77,.77]:
  add(a,'HelmetSide',(.20,1.03,1.4),(x,1.96,.08),metal,'Metal')
  add(a,'HelmetCheek',(.27,.40,.16),(x,1.54,-.65),metal,'Metal')
  add(a,'CheekStud',(.10,.10,.09),(x,1.62,-.76),trim,'Metal','Body','Ball')
 if name=='Stahlritter':
  # Raised slit visor and layered blue crest.
  add(a,'RaisedVisor',(1.40,.41,.12),(0,2.47,-.81),metal,'Metal')
  for x in [-.50,-.25,0,.25,.50]: add(a,'VisorSlot',(.08,.24,.035),(x,2.47,-.89),dark)
  for j in range(7):
   add(a,'BluePlume',(.27,.50-j*.035,.18),(0,2.99-j*.028,.02+j*.16),cloth,'Fabric',rotation=rotate(x=-j*8))
  fleur(a,0,.36,-.85,.63,trim)
  fleur(a,0,-1.40,-.75,.40,trim)
 elif name=='DunklerRitter':
  add(a,'ClosedHelmetFace',(1.30,.94,.15),(0,1.94,-.77),metal,'Metal')
  add(a,'HelmetRidge',(.13,1.06,.14),(0,1.98,-.88),trim,'Metal')
  for x in [-.34,.34]: add(a,'RedEyeSlit',(.47,.07,.05),(x,2.12,-.89),light,'Neon',rotation=rotate(z=(10 if x>0 else -10)))
  for x in [-.42,-.21,0,.21,.42]: add(a,'HelmetAirSlit',(.06,.26,.05),(x,1.65,-.87),dark)
  for x in [-.77,.77]: add(a,'HelmetHorn',(.32,.80,.38),(x,2.87,.02),metal,'Metal',shape='Wedge',rotation=rotate(z=(-20 if x>0 else 20)))
  for x in [-1.70,1.70]:
   add(a,'ShoulderSpike',(.3,.58,.38),(x,1.38,.04),metal,'Metal','Arm' if x>0 else 'Body','Wedge',rotate(z=-30 if x>0 else 30))
  for j in range(3): add(a,'RedScarf',(1.91,.16,1.20),(0,1.05+j*.11,0),cloth,'Fabric')
  rune(a,0,.32,-.85,.92,trim)
  for x in [-.37,.37]: bar(a,'ChestThorn',(0,.5),(x,.76),.07,.05,trim,-.86)
 elif name=='Sonnenpaladin':
  add(a,'CrownBand',(1.79,.16,1.64),(0,2.75,0),trim,'Metal')
  for x in [-.69,-.35,0,.35,.69]:
   height=.59 if x==0 else .43
   add(a,'CrownPoint',(.20,height,.19),(x,2.99,-.65),trim,'Metal',shape='Wedge')
   add(a,'CrownGem',(.12,.17,.07),(x,2.78,-.84),light,'Neon')
  sun(a,0,.34,-.86,.30,trim)
  for x in [-.9,.9]: add(a,'CapeClasp',(.30,.30,.14),(x,.96,-.61),trim,'Metal','Body','Ball')
  for j in [-1,0,1]: add(a,'TabardOrnament',(.13,.21,.045),(j*.17,-1.57,-.75),trim,'Metal',rotation=rotate(z=45))
 else:
  # Hood and a sculpted fur collar built from low-poly Roblox balls and wedges.
  add(a,'HoodBack',(1.83,1.57,.33),(0,2,.84),cloth,'Fabric')
  for side,x in [('Left',-.75),('Right',.75)]:
   add(a,'HoodFlap',(.34,1.36,.20),(x,1.93,-.76),cloth,'Fabric',rotation=rotate(z=(-11 if x>0 else 11)))
  for x in [-.36,.36]: add(a,'HoodPeak',(.82,.36,1.65),(x,2.63,0),cloth,'Fabric',rotation=rotate(z=(-24 if x>0 else 24)))
  add(a,'HoodSilverRidge',(.12,.63,.10),(0,2.59,-.88),trim,'Metal',rotation=rotate(z=-18))
  for j in range(13):
   ang=math.pi*j/12;x=math.cos(ang)*1.25;z=-math.sin(ang)*.62
   fur=(181+j%3*13,181+j%3*13,173+j%3*13)
   add(a,'FurCollar',(.44,.40,.42),(x,1.1,z),fur,'Fabric','Body','Ball')
   add(a,'FurPoint',(.19,.37,.23),(x, .94,z-.20),fur,'Fabric','Body','Wedge',rotate(z=(j%3-1)*24))
  rune(a,0,.30,-.86,.71,light)
 # Shield has a kite silhouette, physically positioned at the left palm.
 sx=-1.56;sz=-.74
 if name!='Frostritter':
  add(a,'ShieldTop',(1.66,1.28,.18),(sx,-.12,sz),metal,'Metal')
  for side,dx in [('left',-.415),('right',.415)]: triangle(a,'ShieldPoint',.83,1.12,.18,(sx+dx,-1.32,sz),metal,side)
  add(a,'ShieldFace',(1.42,1.11,.045),(sx,-.12,sz-.125),cloth,'Fabric')
  for side,dx in [('left',-.355),('right',.355)]: triangle(a,'ShieldPointFace',.71,.95,.045,(sx+dx,-1.24,sz-.125),cloth,side,material='Fabric')
  for x in [sx-.76,sx+.76]: add(a,'ShieldSideRim',(.085,1.29,.08),(x,-.12,sz-.145),trim,'Metal')
  for side in [-1,1]: bar(a,'ShieldLowerRim',(sx+side*.78,-.75),(sx,-1.91),.075,.07,trim,sz-.145)
  add(a,'ShieldTopRim',(1.66,.09,.08),(sx,.52,sz-.145),trim,'Metal')
  for dx in [-.66,.66]:
   for y in [-.60,.37]: add(a,'ShieldRivet',(.085,.085,.09),(sx+dx,y,sz-.18),trim,'Metal','Body','Ball')
  if name=='Stahlritter': fleur(a,sx,-.24,sz-.19,.91,trim)
  elif name=='Sonnenpaladin': sun(a,sx,-.32,sz-.20,.43,trim)
  else: rune(a,sx,-.26,sz-.20,1.13,trim)
 else:
  # Twelve planar rim segments and disk plates form a low-poly round shield.
  for j in range(12):
   angle=2*math.pi*j/12
   add(a,'ShieldDiskPanel',(.52,1.82,.13),(sx,-.31,sz),cloth,'Metal',rotation=rotate(z=math.degrees(angle)))
   add(a,'ShieldRoundRim',(.10,.47,.14),(sx+math.cos(angle)*.94,-.31+math.sin(angle)*.94,sz-.11),metal,'Metal',rotation=rotate(z=math.degrees(angle)))
   add(a,'ShieldRivet',(.085,.085,.075),(sx+math.cos(angle)*.83,-.31+math.sin(angle)*.83,sz-.19),trim,'Metal','Body','Ball')
  rune(a,sx,-.31,sz-.23,1.1,trim)
  add(a,'ShieldBoss',(.33,.33,.17),(sx,-.31,sz-.23),light,'Metal','Body','Ball')
 add(a,'ShieldGrip',(.64,.13,.59),(-1.38,-.92,-.30),(65,43,29),'Wood')
 # Weapon handle passes through the right hand. Every decorative part shares its grip.
 wx=1.38;g='Weapon'
 add(a,'Weapon',(.21,.83,.21),(wx,-.92,0),(65,42,28),'Wood',g)
 for y in [-1.23,-1.08,-.93,-.78,-.63]: add(a,'HandleWrap',(.25,.052,.25),(wx,y,0),dark,'Fabric',g)
 add(a,'Pommel',(.32,.31,.32),(wx,-1.49,0),trim,'Metal',g,'Ball')
 add(a,'Guard',(1.10,.14,.28),(wx,-.46,0),trim,'Metal',g)
 for side in [-1,1]: add(a,'GuardTip',(.25,.19,.29),(wx+side*.50,-.40,0),trim,'Metal',g,rotation=rotate(z=side*20))
 bladeColor=(197,213,221) if name not in ['DunklerRitter','Frostritter'] else (65,67,78) if name=='DunklerRitter' else (141,178,202)
 width=.48 if name!='DunklerRitter' else .66
 add(a,'BladeCore',(width,2.45,.13),(wx,.86,0),bladeColor,'Metal',g)
 for x in [wx-width/2,wx+width/2]: add(a,'BladeEdge',(.045,2.45,.16),(x,.86,0),trim if name=='Sonnenpaladin' else (214,228,234),'Metal',g)
 for side,dx in [('left',-width/4),('right',width/4)]:
  # Point faces up: rotate the downward-pointing kite triangles by 180 degrees.
  r=(TRI if side=='left' else rotate(y=180)@TRI)
  add(a,'BladeTip',(.13,width/2,.48),(wx+dx,2.31,0),bladeColor,'Metal',g,'Wedge',rotate(z=180)@r)
 accent=trim if name in ['Stahlritter','Sonnenpaladin'] else light
 add(a,'BladeFuller',(.055,2.2,.035),(wx,.87,-.091),accent,'Metal' if name in ['Stahlritter','Sonnenpaladin'] else 'Neon',g)
 if name in ['DunklerRitter','Frostritter']:
  for y in [.25,.70,1.15,1.6]: rune(a,wx,y,-.112,.22,light,g)
 else:
  for y in [.45,1.25]: add(a,'BladeDiamond',(.16,.16,.035),(wx,y,-.119),trim,'Metal',g,rotation=rotate(z=45))
 # Attacking arm is a shoulder/elbow/wrist chain.
 for spec in a:
  if spec['name']=='RightArm':spec['size']=[.7,.9,.78];spec['pos']=[1.38,.4,0]
 add(a,'RightForearm',(.7,.8,.78),(1.38,-.4,0),dark,'Fabric','Forearm')
# Bind pose: arm forward, wrist counter-rotated so the blade clears the body.
posed_pivots={}
for name,parts in models.items():
 shoulder=np.array([1.38,.95,0.]);old_elbow=np.array([1.38,0.,0.]);old_wrist=np.array([1.38,-.82,0.]);old_hand=np.array([1.38,-.92,0.])
 arm_rotation=rotate(x=25);hand_rotation=arm_rotation@rotate(x=-55)
 new_elbow=shoulder+arm_rotation@(old_elbow-shoulder)
 new_wrist=shoulder+arm_rotation@(old_wrist-shoulder)
 new_hand=new_wrist+hand_rotation@(old_hand-old_wrist)
 for spec in parts:
  if spec['group'] in ['Arm','Forearm']:
   spec['pos']=(shoulder+arm_rotation@(np.array(spec['pos'])-shoulder)).tolist()
   spec['rotation']=(arm_rotation@np.array(spec['rotation'])).tolist()
  elif spec['group'] in ['Hand','Weapon']:
   spec['pos']=(new_wrist+hand_rotation@(np.array(spec['pos'])-old_wrist)).tolist()
   spec['rotation']=(hand_rotation@np.array(spec['rotation'])).tolist()
 posed_pivots[name]={'RightShoulder':shoulder,'RightElbow':new_elbow,'RightWrist':new_wrist,'RightGrip':new_hand}

(P/'knight_geometry.json').write_text(json.dumps(models,indent=2))
# XML export helpers. Geometry is shared verbatim with the preview renderer.
materials={'SmoothPlastic':272,'Fabric':1312,'Wood':512,'Metal':1088,'Neon':288}
serial=0
def item(parent,cls,name):
 global serial;serial+=1
 obj=E.SubElement(parent,'Item',{'class':cls,'referent':'RBX'+str(serial)});pr=E.SubElement(obj,'Properties');E.SubElement(pr,'string',name='Name').text=name
 return obj,pr
def cf(pr,key,pos,rotation):
 frame=E.SubElement(pr,'CoordinateFrame',name=key)
 for ax,value in zip('XYZ',pos): E.SubElement(frame,ax).text=str(float(value))
 for i in range(3):
  for j in range(3): E.SubElement(frame,f'R{i}{j}').text=str(float(rotation[i][j]))
def model(parent,name,parts,offset=(0,0,0)):
 obj,pr=item(parent,'Model',name);byname={};refs=[]
 for spec in parts:
  cls='WedgePart' if spec['shape']=='Wedge' else 'Part'
  part,prop=item(obj,cls,spec['name']);refs.append(part.get('referent'));byname[spec['name']]=(part,spec)
  for key,value in [('Anchored',spec['name']=='Torso'),('Massless',True),('CanCollide',False),('CanTouch',False),('CanQuery',False)]:E.SubElement(prop,'bool',name=key).text=str(value).lower()
  sz=E.SubElement(prop,'Vector3',name='size')
  for ax,value in zip('XYZ',spec['size']):E.SubElement(sz,ax).text=str(value)
  cf(prop,'CFrame',np.array(spec['pos'])+offset,spec['rotation'])
  r,g,b=spec['color'];E.SubElement(prop,'Color3uint8',name='Color3uint8').text=str(0xff000000 | r<<16 | g<<8 | b)
  E.SubElement(prop,'token',name='Material').text=str(materials[spec['material']])
  if cls=='Part': E.SubElement(prop,'token',name='shape').text='0' if spec['shape']=='Ball' else '1'
  for key in ['TopSurface','BottomSurface']:E.SubElement(prop,'token',name=key).text='0'
 E.SubElement(pr,'Ref',name='PrimaryPart').text=byname['Torso'][0].get('referent')
 drivers={'Arm':'RightArm','Forearm':'RightForearm','Hand':'RightHand','Weapon':'Weapon','Body':'Torso'}
 for joint,a,b,pivot in [('RightShoulder','Torso','RightArm',(1.38,.95,0)),('RightElbow','RightArm','RightForearm',(1.38,0,0)),('RightWrist','RightForearm','RightHand',(1.38,-.82,0)),('RightGrip','RightHand','Weapon',(1.38,-.92,0))]:
  pivot=posed_pivots[name][joint]
  m,prop=item(obj,'Motor6D',joint)
  for key,n in [('Part0',a),('Part1',b)]:E.SubElement(prop,'Ref',name=key).text=byname[n][0].get('referent')
  for key,n in [('C0',a),('C1',b)]:
   spec=byname[n][1];rot=np.array(spec['rotation']);cf(prop,key,rot.T@(np.array(pivot)-spec['pos']),rot.T)
 for i,spec in enumerate(parts):
  if spec['name'] in ['Torso','RightArm','RightForearm','RightHand','Weapon']:continue
  w,prop=item(obj,'WeldConstraint','DetailWeld')
  E.SubElement(prop,'Ref',name='Part0').text=byname[drivers[spec['group']]][0].get('referent')
  E.SubElement(prop,'Ref',name='Part1').text=refs[i]
  E.SubElement(prop,'bool',name='Enabled').text='true'
 return obj
for name,parts in models.items():
 root=E.Element('roblox',version='4');E.SubElement(root,'External').text='null';E.SubElement(root,'External').text='nil'
 model(root,name,parts)
 E.indent(root);E.ElementTree(root).write(P/(name+'.rbxmx'),encoding='utf-8',xml_declaration=True)
# Dedicated Studio showroom. No gameplay scripts or save changes.
root=E.Element('roblox',version='4');E.SubElement(root,'External').text='null';E.SubElement(root,'External').text='nil'
work,wp=item(root,'Workspace','Workspace')
for idx,(name,parts) in enumerate(models.items()):
 mod=model(work,name,parts,offset=((idx-1.5)*9,3.42,0))
 platform,prop=item(work,'Part','Podest_'+name)
 E.SubElement(prop,'bool',name='Anchored').text='true';sz=E.SubElement(prop,'Vector3',name='size')
 for ax,value in zip('XYZ',[7,.5,6]):E.SubElement(sz,ax).text=str(value)
 cf(prop,'CFrame',[(idx-1.5)*9,.25,0],I)
 E.SubElement(prop,'Color3uint8',name='Color3uint8').text=str(0xff000000 | 24<<16 | 31<<8 | 41)
 label,lp=item(platform,'BillboardGui','NameLabel');E.SubElement(lp,'bool',name='AlwaysOnTop').text='true'
 size=E.SubElement(lp,'UDim2',name='Size')
 for key,val in [('XS',0),('XO',260),('YS',0),('YO',44)]:E.SubElement(size,key).text=str(val)
 off=E.SubElement(lp,'Vector3',name='StudsOffset')
 for ax,value in zip('XYZ',[0,7.3,0]):E.SubElement(off,ax).text=str(value)
 text,tp=item(label,'TextLabel','Text');E.SubElement(tp,'string',name='Text').text=f'{idx+1}  '+name
 E.SubElement(tp,'float',name='BackgroundTransparency').text='1';E.SubElement(tp,'bool',name='TextScaled').text='true'
 size=E.SubElement(tp,'UDim2',name='Size')
 for key,val in [('XS',1),('XO',0),('YS',1),('YO',0)]:E.SubElement(size,key).text=str(val)
 col=E.SubElement(tp,'Color3',name='TextColor3')
 for ax in 'RGB':E.SubElement(col,ax).text='1'
 E.SubElement(tp,'float',name='TextStrokeTransparency').text='.3'
floor,fp=item(work,'Part','StudioFloor');E.SubElement(fp,'bool',name='Anchored').text='true'
sz=E.SubElement(fp,'Vector3',name='size')
for ax,value in zip('XYZ',[120,1,100]):E.SubElement(sz,ax).text=str(value)
cf(fp,'CFrame',[0,-.5,0],I);E.SubElement(fp,'Color3uint8',name='Color3uint8').text=str(0xff000000 | 14<<16 | 19<<8 | 26)
lighting,lp=item(root,'Lighting','Lighting')
E.SubElement(lp,'float',name='Brightness').text='2.5';E.SubElement(lp,'float',name='ClockTime').text='14'
for key,vals in [('Ambient',[.35,.36,.40]),('OutdoorAmbient',[.40,.42,.47])]:
 col=E.SubElement(lp,'Color3',name=key)
 for ax,val in zip('RGB',vals):E.SubElement(col,ax).text=str(val)
cam,cp=item(work,'Camera','ShowcaseCamera')
pos=np.array([12,11,-44.]);target=np.array([0,3.1,0]);back=(pos-target)/np.linalg.norm(pos-target);right=np.cross([0,1,0],back);right/=np.linalg.norm(right);up=np.cross(back,right)
cf(cp,'CFrame',pos,np.column_stack([right,up,back]));E.SubElement(cp,'float',name='FieldOfView').text='45';E.SubElement(wp,'Ref',name='CurrentCamera').text=cam.get('referent')
E.indent(root);E.ElementTree(root).write(P/'Ritter-Ausstellung.rbxlx',encoding='utf-8',xml_declaration=True)
print('Exported four jointed knight models and Studio showroom:',{name:len(parts) for name,parts in models.items()})
