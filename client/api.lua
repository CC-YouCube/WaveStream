local expect = require "cc.expect"

--- Converts a character to its hexadecimal representation for URL encoding
---@param char string The character to convert
---@return string The hexadecimal representation of the character, prefixed with '%'
local function char_to_hex(char)
    return string.format("%%%02X", string.byte(char))
end

-- TODO: make this function "public"
--- Encode url hopefully according to RFC 3986
---@param url string The URL to encode
---@return string The URL-encoded version of the input string
local function url_encode(url)
    expect(1, url, "string")
    return (url:gsub("([^%w%-%.%_%~])", char_to_hex):gsub(" ", "%%20"))
end

-- TODO: make this function "public"
-- Definitely not base on https://github.com/Phoenix-ComputerCraft/libsystem-craftos/blob/713e580e6a9229ca1e843b4dcc9bb3c3fde7c3ca/serialization.lua#L13-L36
local b64str = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
--- Encodes a binary string into urlsafe Base64 (RFC 4648) -> No padding and replace `+` with `-` and `/` with `_`
---@param str string The string to encode
---@return string The string's representation in Base64
local function urlsafe_b64encode(str)
    expect(1, str, "string")
    local retval = ""
    for s in str:gmatch "..." do
        local n = s:byte(1) * 65536 + s:byte(2) * 256 + s:byte(3)
        local a, b, c, d = bit32.extract(n, 18, 6), bit32.extract(n, 12, 6), bit32.extract(n, 6, 6), bit32.extract(n, 0, 6)
        retval = retval .. b64str:sub(a+1, a+1) .. b64str:sub(b+1, b+1) .. b64str:sub(c+1, c+1) .. b64str:sub(d+1, d+1)
    end
    if #str % 3 == 1 then
        local n = str:byte(-1)
        local a, b = bit32.rshift(n, 2), bit32.lshift(bit32.band(n, 3), 4)
        retval = retval .. b64str:sub(a+1, a+1) .. b64str:sub(b+1, b+1)
    elseif #str % 3 == 2 then
        local n = str:byte(-2) * 256 + str:byte(-1)
        local a, b, c, _ = bit32.extract(n, 10, 6), bit32.extract(n, 4, 6), bit32.lshift(bit32.extract(n, 0, 4), 2)
        retval = retval .. b64str:sub(a+1, a+1) .. b64str:sub(b+1, b+1) .. b64str:sub(c+1, c+1)
    end
    return retval
end

--- API
---@class API
---@field host string The host of the server
---@field tls boolean enable/disable TLS/SSL
local API = {VERSION = 1}
API.__index = API

--- Create a new API instance
---@param host string The host of the server
---@param tls boolean|nil enable/disable TLS/SSL (enable by default)
---@return API The nft image
function API.new(host, tls)
    return setmetatable({
        host = host,
        tls = tls == nil and true or tls
    }, API)
end

-- TODO: make this function "public"
-- TODO: maby check for terminate event
--- Very advanced function that will not allow you to leave a file or http connection open!
---@param block function The
---@param file table Any table that has a close function
---@return any The result from the block
local function with(file, block)
    local success, result = pcall(block, file)
    file:close()
    if not success then error(result) end
    return result
end

--- Converts image from url to NFT image
---@overload fun(params:table): string|nil,string|nil,file|nil
---@overload fun(url:string, size:table<number, number>, dither:boolean): string|nil,string|nil,file|nil
---@param url string The URL of the image to convert
---@param width number|nil The desired width of the output image
---@param height number|nil The desired height of the output image
---@param dither boolean|nil Enables dithering for the image
---@return string|nil,string|nil,file|nil
function API:nft(url, width, height, dither)
    local params = type(url) == "table" and url or { url = url, width = width, height = height, dither = dither }
    if type(params.width) == "table" then
        local size = params.width
        params.dither = params.height
        params.width  = size[1]
        params.height = size[2]
    end

    expect(1, params.url, "string", "table")
    expect(2, params.width, "number", "nil")
    expect(3, params.height, "number", "nil")
    expect(4, params.dither, "boolean", "nil")

    local protool = self.tls and "https" or "http"
    -- TODO: add option to disable urlsafe_b64encode
    -- TODO: add api for adding params
    local url_builder = {protool, "://", self.host, "/api/v1/img/nft?url=", urlsafe_b64encode(params.url), "&urlIsBase64=true"}

    if width then table.insert(url_builder, "&width="..params.width) end
    if height then table.insert(url_builder, "&height="..params.height) end
    if dither then table.insert(url_builder, "&dither="..tostring(params.dither)) end

    local request, err, err_response = http.get(table.concat(url_builder))
    if request then
        return with(request, function()
            return request.readAll()
        end)
    end
    return request, err, err_response
end

-- TODO: WIP
function API:dfpwm(url)
    expect(1, url, "string")
    local protool = self.tls and "https" or "http"
    return protool.."://"..self.host.."/api/v1/audio/dfpwm?url="..urlsafe_b64encode(url).."&urlIsBase64=true"
end

return setmetatable(API, {
    __call = function(cls, ...)
        return cls.new(...)
    end
})
