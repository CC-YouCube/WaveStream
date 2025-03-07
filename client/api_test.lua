local API = require "api"
local api = API.new("127.0.0.1:5000",false)

local function wait_for_input()
    while true do
        local event=({os.pullEvent()})[1]
        if event=="mouse_click"or event=="key"then break end
    end
end

local function nft_example()
    local response, err, err_response = api:nft(
        "https://i.pinimg.com/originals/a0/5d/8f/a05d8f03367754bf863981fa0a08db69.jpg",
            {term.getSize()}, true
    )
    if response == nil then error(err) end
    local img = paintutils.parseImage(response)
    local bgc = term.getBackgroundColour()
    paintutils.drawImage(img,1,1)
    wait_for_input()
    term.setBackgroundColour(bgc)
    term.setCursorPos(1,1)
    term.clear()
end
nft_example()
