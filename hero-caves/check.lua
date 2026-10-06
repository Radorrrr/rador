for _,name in ipairs({'Game.server.lua','Game.client.lua','CharacterDesign.lua'}) do
 local fn,err=loadfile('/workspace/hero-caves/'..name)
 assert(fn,err)
 print(name..': syntax OK')
end
local f=assert(io.open('/workspace/hero-caves/Game.server.lua','r'))
local source=f:read('*a'); f:close()
local code=assert(source:match('(local function hp%(wave%).-\nend)'))
local hp=assert(load(code..'\nreturn hp'))()
for wave=5,100,5 do assert(hp(wave)==10*hp(wave-1)) end
for wave=2,100 do if wave%5~=0 and (wave-1)%5~=0 then assert(hp(wave)>=hp(wave-1)) end end
print('Boss HP formula: 20 bosses verified')
