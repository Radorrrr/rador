from pathlib import Path
import bpy,json,math
from mathutils import Matrix,Vector
P=Path(__file__).parent
models=json.loads((P/'knight_geometry.json').read_text())
# Roblox +Y up -> Blender +Z up; preserve handedness and every part transform.
AXIS=Matrix(((1,0,0),(0,0,-1),(0,1,0)))
colors={}
def material(p):
 key=(tuple(p['color']),p['material'])
 if key in colors:return colors[key]
 m=bpy.data.materials.new(p['material']+str(p['color']));m.use_nodes=True
 shader=m.node_tree.nodes.get('Principled BSDF')
 # Roblox Color3 is sRGB; shader RGB is scene-linear.
 def linear(c):
  c=c/255;return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4
 rgb=tuple(linear(v) for v in p['color']);shader.inputs['Base Color'].default_value=(*rgb,1)
 shader.inputs['Metallic'].default_value=.55 if p['material']=='Metal' else 0
 shader.inputs['Roughness'].default_value=.42 if p['material']=='Metal' else .9 if p['material'] in ['Fabric','Wood'] else .55
 if p['material']=='Neon':
  shader.inputs['Emission Color'].default_value=(*rgb,1);shader.inputs['Emission Strength'].default_value=2.3
 colors[key]=m;return m
boxverts=[(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
boxfaces=[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)]
wedgeverts=[(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(-1,1,1),(1,1,1)]
wedgefaces=[(0,3,2,1),(2,3,4,5),(0,1,5,4),(0,4,3),(1,2,5)]
def geometry(p):
 rot=Matrix(p['rotation']);pos=Vector(p['pos']);size=Vector(p['size'])
 if p['shape']=='Ball':
  bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=AXIS@pos)
  obj=bpy.context.object
  transform=(AXIS@rot).to_4x4();transform.translation=AXIS@pos;obj.matrix_world=transform
  obj.scale=size/2
  for face in obj.data.polygons:face.use_smooth=True
 else:
  vertices,faces=(wedgeverts,wedgefaces) if p['shape']=='Wedge' else (boxverts,boxfaces)
  world=[AXIS@(pos+rot@Vector([v[k]*size[k]/2 for k in range(3)])) for v in vertices]
  mesh=bpy.data.meshes.new(p['name']);mesh.from_pydata(world,[],faces);mesh.update()
  obj=bpy.data.objects.new(p['name'],mesh);bpy.context.collection.objects.link(obj)
 obj.name=p['name'];obj.data.materials.append(material(p))
 return obj
def point(obj,target):obj.rotation_euler=(Vector(target)-obj.location).to_track_quat('-Z','Y').to_euler()
def area(name,pos,power,size,color):
 light=bpy.data.lights.new(name,'AREA');light.energy=power;light.shape='DISK';light.size=size;light.color=color
 obj=bpy.data.objects.new(name,light);bpy.context.collection.objects.link(obj);obj.location=pos;point(obj,(0,0,.1))
for idx,(name,parts) in enumerate(models.items()):
 bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);colors={}
 for p in parts:geometry(p)
 bpy.ops.mesh.primitive_plane_add(size=200,location=(0,0,-2.99));floor=bpy.context.object
 floor.data.materials.append(material(dict(color=[26,32,41],material='SmoothPlastic')))
 # Low display plinth, matching the exported gallery's simple platform.
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,-3.15));plinth=bpy.context.object;plinth.scale=(5.7,4.5,.30)
 plinth.data.materials.append(material(dict(color=[34,42,54],material='SmoothPlastic')))
 area('Key',(-5,7,8),1250,5.0,(1,.91,.79));area('Fill',(6,5,4),850,5,(.69,.81,1));area('Rim',(1,-4,7),1500,4,(.78,.86,1))
 camera=bpy.data.cameras.new('Camera');cam=bpy.data.objects.new('Camera',camera);bpy.context.collection.objects.link(cam)
 cam.location=(7,14,4.2);point(cam,(0,0,.15));camera.type='ORTHO';camera.ortho_scale=7.35
 scene=bpy.context.scene;scene.camera=cam;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False;scene.cycles.max_bounces=4;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=2
 scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.11,.13,.17,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.25
 scene.render.resolution_x=720;scene.render.resolution_y=790;scene.render.resolution_percentage=100
 scene.render.image_settings.file_format='PNG';scene.render.filepath=str(P/(name+'.png'))
 scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
 bpy.ops.wm.save_as_mainfile(filepath=str(P/(name+'.blend')))
 bpy.ops.render.render(write_still=True)
 print('Finished preview:',name,flush=True)
