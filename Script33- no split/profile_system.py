import os, json
import config 

# Ensure the profiles data directory exists
os.makedirs(config.PROFILE_DATA_PATH, exist_ok=True) # Ensure directory exists at startup
AVAILABLE_AVATARS = [f for f in os.listdir(config.AVATAR_PROFILES_PATH) if f.lower().endswith((".png", ".jpg"))]
AVAILABLE_REWARDS = [f for f in os.listdir(config.REWARDS_CARDS_PATH) if f.endswith((".png", ".jpg"))]


def load_profiles():
    if os.path.exists(config.PROFILE_FILE):
        with open(config.PROFILE_FILE, "r", encoding="utf-8") as f:
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
    with open(config.PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4, ensure_ascii=False)


def create_profile(name, age, avatar):
    profiles = load_profiles()
    # Check for duplicates
    for p in profiles:
        if p.get("name") == name:
            print(f"⚠️ Profile with name '{name}' already exists.")
            return p

    new_profile = {"name": name, "age": age, "avatar": avatar, "rewards": []}
    profiles.append(new_profile)
    save_profiles(profiles)
    return new_profile


def delete_profile(name):
    profiles = load_profiles()
    new_profiles = [p for p in profiles if p.get("name") != name]
    save_profiles(new_profiles)

def unlock_reward(profile_name, reward_filename):
    """Mark a reward as unlocked for a specific profile."""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            rewards = set(p.get("rewards", []))
            rewards.add(reward_filename)
            p["rewards"] = list(rewards)
            break
    save_profiles(profiles)


def get_unlocked_rewards(profile_name):
    """Return a list of unlocked rewards for a given user."""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            return p.get("rewards", [])
    return []
