from pathlib import Path
import json,xml.etree.ElementTree as E
import numpy as np
P=Path(__file__).parent
models=json.loads((P/'knight_geometry.json').read_text())
for name,specs in models.items():
 root=E.parse(P/(name+'.rbxmx')).getroot();refs={x.get('referent'):x for x in root.iter('Item')}
 parts=[x for x in refs.values() if x.get('class') in ['Part','WedgePart']]
 assert len(parts)==len(specs)
 for ref in root.iter('Ref'):assert ref.text in refs
 for spec,part in zip(specs,parts):
  assert all(v>0 for v in spec['size'])
  r=np.array(spec['rotation']);assert np.allclose(r.T@r,np.eye(3),atol=1e-9) and np.isclose(np.linalg.det(r),1)
  props=part.find('Properties'); assert props.find('Color3uint8') is not None
  assert props.find('bool[@name="Anchored"]').text==str(spec['name']=='Torso').lower()
 assert len(root.findall('.//Item[@class="Motor6D"]'))==4
 assert len(root.findall('.//Item[@class="WeldConstraint"]'))==len(specs)-5
 byname={s['name']:s for s in specs}
 assert np.allclose(byname['Weapon']['pos'],byname['RightHand']['pos'])
 assert byname['Weapon']['pos'][2]<-.5
 def frame(node):
  p=np.array([float(node.find(ax).text) for ax in 'XYZ'])
  r=np.array([[float(node.find(f'R{i}{j}').text) for j in range(3)] for i in range(3)])
  return p,r
 # Each motor's Part0*C0 and Part1*C1 must produce the same world pivot.
 for motor in root.findall('.//Item[@class="Motor6D"]'):
  pr=motor.find('Properties');jointframes=[]
  for partkey,offsetkey in [('Part0','C0'),('Part1','C1')]:
   part=refs[pr.find(f'Ref[@name="{partkey}"]').text]
   pos,rot=frame(part.find('Properties/CoordinateFrame[@name="CFrame"]'))
   localpos,localrot=frame(pr.find(f'CoordinateFrame[@name="{offsetkey}"]'))
   jointframes.append((pos+rot@localpos,rot@localrot))
  assert np.allclose(jointframes[0][0],jointframes[1][0]) and np.allclose(jointframes[0][1],jointframes[1][1])
 print(name,':',len(parts),'parts, color serialization, shared joint pivots and hand grip verified')
root=E.parse(P/'Ritter-Ausstellung.rbxlx').getroot();refs=[x.get('referent') for x in root.iter('Item')]
assert len(refs)==len(set(refs))
for ref in root.iter('Ref'):assert ref.text in refs
assert len(root.findall('.//Item[@class="Model"]'))==4
assert not root.findall('.//Item[@class="Script"]')
print('Showroom: four models, valid references and no game scripts.')
