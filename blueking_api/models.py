class Permission(object):
    def __init__(self, permission):
        self.permission = permission
        self.permission_index = self.key_by_permission_name()

    def key_by_permission_name(self):
        result = {}
        for item in self.permission:
            if item['function_code'] not in result:
                result[item['function_code']] = {item['biz_id']}
            else:
                result[item['function_code']].add(item['biz_id'])
        return result

    def can(self, permission_name, biz_id=-1):
        if permission_name not in self.permission_index:
            return False
        elif biz_id not in self.permission_index[permission_name]:
            return False
        return True
