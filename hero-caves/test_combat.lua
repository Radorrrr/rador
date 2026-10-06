local queue={};local now=0;local hits=0;local valid=true;local moves={}
local cf=setmetatable({},{__mul=function(a,b) return a end})
CFrame={Angles=function() return cf end}
TweenInfo={new=function(duration) return {duration=duration} end}
Enum={EasingStyle={Quad=1},EasingDirection={InOut=1}}
local tween={Create=function(_,joint,info,props)
 return {Play=function() moves[#moves+1]={joint=joint,time=now,duration=info.duration}; joint.C0=props.C0 end}
end}
game={GetService=function() return tween end}
task={delay=function(delay,callback) queue[#queue+1]={time=now+delay,callback=callback} end}
local function advance(time)
 while true do
  table.sort(queue,function(a,b) return a.time<b.time end)
  if not queue[1] or queue[1].time>time then break end
  local job=table.remove(queue,1); now=job.time; job.callback()
 end
 now=time
end
local A=dofile('/workspace/hero-caves/CombatAnimation.lua')
local function rig() return {shoulder={Parent=true},elbow={Parent=true},wrist={Parent=true},shoulderRest=cf,elbowRest=cf,wristRest=cf} end
for _,weapon in ipairs({'Sword','Axe','Staff'}) do
 queue={};moves={};now=0;hits=0;valid=true
 assert(A.attack(rig(),weapon,function() hits=hits+1 end,function() return valid end))
 assert(hits==0 and #moves==3)
 advance(.179); assert(hits==0 and #moves==3)
 advance(.33); assert(hits==0 and #moves==6)
 advance(.35); assert(hits==1)
 advance(1); assert(hits==1 and #moves==9)
end
queue={};moves={};now=0;hits=0;valid=true
A.attack(rig(),'Sword',function() hits=hits+1 end,function() return valid end)
advance(.1); valid=false; advance(1); assert(hits==0 and #moves==6)
queue={};moves={};now=0;hits=0;valid=true
A.attack(rig(),'Axe',function() hits=hits+1 end,function() return valid end)
advance(.2); valid=false; advance(1); assert(hits==0 and #moves==9)
print('CombatAnimation: all weapon timelines, one hit at contact, cancellation and recovery passed')
