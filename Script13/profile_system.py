import os, json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_DIR = os.path.join(BASE_DIR, "../assets/profiles/data")
AVATAR_DIR = os.path.join(BASE_DIR, "../assets/profiles/avatars")
PROFILES_FILE = os.path.join(PROFILES_DIR, "profiles.json")

AVAILABLE_AVATARS = ["avatar1.png", "avatar2.png", "avatar3.png", "avatar4.png"]


def load_profiles():
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict):
                    # convert old format to list
                    return list(data.values())
            except json.JSONDecodeError:
                pass
    return []


def save_profiles(profiles):
    with open(PROFILES_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4, ensure_ascii=False)


def create_profile(name, age, avatar):
    profiles = load_profiles()
    # Check for duplicates
    for p in profiles:
        if p.get("name") == name:
            print(f"⚠️ Profile with name '{name}' already exists.")
            return p

    new_profile = {"name": name, "age": age, "avatar": avatar}
    profiles.append(new_profile)
    save_profiles(profiles)
    return new_profile


def delete_profile(name):
    profiles = load_profiles()
    new_profiles = [p for p in profiles if p.get("name") != name]
    save_profiles(new_profiles)
