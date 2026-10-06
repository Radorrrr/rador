-- Hero Caves prototype. All economy and combat are server-authoritative.
local Players = game:GetService('Players')
local RS = game:GetService('ReplicatedStorage')
local Tween = game:GetService('TweenService')
local Run = game:GetService('RunService')
local Debris = game:GetService('Debris')
local CharacterDesign = require(RS:WaitForChild('CharacterDesign'))
local SaveData = require(game:GetService('ServerScriptService'):WaitForChild('SaveData'))
local CombatAnimation = require(RS:WaitForChild('CombatAnimation'))
local heroes = {
 {name='Ritter', cost=0, damage=6, speed=1, weapon='Sword', color=Color3.fromRGB(95,145,210)},
 {name='Berserker', cost=100, damage=18, speed=0.8, weapon='Axe', color=Color3.fromRGB(210,95,60)},
 {name='Magier', cost=500, damage=45, speed=1.2, weapon='Staff', color=Color3.fromRGB(145,85,210)},
 {name='Paladin', cost=2000, damage=150, speed=1, weapon='Sword', color=Color3.fromRGB(235,190,70)},
}
local function damage(id, level) return heroes[id].damage * (1.22 ^ (level-1)) end
local function upgradeCost(id, level) return math.floor((heroes[id].cost * 0.15 + 15) * 1.35 ^ (level-1)) end
local function hp(wave)
 if wave%5==0 then return hp(wave-1)*10 end
 return math.floor(35*1.22^(wave-1))
end
local folder=Instance.new('Folder'); folder.Name='HeroCaves'; folder.Parent=workspace
local remote=Instance.new('RemoteEvent'); remote.Name='HeroCavesEvent'; remote.Parent=RS
local states={}
local opening={}
local closingProfiles={}
local shuttingDown=false
local function part(parent,name,size,cf,color)
 local p=Instance.new('Part'); p.Name=name; p.Size=size; p.CFrame=cf; p.Color=color
 p.Anchored=true; p.TopSurface=Enum.SurfaceType.Smooth; p.BottomSurface=Enum.SurfaceType.Smooth; p.Parent=parent
 return p
end
local function label(p,text,size)
 local gui=Instance.new('BillboardGui'); gui.Size=UDim2.fromOffset(size or 230,65); gui.StudsOffset=Vector3.new(0,4,0); gui.AlwaysOnTop=true; gui.MaxDistance=150; gui.Parent=p
 local t=Instance.new('TextLabel'); t.Size=UDim2.fromScale(1,1); t.BackgroundTransparency=1; t.Text=text; t.TextColor3=Color3.new(1,1,1); t.TextStrokeTransparency=0.3; t.TextScaled=true; t.Font=Enum.Font.GothamBold; t.Parent=gui
 return t,gui
end
local function actor(parent,name,cf,color,weapon)
 local designed, designedWeapon, rig=CharacterDesign.create(parent,name,cf)
 if designed then return designed,designedWeapon,rig end
 local m=Instance.new('Model'); m.Name=name; m.Parent=parent
 local root=part(m,'Torso',Vector3.new(2,2.5,1),cf,color); m.PrimaryPart=root
 local head=part(m,'Head',Vector3.new(1.4,1.4,1.4),cf*CFrame.new(0,2,0),Color3.fromRGB(240,205,160)); head.Shape=Enum.PartType.Ball
 part(m,'LeftLeg',Vector3.new(.8,1.5,.8),cf*CFrame.new(-.5,-2,0),color)
 part(m,'RightLeg',Vector3.new(.8,1.5,.8),cf*CFrame.new(.5,-2,0),color)
 part(m,'LeftArm',Vector3.new(.7,2,.7),cf*CFrame.new(-1.4,0,0),color)
 local arm=part(m,'RightArm',Vector3.new(.7,2,.7),cf*CFrame.new(1.4,0,0),color)
 local blade
 if weapon then
  blade=part(m,'Weapon',Vector3.new(.3,3,.35),arm.CFrame*CFrame.new(0,-.3,-1),Color3.fromRGB(210,220,235))
  if weapon=='Axe' then blade.Size=Vector3.new(1.8,2,.5) end
  if weapon=='Staff' then
   blade.Color=Color3.fromRGB(100,65,40)
   local orb=part(m,'Orb',Vector3.new(.9,.9,.9),blade.CFrame*CFrame.new(0,1.6,0),Color3.fromRGB(170,90,255)); orb.Shape=Enum.PartType.Ball; orb.Material=Enum.Material.Neon
  end
 end
 for _,p in ipairs(m:GetChildren()) do if p:IsA('BasePart') then p.CanCollide=false end end
 return m,blade
end
part(folder,'Ground',Vector3.new(500,1,500),CFrame.new(0,-.5,0),Color3.fromRGB(65,105,65))
part(folder,'Plaza',Vector3.new(65,1,65),CFrame.new(0,.05,0),Color3.fromRGB(120,120,115))
local spawn=Instance.new('SpawnLocation'); spawn.Name='TownSpawn'; spawn.Size=Vector3.new(8,1,8); spawn.Position=Vector3.new(0,1,0); spawn.Anchored=true; spawn.Neutral=true; spawn.Parent=folder
local merchant=actor(folder,'Heldenhändler',CFrame.new(0,3,20),Color3.fromRGB(190,145,65),'Staff')
label(merchant.PrimaryPart,'HELDENHÄNDLER')
local prompt=Instance.new('ProximityPrompt'); prompt.ActionText='Helden kaufen'; prompt.ObjectText='Heldenhändler'; prompt.MaxActivationDistance=14; prompt.HoldDuration=0; prompt.Parent=merchant.PrimaryPart
prompt.Triggered:Connect(function(player) remote:FireClient(player,'Shop') end)
for i,name in ipairs({'Schmied – bald verfügbar','Chronist – bald verfügbar'}) do
 local npc=actor(folder,name,CFrame.new(i==1 and -18 or 18,3,20),Color3.fromRGB(100,90,80)); label(npc.PrimaryPart,name)
end
local function snapshot(s,message)
 local list={}
 for id,def in ipairs(heroes) do
  local h=s.heroes[id]; local level=h and h.level or 0
  table.insert(list,{id=id,name=def.name,cost=def.cost,level=level,damage=damage(id,math.max(level,1)),speed=def.speed,upgrade=upgradeCost(id,math.max(level,1)),arriving=h and not h.ready or false})
 end
 remote:FireClient(s.player,'State',{gold=s.gold,wave=s.wave,farming=s.farming,remaining=s.deadline and math.max(0,s.deadline-os.clock()) or nil,heroes=list,message=message,saveStatus=s.saveStatus})
 s.goldValue.Value=s.gold
end
local function spawnMob(s)
 if s.mob then s.mob:Destroy() end
 local boss=s.wave%5==0
 s.health=hp(s.wave); s.maxHealth=s.health; s.deadline=nil; s.active=false
 local start=s.center+Vector3.new(0,3,-22)
 s.mob=actor(s.base,boss and 'Boss' or 'Höhlengegner',CFrame.new(start),boss and Color3.fromRGB(175,45,45) or Color3.fromRGB(85,170,90))
 if boss then s.mob:ScaleTo(1.7) end
 s.healthLabel=label(s.mob.PrimaryPart,'')
 local gui=s.healthLabel.Parent
 local bg=Instance.new('Frame'); bg.Size=UDim2.new(1,0,0,10); bg.Position=UDim2.new(0,0,1,2); bg.BackgroundColor3=Color3.fromRGB(45,45,45); bg.Parent=gui
 s.bar=Instance.new('Frame'); s.bar.Size=UDim2.fromScale(1,1); s.bar.BackgroundColor3=boss and Color3.fromRGB(240,70,70) or Color3.fromRGB(80,220,100); s.bar.BorderSizePixel=0; s.bar.Parent=bg
 local mob=s.mob
 task.spawn(function()
  local t0=os.clock(); local from=mob:GetPivot(); local target=CFrame.new(s.center+Vector3.new(0,boss and 5 or 3,0))
  while states[s.player]==s and s.mob==mob and os.clock()-t0<1.4 do mob:PivotTo(from:Lerp(target,math.min(1,(os.clock()-t0)/1.4))); task.wait() end
  if states[s.player]~=s or s.mob~=mob then return end
  mob:PivotTo(target); s.active=true
  if boss then s.deadline=os.clock()+30 end
  snapshot(s)
 end)
end
local function addHero(s,id,walk)
 local slot=id; local angle=(slot-1)*math.pi/2+math.pi/4
 local pos=s.center+Vector3.new(math.cos(angle)*4.2,3,math.sin(angle)*4.2)
 local target=CFrame.lookAt(pos,Vector3.new(s.center.X,pos.Y,s.center.Z))
 local m,blade,rig=actor(s.base,heroes[id].name,walk and CFrame.new(0,3,20) or target,heroes[id].color,heroes[id].weapon)
 label(m.PrimaryPart,heroes[id].name,120)
 local h={level=1,model=m,blade=blade,rig=rig,ready=not walk,nextAttack=0}; s.heroes[id]=h
 if not walk then return end
 task.spawn(function()
  local points={Vector3.new(0,3,30),Vector3.new(s.center.X,3,30),pos}
  for _,point in ipairs(points) do
   local from=m:GetPivot(); local duration=(point-from.Position).Magnitude/16; local t0=os.clock()
   while states[s.player]==s and os.clock()-t0<duration do
    local p=from.Position:Lerp(point,math.min(1,(os.clock()-t0)/duration)); m:PivotTo(CFrame.lookAt(p,Vector3.new(point.X+0.001,p.Y,point.Z))); task.wait()
   end
   if states[s.player]~=s then return end
  end
  m:PivotTo(target); h.ready=true; h.nextAttack=os.clock(); snapshot(s)
 end)
end
local function attack(s,id,h)
 local target=s.mob; local amount=damage(id,h.level)
 local function valid()
  return states[s.player]==s and s.active and s.mob==target and target.Parent~=nil and h.model.Parent~=nil
 end
 CombatAnimation.attack(h.rig,heroes[id].weapon,function()
  if not valid() or s.health<=0 or (s.deadline and os.clock()>=s.deadline) then return end
  local function hit()
   if not valid() or s.health<=0 or (s.deadline and os.clock()>=s.deadline) then return end
   s.health=math.max(0,s.health-amount)
   local glow=Instance.new('Highlight'); glow.Adornee=target; glow.FillColor=Color3.fromRGB(255,220,130); glow.FillTransparency=.4; glow.OutlineTransparency=1; glow.Parent=target; Debris:AddItem(glow,.12)
  end
  if heroes[id].weapon=='Staff' then
   local orb=h.model:FindFirstChild('Orb')
   local ball=part(s.base,'Magic',Vector3.new(.5,.5,.5),orb and orb.CFrame or h.blade.CFrame,Color3.fromRGB(107,218,255))
   ball.Shape=Enum.PartType.Ball; ball.Material=Enum.Material.Neon; ball.CanCollide=false
   Tween:Create(ball,TweenInfo.new(.12),{Position=target.PrimaryPart.Position}):Play(); Debris:AddItem(ball,.15)
   task.delay(.12,hit)
  else hit() end
 end,valid)
end
local function pack(s)
 local levels={}
 for id,h in pairs(s.heroes) do levels[tostring(id)]=h.level end
 return {version=1,gold=s.gold,wave=s.wave,farming=s.farming,levels=levels}
end
local function save(s,release)
 local ok,reason=SaveData.save(s.profile,pack(s),release)
 if not ok then
  s.saveStatus='Speichern fehlgeschlagen – erneuter Versuch folgt'
  if reason=='ownership' and s.player.Parent==Players then
   s.player:Kick('Dein Spielstand wurde auf einem anderen Server geöffnet. Bitte verbinde dich erneut.')
  end
 else s.saveStatus=s.profile.persistent and 'Spielstand gespeichert' or 'Nur diese Sitzung – Spiel noch nicht veröffentlicht' end
 return ok
end
local function join(player)
 if states[player] or opening[player] or shuttingDown then return end
 opening[player]=true
 local profile,loadError=SaveData.open(player)
 opening[player]=nil
 if not profile then if player.Parent==Players then player:Kick(loadError) end; return end
 if player.Parent~=Players or shuttingDown then SaveData.save(profile,profile.data,true); return end
 local loaded=profile.data
 local used={}; for _,s in pairs(states) do used[s.slot]=true end
 local slot=1; while used[slot] do slot=slot+1 end
 local column=(slot-1)%4; local row=math.floor((slot-1)/4)
 local center=Vector3.new((column-1.5)*58,0,90+row*75)
 local base=Instance.new('Model'); base.Name=player.Name..'_Base'; base.Parent=folder
 local platform=part(base,'Base',Vector3.new(48,1,55),CFrame.new(center),Color3.fromRGB(100,95,85)); label(platform,player.DisplayName..'s Base')
 for _,offset in ipairs({Vector3.new(-10,6,-24),Vector3.new(10,6,-24),Vector3.new(0,13,-24)}) do
  part(base,'CaveRock',offset.X==0 and Vector3.new(26,7,10) or Vector3.new(9,14,10),CFrame.new(center+offset),Color3.fromRGB(55,60,65))
 end
 part(base,'CaveDark',Vector3.new(12,10,1),CFrame.new(center+Vector3.new(0,5,-28)),Color3.fromRGB(12,15,20))
 part(base,'Path',Vector3.new(8,.25,center.Z-30),CFrame.new(center.X,.2,(center.Z+30)/2),Color3.fromRGB(150,130,95))
 local leader=Instance.new('Folder'); leader.Name='leaderstats'; leader.Parent=player
 local gold=Instance.new('IntValue'); gold.Name='Gold'; gold.Parent=leader
 local s={player=player,slot=slot,base=base,center=center,gold=loaded.gold,goldValue=gold,wave=loaded.wave,farming=loaded.farming,heroes={},lastRequest=0,profile=profile,saveStatus=profile.persistent and 'Spielstand geladen' or 'Nur diese Sitzung – Spiel noch nicht veröffentlicht'}; states[player]=s
 for id=1,#heroes do
  local level=loaded.levels[tostring(id)] or 0
  if level>0 then addHero(s,id,false); s.heroes[id].level=level end
 end
 spawnMob(s); snapshot(s)
end
Players.PlayerAdded:Connect(join)
Players.PlayerRemoving:Connect(function(player)
 local s=states[player]; states[player]=nil
 if s then
  s.base:Destroy(); closingProfiles[s]=true
  save(s,true); closingProfiles[s]=nil
 end
end)
task.spawn(function()
 while not shuttingDown do
  task.wait(45)
  if shuttingDown then break end
  for _,s in pairs(states) do task.spawn(function() save(s,false) end) end
 end
end)
game:BindToClose(function()
 shuttingDown=true
 local pending={}
 for player,s in pairs(states) do states[player]=nil; pending[s]=true end
 for s in pairs(closingProfiles) do pending[s]=true end
 for s in pairs(pending) do
  task.spawn(function() save(s,true); pending[s]=nil end)
 end
 local started=os.clock()
 while next(pending) and os.clock()-started<25 do task.wait(.1) end
end)
for _,p in ipairs(Players:GetPlayers()) do task.spawn(join,p) end
remote.OnServerEvent:Connect(function(player,action,id)
 local s=states[player]; if not s then return end
 local now=os.clock(); if now-s.lastRequest<.15 then return end; s.lastRequest=now
 if action=='Sync' then snapshot(s); return end
 if action=='Retry' and s.farming then s.farming=false; s.wave=s.wave+1; spawnMob(s)
 elseif action=='Base' then
  local character=player.Character; if character then character:PivotTo(CFrame.new(s.center+Vector3.new(0,5,20))) end
 elseif action=='Town' then
  if player.Character then player.Character:PivotTo(CFrame.new(0,5,0)) end
 elseif action=='Buy' and type(id)=='number' and heroes[id] and not s.heroes[id] then
  local root=player.Character and player.Character:FindFirstChild('HumanoidRootPart')
  if not root or (root.Position-merchant.PrimaryPart.Position).Magnitude>20 then snapshot(s,'Gehe zum Heldenhändler.'); return end
  if s.gold<heroes[id].cost then snapshot(s,'Nicht genug Gold.'); return end
  s.gold=s.gold-heroes[id].cost; addHero(s,id,true)
 elseif action=='Upgrade' and type(id)=='number' and s.heroes[id] then
  local h=s.heroes[id]; if h.level>=100 then snapshot(s,'Maximales Level erreicht.'); return end
  local cost=upgradeCost(id,h.level)
  if s.gold<cost then snapshot(s,'Nicht genug Gold.'); return end
  s.gold=s.gold-cost; h.level=h.level+1
 end
 snapshot(s)
end)
local lastSync=0
Run.Heartbeat:Connect(function()
 local now=os.clock()
 for _,s in pairs(states) do
  if s.active then
   if s.deadline and now>=s.deadline then
    s.wave=s.wave-1; s.farming=true; spawnMob(s); snapshot(s,'Boss gescheitert. Verbessere deine Helden und versuche es erneut!')
   else
    for id,h in pairs(s.heroes) do
     if h.ready and now>=h.nextAttack and s.health>0 then
      h.nextAttack=now+1/heroes[id].speed; attack(s,id,h)
     end
    end
    if s.health<=0 then
     s.gold=s.gold+math.floor(10*1.18^(s.wave-1)*(s.wave%5==0 and 5 or 1))
     s.active=false; s.deadline=nil
     local defeatedMob=s.mob
     if not s.farming then s.wave=s.wave+1 end
     snapshot(s)
     task.delay(.5,function() if states[s.player]==s and s.mob==defeatedMob and not s.active then spawnMob(s) end end)
    end
   end
  end
  if s.healthLabel and s.healthLabel.Parent then
   s.healthLabel.Text=string.format('%s · Welle %d\n%d / %d HP',s.wave%5==0 and 'BOSS' or 'Gegner',s.wave,math.ceil(s.health),s.maxHealth)
   s.bar.Size=UDim2.fromScale(math.clamp(s.health/s.maxHealth,0,1),1)
  end
  if now-lastSync>=.5 then snapshot(s) end
 end
 if now-lastSync>=.5 then lastSync=now end
end)
