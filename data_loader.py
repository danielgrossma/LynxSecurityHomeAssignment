import json
import os
import pandas as pd
import sqlite3

class IAMData:
    def __init__(self, filename="data.json", folder="data"):
        self.data = self._load_data(filename, folder)
        self.check_results = self._perform_integrity_checks()
        self.conn = sqlite3.connect(':memory:')
        self._to_sql()

    def _load_data(self, filename, folder):
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            print(f"file {file_path} not found")

        with open(file_path, 'r') as f:
            return json.load(f)

    def _to_sql(self):
        users = pd.DataFrame(self.data['Users'])
        roles = pd.DataFrame(self.data['Roles'])
        applications = pd.DataFrame(self.data['Applications'])
        groups = pd.DataFrame(self.data['Groups'])
        resources = pd.DataFrame(self.data['Resources'])

        roles['AssociatedUsers'] = roles['AssociatedUsers'].apply(lambda x: json.dumps(x))
        applications['AssociatedUsers'] = applications['AssociatedUsers'].apply(lambda x: json.dumps(x))
        groups['AssociatedUsers'] = groups['AssociatedUsers'].apply(lambda x: json.dumps(x))

        conn = self.conn

        users.astype(str).to_sql('Users', conn, if_exists='replace', index=False)
        roles.astype(str).to_sql('Roles', conn, if_exists='replace', index=False)
        applications.astype(str).to_sql('Applications', conn, if_exists='replace', index=False)
        groups.astype(str).to_sql('Groups', conn, if_exists='replace', index=False)
        resources.astype(str).to_sql('Resources', conn, if_exists='replace', index=False)

    def _perform_integrity_checks(self):
        results = {}

        # Check for required keys
        required_keys = ['Users', 'Roles', 'Applications', 'Groups', 'Resources']
        for key in required_keys:
            results[f"{key} Table Exists"] = key in self.data

        # Check if tables are not empty
        for key in required_keys:
            if key in self.data:
                results[f"{key} Table Not Empty"] = len(self.data[key]) > 0
            else:
                results[f"{key} Table Not Empty"] = False

        # Check for unique IDs
        id_fields = {
            'Users': 'UserID',
            'Roles': 'RoleID',
            'Applications': 'ApplicationID',
            'Groups': 'GroupID',
            'Resources': 'ResourceID'
        }
        for key, id_field in id_fields.items():
            if key in self.data and results[f"{key} Table Not Empty"]:
                ids = [item.get(id_field) for item in self.data[key]]
                results[f"{key} IDs Unique"] = len(ids) == len(set(ids))
            elif key in self.data:  # Table is empty, unique IDs is vacuously true
                results[f"{key} IDs Unique"] = True
            else:
                results[f"{key} IDs Unique"] = False  # Table doesn't exist

        # Check for unique Names (except Users)
        name_fields = {
            'Roles': 'RoleName',
            'Applications': 'ApplicationName',
            'Groups': 'GroupName',
            'Resources': 'ResourceName'
        }
        for key, name_field in name_fields.items():
            if key in self.data and results[f"{key} Table Not Empty"]:
                names = [item.get(name_field) for item in self.data[key]]
                results[f"{key} Names Unique"] = len(names) == len(set(names))
            elif key in self.data:  # Table is empty, unique names is vacuously true
                results[f"{key} Names Unique"] = True
            else:
                results[f"{key} Names Unique"] = False  # Table doesn't exist

        # requirements:

        # 1. Users: At least 20 users with various attributes.
        user_check = len(self.data.get("Users", [])) >= 20
        results["Users Check (at least 20)"] = user_check

        # 2. Roles: At least 5 different roles.
        # This check can be replaced or augmented by the unique name check
        roles_check = len(set([role.get('RoleName', '') for role in self.data.get('Roles', [])])) >= 5
        results["Roles Check (at least 5 different names)"] = roles_check

        # 3. Applications: At least 5 different applications.
        applications_check = len(self.data.get("Applications", [])) >= 5
        results["Applications Check (at least 5)"] = applications_check

        # 4. Groups: At least 3 different groups.
        groups_check = len(self.data.get("Groups", [])) >= 3
        results["Groups Check (at least 3)"] = groups_check

        # 5. Resources: At least 5 different resources.
        resources_check = len(self.data.get("Resources", [])) >= 5
        results["Resources Check (at least 5)"] = resources_check

        return results

    def print_check_results(self):
        print("Data Integrity Check Results:")
        for check, result in self.check_results.items():
            print(f"- {check}: {'PASSED' if result else 'FAILED'}")

    def sql(self, query):
        return pd.read_sql(query, self.conn)