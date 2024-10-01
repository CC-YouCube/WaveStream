-- TODO: WIP
-- TODO: add noice UI https://github.com/MCJack123/PrimeUI
-- TODO: Support playlist
local aukit = require "aukit"
local loop = require "taskmaster"()
local api = require "api"("127.0.0.1:5000", false)

local speakers = {peripheral.find("speaker")}
if #speakers == 0 then error("No speaker attached") end
if #speakers == 2 and peripheral.getName(speakers[1]) == "right" and peripheral.getName(speakers[2]) == "left" then speakers = {speakers[2], speakers[1]} end

local path = table.concat({...}, " ")
if path:match("^%s*$") ~= nil then error("Usage: wavestream <URL>") end

local mono = #speakers == 1
--aukit.defaultInterpolation = aukit.defaultInterpolation

local handle, err = http.get(api:dfpwm(path), nil, true)
    if not handle then error("Could not connect to " .. path .. ": " .. err) end
    local code = handle.getResponseCode()
    if code ~= 200 then handle.close() error("Could not connect to " .. path .. ": HTTP " .. code) end
local closed = false
local function data()
    if closed then return nil end
    local d = handle.read(48000) -- 48000
    if not d then handle.close() closed = true return nil end return d
end

local iter, length = aukit.stream.dfpwm(data, 48000, 1, mono)
if length == nil then length = 0 end

print("Streaming...")
local w = term.getSize()
local y = select(2, term.getCursorPos())
local fg, bg = colors.toBlit(term.getTextColor()), colors.toBlit(term.getBackgroundColor())
term.write(("00:00 %s %02d:%02d"):format(("\127"):rep(w - 12), math.floor(length / 60), length % 60))
local function progress(pos)
    pos = math.min(pos, 5999)
    local p = pos / length
    term.setCursorPos(1, y)
    if p > 1 then
        term.blit(("%02d:%02d %s --:--"):format(math.floor(pos / 60), pos % 60, (" "):rep(w - 12)), fg:rep(w), bg:rep(6) .. fg:rep(w - 12) .. bg:rep(6))
    else
        term.blit(("%02d:%02d %s%s %02d:%02d"):format(math.floor(pos / 60), pos % 60, (" "):rep(math.floor((w - 12) * p)), ("\127"):rep((w - 12) - math.floor((w - 12) * p)), math.floor(length / 60), length % 60),
        fg:rep(w), bg:rep(6) .. fg:rep(math.floor((w - 12) * p)) .. bg:rep((w - 12) - math.floor((w - 12) * p) + 6))
    end
end
local player = aukit.player(loop, iter, table.unpack(speakers))
loop:addTask(function()
    while true do
        local _, param = os.pullEvent("key")
        if param == keys.space then
            if player.isPaused then player:play()
            else player:pause() end
        elseif param == keys.left then
            player:seek(math.max(player:livePosition() - 5, 0))
        elseif param == keys.right then
            player:seek(player:livePosition() + 5)
        elseif param == keys.q then
            player:stop()
            handle.close()
            return
        end
        progress(player:livePosition())
    end
end)
loop:addTimer(0.25, function()
    if player.playerTask == nil then return 0 end
    progress(player:livePosition())
end)
loop:run(2)
sleep(0)
