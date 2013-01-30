from support import model, assert_equal

@given('we select all users')
def impl(ctx):
    ctx.users = model('res.users').browse([('login', '!=', 'admin')])

@given('we select admin user')
def impl(ctx):
    ctx.found_item = model('res.users').browse([('login', '=', 'admin')])

@step('we select users below')
def impl(ctx):
    logins = [row['login'] for row in ctx.table]
    ctx.found_items = model('res.users').browse([('login', 'in', logins)])
    assert_equal(len(ctx.found_items), len(logins))

def assign_groups(user, groups):
    group_ids = [g.id for g in groups]
    curr_groups= [g.id for g in user.groups_id]
    user.groups_id = list(set(group_ids + curr_groups))

@step('we assign all groups to the users')
def impl(ctx):
    groups = model('res.groups').browse([])
    for user in ctx.found_items:
        assign_groups(user, groups)

@given(u'we assign to {users} the groups bellow')
def impl(ctx, users):
    # search groups by name and full name
    group_names = [row['group_name'] for row in ctx.table]
    group_names = list(set(group_names))
    group_full_names = [name for name in group_names if '/' in name]
    group_single_names = [name for name in group_names if not '/' in name]
    search_cond = [('name', 'in', group_single_names)]
    # it isn't possible to use the 'in' operator on full_name
    full_name_conds = [('full_name', '=', full_name)
            for full_name in group_full_names]
    for cond in full_name_conds:
        search_cond.insert(0, '|')
        search_cond.append(cond)
    groups = model('res.groups').browse(search_cond)
    assert_equal(len(groups), len(group_names))
    assert users in ('user', 'users')
    if users == "users":
        for user in ctx.found_items:
            assign_groups(user, groups)
    if users == "user":
        assign_groups(ctx.found_item, groups)

@step('we activate the extended view on the users')
def impl(ctx):
    for user in ctx.found_items:
        user.view = 'extended'
