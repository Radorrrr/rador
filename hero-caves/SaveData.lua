-- Durable player profiles, isolated Studio data, and expiring session ownership.
local DataStoreService=game:GetService('DataStoreService')
local HttpService=game:GetService('HttpService')
local RunService=game:GetService('RunService')
local SaveData={}
local STORE_NAME=RunService:IsStudio() and 'HeroCaves_Studio_v1' or 'HeroCaves_Progress_v1'
local store=DataStoreService:GetDataStore(STORE_NAME)
local LOCK_SECONDS=180
local function integer(value, fallback, low, high)
 if type(value)~='number' or value~=value or value==math.huge or value==-math.huge then return fallback end
 return math.clamp(math.floor(value),low,high)
end
function SaveData.normalize(data)
 if data~=nil and type(data)~='table' then error('Ungültiger gespeicherter Spielstand') end
 data=data or {}
 if data.version~=nil and data.version~=1 then error('Unbekannte Spielstand-Version') end
 local levels={}
 for id=1,4 do levels[tostring(id)]=integer(type(data.levels)=='table' and data.levels[tostring(id)] or nil,id==1 and 1 or 0,id==1 and 1 or 0,100) end
 local wave=integer(data.wave,1,1,1000)
 return {version=1,gold=integer(data.gold,0,0,9000000000000000),wave=wave,farming=data.farming==true and wave%5==4,levels=levels}
end
local function attempt(callback)
 local lastError
 for i=1,3 do
  local ok,result=pcall(callback)
  if ok then return true,result end
  lastError=result
  if i<3 then task.wait(i) end
 end
 return false,lastError
end
function SaveData.open(player)
 -- Unpublished places and local multi-player test identities have no durable profile.
 if game.GameId==0 or player.UserId<=0 then
  return {data=SaveData.normalize(nil),persistent=false,closed=false}
 end
 local profile={key='Player_'..player.UserId,token=HttpService:GenerateGUID(false),persistent=true,closed=false,saving=false}
 local claimed=false
 local ok,result=attempt(function()
  return store:UpdateAsync(profile.key,function(old)
   local now=os.time()
   if type(old)=='table' and type(old.session)=='table' and old.session.token~=profile.token and type(old.session.expires)=='number' and old.session.expires>now then return nil end
   local data=SaveData.normalize(old)
   data.session={token=profile.token,expires=now+LOCK_SECONDS}
   claimed=true
   return data
  end)
 end)
 if not ok then warn('Hero Caves: Laden fehlgeschlagen: '..tostring(result)); return nil,'Spielstand konnte nicht geladen werden. Prüfe in Studio die API-Freigabe und versuche es erneut.' end
 if not claimed or not result then return nil,'Dein Spielstand wird noch von einem anderen Server verwendet. Warte kurz und versuche es erneut.' end
 profile.data=SaveData.normalize(result)
 return profile
end
function SaveData.save(profile,data,release)
 if profile.closed then return true end
 if not profile.persistent then if release then profile.closed=true end; return true end
 local start=os.clock()
 while profile.saving and os.clock()-start<20 do task.wait(.1) end
 if profile.saving then return false,'busy' end
 if profile.closed then return true end
 profile.saving=true
 local ok,result=attempt(function()
  return store:UpdateAsync(profile.key,function(old)
   if type(old)~='table' or not old.session or old.session.token~=profile.token then return nil end
   local new=SaveData.normalize(data)
   new.savedAt=os.time()
   if not release then new.session={token=profile.token,expires=os.time()+LOCK_SECONDS} end
   return new
  end)
 end)
 profile.saving=false
 if not ok then warn('Hero Caves: Speichern fehlgeschlagen: '..tostring(result)); return false,'unavailable' end
 if not result then return false,'ownership' end
 if release then profile.closed=true end
 return true
end
return SaveData
