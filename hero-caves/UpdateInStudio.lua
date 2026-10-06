-- Copy all of this into Studio's Command Bar while the game is stopped.
assert(not game:GetService('RunService'):IsRunning(),'Beende zuerst den Play-Test.')
local pack=workspace:FindFirstChild('HeroCavesUpdate')
assert(pack and pack:IsA('Folder'),'Importiere zuerst HeroCavesUpdate.rbxmx in Workspace.')
local server=game:GetService('ServerScriptService')
local replicated=game:GetService('ReplicatedStorage')
local client=game:GetService('StarterPlayer'):WaitForChild('StarterPlayerScripts')
local targets={
 {'SaveData',server,'ModuleScript'},
 {'CharacterDesign',replicated,'ModuleScript'},
 {'CombatAnimation',replicated,'ModuleScript'},
 {'HeroCavesServer',server,'Script'},
 {'HeroCavesClient',client,'LocalScript'},
}
for _,target in ipairs(targets) do
 local source=pack:FindFirstChild(target[1])
 assert(source and source:IsA(target[3]),'Update-Datei unvollständig: '..target[1])
end
local backup=Instance.new('Folder'); backup.Name='HeroCavesBackup_'..os.date('%Y%m%d_%H%M%S'); backup.Parent=game:GetService('ServerStorage')
for _,target in ipairs(targets) do
 local name,destination=target[1],target[2]
 local old=destination:FindFirstChild(name)
 if old then old.Parent=backup; if old:IsA('BaseScript') then old.Disabled=true end end
 local new=pack[name]:Clone()
 if new:IsA('BaseScript') then new.Disabled=false end
 new.Parent=destination
end
pack:Destroy()
print('Hero Caves aktualisiert. Vorherige Scripts liegen unter ServerStorage/'..backup.Name..'. Jetzt dieselbe Experience veröffentlichen.')
