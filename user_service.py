class UserService:
    def __init__(self):
        self.users = []

    def add_user(self, name, email):
        if not name:
            return False

        if not email:
            return False

        user = {
            "name": name,
            "email": email,
            "active": True
        }

        self.users.append(user)
        return True

    def deactivate_user(self, email):
        for user in self.users:
            if user["email"] == email:
                user["active"] = False
                return True

        return False

    def get_active_users(self):
        active_users = []

        for user in self.users:
            if user["active"]:
                active_users.append(user)

        return active_users