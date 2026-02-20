from user_store import add_user, list_users

add_user("admin", "secret")
add_user("alice", "alicepw")
add_user("bob", "bobpw")

print("Created sample users:", list_users())
