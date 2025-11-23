# profile_system.py - ENHANCED WITH PROGRESS TRACKING
import os, json
import config 

# Ensure the profiles data directory exists
os.makedirs(config.PROFILE_DATA_PATH, exist_ok=True)
AVAILABLE_AVATARS = [f for f in os.listdir(config.AVATAR_PROFILES_PATH) if f.lower().endswith((".png", ".jpg"))]
AVAILABLE_REWARDS = [f for f in os.listdir(config.REWARDS_CARDS_PATH) if f.endswith((".png", ".jpg"))]

# ==========================================================
# REWARD UNLOCK CRITERIA
# ==========================================================
REWARD_CRITERIA = {
    # Learning Level Completions
    "reward_01.png": {"type": "learning_complete", "level": 1},
    "reward_02.png": {"type": "learning_complete", "level": 2},
    "reward_03.png": {"type": "learning_complete", "level": 3},
    
    # Quiz Perfect Scores (100%)
    "reward_04.png": {"type": "quiz_perfect", "level": 1},
    "reward_05.png": {"type": "quiz_perfect", "level": 2},
    "reward_06.png": {"type": "quiz_perfect", "level": 3},
    
    # Quiz Good Scores (90%+)
    "reward_07.png": {"type": "quiz_good", "level": 1, "min_score": 90},
    "reward_08.png": {"type": "quiz_good", "level": 2, "min_score": 90},
    
    # Multiple Completions
    "reward_09.png": {"type": "all_learning", "levels": [1, 2, 3]},
    "reward_10.png": {"type": "all_quiz", "levels": [1, 2, 3], "min_score": 90},
}

# ==========================================================
# PROFILE DATA STRUCTURE
# ==========================================================
def get_default_profile_data():
    """Return default profile structure with progress tracking"""
    return {
        "name": "",
        "age": "",
        "avatar": AVAILABLE_AVATARS[0] if AVAILABLE_AVATARS else "default.png",
        "rewards": [],
        "progress": {
            "learning": {},  # {1: True, 2: False, ...}
            "quiz": {}       # {1: {"completed": True, "score": 95, "attempts": 2}, ...}
        }
    }

# ==========================================================
# PROFILE DATA MIGRATION & CLEANUP
# ==========================================================
def cleanup_profile_data():
    """Clean up and migrate profile data to new format"""
    import shutil
    
    if not os.path.exists(config.PROFILE_FILE):
        print("No profile file found. Nothing to clean up.")
        return
    
    # Create backup first
    backup_path = config.PROFILE_FILE + ".backup"
    shutil.copy(config.PROFILE_FILE, backup_path)
    print(f"✅ Backup created: {backup_path}")
    
    try:
        with open(config.PROFILE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        valid_profiles = []
        
        # Handle list format
        if isinstance(data, list):
            for i, profile in enumerate(data):
                if not isinstance(profile, dict):
                    print(f"⚠️ Skipping invalid profile at index {i}: {type(profile)}")
                    continue
                
                # Ensure required fields
                if "name" not in profile or not profile["name"]:
                    print(f"⚠️ Skipping profile without name at index {i}")
                    continue
                
                # Add default values if missing
                if "avatar" not in profile or not profile["avatar"]:
                    profile["avatar"] = AVAILABLE_AVATARS[0] if AVAILABLE_AVATARS else "default.png"
                
                if "age" not in profile:
                    profile["age"] = ""
                
                if "rewards" not in profile:
                    profile["rewards"] = []
                
                if "progress" not in profile:
                    profile["progress"] = {"learning": {}, "quiz": {}}
                
                valid_profiles.append(profile)
        
        # Handle dict format (old format)
        elif isinstance(data, dict):
            for key, profile in data.items():
                if not isinstance(profile, dict):
                    print(f"⚠️ Skipping invalid profile for key '{key}': {type(profile)}")
                    continue
                
                # Ensure name field
                if "name" not in profile:
                    profile["name"] = key
                
                # Add defaults
                if "avatar" not in profile or not profile["avatar"]:
                    profile["avatar"] = AVAILABLE_AVATARS[0] if AVAILABLE_AVATARS else "default.png"
                
                if "age" not in profile:
                    profile["age"] = ""
                
                if "rewards" not in profile:
                    profile["rewards"] = []
                
                if "progress" not in profile:
                    profile["progress"] = {"learning": {}, "quiz": {}}
                
                valid_profiles.append(profile)
        
        # Save cleaned profiles
        if valid_profiles:
            save_profiles(valid_profiles)
            print(f"✅ Cleaned and saved {len(valid_profiles)} profile(s)")
        else:
            print("⚠️ No valid profiles found. Starting with empty profile list.")
            save_profiles([])
        
        return valid_profiles
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return None


# ==========================================================
# LOAD/SAVE PROFILES
# ==========================================================
def load_profiles():
    if os.path.exists(config.PROFILE_FILE):
        with open(config.PROFILE_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    # Ensure all profiles have progress structure
                    valid_profiles = []
                    for profile in data:
                        # Skip invalid profiles (non-dict entries)
                        if not isinstance(profile, dict):
                            print(f"⚠️ Skipping invalid profile entry: {profile}")
                            continue
                        
                        # Ensure progress structure exists
                        if "progress" not in profile:
                            profile["progress"] = {"learning": {}, "quiz": {}}
                        
                        valid_profiles.append(profile)
                    return valid_profiles
                    
                elif isinstance(data, dict):
                    # Convert old format to list
                    valid_profiles = []
                    for key, profile in data.items():
                        # Skip invalid profiles
                        if not isinstance(profile, dict):
                            print(f"⚠️ Skipping invalid profile entry for key {key}: {profile}")
                            continue
                        
                        # Ensure progress structure exists
                        if "progress" not in profile:
                            profile["progress"] = {"learning": {}, "quiz": {}}
                        
                        valid_profiles.append(profile)
                    return valid_profiles
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error loading profiles.json: {e}")
                print("Creating backup and starting fresh...")
                # Backup corrupted file
                if os.path.exists(config.PROFILE_FILE):
                    backup_path = config.PROFILE_FILE + ".backup"
                    import shutil
                    shutil.copy(config.PROFILE_FILE, backup_path)
                    print(f"Backup saved to: {backup_path}")
    return []


def save_profiles(profiles):
    with open(config.PROFILE_FILE, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4, ensure_ascii=False)


# ==========================================================
# CREATE/DELETE PROFILE
# ==========================================================
def create_profile(name, age, avatar):
    profiles = load_profiles()
    # Check for duplicates
    for p in profiles:
        if p.get("name") == name:
            print(f"⚠️ Profile with name '{name}' already exists.")
            return p

    new_profile = get_default_profile_data()
    new_profile.update({"name": name, "age": age, "avatar": avatar})
    profiles.append(new_profile)
    save_profiles(profiles)
    return new_profile


def delete_profile(name):
    profiles = load_profiles()
    new_profiles = [p for p in profiles if p.get("name") != name]
    save_profiles(new_profiles)

# ==========================================================
# PROGRESS TRACKING
# ==========================================================
def mark_learning_complete(profile_name, level):
    """Mark a learning level as completed"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            if "progress" not in p:
                p["progress"] = {"learning": {}, "quiz": {}}
            p["progress"]["learning"][str(level)] = True
            print(f"✅ {profile_name} completed Learning Level {level}")
            
            # Check for reward unlocks
            check_and_unlock_rewards(p)
            break
    save_profiles(profiles)


def mark_quiz_complete(profile_name, level, score, total_questions):
    """Mark a quiz level as completed with score"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            if "progress" not in p:
                p["progress"] = {"learning": {}, "quiz": {}}
            
            level_str = str(level)
            score_percent = int((score / total_questions) * 100) if total_questions > 0 else 0
            
            # Update or create quiz progress
            if level_str not in p["progress"]["quiz"]:
                p["progress"]["quiz"][level_str] = {
                    "completed": True,
                    "best_score": score_percent,
                    "attempts": 1,
                    "last_score": score_percent
                }
            else:
                quiz_data = p["progress"]["quiz"][level_str]
                quiz_data["attempts"] = quiz_data.get("attempts", 0) + 1
                quiz_data["last_score"] = score_percent
                quiz_data["completed"] = True
                # Update best score if improved
                if score_percent > quiz_data.get("best_score", 0):
                    quiz_data["best_score"] = score_percent
            
            print(f"✅ {profile_name} completed Quiz Level {level} - Score: {score_percent}%")
            
            # Check for reward unlocks
            check_and_unlock_rewards(p)
            break
    save_profiles(profiles)


# ==========================================================
# ACCESS CONTROL
# ==========================================================
def is_quiz_unlocked(profile_name, quiz_level):
    """Check if a quiz level is unlocked (requires matching learning level complete)"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            return learning.get(str(quiz_level), False)
    return False


def is_learning_unlocked(profile_name, learning_level):
    """Check if a learning level is unlocked"""
    # Level 1 is always unlocked
    if learning_level == 1:
        return True
    
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            quiz = progress.get("quiz", {})
            
            # Previous level quiz must be completed with 90%+
            prev_level = str(learning_level - 1)
            if prev_level in quiz:
                quiz_data = quiz[prev_level]
                return quiz_data.get("best_score", 0) >= 90
            return False
    return False


def get_unlock_status(profile_name):
    """Get complete unlock status for all levels"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            return {
                "learning": {
                    1: True,  # Always unlocked
                    2: is_learning_unlocked(profile_name, 2),
                    3: is_learning_unlocked(profile_name, 3),
                },
                "quiz": {
                    1: is_quiz_unlocked(profile_name, 1),
                    2: is_quiz_unlocked(profile_name, 2),
                    3: is_quiz_unlocked(profile_name, 3),
                }
            }
    return {"learning": {1: True, 2: False, 3: False}, "quiz": {1: False, 2: False, 3: False}}


# ==========================================================
# REWARDS SYSTEM
# ==========================================================
def check_and_unlock_rewards(profile):
    """Check all reward criteria and unlock eligible rewards"""
    newly_unlocked = []
    current_rewards = set(profile.get("rewards", []))
    progress = profile.get("progress", {})
    learning = progress.get("learning", {})
    quiz = progress.get("quiz", {})
    
    for reward_file, criteria in REWARD_CRITERIA.items():
        # Skip if already unlocked
        if reward_file in current_rewards:
            continue
        
        # Check criteria
        unlocked = False
        
        if criteria["type"] == "learning_complete":
            level = str(criteria["level"])
            unlocked = learning.get(level, False)
        
        elif criteria["type"] == "quiz_perfect":
            level = str(criteria["level"])
            if level in quiz:
                unlocked = quiz[level].get("best_score", 0) == 100
        
        elif criteria["type"] == "quiz_good":
            level = str(criteria["level"])
            min_score = criteria.get("min_score", 90)
            if level in quiz:
                unlocked = quiz[level].get("best_score", 0) >= min_score
        
        elif criteria["type"] == "all_learning":
            required_levels = [str(l) for l in criteria.get("levels", [])]
            unlocked = all(learning.get(l, False) for l in required_levels)
        
        elif criteria["type"] == "all_quiz":
            required_levels = [str(l) for l in criteria.get("levels", [])]
            min_score = criteria.get("min_score", 90)
            unlocked = all(
                quiz.get(l, {}).get("best_score", 0) >= min_score 
                for l in required_levels
            )
        
        # Unlock reward if criteria met
        if unlocked:
            newly_unlocked.append(reward_file)
            current_rewards.add(reward_file)
    
    # Update profile with new rewards
    if newly_unlocked:
        profile["rewards"] = list(current_rewards)
        print(f"🎉 Unlocked {len(newly_unlocked)} new reward(s): {', '.join(newly_unlocked)}")
    
    return newly_unlocked


def unlock_reward(profile_name, reward_filename):
    """Manually unlock a specific reward"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            rewards = set(p.get("rewards", []))
            if reward_filename not in rewards:
                rewards.add(reward_filename)
                p["rewards"] = list(rewards)
                print(f"🏅 Unlocked reward: {reward_filename}")
            break
    save_profiles(profiles)


def get_unlocked_rewards(profile_name):
    """Return a list of unlocked rewards for a given user."""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            return p.get("rewards", [])
    return []


# ==========================================================
# PROGRESS SUMMARY
# ==========================================================
def get_progress_summary(profile_name):
    """Get detailed progress summary for a profile"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            quiz = progress.get("quiz", {})
            
            summary = {
                "learning_completed": [int(k) for k, v in learning.items() if v],
                "quiz_completed": [int(k) for k, v in quiz.items() if v.get("completed")],
                "quiz_scores": {int(k): v.get("best_score", 0) for k, v in quiz.items()},
                "total_rewards": len(p.get("rewards", [])),
                "total_attempts": sum(v.get("attempts", 0) for v in quiz.values()),
                "unlock_status": get_unlock_status(profile_name)
            }
            return summary
    
    return {
        "learning_completed": [],
        "quiz_completed": [],
        "quiz_scores": {},
        "total_rewards": 0,
        "total_attempts": 0,
        "unlock_status": {"learning": {1: True, 2: False, 3: False}, "quiz": {1: False, 2: False, 3: False}}
    }
