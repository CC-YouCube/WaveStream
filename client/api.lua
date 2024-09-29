local expect = require "cc.expect"

--- Converts a character to its hexadecimal representation for URL encoding
---@param char string The character to convert
---@return string The hexadecimal representation of the character, prefixed with '%'
local function char_to_hex(char)
    return string.format("%%%02X", string.byte(char))
end

-- TODO: maybe make this function "public"
--- Encode url hopefully according to RFC 3986
---@param url string The URL to encode
---@return string The URL-encoded version of the input string
local function url_encode(url)
    expect(1, url, "string")
    return (url:gsub("([^%w%-%.%_%~])", char_to_hex):gsub(" ", "%%20"))
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

--- Converts image from url to NFT image
---@overload fun(params:table): string
---@overload fun(url:string, size:table, dither:boolean): string
---@param url string The URL of the image to convert
---@param width number|nil The desired width of the output image
---@param height number|nil The desired height of the output image
---@param dither boolean|nil Enables dithering for the image
---@return string The nft image
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
    -- TODO: add option to urlsafe_b64encode
    -- TODO: add api for adding params
    local url_builder = {protool, "://", self.host, "/api/v1/img/nft?url=", url_encode(params.url)}

    if width then table.insert(url_builder, "&width="..params.width) end
    if height then table.insert(url_builder, "&height="..params.height) end
    if dither then table.insert(url_builder, "&dither="..tostring(params.dither)) end

    -- TODO: Error handling
    local request = http.get(table.concat(url_builder))
    local response = request.readAll()
    request.close()
    return response
end

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

return setmetatable(API, {
    __call = function(cls, ...)
        return cls.new(...)
    end
})
