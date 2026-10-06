local Players=game:GetService('Players')
local RS=game:GetService('ReplicatedStorage')
local event=RS:WaitForChild('HeroCavesEvent')
local gui=Instance.new('ScreenGui'); gui.Name='HeroCavesUI'; gui.ResetOnSpawn=false; gui.Parent=Players.LocalPlayer:WaitForChild('PlayerGui')
local panel=Instance.new('Frame'); panel.Size=UDim2.new(0,350,0,430); panel.Position=UDim2.new(0,12,0,12); panel.BackgroundColor3=Color3.fromRGB(24,29,38); panel.Parent=gui
local scale=Instance.new('UIScale'); scale.Parent=panel
local function fit() local camera=workspace.CurrentCamera; if camera then scale.Scale=math.min(1,camera.ViewportSize.X/380,camera.ViewportSize.Y/500) end end
fit(); workspace:GetPropertyChangedSignal('CurrentCamera'):Connect(fit)
if workspace.CurrentCamera then workspace.CurrentCamera:GetPropertyChangedSignal('ViewportSize'):Connect(fit) end
local function text(y,height,value)
 local t=Instance.new('TextLabel'); t.Position=UDim2.fromOffset(12,y); t.Size=UDim2.new(1,-24,0,height); t.BackgroundTransparency=1; t.TextColor3=Color3.new(1,1,1); t.TextSize=16; t.Font=Enum.Font.Gotham; t.TextWrapped=true; t.Text=value; t.Parent=panel; return t
end
local function button(y,x,width,title,callback)
 local b=Instance.new('TextButton'); b.Position=UDim2.fromOffset(x,y); b.Size=UDim2.fromOffset(width,30); b.Text=title; b.TextColor3=Color3.new(1,1,1); b.BackgroundColor3=Color3.fromRGB(65,100,150); b.Font=Enum.Font.GothamBold; b.TextSize=13; b.Parent=panel; b.Activated:Connect(callback); return b
end
text(8,25,'HERO CAVES')
local status=text(38,50,'Lade deine Base …')
button(92,12,155,'Zu meiner Base',function() event:FireServer('Base') end)
button(92,179,155,'Zum Händler',function() event:FireServer('Town') end)
local shopOpen=false
local rows={}
for i=1,4 do
 local y=133+(i-1)*58
 rows[i]={label=text(y,26,''),button=button(y+27,12,322,'',function()
  local row=rows[i]; if not row.data then return end
  if row.data.level>0 then event:FireServer('Upgrade',i)
  elseif shopOpen then event:FireServer('Buy',i) else event:FireServer('Town') end
 end)}
end
local retry=button(368,12,322,'Boss erneut versuchen',function() event:FireServer('Retry') end); retry.Visible=false
local message=text(400,26,'Käufe beim Händler • Upgrades überall')
local saveStatus=text(430,32,'')
panel.Size=UDim2.fromOffset(350,472)
local messageUntil=0
local function n(value) if value>=1e6 then return string.format('%.1fM',value/1e6) elseif value>=1000 then return string.format('%.1fk',value/1000) else return tostring(math.floor(value)) end end
local state
local function render()
 if not state then return end
 status.Text='Gold: '..n(state.gold)..'  |  Welle: '..state.wave..(state.farming and ' · Gold sammeln' or '')..(state.remaining and string.format('\nBoss: %.1f Sekunden',state.remaining) or '')
 retry.Visible=state.farming
 saveStatus.Text=state.saveStatus or ''
 saveStatus.TextSize=12
 for i,h in ipairs(state.heroes) do
  local row=rows[i]; row.data=h
  row.label.Text=h.name..' · Lv. '..h.level..' · '..n(h.damage)..' Schaden · '..h.speed..'/s'
  row.button.Text=h.level>0 and (h.level>=100 and 'Maximales Level' or 'Upgrade: '..n(h.upgrade)..' Gold'..(h.arriving and ' · unterwegs' or '')) or (shopOpen and 'Kaufen: '..n(h.cost)..' Gold' or 'Beim Händler kaufen: '..n(h.cost)..' Gold')
 end
 if os.clock()>messageUntil then message.Text=shopOpen and 'Heldenkauf in der Nähe des Händlers' or 'Käufe beim Händler • Upgrades überall' end
end
event.OnClientEvent:Connect(function(kind,data)
 if kind=='Shop' then shopOpen=true; render()
 elseif kind=='State' then state=data; if data.message then message.Text=data.message; messageUntil=os.clock()+5 end; render() end
end)
event:FireServer('Sync')
