-- Joint keyframes: wind-up, swing/contact, recovery. C0 changes replicate to clients.
local TweenService=game:GetService('TweenService')
local CombatAnimation={}
local poses={
 Sword={wind={-65,-25,10,-20},hit={85,0,-175,20}},
 Axe={wind={-85,-15,5,-10},hit={90,0,-180,20}},
 Staff={wind={-30,-35,15,0},hit={70,0,-160,20}},
}
function CombatAnimation.attack(rig,weaponType,onHit,isValid)
 if not rig or not isValid() then return false end
 local pose=poses[weaponType] or poses.Sword
 local function move(values,duration)
  local shoulder=rig.shoulderRest*CFrame.Angles(0,math.rad(values[4]),0)*CFrame.Angles(math.rad(values[1]),0,0)
  local elbow=rig.elbowRest*CFrame.Angles(math.rad(values[2]),0,0)
  local wrist=rig.wristRest*CFrame.Angles(math.rad(values[3]),0,0)
  for _,pair in ipairs({{rig.shoulder,shoulder},{rig.elbow,elbow},{rig.wrist,wrist}}) do
   TweenService:Create(pair[1],TweenInfo.new(duration,Enum.EasingStyle.Quad,Enum.EasingDirection.InOut),{C0=pair[2]}):Play()
  end
 end
 move(pose.wind,.18)
 task.delay(.18,function()
  if not isValid() then if rig.shoulder.Parent then move({0,0,0,0},.22) end; return end
  move(pose.hit,.16)
  task.delay(.16,function()
   if isValid() then onHit() end
   task.delay(.06,function()
    if rig.shoulder.Parent then move({0,0,0,0},.22) end
   end)
  end)
 end)
 return true
end
return CombatAnimation
