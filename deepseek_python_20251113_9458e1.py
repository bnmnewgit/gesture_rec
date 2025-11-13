#!/usr/bin/env python3
"""
COMPLETE CONSOLE GESTURE DETECTION SYSTEM
For Raspberry Pi 3 B+ with MediaPipe
- Real-time pose detection
- 4 gesture recognition
- Terminal-based interface
- Performance optimized for Pi
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import os
import sys

class ConsoleGestureSystem:
    def __init__(self):
        # Initialize performance tracking
        self.frame_count = 0
        self.start_time = time.time()
        self.last_gesture = "NO_GESTURE"
        self.gesture_streak = 0
        self.current_fps = 0
        
        # MediaPipe initialization
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize Pose model with optimized settings for Pi
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,      # False for video (better performance)
            model_complexity=1,           # 1 = balanced, 0 = fast, 2 = heavy
            min_detection_confidence=0.7, # How sure to detect a person
            min_tracking_confidence=0.5   # How sure to keep tracking
        )
        
        # Camera setup
        self.cap = None
        self.setup_camera()
        
        # Gesture configuration
        self.raise_threshold = 0.05       # How much above shoulder = "raised"
        self.cross_threshold = 0.15       # How close for crossed arms
        
        print("✅ Console Gesture System Initialized")
    
    def setup_camera(self):
        """Initialize camera with Raspberry Pi optimized settings"""
        try:
            self.cap = cv2.VideoCapture(0)
            
            # Low resolution for Pi 3 B+ performance
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            self.cap.set(cv2.CAP_PROP_FPS, 15)
            
            # Test camera
            if not self.cap.isOpened():
                raise Exception("Camera not accessible")
                
            print("✅ Camera configured: 320x240 @ 15FPS")
            
        except Exception as e:
            print(f"❌ Camera setup failed: {e}")
            sys.exit(1)
    
    def is_hand_raised(self, shoulder_y, wrist_y, elbow_y):
        """
        Determine if hand is raised above shoulder level
        
        Args:
            shoulder_y: Y-coordinate of shoulder (0-1, lower = higher)
            wrist_y: Y-coordinate of wrist (0-1, lower = higher)
            elbow_y: Y-coordinate of elbow (0-1, lower = higher)
            
        Returns:
            bool: True if hand is raised
        """
        # In MediaPipe: LOWER y-value = HIGHER position
        wrist_above_shoulder = wrist_y < (shoulder_y - self.raise_threshold)
        wrist_above_elbow = wrist_y < (elbow_y - self.raise_threshold)
        
        return wrist_above_shoulder and wrist_above_elbow
    
    def detect_gesture(self, landmarks):
        """
        Convert body landmarks into gesture commands
        
        Args:
            landmarks: 33 body points from MediaPipe Pose
            
        Returns:
            str: Detected gesture name
        """
        try:
            # Extract key landmarks using MediaPipe's indexing
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
            left_wrist = landmarks[self.mp_pose.PoseLandmark.LEFT_WRIST.value]
            right_wrist = landmarks[self.mp_pose.PoseLandmark.RIGHT_WRIST.value]
            left_elbow = landmarks[self.mp_pose.PoseLandmark.LEFT_ELBOW.value]
            right_elbow = landmarks[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value]
            
            # Check hand raised status
            left_raised = self.is_hand_raised(left_shoulder.y, left_wrist.y, left_elbow.y)
            right_raised = self.is_hand_raised(right_shoulder.y, right_wrist.y, right_elbow.y)
            
            # 🎯 CRITICAL: Check BOTH hands FIRST (fixes the logic error)
            if left_raised and right_raised:
                return "BOTH_HANDS_UP"
            
            # Check crossed arms (wrists near opposite shoulders)
            left_crossed = abs(left_wrist.x - right_shoulder.x) < self.cross_threshold
            right_crossed = abs(right_wrist.x - left_shoulder.x) < self.cross_threshold
            
            if left_crossed and right_crossed:
                return "CROSSED_ARMS"
            
            # Check single hand raises LAST
            if left_raised:
                return "LEFT_HAND_UP"
            elif right_raised:
                return "RIGHT_HAND_UP"
            
            return "NO_GESTURE"
            
        except Exception as e:
            print(f"❌ Gesture detection error: {e}")
            return "NO_GESTURE"
    
    def calculate_fps(self):
        """Calculate current frames per second"""
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        return self.frame_count / elapsed_time if elapsed_time > 0 else 0
    
    def print_terminal_display(self, gesture, confidence_streak):
        """
        Update terminal with current system status
        
        Args:
            gesture: Current detected gesture
            confidence_streak: How many frames gesture has been consistent
        """
        os.system('clear')  # Clear terminal (use 'cls' on Windows)
        
        print("🎯 CONSOLE GESTURE DETECTION SYSTEM")
        print("=" * 55)
        print(f"Frame: {self.frame_count:6d} | FPS: {self.current_fps:5.1f} | Confidence: {confidence_streak:2d}")
        print("=" * 55)
        
        # Gesture display with visual indicators
        gesture_display = {
            "BOTH_HANDS_UP": "👆👆 BOTH HANDS UP   [ON COMMAND]",
            "LEFT_HAND_UP":  "👆 LEFT HAND UP     [ON COMMAND]", 
            "RIGHT_HAND_UP": "👆 RIGHT HAND UP    [OFF COMMAND]",
            "CROSSED_ARMS":  "❌ CROSSED ARMS     [OFF COMMAND]",
            "NO_GESTURE":    "➖ NO GESTURE       [WAITING...]"
        }
        
        print(f"CURRENT GESTURE: {gesture_display[gesture]}")
        print("=" * 55)
        
        # Gesture guide
        print("GESTURE GUIDE:")
        print("  👆👆  Raise BOTH hands    → BOTH_HANDS_UP  (TURN ON)")
        print("  👆    Raise LEFT hand     → LEFT_HAND_UP   (TURN ON)")
        print("  👆    Raise RIGHT hand    → RIGHT_HAND_UP  (TURN OFF)")
        print("  ❌    Cross arms          → CROSSED_ARMS   (TURN OFF)")
        print("=" * 55)
        
        # Performance info
        print("SYSTEM INFO:")
        print(f"  Resolution: 320x240 | Target FPS: 15")
        print(f"  Raise threshold: {self.raise_threshold} | Cross threshold: {self.cross_threshold}")
        print("=" * 55)
        print("Press CTRL + C to exit the system")
        print("-" * 55)
    
    def process_frame(self, frame):
        """
        Process a single camera frame for gesture detection
        
        Args:
            frame: Camera frame from OpenCV
            
        Returns:
            str: Detected gesture
        """
        # Convert BGR to RGB (MediaPipe requires RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process with MediaPipe Pose detection
        results = self.pose.process(rgb_frame)
        
        current_gesture = "NO_GESTURE"
        
        if results.pose_landmarks:
            current_gesture = self.detect_gesture(results.pose_landmarks.landmark)
        
        return current_gesture
    
    def update_gesture_streak(self, current_gesture):
        """
        Track how many consecutive frames show the same gesture
        This adds stability to gesture recognition
        
        Args:
            current_gesture: Gesture detected in current frame
            
        Returns:
            int: Current streak count
        """
        if current_gesture == self.last_gesture:
            self.gesture_streak += 1
        else:
            self.gesture_streak = 1
            self.last_gesture = current_gesture
            
        return self.gesture_streak
    
    def run(self):
        """
        Main system loop - runs gesture detection continuously
        """
        print("🚀 Starting Console Gesture Detection System...")
        print("📷 Initializing camera feed...")
        
        # Small delay to ensure camera is ready
        time.sleep(2)
        
        print("✅ System ready! Detecting gestures...")
        
        try:
            while True:
                # Capture frame from camera
                success, frame = self.cap.read()
                if not success:
                    print("❌ Failed to read camera frame")
                    break
                
                self.frame_count += 1
                
                # Performance optimization: Skip every 2nd frame on Pi 3 B+
                if self.frame_count % 2 != 0:
                    continue
                
                # Process frame and detect gesture
                current_gesture = self.process_frame(frame)
                
                # Update gesture consistency tracking
                confidence_streak = self.update_gesture_streak(current_gesture)
                
                # Calculate current FPS
                self.current_fps = self.calculate_fps()
                
                # Update terminal display
                self.print_terminal_display(current_gesture, confidence_streak)
                
                # Only consider "confirmed" gestures after multiple frames
                confirmed_gesture = current_gesture if confidence_streak >= 3 else "NO_GESTURE"
                
                # Here we would trigger appliance control (future enhancement)
                if confirmed_gesture != "NO_GESTURE" and confidence_streak == 3:
                    self.handle_gesture_command(confirmed_gesture)
                
                # Small delay to reduce CPU usage
                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n🛑 System shutdown requested by user...")
        except Exception as e:
            print(f"\n❌ System error: {e}")
        finally:
            self.cleanup()
    
    def handle_gesture_command(self, gesture):
        """
        Placeholder for appliance control logic
        This will be expanded when we add GPIO control
        
        Args:
            gesture: Confirmed gesture command
        """
        # This is where we'll add relay control later
        on_commands = ["BOTH_HANDS_UP", "LEFT_HAND_UP"]
        off_commands = ["RIGHT_HAND_UP", "CROSSED_ARMS"]
        
        if gesture in on_commands:
            print(f"🔧 [ACTION] Would turn ON appliance - {gesture}")
        elif gesture in off_commands:
            print(f"🔧 [ACTION] Would turn OFF appliance - {gesture}")
    
    def cleanup(self):
        """Clean up system resources properly"""
        print("\n🧹 Cleaning up system resources...")
        
        if self.cap:
            self.cap.release()
        
        cv2.destroyAllWindows()
        
        # Calculate final statistics
        total_time = time.time() - self.start_time
        avg_fps = self.frame_count / total_time if total_time > 0 else 0
        
        print("📊 SESSION SUMMARY:")
        print(f"   Total frames processed: {self.frame_count}")
        print(f"   Total time: {total_time:.1f} seconds")
        print(f"   Average FPS: {avg_fps:.1f}")
        print(f"   Final gesture: {self.last_gesture}")
        print("✅ System shutdown completed! 👋")

def main():
    """Main function to start the gesture detection system"""
    print("🤖 GESTURE CONTROL SYSTEM BOOT-UP")
    print("=" * 50)
    print("Hardware: Raspberry Pi 3 B+")
    print("Software: Python 3.11 + MediaPipe + OpenCV")
    print("=" * 50)
    
    # Create and run the gesture system
    gesture_system = ConsoleGestureSystem()
    gesture_system.run()

if __name__ == "__main__":
    main()