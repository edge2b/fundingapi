#!/usr/bin/env tarantool
uuid = require('uuid');

box.cfg {
    listen = '0.0.0.0:3333'
}

box.once('init', function()
    box.schema.user.grant('guest', 'read,write,execute', 'universe')

    local mapping_space = box.schema.create_space('mapping')
    mapping_space:format({
        {name='resource_id', type='unsigned'},
        {name='client_address', type='string'},
        {name='private_key', type='string'},
        {name='funding_address', type='string'},
        {name='uuid', type='string'},
        {name='created_at',  type='unsigned'},
        {name='recheck_at',  type='unsigned'},
        {name='expired_at',  type='unsigned'},
        {name='tx',  type='string'},
    })

    mapping_space:create_index('primary', {type = 'tree', parts = {1, 'unsigned'}})
    -- mapping_space:create_index('active',  {type = 'tree', unique = false, parts = {2, 'unsigned', 4, 'str'}})
    -- mapping_space:create_index('address', {type = 'tree', unique = false, parts = {2, 'unsigned', 7, 'str'}})
    -- mapping_space:create_index('unique',  {type = 'tree', unique = true,  parts = {5, 'str', 7, 'str'}})
    -- mapping_space:create_index('resource',{type = 'tree', unique = false, parts = {2, 'unsigned'}})
    -- mapping_space:create_index('uuid',    {type = 'hash', parts = {8, 'str'}})
    mapping_space:create_index('expired', { type = 'tree', unique = false, parts={9, 'unsigned'}})
    -- mapping_space:create_index('address', {type = 'tree', unique = false, parts = {2, 'unsigned', 7, 'str'}})
    mapping_space:create_index('unique',  {type = 'tree', unique = true,  parts = {3, 'str', 5, 'str'}})
    -- mapping_space:create_index('resource',{type = 'tree', unique = false, parts = {2, 'unsigned'}})
    mapping_space:create_index('uuid',    {type = 'hash', parts = {6, 'str'}})

    local resource_space = box.schema.create_space('resource')
    resource_space:create_index('primary',  {type = 'tree', parts = {1, 'unsigned'}})
    resource_space:create_index('uuid',     {type = 'hash', parts = {2, 'str'}})
    resource_space:create_index('name',     {type = 'tree', unique = true, parts = {3, 'str'}})
    resource_space:format({
        {name='id', type='unsigned'},
        {name='uuid', type='string'},
        {name='name', type='string'},
        {name='description', type='string'},
        {name='contract_address', type='string'},
        {name='network_name', type='string'},
        {name='active', type='bool'},
    })
end)


box.once("db_version:0.1", function()
    local account_space = box.schema.create_space('account')
    account_space:create_index('primary',  {type = 'tree', parts = {1, 'unsigned'}})
    account_space:create_index('uuid',     {type = 'hash', parts = {3, 'str'}})
    account_space:create_index('address',  {type = 'tree', unique = true, parts = {4, 'str'}})
    account_space:create_index('email',    {type = 'tree', unique = true, parts = {5, 'str'}})
    account_space:format({
        {name='id',     type='unsigned'},
        {name='resource_id', type='unsigned'},
        {name='uuid',   type='string'},
        {name='address',type='string'},
        {name='email',  type='string'},
        {name='name',   type='string'},
        {name='created_at',  type='unsigned'},
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


function get_account(account_uuid)
    local result = box.space.account.index.uuid:select(client_uuid)
    if #result > 0 then
        return ({
            ["uuid"]=result[1][3],
            ["resource"]=get_resource(result[1][2]),
        })
    end
end


function get_account_by_email(email)
    local result = box.space.account.index.email:select(email)
    if #result > 0 then
        return ({
            ["uuid"]=result[1][3],
            ["resource"]=get_resource(result[1][2]),
        })
    end
end


function register_resource(name, description, contract_address, network_name)
    print("Create resource", name, description, contract_address, network_name)
    local resource_uuid = uuid.str()
    local result = box.space.resource.index.name:select({name})
    if #result > 0 then
        return result[1]
    end
    if network_name ~= 'ropsten' and network_name ~= 'mainnet' and network_name ~= 'rinkeby' and network_name ~= 'kovan' then
        return error("wrong network_name")
    end
    return box.space.resource:auto_increment({resource_uuid, name, description, contract_address, network_name, t})
end


function get_resource( resource_id )
    local resource = box.space.resource.index.primary:select({resource_id})[1]
    return {
        ["uuid"]=resource[2],
        ["name"]=resource[3],
        ["description"]=resource[4],
        ["address"]=resource[5],
        ["network_type"]=resource[6],
    }
end


function assign_tx_id(uuid, tx_id)
    mapping_id = box.space.mapping.index.uuid:select(uuid)[1][1]
    box.space.mapping:update(mapping_id, {{'=', 10, tx_id}})
end


function update_recheck(uuid, period)
    mapping = box.space.mapping.index.uuid:select(uuid)[1]
    local created_at = mapping[7]
    local recheck_at = mapping[8]
    box.space.mapping:update(mapping[1], {{'=', 8, created_at + period * (((recheck_at - created_at) / period) + 1)}})
end


function get_mappings()
    local mappings = {}
    local results = box.space.mapping.index.expired:select({os.time()}, {iterator = 'GE'})

    if #results == 0 then
        return {}
    end
    local index = 1
    for i = 1, #results do
        if results[i][8] < os.time() and results[i][10] == nil then
            local resource_id = results[i][2]
            local resource = get_resource(resource_id)
            mappings[index] = {
                ["resource"]=resource,
                ["client_address"]=results[i][3],
                ["private_key"]=results[i][4],
                ["funding_address"]=results[i][5],
                ["uuid"]=results[i][6],
            }
            index = index + 1
        end
    end
    return mappings
end


function register_client(resource_uuid, target_address, private_key, funding_address, expired_at)
    print("Get mapping ETH", resource_uuid, target_address, private_key, funding_address, expired_at)
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
    box.space.mapping:auto_increment({resource_id, target_address, private_key, funding_address, client_uuid, os.time(), os.time(), expired_at, nil})
    return get_client(client_uuid)
end


function create_account(resource_uuid, target_address, email, name)
    print("Create account", resource_uuid, target_address, email, name)
    local result = box.space.resource.index.uuid:select({resource_uuid})

    if #result == 0 then
        return
    end

    local resource_id = result[1][1]
    local client_uuid = uuid.str()

    result = get_account_by_email(email)

    if result then
        return result
    end

    box.space.account:auto_increment({resource_id, client_uuid, target_address, email, name, os.time()})
    return get_account(client_uuid)
end
