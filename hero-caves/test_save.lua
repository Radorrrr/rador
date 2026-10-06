local root='/workspace/hero-caves/'
math.clamp=function(x,lo,hi) return math.max(lo,math.min(hi,x)) end
local function copy(v) if type(v)~='table' then return v end; local t={}; for k,x in pairs(v) do t[k]=copy(x) end; return t end
local memory={}; local calls=0; local fail=false; local studio=true; local selected
local store={UpdateAsync=function(_,key,callback)
 calls=calls+1; if fail then error('simulated API failure') end
 local new=callback(copy(memory[key])); if new==nil then return nil end
 memory[key]=copy(new); return copy(new)
end}
local counter=0
local services={DataStoreService={GetDataStore=function(_,name) selected=name; return store end},HttpService={GenerateGUID=function() counter=counter+1; return 'session-'..counter end},RunService={IsStudio=function() return studio end}}
game={GameId=123,GetService=function(_,name) return services[name] end}
task={wait=function() end}; warn=function() end
local S=dofile(root..'SaveData.lua')
assert(selected=='HeroCaves_Studio_v1')
local p=assert(S.open({UserId=7})); assert(p.data.gold==0 and p.data.levels['1']==1)
local blocked=S.open({UserId=7}); assert(blocked==nil)
local data={version=1,gold=1234,wave=9,farming=true,levels={['1']=15,['2']=7,['3']=1,['4']=0}}
assert(S.save(p,data,false)); assert(memory.Player_7.session.token==p.token)
assert(S.save(p,data,true)); assert(memory.Player_7.session==nil)
local reopened=assert(S.open({UserId=7})); assert(reopened.data.gold==1234 and reopened.data.wave==9 and reopened.data.farming and reopened.data.levels['2']==7)
assert(S.save(reopened,data,true)); assert(S.save(p,{gold=0},true)); assert(memory.Player_7.gold==1234)
fail=true; local before=copy(memory.Player_7); local broken=S.open({UserId=7}); assert(broken==nil); assert(memory.Player_7.gold==before.gold); fail=false
local current=assert(S.open({UserId=7})); memory.Player_7.session.expires=0
local newer=assert(S.open({UserId=7})); local ok,reason=S.save(current,{gold=0},false); assert(not ok and reason=='ownership'); assert(memory.Player_7.gold==1234)
assert(S.save(newer,data,true))
local malformed=S.normalize({gold=0/0,wave=-1,levels={['1']=500,['2']=-20,['3']=math.huge},farming=true}); assert(malformed.gold==0 and malformed.wave==1 and malformed.levels['1']==100 and malformed.levels['2']==0 and not malformed.farming)
assert(not pcall(S.normalize,{version=2})); assert(not pcall(S.normalize,'invalid'))
local callCount=calls; game.GameId=0; local temporary=assert(S.open({UserId=7})); assert(not temporary.persistent); assert(S.save(temporary,data,true)); assert(calls==callCount)
game.GameId=123; local localPlayer=assert(S.open({UserId=-1})); assert(not localPlayer.persistent)
studio=false; dofile(root..'SaveData.lua'); assert(selected=='HeroCaves_Progress_v1')
print('SaveData: round-trip, levels, farming, session exclusion, ownership, API failure, schema validation and Studio isolation passed')
