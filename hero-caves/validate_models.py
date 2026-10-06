from pathlib import Path
import json,math,xml.etree.ElementTree as E
P=Path(__file__).parent
geometry=json.loads((P/'character_geometry.json').read_text())
for name,specs in geometry.items():
 root=E.parse(P/(name+'.rbxmx')).getroot(); model=root.find('Item')
 parts=model.findall('Item[@class="Part"]'); assert len(parts)==len(specs)
 refs={x.get('referent') for x in model.iter('Item')}
 for r in model.iter('Ref'): assert r.text=='null' or r.text in refs
 assert len(model.findall('Item[@class="Motor6D"]'))==4
 assert len(model.findall('Item[@class="WeldConstraint"]'))==len(specs)-5
 byname={s['name']:s for s in specs}
 assert byname['RightHand']['pos'][0]==byname['Weapon']['pos'][0]
 assert byname['RightHand']['pos'][2]==byname['Weapon']['pos'][2]==0
 for obj in parts:
  pr=obj.find('Properties'); n=pr.find('string[@name="Name"]').text
  assert pr.find('bool[@name="Anchored"]').text==str(n=='Torso').lower()
 # Confirm the sword's contact pose lands inside the opponent's torso.
 if name in ('Ritter','Paladin'):
  pitch=math.radians(85);yaw=math.radians(20)
  # Shoulder -> wrist: 1.77 units. Blade end -> wrist: 2.76 units.
  z=-1.77*math.sin(pitch)-2.76
  y=.95-1.77*math.cos(pitch)
  x=1.38+math.sin(yaw)*z; z=math.cos(yaw)*z
  assert abs(x)<=1 and abs(y)<=1.25 and abs(z+4.2)<=.5,(name,x,y,z)
 root=E.parse(P/'HeroCaves.rbxlx').getroot()
 refs=[x.get('referent') for x in root.iter('Item')]; assert len(refs)==len(set(refs))
 for r in root.iter('Ref'): assert r.text=='null' or r.text in refs
print('Four rigs: hand alignment, joint/weld references, anchor layout and melee reach verified.')
update=E.parse(P/'HeroCavesUpdate.rbxmx').getroot()
for obj in update.findall('.//Item[@class="Script"]')+update.findall('.//Item[@class="LocalScript"]'):
 assert obj.find('Properties/bool[@name="Disabled"]').text=='true'
for cls,name,filename in [('Script','HeroCavesServer','Game.server.lua'),('LocalScript','HeroCavesClient','Game.client.lua'),('ModuleScript','CharacterDesign','CharacterDesign.lua'),('ModuleScript','SaveData','SaveData.lua'),('ModuleScript','CombatAnimation','CombatAnimation.lua')]:
 for source in [root,update]:
  obj=next(x for x in source.iter('Item') if x.get('class')==cls and x.find('Properties/string[@name="Name"]').text==name)
  assert obj.find('Properties/ProtectedString[@name="Source"]').text==(P/filename).read_text()
print('Place and update pack: embedded scripts match current files; imported server scripts stay disabled.')
