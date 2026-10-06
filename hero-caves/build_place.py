from pathlib import Path
import xml.etree.ElementTree as ET
root_path = Path(__file__).parent
root = ET.Element('roblox', {'version': '4'})
ET.SubElement(root, 'External').text = 'null'
ET.SubElement(root, 'External').text = 'nil'
def item(parent, cls, name, source=None):
    obj = ET.SubElement(parent, 'Item', {'class': cls, 'referent': 'RBX' + name})
    props = ET.SubElement(obj, 'Properties')
    ET.SubElement(props, 'string', {'name': 'Name'}).text = name
    if source is not None:
        ET.SubElement(props, 'ProtectedString', {'name': 'Source'}).text = source
        if cls != 'ModuleScript':
            ET.SubElement(props, 'bool', {'name': 'Disabled'}).text = 'false'
    return obj
item(root, 'Workspace', 'Workspace')
replicated = item(root, 'ReplicatedStorage', 'ReplicatedStorage')
item(replicated, 'ModuleScript', 'CombatAnimation', (root_path / 'CombatAnimation.lua').read_text())
item(replicated, 'ModuleScript', 'CharacterDesign', (root_path / 'CharacterDesign.lua').read_text())
assets = item(root, 'ServerStorage', 'ServerStorage')
gallery = item(assets, 'Folder', 'CharacterModels')
for hero in ['Ritter', 'Berserker', 'Magier', 'Paladin']:
    model = ET.parse(root_path / (hero + '.rbxmx')).getroot().find('Item')
    for obj in model.iter('Item'):
        obj.set('referent', hero + obj.get('referent'))
    for ref in model.iter('Ref'):
        if ref.text and ref.text != 'null': ref.text = hero + ref.text
    gallery.append(model)
server = item(root, 'ServerScriptService', 'ServerScriptService')
item(server, 'ModuleScript', 'SaveData', (root_path / 'SaveData.lua').read_text())
item(server, 'Script', 'HeroCavesServer', (root_path / 'Game.server.lua').read_text())
starter = item(root, 'StarterPlayer', 'StarterPlayer')
client = item(starter, 'StarterPlayerScripts', 'StarterPlayerScripts')
item(client, 'LocalScript', 'HeroCavesClient', (root_path / 'Game.client.lua').read_text())
ET.indent(root)
ET.ElementTree(root).write(root_path / 'HeroCaves.rbxlx', encoding='utf-8', xml_declaration=True)

# Importable script update pack; keeps the user's existing place and experience.
update = ET.Element('roblox', {'version': '4'})
ET.SubElement(update, 'External').text = 'null'
ET.SubElement(update, 'External').text = 'nil'
pack = item(update, 'Folder', 'HeroCavesUpdate')
for cls, name, filename in [('ModuleScript','CombatAnimation','CombatAnimation.lua'), ('ModuleScript','SaveData','SaveData.lua'), ('ModuleScript','CharacterDesign','CharacterDesign.lua'), ('Script','HeroCavesServer','Game.server.lua'), ('LocalScript','HeroCavesClient','Game.client.lua')]:
    entry=item(pack,cls,name,(root_path/filename).read_text())
    if cls in ('Script','LocalScript'):
        entry.find("Properties/bool[@name='Disabled']").text='true'
ET.indent(update)
ET.ElementTree(update).write(root_path / 'HeroCavesUpdate.rbxmx', encoding='utf-8', xml_declaration=True)
