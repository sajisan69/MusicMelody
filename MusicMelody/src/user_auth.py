import json
import os

class UserAuth:
    def __init__(self):
        # Locate the data/users.json file relative to this script
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.users_file = os.path.join(self.base_dir, "data", "users.json")

        self._ensure_file()
        self.users = self._load_users()

    def _ensure_file(self):
        if not os.path.exists(self.users_file):
            # Make sure the 'data' folder exists too
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, 'w') as f:
                json.dump({}, f)

    def _load_users(self):
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    def _save_users(self):
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=4)
        except Exception as e:
            print(f"Error saving users: {e}")

    def login(self, username, password):
        if username in self.users:
            if self.users[username] == password:
                return True, "Login Successful"
            else:
                return False, "Incorrect Password"
        return False, "User not found"

    def signup(self, username, password):
        if username in self.users:
            return False, "User already exists"
        if not username or not password:
            return False, "Username/Password cannot be empty"

        self.users[username] = password
        self._save_users()
        return True, "Account created successfully"