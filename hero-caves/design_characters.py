"""One geometry source for Studio models, runtime module, and illustrated preview."""
from pathlib import Path
import json, math, xml.etree.ElementTree as E
P=Path(__file__).parent
skin=(231,184,139); steel=(128,151,172); dark=(38,48,63); gold=(222,174,66)
models={}
def add(parts,name,size,pos,color,material='SmoothPlastic',group='Body',shape='Block'):
 parts.append(dict(name=name,size=size,pos=pos,color=color,material=material,group=group,shape=shape))
for hero in ['Ritter','Berserker','Magier','Paladin']:
 a=[]; models[hero]=a
 cloth={'Ritter':(35,80,139),'Berserker':(115,47,35),'Magier':(72,39,123),'Paladin':(229,218,181)}[hero]
 add(a,'Torso',(2,2.3,1),(0,0,0),cloth,'Fabric')
 add(a,'Head',(1.45,1.45,1.3),(0,1.9,0),skin)
 for side,x in [('Left',-0.55),('Right',0.55)]:
  add(a,side+'Leg',(.85,1.65,.85),(x,-1.9,0),dark,'Fabric')
  add(a,side+'Boot',(.95,.65,1.15),(x,-2.48,-.12),(53,39,30),'Wood')
 for side,x in [('Left',-1.38),('Right',1.38)]:
  group='Arm' if side=='Right' else 'Body'
  add(a,side+'Arm',(.7,1.7,.8),(x,.1,0),cloth,'Fabric',group)
  add(a,side+'Hand',(.72,.55,.82),(x,-.92,0),skin,'SmoothPlastic',group)
 for x in [-.3,.3]:
  add(a,'EyeWhite',(.26,.2,.06),(x,2,-.672),(250,249,233))
  add(a,'Eye',(.12,.17,.08),(x,2,-.716),dark)
  add(a,'Brow',(.34,.08,.07),(x,2.2,-.7),dark)
 add(a,'Mouth',(.35,.06,.06),(0,1.64,-.68),(91,48,38))
 add(a,'Belt',(2.09,.28,1.08),(0,-.65,0),(66,42,29),'Wood')
 add(a,'Buckle',(.38,.33,.12),(0,-.65,-.6),gold,'Metal')
 if hero in ['Ritter','Paladin']:
  metal=steel if hero=='Ritter' else gold
  add(a,'Breastplate',(1.85,1.35,.2),(0,.2,-.61),metal,'Metal')
  add(a,'ChestInset',(1.35,.88,.06),(0,.2,-.75),cloth,'Fabric')
  add(a,'CrestVertical',(.16,.64,.08),(0,.24,-.8),gold if hero=='Ritter' else (255,246,209),'Metal')
  add(a,'CrestHorizontal',(.54,.15,.08),(0,.34,-.81),gold if hero=='Ritter' else (255,246,209),'Metal')
  for x in [-.73,.73]:
   for y in [-.25,.65]: add(a,'ArmorRivet',(.09,.09,.09),(x,y,-.76),gold,'Metal','Body','Ball')
  for side,x in [('Left',-1.38),('Right',1.38)]:
   g='Arm' if side=='Right' else 'Body'
   add(a,side+'Pauldron',(.99,.63,1.05),(x,.9,0),metal,'Metal',g)
   add(a,side+'Gauntlet',(.78,.5,.9),(x,-.5,0),metal,'Metal',g)
   add(a,side+'Kneeguard',(.93,.5,.16),(-.55 if side=='Left' else .55,-1.7,-.49),metal,'Metal')
  add(a,'HelmetCap',(1.65,.52,1.5),(0,2.54,0),metal,'Metal')
  for x in [-.73,.73]: add(a,'HelmetCheek',(.17,.75,1.42),(x,2.02,0),metal,'Metal')
  add(a,'HelmetNose',(.14,.64,.15),(0,2.11,-.76),metal,'Metal')
  add(a,'Plume',(.25,.75,1.02),(0,3.03,.08),cloth,'Fabric')
  add(a,'Cape',(1.8,2.8,.16),(0,-.3,.69),cloth,'Fabric')
  add(a,'Shield',(1.15,1.65,.2),(-1.5,-.28,-.64),metal,'Metal')
  add(a,'ShieldInset',(.9,1.38,.08),(-1.5,-.28,-.8),cloth,'Fabric')
  add(a,'ShieldCrossV',(.15,.9,.06),(-1.5,-.28,-.87),gold,'Metal')
  add(a,'ShieldCrossH',(.62,.15,.06),(-1.5,-.15,-.88),gold,'Metal')
  add(a,'Weapon',(.22,.82,.22),(1.38,-.92,-.88),(66,42,29),'Wood','Weapon')
  add(a,'Pommel',(.35,.25,.35),(1.38,-1.38,-.88),metal,'Metal','Weapon')
  add(a,'SwordGuard',(1.04,.18,.36),(1.38,-.48,-.88),gold,'Metal','Weapon')
  add(a,'SwordBlade',(.43,2.15,.13),(1.38,.7,-.88),(201,220,229),'Metal','Weapon')
  add(a,'BladeFuller',(.08,1.85,.035),(1.38,.7,-.96),steel,'Metal','Weapon')
  add(a,'SwordTip',(.26,.32,.13),(1.38,1.94,-.88),(223,233,240),'Metal','Weapon')
 elif hero=='Berserker':
  add(a,'Hair',(1.54,.38,1.35),(0,2.53,0),(85,46,25),'Wood')
  add(a,'Beard',(1.1,.5,.25),(0,1.49,-.73),(107,56,29),'Wood')
  for x in [-1.35,1.35]:
   g='Arm' if x>0 else 'Body'
   add(a,'FurShoulder',(1.05,.85,1.1),(x,.82,0),(115,98,76),'Fabric',g)
   for d in [-.33,0,.33]: add(a,'FurTuft',(.25,.45,.18),(x+d,.38,-.57),(163,139,108),'Fabric',g)
  add(a,'Harness',(.35,1.8,.13),(-.48,.2,-.58),(75,46,30),'Wood')
  add(a,'Weapon',(.24,2.7,.24),(1.38,.03,-.88),(107,69,36),'Wood','Weapon')
  for y in [-1,-.75,-.5]: add(a,'GripBand',(.3,.11,.3),(1.38,y,-.88),(55,35,25),'Fabric','Weapon')
  for x in [.76,2]:
   add(a,'AxeBlade',(.95,1.05,.2),(x,1.08,-.88),steel,'Metal','Weapon')
   add(a,'AxeEdge',(.16,1.2,.23),(x+(-.48 if x<1 else .48),1.08,-.88),(212,223,229),'Metal','Weapon')
  add(a,'AxeSocket',(.45,.85,.4),(1.38,1.08,-.88),dark,'Metal','Weapon')
 else:
  add(a,'RobeSkirt',(2.05,1.8,1.17),(0,-1.48,0),cloth,'Fabric')
  for x in [-.82,.82]: add(a,'RobeTrim',(.13,3.25,.06),(x,-.73,-.65),gold,'Fabric')
  add(a,'RobeHem',(2.16,.15,1.23),(0,-2.33,0),gold,'Fabric')
  add(a,'HoodBack',(1.75,1.55,.32),(0,2,.72),cloth,'Fabric')
  add(a,'HatBrim',(2.3,.18,1.9),(0,2.63,0),cloth,'Fabric')
  for i in range(5): add(a,'HatTier',(1.6-i*.27,.25,1.45-i*.24),(i*.05,2.85+i*.24,0),cloth,'Fabric')
  add(a,'HatBand',(1.66,.16,1.5),(0,2.79,0),gold,'Fabric')
  add(a,'Pendant',(.35,.42,.14),(0,.55,-.62),(101,219,245),'Neon','Body','Ball')
  add(a,'Weapon',(.22,3.65,.22),(1.38,.22,-.88),(91,57,32),'Wood','Weapon')
  for y in [-1.05,-.75,.9]: add(a,'StaffRing',(.34,.15,.34),(1.38,y,-.88),gold,'Metal','Weapon')
  for x in [1.05,1.71]: add(a,'CrystalProng',(.13,.85,.17),(x,2.08,-.88),gold,'Metal','Weapon')
  add(a,'Orb',(.65,.85,.65),(1.38,2.18,-.88),(107,218,255),'Neon','Weapon','Ball')
# Split the attacking arm into a jointed chain and seat each handle in the palm.
for hero,parts in models.items():
 for spec in parts:
  if spec['name']=='RightArm': spec['size']=(.7,.9,.8); spec['pos']=(1.38,.4,0)
  if spec['name']=='RightHand': spec['group']='Hand'
  if spec['name']=='RightGauntlet': spec['group']='Forearm'
  if spec['group']=='Weapon': spec['pos']=(spec['pos'][0],spec['pos'][1],spec['pos'][2]+.88)
 add(parts,'RightForearm',(.7,.8,.8),(1.38,-.4,0),parts[0]['color'],'Fabric','Forearm')

# Emit data as Lua, keeping models available without asset permissions.
def lua(v):
 if isinstance(v,dict): return '{'+','.join(k+'='+lua(x) for k,x in v.items())+'}'
 if isinstance(v,(list,tuple)): return '{'+','.join(map(lua,v))+'}'
 if isinstance(v,str): return json.dumps(v,ensure_ascii=False)
 return str(v)
module='local designs = {\n'+',\n'.join('['+lua(k)+']='+lua(v) for k,v in models.items())+'\n}\n'
module+=(P/'CharacterRig.template.lua').read_text()
(P/'CharacterDesign.lua').write_text(module)
# Export separate importable Roblox models.
materials={'SmoothPlastic':272,'Fabric':1312,'Wood':512,'Metal':1088,'Neon':288}
for hero,parts in models.items():
 root=E.Element('roblox',version='4'); E.SubElement(root,'External').text='null'; E.SubElement(root,'External').text='nil'
 obj=E.SubElement(root,'Item',{'class':'Model','referent':'MODEL'}); props=E.SubElement(obj,'Properties'); E.SubElement(props,'string',name='Name').text=hero
 E.SubElement(props,'Ref',name='PrimaryPart').text='P0'
 for i,s in enumerate(parts):
  it=E.SubElement(obj,'Item',{'class':'Part','referent':'P'+str(i)}); pr=E.SubElement(it,'Properties')
  E.SubElement(pr,'string',name='Name').text=s['name']
  for k,v in [('Anchored',s['name']=='Torso'),('Massless',True),('CanCollide',False),('CanTouch',False),('CanQuery',False)]: E.SubElement(pr,'bool',name=k).text=str(v).lower()
  sz=E.SubElement(pr,'Vector3',name='size')
  for axis,v in zip('XYZ',s['size']): E.SubElement(sz,axis).text=str(v)
  cf=E.SubElement(pr,'CoordinateFrame',name='CFrame')
  for axis,v in zip('XYZ',s['pos']): E.SubElement(cf,axis).text=str(v)
  for row in range(3):
   for col in range(3): E.SubElement(cf,'R'+str(row)+str(col)).text=str(int(row==col))
  color=E.SubElement(pr,'Color3',name='Color')
  for axis,v in zip('RGB',s['color']): E.SubElement(color,axis).text=str(v/255)
  E.SubElement(pr,'token',name='Material').text=str(materials[s['material']])
  E.SubElement(pr,'token',name='shape').text='0' if s['shape']=='Ball' else '1'
  for key in ['TopSurface','BottomSurface']: E.SubElement(pr,'token',name=key).text='0'
 # Export the same three-bone chain and hand grip used by the runtime.
 byname={s['name']:(i,s) for i,s in enumerate(parts)}
 def frame(pr,key,xyz):
  cf=E.SubElement(pr,'CoordinateFrame',name=key)
  for axis,v in zip('XYZ',xyz): E.SubElement(cf,axis).text=str(v)
  for row in range(3):
   for col in range(3): E.SubElement(cf,'R'+str(row)+str(col)).text=str(int(row==col))
 drivers={'Arm':'RightArm','Forearm':'RightForearm','Hand':'RightHand','Weapon':'Weapon','Body':'Torso'}
 for j,(name,a,b,pivot) in enumerate([
  ('RightShoulder','Torso','RightArm',(1.38,.95,0)),
  ('RightElbow','RightArm','RightForearm',(1.38,0,0)),
  ('RightWrist','RightForearm','RightHand',(1.38,-.82,0)),
  ('RightGrip','RightHand','Weapon',(1.38,-.92,0))]):
  motor=E.SubElement(obj,'Item',{'class':'Motor6D','referent':'J'+str(j)}); pr=E.SubElement(motor,'Properties')
  E.SubElement(pr,'string',name='Name').text=name
  for key,n in [('Part0',a),('Part1',b)]: E.SubElement(pr,'Ref',name=key).text='P'+str(byname[n][0])
  for key,n in [('C0',a),('C1',b)]: frame(pr,key,tuple(pivot[k]-byname[n][1]['pos'][k] for k in range(3)))
 for i,spec in enumerate(parts):
  if spec['name'] in ['Torso','RightArm','RightForearm','RightHand','Weapon']: continue
  weld=E.SubElement(obj,'Item',{'class':'WeldConstraint','referent':'W'+str(i)}); pr=E.SubElement(weld,'Properties')
  E.SubElement(pr,'string',name='Name').text='DetailWeld'
  E.SubElement(pr,'Ref',name='Part0').text='P'+str(byname[drivers[spec['group']]][0])
  E.SubElement(pr,'Ref',name='Part1').text='P'+str(i)
  E.SubElement(pr,'bool',name='Enabled').text='true'
 E.indent(root); E.ElementTree(root).write(P/(hero+'.rbxmx'),encoding='utf-8',xml_declaration=True)
(P/'character_geometry.json').write_text(json.dumps(models,ensure_ascii=False,indent=2))
print('Four character models and runtime module generated:', {k:len(v) for k,v in models.items()})
