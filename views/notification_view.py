def show_notifications(notifications):
    print("\nYOUR NOTIFICATIONS")
    if not notifications:
        print("No notifications.")
        return

    for n in notifications:
        print(f"[{n.created_at}] {n.message}")