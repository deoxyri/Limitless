def var_holder_return_function(data, joints_description):
    from operator import attrgetter
    var_holder = {}

    for skeleton in data.skeletons:
        i = 0
        while i < len(joints_description):
            var_holder['data_' + joints_description[i]] = attrgetter('{}.projection'.format(joints_description[i]))(
                skeleton)
            i += 1

            locals().update(var_holder)

    return var_holder
