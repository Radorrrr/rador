local Designer = {}
function Designer.create(parent, name, cf)
 local specs=designs[name]; if not specs then return nil end
 local model=Instance.new('Model'); model.Name=name; model.Parent=parent
 local parts={}; local bySpec={}
 for _,s in ipairs(specs) do
  local p=Instance.new('Part'); p.Name=s.name; p.Size=Vector3.new(table.unpack(s.size)); p.CFrame=cf*CFrame.new(table.unpack(s.pos))
  p.Color=Color3.fromRGB(table.unpack(s.color)); p.Material=Enum.Material[s.material]; p.Shape=Enum.PartType[s.shape]
  p.Anchored=s.name=='Torso'; p.Massless=true; p.CanCollide=false; p.CanTouch=false; p.CanQuery=false
  p.TopSurface=Enum.SurfaceType.Smooth; p.BottomSurface=Enum.SurfaceType.Smooth; p.Parent=model
  parts[s.name]=p; bySpec[p]=s
  if s.name=='Torso' then model.PrimaryPart=p end
 end
 local torso=parts.Torso; local upper=parts.RightArm; local forearm=parts.RightForearm; local hand=parts.RightHand; local weapon=parts.Weapon
 local function joint(name,p0,p1,worldPivot)
  local motor=Instance.new('Motor6D'); motor.Name=name; motor.Part0=p0; motor.Part1=p1
  motor.C0=p0.CFrame:ToObjectSpace(worldPivot); motor.C1=p1.CFrame:ToObjectSpace(worldPivot); motor.Parent=p0
  return motor
 end
 local shoulder=joint('RightShoulder',torso,upper,cf*CFrame.new(1.38,.95,0))
 local elbow=joint('RightElbow',upper,forearm,cf*CFrame.new(1.38,0,0))
 local wrist=joint('RightWrist',forearm,hand,cf*CFrame.new(1.38,-.82,0))
 local grip=joint('RightGrip',hand,weapon,cf*CFrame.new(1.38,-.92,0))
 local drivers={Arm=upper,Forearm=forearm,Hand=hand,Weapon=weapon,Body=torso}
 for p,s in pairs(bySpec) do
  if p~=torso and p~=upper and p~=forearm and p~=hand and p~=weapon then
   local weld=Instance.new('WeldConstraint'); weld.Name='DetailWeld'; weld.Part0=drivers[s.group] or torso; weld.Part1=p; weld.Parent=p
  end
 end
 local gripPoint=Instance.new('Attachment'); gripPoint.Name='GripPoint'; gripPoint.Parent=hand
 local tip=Instance.new('Attachment'); tip.Name='HitPoint'; tip.Position=Vector3.new(0,name=='Berserker' and 1.05 or name=='Magier' and 2 or 2.85,0); tip.Parent=weapon
 model:SetAttribute('Rigged',true)
 return model,weapon,{shoulder=shoulder,elbow=elbow,wrist=wrist,grip=grip,shoulderRest=shoulder.C0,elbowRest=elbow.C0,wristRest=wrist.C0,gripRest=grip.C0}
end
return Designer
