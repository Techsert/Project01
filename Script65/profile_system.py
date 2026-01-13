# profile_system.py - FIXED REWARD SYSTEM WITH SCORE THRESHOLDS
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
    3: ["T1", "T2", "T3"],  # Level 3 has 3 topics
}

# ==========================================================
# ✅ FIXED: REWARD UNLOCK CRITERIA WITH SCORE THRESHOLDS
# ==========================================================
REWARD_CRITERIA = {
    # ===== TOPIC COMPLETION REWARDS =====
    # Level 1 Topics
    "reward_01.png": {"type": "topic_complete", "level": 1, "topic": "T1"},
    "reward_02.png": {"type": "topic_complete", "level": 1, "topic": "T2"},
    "reward_03.png": {"type": "topic_complete", "level": 1, "topic": "T3"},
    
    # Level 2 Topics
    "reward_04.png": {"type": "topic_complete", "level": 2, "topic": "T1"},
    "reward_05.png": {"type": "topic_complete", "level": 2, "topic": "T2"},
    "reward_06.png": {"type": "topic_complete", "level": 2, "topic": "T3"},
    
    # Level 3 Topics
    "reward_07.png": {"type": "topic_complete", "level": 3, "topic": "T1"},
    "reward_08.png": {"type": "topic_complete", "level": 3, "topic": "T2"},
    "reward_09.png": {"type": "topic_complete", "level": 3, "topic": "T3"},
    
    # ===== LEARNING LEVEL COMPLETION REWARDS =====
##    "reward_10.png": {"type": "learning_complete", "level": 1},
##    "reward_11.png": {"type": "learning_complete", "level": 2},
##    "reward_12.png": {"type": "learning_complete", "level": 3},
    
    # ✅ FIXED: QUIZ REWARDS WITH SCORE THRESHOLDS
    # Quiz Level 1 - Good Score (75-99%)
    "reward_13.png": {"type": "quiz_score", "level": 1, "min_score": 75, "max_score": 99},
    
    # Quiz Level 1 - Perfect Score (100%)
    "reward_14.png": {"type": "quiz_score", "level": 1, "min_score": 100, "max_score": 100},
    "reward_15.png": {"type": "quiz_score", "level": 1, "min_score": 100, "max_score": 100},
    
    # Quiz Level 2 - Good Score (75-99%)
    "reward_16.png": {"type": "quiz_score", "level": 2, "min_score": 75, "max_score": 99},
    
    # Quiz Level 2 - Perfect Score (100%)
    "reward_17.png": {"type": "quiz_score", "level": 2, "min_score": 100, "max_score": 100},
    "reward_18.png": {"type": "quiz_score", "level": 2, "min_score": 100, "max_score": 100},
    
    # Quiz Level 3 - Good Score (75-99%)
    "reward_19.png": {"type": "quiz_score", "level": 3, "min_score": 75, "max_score": 99},
    
    # Quiz Level 3 - Perfect Score (100%)
    "reward_20.png": {"type": "quiz_score", "level": 3, "min_score": 100, "max_score": 100},
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
            "learning": {},
            "quiz": {}
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
                            continue
                        
                        if "progress" not in profile:
                            profile["progress"] = {"learning": {}, "quiz": {}}
                        
                        # Migration for old format
                        if profile["progress"]["learning"] and not isinstance(list(profile["progress"]["learning"].values())[0], dict):
                            old_learning = profile["progress"]["learning"]
                            new_learning = {}
                            for level_str, completed in old_learning.items():
                                if completed:
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
                            continue
                        
                        if "progress" not in profile:
                            profile["progress"] = {"learning": {}, "quiz": {}}
                        
                        valid_profiles.append(profile)
                    return valid_profiles
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error loading profiles.json: {e}")
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
def mark_learning_topic_complete(profile_name, level, topic):
    """
    Mark a specific learning topic as completed.
    ✅ FIXED: Immediately check and unlock rewards after marking complete
    """
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            if "progress" not in p:
                p["progress"] = {"learning": {}, "quiz": {}}
            
            level_str = str(level)
            
            if level_str not in p["progress"]["learning"]:
                p["progress"]["learning"][level_str] = {}
            
            p["progress"]["learning"][level_str][topic] = True
            print(f"✅ {profile_name} completed Learning Level {level} - Topic {topic}")
            
            # ✅ Check for rewards immediately (without popup parameter)
            newly_unlocked = check_and_unlock_rewards(p, reward_popup=None)
            
            if newly_unlocked:
                print(f"🎁 Unlocked {len(newly_unlocked)} rewards: {newly_unlocked}")
            
            break
    save_profiles(profiles)

def is_learning_level_complete(profile_name, level):
    """Check if ALL topics in a learning level are completed"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            level_str = str(level)
            
            if level_str not in learning:
                return False
            
            required_topics = LEARNING_STRUCTURE.get(level, ["T1"])
            completed_topics = learning[level_str]
            
            return all(completed_topics.get(t, False) for t in required_topics)
    
    return False


def mark_quiz_complete(profile_name, level, score, total_questions):
    """Mark a quiz level as completed with score"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            if "progress" not in p:
                p["progress"] = {"learning": {}, "quiz": {}}
            
            level_str = str(level)
            score_percent = int((score / total_questions) * 100) if total_questions > 0 else 0
            
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
            check_and_unlock_rewards(p)
            break
    save_profiles(profiles)


# ==========================================================
# ACCESS CONTROL - FIXED
# ==========================================================
def is_topic_unlocked(profile_name, level, topic):
    """
    ✅ FIXED: Check if a specific topic is unlocked
    
    Logic:
    - Level 1, Topic T1 is ALWAYS unlocked
    - Other topics require previous topic in SAME level completed
    - Level 2+ Topic T1 requires previous level's quiz with 90%+
    """
    # ✅ Level 1 Topic 1 is ALWAYS unlocked (entry point)
    if level == 1 and topic == "T1":
        return True
    
    if not profile_name:
        return False
    
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            quiz = progress.get("quiz", {})
            
            level_str = str(level)
            topics = LEARNING_STRUCTURE.get(level, ["T1"])
            
            # ✅ For T1 of level 2+, check if previous level's quiz passed
            if topic == "T1" and level > 1:
                prev_level = str(level - 1)
                if prev_level in quiz:
                    return quiz[prev_level].get("best_score", 0) >= 90
                return False
            
            # ✅ For other topics (T2, T3, etc.), check if previous topic completed
            try:
                topic_index = topics.index(topic)
            except ValueError:
                return False
            
            if topic_index == 0:
                # This is T1, already handled above
                return level == 1
            
            # ✅ Check if previous topic is completed
            prev_topic = topics[topic_index - 1]
            
            # ✅ FIX: If level not started yet, only T1 can be unlocked
            if level_str not in learning:
                return False
            
            completed = learning[level_str]
            return completed.get(prev_topic, False)
    
    return False


def is_quiz_unlocked(profile_name, quiz_level):
    """
    ✅ Check if a quiz level is unlocked
    Requires ALL topics of the same learning level to be completed
    """
    return is_learning_level_complete(profile_name, quiz_level)


def get_unlock_status(profile_name):
    """Get complete unlock status for all levels and topics"""
    if not profile_name:
        return {
            "learning": {
                1: {"T1": True, "T2": False, "T3": False},
                2: {"T1": False, "T2": False, "T3": False},
                3: {"T1": False, "T2": False, "T3": False}
            },
            "quiz": {1: False, 2: False, 3: False}
        }
    
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
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
    
    # Default for new users
    return {
        "learning": {
            1: {"T1": True, "T2": False, "T3": False},
            2: {"T1": False, "T2": False, "T3": False},
            3: {"T1": False, "T2": False, "T3": False}
        },
        "quiz": {1: False, 2: False, 3: False}
    }


# ==========================================================
# ✅ FIXED: REWARDS SYSTEM WITH SCORE-BASED LOGIC
# ==========================================================
def check_and_unlock_rewards(profile, reward_popup=None):
    """
    Check all reward criteria and unlock eligible rewards.
    ✅ FIXED: Properly handles score thresholds for quiz rewards
    
    Args:
        profile: Profile dictionary
        reward_popup: Optional RewardPopup instance to display unlocked rewards
    
    Returns:
        List of newly unlocked reward filenames
    """
    newly_unlocked = []
    current_rewards = set(profile.get("rewards", []))
    
    # ✅ CRITICAL FIX: Track rewards BEFORE checking
    rewards_before_check = current_rewards.copy()
    
    progress = profile.get("progress", {})
    learning = progress.get("learning", {})
    quiz = progress.get("quiz", {})
    
    print(f"🔍 Checking rewards for {profile.get('name', 'Unknown')}")
    print(f"   Rewards before check: {len(rewards_before_check)}")
    print(f"   Learning progress: {learning}")
    print(f"   Quiz progress: {quiz}")
    
    for reward_file, criteria in REWARD_CRITERIA.items():
        # ✅ Skip if reward was ALREADY unlocked before this check
        if reward_file in rewards_before_check:
            continue
        
        unlocked = False
        
        # ✅ Individual topic completion
        if criteria["type"] == "topic_complete":
            level = str(criteria["level"])
            topic = criteria["topic"]
            if level in learning:
                unlocked = learning[level].get(topic, False)
                if unlocked:
                    print(f"   ✅ Unlocking {reward_file}: Completed Level {level} - {topic}")
        
        # ✅ Learning level completion
        elif criteria["type"] == "learning_complete":
            level = criteria["level"]
            unlocked = is_learning_level_complete(profile.get("name"), level)
            if unlocked:
                print(f"   ✅ Unlocking {reward_file}: Learning Level {level} complete")
        
        # ✅ FIXED: Quiz score-based rewards with min/max thresholds
        elif criteria["type"] == "quiz_score":
            level = str(criteria["level"])
            min_score = criteria.get("min_score", 0)
            max_score = criteria.get("max_score", 100)
            
            if level in quiz:
                best_score = quiz[level].get("best_score", 0)
                
                # ✅ Check if score falls within the reward's range
                if min_score <= best_score <= max_score:
                    unlocked = True
                    print(f"   ✅ Unlocking {reward_file}: Quiz Level {level} score {best_score}% (range {min_score}-{max_score}%)")
        
        # ✅ If unlocked AND wasn't in the list before, add it
        if unlocked:
            newly_unlocked.append(reward_file)
            current_rewards.add(reward_file)
            
            # ✅ Only add to popup if this is a BRAND NEW unlock
            if reward_popup:
                reward_popup.add_reward(reward_file)
                print(f"   🎁 Added {reward_file} to reward popup")
    
    if newly_unlocked:
        profile["rewards"] = list(current_rewards)
        print(f"🎉 Unlocked {len(newly_unlocked)} new reward(s): {', '.join(newly_unlocked)}")
    else:
        print(f"   No new rewards unlocked this session")
    
    return newly_unlocked


def get_progress_summary(profile_name):
    """Get detailed progress summary for a profile"""
    profiles = load_profiles()
    for p in profiles:
        if p.get("name") == profile_name:
            progress = p.get("progress", {})
            learning = progress.get("learning", {})
            quiz = progress.get("quiz", {})
            
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
