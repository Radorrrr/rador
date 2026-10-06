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
item(replicated, 'ModuleScript', 'CharacterDesign', (root_path / 'CharacterDesign.lua').read_text())
assets = item(root, 'ServerStorage', 'ServerStorage')
gallery = item(assets, 'Folder', 'CharacterModels')
for hero in ['Ritter', 'Berserker', 'Magier', 'Paladin']:
    model = ET.parse(root_path / (hero + '.rbxmx')).getroot().find('Item')
    for obj in model.iter('Item'):
        obj.set('referent', hero + obj.get('referent'))
    model.find("Properties/Ref[@name='PrimaryPart']").text = hero + 'P0'
    gallery.append(model)
server = item(root, 'ServerScriptService', 'ServerScriptService')
item(server, 'Script', 'HeroCavesServer', (root_path / 'Game.server.lua').read_text())
starter = item(root, 'StarterPlayer', 'StarterPlayer')
client = item(starter, 'StarterPlayerScripts', 'StarterPlayerScripts')
item(client, 'LocalScript', 'HeroCavesClient', (root_path / 'Game.client.lua').read_text())
ET.indent(root)
ET.ElementTree(root).write(root_path / 'HeroCaves.rbxlx', encoding='utf-8', xml_declaration=True)
