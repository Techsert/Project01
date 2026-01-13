# audio_manager.py
# NEW FILE - Centralizes audio management and fixes audio context issues

import pygame
import os
import config

class AudioManager:
    """
    Centralized audio management system.
    Fixes audio context issues when switching between screens.
    """
    
    # Audio types
    BG_MUSIC = 'bg_music'
    VIDEO_AUDIO = 'video_audio'
    NARRATION = 'narration'
    SOUND_EFFECT = 'sound_effect'
    
    def __init__(self):
        """Initialize the audio manager."""
        pygame.mixer.init()
        
        # Audio state
        self.current_audio_type = self.BG_MUSIC
        self.current_audio_path = None
        self.was_playing = False
        self.playback_position = 0  # For resuming playback
        
        # Background music
        self.bg_music_path = os.path.join(config.SOUND_MAIN_PATH, "bg_sound.mp3")
        self.bg_music_volume = config.BG_MUSIC_VOLUME
        
        # Hover sound channel
        self.hover_channel = pygame.mixer.Channel(config.HOVER_CHANNEL_ID)
        
        # Audio context stack for nested screens
        self.context_stack = []
    
    def play_bg_music(self, loop=True):
        """Play background music."""
        try:
            if not os.path.exists(self.bg_music_path):
                print(f"⚠️ Background music not found: {self.bg_music_path}")
                return False
            
            pygame.mixer.music.load(self.bg_music_path)
            pygame.mixer.music.set_volume(self.bg_music_volume)
            pygame.mixer.music.play(-1 if loop else 0)
            
            self.current_audio_type = self.BG_MUSIC
            self.current_audio_path = self.bg_music_path
            self.was_playing = True
            
            return True
        except Exception as e:
            print(f"❌ Error playing background music: {e}")
            return False
    
    def play_sound(self, path, audio_type=NARRATION):
        """
        Play a sound file (narration, video audio, etc.)
        
        Args:
            path: Path to audio file
            audio_type: Type of audio (NARRATION, VIDEO_AUDIO, etc.)
        """
        try:
            if not os.path.exists(path):
                print(f"⚠️ Audio file not found: {path}")
                return False
            
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
            
            self.current_audio_type = audio_type
            self.current_audio_path = path
            self.was_playing = True
            self.playback_position = 0
            
            return True
        except Exception as e:
            print(f"❌ Error playing sound {path}: {e}")
            return False
    
    def play_hover_sound(self, path):
        """Play hover sound effect on dedicated channel."""
        try:
            if not os.path.exists(path):
                print(f"⚠️ Hover sound not found: {path}")
                return False
            
            sound = pygame.mixer.Sound(path)
            if self.hover_channel.get_busy():
                self.hover_channel.stop()
            self.hover_channel.play(sound)
            return True
        except Exception as e:
            print(f"❌ Error playing hover sound: {e}")
            return False
    
    def stop_all_sounds(self):
        """Stop all audio channels."""
        try:
            pygame.mixer.music.stop()
            for i in range(pygame.mixer.get_num_channels()):
                pygame.mixer.Channel(i).stop()
        except Exception as e:
            print(f"❌ Error stopping sounds: {e}")
    
    def pause_music(self):
        """Pause current music and save position."""
        try:
            if pygame.mixer.music.get_busy():
                self.playback_position = pygame.mixer.music.get_pos() / 1000.0  # Convert to seconds
                pygame.mixer.music.pause()
                self.was_playing = True
        except Exception as e:
            print(f"❌ Error pausing music: {e}")
    
    def resume_music(self):
        """Resume paused music from saved position."""
        try:
            if self.was_playing:
                pygame.mixer.music.unpause()
        except Exception as e:
            print(f"❌ Error resuming music: {e}")
    
    def push_audio_context(self):
        """
        Save current audio context to stack.
        Call this before opening a new screen that will change audio.
        """
        context = {
            'type': self.current_audio_type,
            'path': self.current_audio_path,
            'was_playing': pygame.mixer.music.get_busy(),
            'position': pygame.mixer.music.get_pos() / 1000.0 if pygame.mixer.music.get_busy() else 0
        }
        self.context_stack.append(context)
        print(f"📥 Pushed audio context: {context['type']}")
    
    def pop_audio_context(self, restore=True):
        """
        Restore previous audio context from stack.
        
        Args:
            restore: If True, automatically restore the audio playback
        
        Returns:
            The popped context dictionary, or None if stack is empty
        """
        if not self.context_stack:
            print("⚠️ Audio context stack is empty")
            return None
        
        context = self.context_stack.pop()
        print(f"📤 Popped audio context: {context['type']}")
        
        if restore:
            self._restore_context(context)
        
        return context
    
    def _restore_context(self, context):
        """Internal method to restore a specific audio context."""
        try:
            if not context['was_playing']:
                print("ℹ️ Audio was not playing, not restoring")
                return
            
            audio_type = context['type']
            audio_path = context['path']
            
            if audio_type == self.BG_MUSIC:
                # Restore background music
                self.play_bg_music()
                print("✅ Restored background music")
            
            elif audio_type == self.VIDEO_AUDIO:
                # Don't auto-restore video audio (user should manually replay)
                print("ℹ️ Video audio not auto-restored (user can replay)")
                self.current_audio_type = self.BG_MUSIC
                self.current_audio_path = None
            
            elif audio_type == self.NARRATION:
                # Don't auto-restore narration (it's usually finished or outdated)
                print("ℹ️ Narration not auto-restored")
                # Fall back to background music
                self.play_bg_music()
            
            else:
                print(f"⚠️ Unknown audio type: {audio_type}")
                self.play_bg_music()
        
        except Exception as e:
            print(f"❌ Error restoring audio context: {e}")
            # Fallback to background music
            self.play_bg_music()
    
    def set_context(self, audio_type, audio_path=None):
        """
        Set current audio context without playing.
        Used by screens to track what audio should be playing.
        """
        self.current_audio_type = audio_type
        self.current_audio_path = audio_path
    
    def get_context(self):
        """Get current audio context."""
        return {
            'type': self.current_audio_type,
            'path': self.current_audio_path,
            'was_playing': self.was_playing
        }
    
    def is_music_playing(self):
        """Check if music is currently playing."""
        return pygame.mixer.music.get_busy()
    
    def set_bg_music_volume(self, volume):
        """Set background music volume (0.0 to 1.0)."""
        self.bg_music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.bg_music_volume)
