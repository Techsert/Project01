# profile_system.py - FIXED WITH CORRECT UNLOCKING LOGIC
import os, json
import config 

# Ensure the profiles data directory exists
os.makedirs(config.PROFILE_DATA_PATH, exist_ok=True)
AVAILABLE_AVATARS = [f for f in os.listdir(config.AVATAR_PROFILES_PATH) if f.lower().endswith((".png", ".jpg"))]
AVAILABLE_REWARDS = [f for f in os.listdir(config.REWARDS_CARDS_PATH) if f.endswith((".png", ".jpg"))]

# ==========================================================
# LEARNING STRUCTURE DEFINITION
# ==========================================================
LEARNING_STRUCTURE = {
    1: ["T1", "T2", "T3"],  # Level 1 has 3 topics
    2: ["T1", "T2", "T3"],  # Level 2 has 3 topics
    3: ["T1", "T2", "T3"],  # Level 3 has 3 topics (add more as needed)
}

# ==========================================================
# REWARD UNLOCK CRITERIA
# ==========================================================
REWARD_CRITERIA = {
    # Learning Level Completions (completing ALL topics in a level)
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
            "learning": {},  # {"1": {"T1": True, "T2": True, "T3": False}, "2": {...}}
            "quiz": {}       # {"1": {"completed": True, "score": 95, "attempts": 2}, ...}
        }
    }

# ==========================================================
# LOAD/SAVE PROFILES
# ==========================================================
def load_profiles():
    if os.path.exists(config.PROFILE_FILE):
        with open(config.PROFILE_FILE, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    valid_profiles = []
                    for profile in data:
                        if not isinstance(profile, dict):
                            print(f"⚠️ Skipping invalid profile entry: {profile}")
                            continue
                        
                        # Ensure progress structure exists with new format
                        if "progress" not in profile:
                            profile["progress"] = {"learning": {}, "quiz": {}}
                        
                        # Migrate old format to new format if needed
                        if profile["progress"]["learning"] and not isinstance(list(profile["progress"]["learning"].values())[0], dict):
                            # Old format detected, migrate
                            old_learning = profile["progress"]["learning"]
                            new_learning = {}
                            for level_str, completed in old_learning.items():
                                if completed:
                                    # Assume all topics completed for old migrated data
                                    topics = LEARNING_STRUCTURE.get(int(level_str), ["T1"])
                                    new_learning[level_str] = {t: True for t in topics}
                                else:
                                    new_learning[level_str] = {}
                            profile["progress"]["learning"] = new_learning
                        
                        valid_profiles.append(profile)
                    return valid_profiles
                    
                elif isinstance(data, dict):
                    valid_profiles = []
                    for key, profile in data.items():
                        if not isinstance(profile, dict):
                            print(f"⚠️ Skipping invalid profile entry for key {key}: {profile}")
                            continue
                        
                        if "progress" not in profile:
                            profile["progress"] = {"learning": {}, "quiz": {}}
                        
                        valid_profiles.append(profile)
                    return valid_profiles
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error loading profiles.json: {e}")
                print("Creating backup and starting fresh...")
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
# PROGRESS TRACKING - TOPIC-BASED
# ==========================================================
def mark_learning_topic_complete(profile_name, level, topic):
    """
    Mark a specific learning topic as completed.
    
    Args:
        profile_name: Name of the profile
        level: Learning level (1, 2, 3, etc.)
        topic: Topic identifier (T1, T2, T3, etc.)
    """
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            if "progress" not in p:
                p["progress"] = {"learning": {}, "quiz": {}}
            
            level_str = str(level)
            
            # Initialize level structure if not exists
            if level_str not in p["progress"]["learning"]:
                p["progress"]["learning"][level_str] = {}
            
            # Mark topic as complete
            p["progress"]["learning"][level_str][topic] = True
            print(f"✅ {profile_name} completed Learning Level {level} - Topic {topic}")
            
            # Check for reward unlocks
            check_and_unlock_rewards(p)
            break
    save_profiles(profiles)


def is_learning_level_complete(profile_name, level):
    """Check if ALL topics in a learning level are completed."""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            level_str = str(level)
            
            if level_str not in learning:
                return False
            
            # Get all required topics for this level
            required_topics = LEARNING_STRUCTURE.get(level, ["T1"])
            completed_topics = learning[level_str]
            
            # Check if all topics are completed
            return all(completed_topics.get(t, False) for t in required_topics)
    
    return False


def get_next_topic(profile_name, level):
    """
    Get the next topic to unlock for a given level.
    Returns None if all topics are completed or level not started.
    """
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            level_str = str(level)
            
            if level_str not in learning:
                return "T1"  # First topic if level not started
            
            completed_topics = learning[level_str]
            required_topics = LEARNING_STRUCTURE.get(level, ["T1"])
            
            # Find first incomplete topic
            for topic in required_topics:
                if not completed_topics.get(topic, False):
                    return topic
            
            return None  # All topics completed
    
    return "T1"  # Default to first topic


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
def is_topic_unlocked(profile_name, level, topic):
    """
    Check if a specific topic is unlocked.
    
    Logic:
    - Level 1, Topic T1 is always unlocked
    - Any topic requires previous topic in same level to be completed
    - Level 2+ Topic T1 requires previous level's quiz with 90%+
    """
    # Level 1, Topic 1 is always unlocked (entry point)
    if level == 1 and topic == "T1":
        return True
    
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            quiz = progress.get("quiz", {})
            
            level_str = str(level)
            topics = LEARNING_STRUCTURE.get(level, ["T1"])
            
            # For T1 of level 2+, check if previous level's quiz passed
            if topic == "T1" and level > 1:
                prev_level = str(level - 1)
                if prev_level in quiz:
                    return quiz[prev_level].get("best_score", 0) >= 90
                return False
            
            # For other topics, check if previous topic completed
            if level_str not in learning:
                return False
            
            completed = learning[level_str]
            topic_index = topics.index(topic) if topic in topics else -1
            
            if topic_index <= 0:
                return True  # First topic (already handled above)
            
            # Check if previous topic is completed
            prev_topic = topics[topic_index - 1]
            return completed.get(prev_topic, False)
    
    return False


def is_quiz_unlocked(profile_name, quiz_level):
    """
    Check if a quiz level is unlocked.
    Requires ALL topics of the same learning level to be completed.
    """
    return is_learning_level_complete(profile_name, quiz_level)


def get_unlock_status(profile_name):
    """Get complete unlock status for all levels and topics"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            
            # Build learning unlock status for each topic
            learning_status = {}
            for level in [1, 2, 3]:
                topics = LEARNING_STRUCTURE.get(level, ["T1"])
                level_status = {}
                for topic in topics:
                    level_status[topic] = is_topic_unlocked(profile_name, level, topic)
                learning_status[level] = level_status
            
            # Build quiz unlock status
            quiz_status = {
                1: is_quiz_unlocked(profile_name, 1),
                2: is_quiz_unlocked(profile_name, 2),
                3: is_quiz_unlocked(profile_name, 3),
            }
            
            return {
                "learning": learning_status,
                "quiz": quiz_status
            }
    
    # Default: only Level 1 Topic 1 unlocked
    return {
        "learning": {
            1: {"T1": True, "T2": False, "T3": False},
            2: {"T1": False, "T2": False, "T3": False},
            3: {"T1": False, "T2": False, "T3": False}
        },
        "quiz": {1: False, 2: False, 3: False}
    }


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
        if reward_file in current_rewards:
            continue
        
        unlocked = False
        
        if criteria["type"] == "learning_complete":
            level = criteria["level"]
            # Check if all topics in level are completed
            unlocked = is_learning_level_complete(profile.get("name"), level)
        
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
            required_levels = criteria.get("levels", [])
            unlocked = all(is_learning_level_complete(profile.get("name"), l) for l in required_levels)
        
        elif criteria["type"] == "all_quiz":
            required_levels = [str(l) for l in criteria.get("levels", [])]
            min_score = criteria.get("min_score", 90)
            unlocked = all(
                quiz.get(l, {}).get("best_score", 0) >= min_score 
                for l in required_levels
            )
        
        if unlocked:
            newly_unlocked.append(reward_file)
            current_rewards.add(reward_file)
    
    if newly_unlocked:
        profile["rewards"] = list(current_rewards)
        print(f"🎉 Unlocked {len(newly_unlocked)} new reward(s): {', '.join(newly_unlocked)}")
    
    return newly_unlocked


def get_progress_summary(profile_name):
    """Get detailed progress summary for a profile"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            quiz = progress.get("quiz", {})
            
            # Get completed learning levels (all topics done)
            learning_completed = []
            for level in [1, 2, 3]:
                if is_learning_level_complete(profile_name, level):
                    learning_completed.append(level)
            
            summary = {
                "learning_completed": learning_completed,
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
        "unlock_status": get_unlock_status(profile_name)
    }
