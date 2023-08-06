local typedefs = require "kong.db.schema.typedefs"

return {
    name = "example",
    fields = {
        {
            consumer = typedefs.no_consumer
        },
        {
            protocols = typedefs.protocols_http
        },
        {
            config = {
                type = "record",
                fields = {
-- add config fileds below

-- add config fields above
                },
            },
        },
    },
}


