#!/usr/bin/env tarantool
package.path = package.path .. ';/usr/local/lua/tarantool-queue/?.lua'
package.path = package.path .. ';/usr/local/share/lua/5.2/queue/?.lua'

uuid = require('uuid');

box.cfg {
    listen = '0.0.0.0:3333'
}

box.once('init', function()
    box.schema.user.grant('guest', 'read,write,execute', 'universe')

    local mapping_space = box.schema.create_space('mapping')
    mapping_space:create_index('primary', {type = 'tree', parts = {1, 'unsigned'}})
    mapping_space:create_index('address', {type = 'tree', unique = false, parts = {2, 'unsigned', 5, 'str'}})
    mapping_space:create_index('unique',  {type = 'tree', unique = true,  parts = {3, 'str', 5, 'str'}})
    mapping_space:create_index('resource',{type = 'tree', unique = false, parts = {2, 'unsigned'}})
    mapping_space:create_index('uuid',    {type = 'hash', parts = {6, 'str'}})
    mapping_space:format({
        {name='id', type='unsigned'},
        {name='resource_id', type='unsigned'},
        {name='client_address', type='string'},
        {name='private_key', type='string'},
        {name='funding_address', type='string'},
        {name='uuid', type='string'},
    })

    local resource_space = box.schema.create_space('resource')
    resource_space:create_index('primary',  {type = 'tree', parts = {1, 'unsigned'}})
    resource_space:create_index('uuid',     {type = 'hash', parts = {2, 'str'}})
    resource_space:create_index('name',     {type = 'tree', unique = true, parts = {3, 'str'}})
    resource_space:format({
        {name='id', type='unsigned'},
        {name='uuid', type='string'},
        {name='name', type='string'},
        {name='description', type='string'},
        {name='active', type='bool'},
    })
end)


function get_client(client_uuid)
    local result = box.space.mapping.index.uuid:select({client_uuid})
    if #result > 0 then
        return ({
            ["client_address"]=result[1][3],
            ["funding_address"]=result[1][5],
            ["uuid"]=result[1][6],
        })
    end
end

function get_client_by_addresses(target_address, funding_address)
    local result = box.space.mapping.index.unique:select({target_address, funding_address})
    if #result > 0 then
        return ({
            ["client_address"]=result[1][3],
            ["funding_address"]=result[1][5],
            ["uuid"]=result[1][6],
        })
    end
end

function register_resource(name, description)
    local resource_uuid = uuid.str()
    local result = box.space.resource.index.name:select({name})
    if #result > 0 then
        return result[1]
    end
    return box.space.resource:auto_increment({resource_uuid, name, description, t})
end


function register_client(resource_uuid, target_address, private_key, funding_address)
    local result = box.space.resource.index.uuid:select({resource_uuid})
    if #result == 0 then
        return
    end
    local resource_id = result[1][1]
    local client_uuid = uuid.str()

    result = get_client_by_addresses(target_address, funding_address)

    if result then
        return result
    end
    box.space.mapping:auto_increment({resource_id, target_address, private_key, funding_address, client_uuid})
    return get_client(client_uuid)
end
