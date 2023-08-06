


local BasePlugin = require("kong.plugins.base_plugin")
local ExampleHandler = BasePlugin:extend()
local kong = kong


function ExampleHandler:access(config)
    ExampleHandler.super.access(self)
-- add process logic below

-- add process logic above
end


return ExampleHandler
