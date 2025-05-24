security_risks = [
{
    "name" : "Partially Offboarded Users",
    "description": "Users who have not been completely removed from all systems post-offboarding",
    "sql":
"""WITH RolesAssociatedUsers AS (
  SELECT DISTINCT trim(value) AS UserID, RoleID, RoleName
  FROM Roles, json_each(Roles.AssociatedUsers)
),
ApplicationsAssociatedUsers AS (
  SELECT DISTINCT trim(value) AS UserID, ApplicationID, ApplicationName
  FROM Applications, json_each(Applications.AssociatedUsers)
),
GroupsAssociatedUsers AS (
  SELECT DISTINCT trim(value) AS UserID, GroupID, GroupName
  FROM Groups, json_each(Groups.AssociatedUsers)
)
SELECT
  RAU.UserID,
  Users.Email,
  Users.Status,
  RAU.RoleID,
  RAU.RoleName,
  NULL AS ApplicationID,
  NULL AS ApplicationName,
  NULL AS GroupID,
  NULL AS GroupName
FROM RolesAssociatedUsers AS RAU
LEFT JOIN Users ON RAU.UserID = Users.UserID
WHERE Users.Status LIKE '%offboarded%'

UNION ALL

SELECT
  AAU.UserID,
  Users.Email,
  Users.Status,
  NULL AS RoleID,
  NULL AS RoleName,
  AAU.ApplicationID,
  AAU.ApplicationName,
  NULL AS GroupID,
  NULL AS GroupName
FROM ApplicationsAssociatedUsers AS AAU
LEFT JOIN Users ON AAU.UserID = Users.UserID
WHERE Users.Status LIKE '%offboarded%'

UNION ALL

SELECT
  GAU.UserID,
  Users.Email,
  Users.Status,
  NULL AS RoleID,
  NULL AS RoleName,
  NULL AS ApplicationID,
  NULL AS ApplicationName,
  GAU.GroupID,
  GAU.GroupName
FROM GroupsAssociatedUsers AS GAU
LEFT JOIN Users ON GAU.UserID = Users.UserID
WHERE Users.Status LIKE '%offboarded%' AND NOT GAU.GroupName LIKE '%offboarded%'
ORDER BY GAU.UserID
"""
},
{
    "name" : "Inactive Users",
    "description": "Users who have not logged in for a significant period (2 months)",
    "sql": "SELECT UserID, Name, Email, LastLogin FROM Users WHERE LastLogin < DATE('now', '-2 months')"
},
{
    "name" : "Never Logged In Users",
    "description": "Users who have never logged into the system after being provisioned",
    "sql": "SELECT UserID, Name, Email, LastLogin FROM Users WHERE LastLogin IS NULL"
},
{
    "name" : "No MFA",
    "description": "Users who do not have MFA enabled",
    "sql": "SELECT UserID, Name, Email, MFAStatus FROM Users WHERE MFAStatus LIKE '%Disabled%' OR MFAStatus IS NULL"
},
{
    "name" : "Weak MFA",
    "description": "Users with MFA methods that are considered weak or less secure",
    "sql": "SELECT UserID, Name, Email, MFAStatus, MFAType FROM Users WHERE MFAStatus LIKE '%enabled%' AND MFAType NOT LIKE '%totp%' AND MFAType NOT LIKE '%security key%'"
},
{
    "name" : "Service Accounts",
    "description": "Non-human accounts used for application or service access",
    "sql": "SELECT UserID, Name, Email, Position FROM Users WHERE Position LIKE '%Service Account%'"
},
{
    "name" : "Local Accounts",
    "description": "Accounts that are local to a specific system or application, not managed centrally",
    "sql":
"""
WITH ApplicationsAssociatedUsers AS (
  SELECT DISTINCT trim(value) AS UserID, ApplicationID, ApplicationName
  FROM Applications, json_each(Applications.AssociatedUsers)
)
SELECT
  AAU.UserID,
  Users.Email,
  Users.Status,
  AAU.ApplicationID,
  AAU.ApplicationName
FROM ApplicationsAssociatedUsers AS AAU
LEFT JOIN Users ON AAU.UserID = Users.UserID
WHERE Users.UserID IS NULL
"""
},
{
    "name" : "Recently Joined Users",
    "description": "Users who have recently joined and may require additional monitoring (3 months)",
    "sql": "SELECT UserID, Name, Email, EmploymentStartDate FROM Users WHERE EmploymentStartDate > DATE('now', '-3 months')"
}
]