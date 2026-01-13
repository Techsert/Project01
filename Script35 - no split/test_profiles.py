from profile_system import *

# Create new profiles
create_profile("Ahmed", 8, "avatar2.png")
create_profile("Sara", 10, "avatar1.png")

# Edit a profile
edit_profile("Ahmed", new_age=9, new_avatar="avatar3.png")

# List all profiles
print("Profiles:", list_profiles())

# Get a specific profile
print("Ahmed:", get_profile("Ahmed"))

# Delete a profile
delete_profile("Sara")
