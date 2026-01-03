"""
Math Hunter - Android Version
Modern Math Quiz Game for Mobile
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.metrics import dp

import random
import json
import os
import datetime

# ============================================================================
# GLOBAL SETTINGS & DATA
# ============================================================================
SCOREBOARD_FILE = "scoreboard.json"

class GameData:
    """Global game state manager"""
    def __init__(self):
        self.questions = []
        self.current_question_idx = 0
        self.score = 0
        self.difficulty = ""
        self.total_questions = 0
        self.question_start_time = 0
        self.time_limit = 15  # seconds for Hard mode
        self.top_scores = []
        
        # Audio
        self.music_on = True
        self.sound_on = True
        self.sound_correct = None
        self.sound_wrong = None
        
        self.load_sounds()
        self.load_scores()
    
    def load_sounds(self):
        """Load sound effects"""
        try:
            self.sound_correct = SoundLoader.load('ding.ogg')
        except:
            print("Warning: ding.ogg not found")
        
        try:
            self.sound_wrong = SoundLoader.load('buzz.ogg')
        except:
            print("Warning: buzz.ogg not found")
    
    def play_sound(self, sound_type):
        """Play sound effect"""
        if not self.sound_on:
            return
        
        if sound_type == 'correct' and self.sound_correct:
            self.sound_correct.play()
        elif sound_type == 'wrong' and self.sound_wrong:
            self.sound_wrong.play()
    
    def load_scores(self):
        """Load top scores from file"""
        if os.path.exists(SCOREBOARD_FILE):
            try:
                with open(SCOREBOARD_FILE, 'r') as f:
                    self.top_scores = json.load(f)
                self.top_scores.sort(key=lambda x: (x['score'], x['total']), reverse=True)
                self.top_scores = self.top_scores[:10]
            except:
                self.top_scores = []
        else:
            self.top_scores = []
    
    def save_scores(self):
        """Save top scores to file"""
        with open(SCOREBOARD_FILE, 'w') as f:
            json.dump(self.top_scores, f, indent=2)
    
    def add_score(self, name, score, total, difficulty):
        """Add new score to scoreboard"""
        now = datetime.datetime.now()
        entry = {
            "name": name,
            "date": now.strftime("%d.%m.%Y"),
            "time": now.strftime("%I:%M%p").lower(),
            "difficulty": difficulty,
            "score": score,
            "total": total
        }
        self.top_scores.append(entry)
        self.top_scores.sort(key=lambda x: (x['score'], x['total']), reverse=True)
        self.top_scores = self.top_scores[:10]
        self.save_scores()
    
    def qualifies_for_scoreboard(self, score):
        """Check if score qualifies for top 10"""
        return len(self.top_scores) < 10 or score > (self.top_scores[-1]['score'] if self.top_scores else -1)
    
    def generate_questions(self, num_questions, difficulty):
        """Generate quiz questions"""
        questions = []
        
        if difficulty == "Easy":
            num_min, num_max = 1, 12
            operators = ['+', '-', '*']
            three_part = 0
        elif difficulty == "Medium":
            num_min, num_max = 10, 50
            operators = ['+', '-', '*', '//']
            three_part = 0
        else:  # Hard
            num_min, num_max = 20, 100
            operators = ['+', '-', '*', '/']
            three_part = 0.4
        
        for _ in range(num_questions):
            while True:
                try:
                    num1 = random.randint(num_min, num_max)
                    num2 = random.randint(max(1, num_min), num_max)
                    op1 = random.choice(operators)
                    
                    if difficulty == "Hard" and random.random() < three_part:
                        num3 = random.randint(max(1, num_min // 2), num_max // 2)
                        op2 = random.choice(operators)
                        question_str = f"{num1} {op1} {num2} {op2} {num3}"
                    else:
                        question_str = f"{num1} {op1} {num2}"
                    
                    result = eval(question_str)
                    is_float = '/' in question_str and '//' not in question_str
                    
                    if is_float:
                        correct = round(float(result), 2)
                    else:
                        correct = int(result)
                    
                    if abs(correct) > 5000:
                        continue
                    if is_float and abs(correct) > 999:
                        continue
                    
                    # Generate options
                    options = {correct}
                    for _ in range(5):
                        if is_float:
                            offset = random.uniform(-abs(correct)/5, abs(correct)/5)
                            if abs(offset) < 0.1:
                                offset = 0.1 if random.random() > 0.5 else -0.1
                            wrong = round(correct + offset, 2)
                        else:
                            offset = random.randint(-max(1, abs(correct)//10), 
                                                   max(1, abs(correct)//10))
                            if offset == 0:
                                offset = random.choice([-1, 1])
                            wrong = correct + offset
                        options.add(wrong)
                    
                    options = list(options)
                    if len(options) < 4:
                        continue
                    
                    options = random.sample(options, 4)
                    if correct not in options:
                        options[random.randint(0, 3)] = correct
                    random.shuffle(options)
                    
                    formatted = []
                    for opt in options:
                        if is_float:
                            formatted.append(f"{opt:.2f}")
                        else:
                            formatted.append(str(int(opt)))
                    
                    questions.append({
                        "question": f"What is {question_str}?",
                        "options": formatted,
                        "correct": correct
                    })
                    break
                except:
                    continue
        
        return questions
    
    def start_quiz(self, num_questions, difficulty):
        """Initialize new quiz"""
        self.difficulty = difficulty
        self.total_questions = num_questions
        self.questions = self.generate_questions(num_questions, difficulty)
        self.current_question_idx = 0
        self.score = 0
        self.question_start_time = datetime.datetime.now()
    
    def get_current_question(self):
        """Get current question data"""
        if self.current_question_idx < len(self.questions):
            return self.questions[self.current_question_idx]
        return None
    
    def check_answer(self, selected_text):
        """Check if answer is correct"""
        question = self.get_current_question()
        if not question:
            return False
        
        try:
            if isinstance(question["correct"], float):
                selected = float(selected_text)
                is_correct = abs(selected - question["correct"]) < 0.001
            else:
                selected = int(selected_text)
                is_correct = selected == question["correct"]
            return is_correct
        except:
            return False
    
    def next_question(self):
        """Move to next question"""
        self.current_question_idx += 1
        self.question_start_time = datetime.datetime.now()
    
    def get_time_remaining(self):
        """Get remaining time for Hard mode"""
        if self.difficulty != "Hard":
            return None
        
        elapsed = (datetime.datetime.now() - self.question_start_time).total_seconds()
        remaining = max(0, self.time_limit - elapsed)
        return remaining
    
    def is_quiz_complete(self):
        """Check if quiz is finished"""
        return self.current_question_idx >= len(self.questions)


# Global game data instance
game_data = GameData()


# ============================================================================
# CUSTOM WIDGETS
# ============================================================================

class ModernButton(Button):
    """Custom styled button for mobile"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Transparent
        self.background_normal = ''
        self.font_size = dp(18)
        self.size_hint_y = None
        self.height = dp(60)
        self.bold = True
        
        with self.canvas.before:
            self.bg_color = Color(0.31, 0.98, 0.48, 1)  # Green default
            self.bg_rect = RoundedRectangle(radius=[dp(15)])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
    
    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def set_color(self, r, g, b, a=1):
        """Change button color"""
        self.bg_color.rgba = (r, g, b, a)


class OptionButton(Button):
    """Quiz option button"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.font_size = dp(16)
        self.size_hint_y = None
        self.height = dp(70)
        self.halign = 'left'
        self.valign = 'middle'
        self.padding = [dp(20), 0]
        self.text_size = (None, None)
        
        with self.canvas.before:
            self.bg_color = Color(0.27, 0.28, 0.35, 1)  # Neutral
            self.bg_rect = RoundedRectangle(radius=[dp(12)])
        
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(size=self.update_text_size)
    
    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
    
    def update_text_size(self, *args):
        self.text_size = (self.width - dp(40), None)
    
    def set_correct(self):
        """Mark as correct answer"""
        self.bg_color.rgba = (0.31, 0.98, 0.48, 1)  # Green
    
    def set_wrong(self):
        """Mark as wrong answer"""
        self.bg_color.rgba = (1, 0.33, 0.33, 1)  # Red
    
    def reset(self):
        """Reset to neutral color"""
        self.bg_color.rgba = (0.27, 0.28, 0.35, 1)


# ============================================================================
# SCREENS
# ============================================================================

class MainMenuScreen(Screen):
    """Main menu screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Logo/Title area
        title_layout = BoxLayout(orientation='vertical', size_hint_y=0.3)
        
        title = Label(
            text='MATH HUNTER',
            font_size=dp(48),
            bold=True,
            color=(0.31, 0.98, 0.48, 1)
        )
        title_layout.add_widget(title)
        
        subtitle = Label(
            text='Test Your Math Skills!',
            font_size=dp(16),
            color=(0.74, 0.76, 0.79, 1)
        )
        title_layout.add_widget(subtitle)
        
        layout.add_widget(title_layout)
        
        # Spacer
        layout.add_widget(Label(size_hint_y=0.1))
        
        # Buttons
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=0.6)
        
        play_btn = ModernButton(text='PLAY GAME')
        play_btn.bind(on_press=self.go_to_difficulty)
        btn_layout.add_widget(play_btn)
        
        scoreboard_btn = ModernButton(text='SCOREBOARD')
        scoreboard_btn.set_color(0.55, 0.91, 0.99)  # Cyan
        scoreboard_btn.bind(on_press=self.go_to_scoreboard)
        btn_layout.add_widget(scoreboard_btn)
        
        settings_btn = ModernButton(text='SETTINGS')
        settings_btn.set_color(0.55, 0.91, 0.99)  # Cyan
        settings_btn.bind(on_press=self.go_to_settings)
        btn_layout.add_widget(settings_btn)
        
        credits_btn = ModernButton(text='CREDITS')
        credits_btn.set_color(0.55, 0.91, 0.99)  # Cyan
        credits_btn.bind(on_press=self.go_to_credits)
        btn_layout.add_widget(credits_btn)
        
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def go_to_difficulty(self, instance):
        self.manager.current = 'difficulty'
    
    def go_to_scoreboard(self, instance):
        self.manager.current = 'scoreboard'
    
    def go_to_settings(self, instance):
        self.manager.current = 'settings'
    
    def go_to_credits(self, instance):
        self.manager.current = 'credits'


class DifficultyScreen(Screen):
    """Difficulty selection screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Title
        title = Label(
            text='SELECT DIFFICULTY',
            font_size=dp(36),
            bold=True,
            size_hint_y=0.15,
            color=(0.55, 0.91, 0.99, 1)
        )
        layout.add_widget(title)
        
        subtitle = Label(
            text='Choose your challenge level',
            font_size=dp(14),
            size_hint_y=0.1,
            color=(0.74, 0.76, 0.79, 1)
        )
        layout.add_widget(subtitle)
        
        # Difficulty buttons
        btn_layout = BoxLayout(orientation='vertical', spacing=dp(15), size_hint_y=0.6)
        
        easy_btn = ModernButton(text='EASY - 30 Questions')
        easy_btn.set_color(0.31, 0.98, 0.48)  # Green
        easy_btn.bind(on_press=lambda x: self.start_quiz(30, 'Easy'))
        btn_layout.add_widget(easy_btn)
        
        medium_btn = ModernButton(text='MEDIUM - 50 Questions')
        medium_btn.set_color(1, 0.72, 0.42)  # Orange
        medium_btn.bind(on_press=lambda x: self.start_quiz(50, 'Medium'))
        btn_layout.add_widget(medium_btn)
        
        hard_btn = ModernButton(text='HARD - 100 Questions')
        hard_btn.set_color(1, 0.33, 0.33)  # Red
        hard_btn.bind(on_press=lambda x: self.start_quiz(100, 'Hard'))
        btn_layout.add_widget(hard_btn)
        
        layout.add_widget(btn_layout)
        
        # Back button
        back_btn = ModernButton(text='BACK', size_hint_y=0.15)
        back_btn.set_color(0.27, 0.28, 0.35)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def start_quiz(self, num_questions, difficulty):
        game_data.start_quiz(num_questions, difficulty)
        self.manager.current = 'quiz'
        # Refresh quiz screen
        self.manager.get_screen('quiz').load_question()
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'


class QuizScreen(Screen):
    """Quiz gameplay screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Header: Score, Question number, Timer
        header = BoxLayout(size_hint_y=0.12, spacing=dp(10))
        
        self.score_label = Label(
            text='Score: 0',
            font_size=dp(16),
            bold=True,
            color=(0.31, 0.98, 0.48, 1)
        )
        header.add_widget(self.score_label)
        
        self.question_label = Label(
            text='Q: 1/30',
            font_size=dp(16),
            color=(0.74, 0.76, 0.79, 1)
        )
        header.add_widget(self.question_label)
        
        self.timer_label = Label(
            text='',
            font_size=dp(16),
            bold=True,
            color=(1, 0.72, 0.42, 1)
        )
        header.add_widget(self.timer_label)
        
        self.main_layout.add_widget(header)
        
        # Question display
        self.question_text = Label(
            text='',
            font_size=dp(24),
            size_hint_y=0.15,
            bold=True,
            color=(0.97, 0.97, 0.95, 1)
        )
        self.main_layout.add_widget(self.question_text)
        
        # Options
        self.options_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=0.6)
        self.option_buttons = []
        
        for i in range(4):
            btn = OptionButton(text=f'{chr(65+i)}. ')
            btn.bind(on_press=self.check_answer)
            self.option_buttons.append(btn)
            self.options_layout.add_widget(btn)
        
        self.main_layout.add_widget(self.options_layout)
        
        # Feedback label
        self.feedback_label = Label(
            text='',
            font_size=dp(28),
            bold=True,
            size_hint_y=0.13
        )
        self.main_layout.add_widget(self.feedback_label)
        
        self.add_widget(self.main_layout)
        
        self.answer_selected = False
        self.timer_event = None
    
    def on_enter(self):
        """Called when screen is displayed"""
        if game_data.difficulty == "Hard":
            self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)
    
    def on_leave(self):
        """Called when leaving screen"""
        if self.timer_event:
            self.timer_event.cancel()
    
    def update_timer(self, dt):
        """Update timer for Hard mode"""
        remaining = game_data.get_time_remaining()
        if remaining is not None:
            self.timer_label.text = f'Time: {int(remaining)}s'
            
            if remaining <= 5:
                self.timer_label.color = (1, 0.33, 0.33, 1)  # Red warning
            
            if remaining <= 0 and not self.answer_selected:
                self.time_up()
    
    def time_up(self):
        """Handle time's up for Hard mode"""
        self.answer_selected = True
        self.feedback_label.text = 'TIME\'S UP!'
        self.feedback_label.color = (1, 0.33, 0.33, 1)
        game_data.play_sound('wrong')
        
        # Show correct answer
        question = game_data.get_current_question()
        if question:
            correct_str = f"{question['correct']:.2f}" if isinstance(
                question['correct'], float) else str(question['correct'])
            
            for btn in self.option_buttons:
                option_text = btn.text.split('. ', 1)[1]
                if option_text == correct_str:
                    btn.set_correct()
        
        # Restart quiz after delay
        Clock.schedule_once(lambda dt: self.restart_quiz(), 1.5)
    
    def load_question(self):
        """Load current question"""
        self.answer_selected = False
        self.feedback_label.text = ''
        
        question = game_data.get_current_question()
        if not question:
            self.finish_quiz()
            return
        
        # Update UI
        self.score_label.text = f'Score: {game_data.score}'
        self.question_label.text = f'Q: {game_data.current_question_idx + 1}/{game_data.total_questions}'
        self.question_text.text = question["question"]
        
        # Update options
        for i, btn in enumerate(self.option_buttons):
            btn.text = f'{chr(65+i)}. {question["options"][i]}'
            btn.reset()
        
        # Reset timer display
        if game_data.difficulty == "Hard":
            self.timer_label.text = f'Time: {game_data.time_limit}s'
            self.timer_label.color = (1, 0.72, 0.42, 1)
        else:
            self.timer_label.text = ''
    
    def check_answer(self, instance):
        """Check selected answer"""
        if self.answer_selected:
            return
        
        self.answer_selected = True
        
        # Get selected option text
        selected_text = instance.text.split('. ', 1)[1]
        is_correct = game_data.check_answer(selected_text)
        
        # Update score
        if is_correct:
            game_data.score += 1
            self.score_label.text = f'Score: {game_data.score}'
            self.feedback_label.text = 'CORRECT!'
            self.feedback_label.color = (0.31, 0.98, 0.48, 1)
            game_data.play_sound('correct')
        else:
            self.feedback_label.text = 'WRONG!'
            self.feedback_label.color = (1, 0.33, 0.33, 1)
            game_data.play_sound('wrong')
        
        # Highlight answers
        question = game_data.get_current_question()
        if question:
            correct_str = f"{question['correct']:.2f}" if isinstance(
                question['correct'], float) else str(question['correct'])
            
            for btn in self.option_buttons:
                option_text = btn.text.split('. ', 1)[1]
                if option_text == correct_str:
                    btn.set_correct()
                elif btn == instance and not is_correct:
                    btn.set_wrong()
        
        # Proceed based on result
        if game_data.difficulty == "Hard" and not is_correct:
            Clock.schedule_once(lambda dt: self.restart_quiz(), 1.5)
        else:
            Clock.schedule_once(lambda dt: self.next_question(), 1.5)
    
    def next_question(self, *args):
        """Move to next question"""
        game_data.next_question()
        
        if game_data.is_quiz_complete():
            self.finish_quiz()
        else:
            self.load_question()
    
    def restart_quiz(self):
        """Restart quiz for Hard mode"""
        game_data.start_quiz(game_data.total_questions, game_data.difficulty)
        self.load_question()
    
    def finish_quiz(self):
        """Complete quiz and go to results"""
        if self.timer_event:
            self.timer_event.cancel()
        self.manager.current = 'results'
        self.manager.get_screen('results').show_results()


class ResultsScreen(Screen):
    """Quiz results screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Title
        self.title = Label(
            text='QUIZ COMPLETE!',
            font_size=dp(36),
            bold=True,
            size_hint_y=0.15,
            color=(0.31, 0.98, 0.48, 1)
        )
        self.main_layout.add_widget(self.title)
        
        # Score display
        self.score_label = Label(
            text='',
            font_size=dp(32),
            bold=True,
            size_hint_y=0.15,
            color=(0.31, 0.98, 0.48, 1)
        )
        self.main_layout.add_widget(self.score_label)
        
        # Name input area (hidden by default)
        self.name_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.3)
        
        name_prompt = Label(
            text='Top 10! Enter your name:',
            font_size=dp(16),
            color=(0.97, 0.97, 0.95, 1)
        )
        self.name_layout.add_widget(name_prompt)
        
        self.name_input = TextInput(
            hint_text='Your name',
            multiline=False,
            size_hint_y=None,
            height=dp(50),
            font_size=dp(18),
            padding=[dp(15), dp(15)]
        )
        self.name_layout.add_widget(self.name_input)
        
        submit_btn = ModernButton(text='SUBMIT SCORE')
        submit_btn.bind(on_press=self.submit_score)
        self.name_layout.add_widget(submit_btn)
        
        self.main_layout.add_widget(self.name_layout)
        
        # Action buttons
        self.button_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=0.4)
        
        play_again_btn = ModernButton(text='PLAY AGAIN')
        play_again_btn.bind(on_press=self.play_again)
        self.button_layout.add_widget(play_again_btn)
        
        menu_btn = ModernButton(text='MAIN MENU')
        menu_btn.set_color(0.55, 0.91, 0.99)
        menu_btn.bind(on_press=self.go_to_menu)
        self.button_layout.add_widget(menu_btn)
        
        self.main_layout.add_widget(self.button_layout)
        
        self.add_widget(self.main_layout)
    
    def show_results(self):
        """Display quiz results"""
        self.score_label.text = f'Score: {game_data.score} / {game_data.total_questions}'
        
        # Check if qualifies for scoreboard
        if game_data.qualifies_for_scoreboard(game_data.score):
            self.name_layout.opacity = 1
            self.name_layout.disabled = False
            self.button_layout.opacity = 0
            self.button_layout.disabled = True
        else:
            self.name_layout.opacity = 0
            self.name_layout.disabled = True
            self.button_layout.opacity = 1
            self.button_layout.disabled = False
    
    def submit_score(self, instance):
        """Submit score to scoreboard"""
        name = self.name_input.text.strip()
        if not name:
            return
        
        game_data.add_score(name, game_data.score, game_data.total_questions, game_data.difficulty)
        self.name_input.text = ''
        self.manager.current = 'scoreboard'
    
    def play_again(self, instance):
        """Play another quiz"""
        self.manager.current = 'difficulty'
    
    def go_to_menu(self, instance):
        """Return to main menu"""
        self.manager.current = 'main_menu'


class ScoreboardScreen(Screen):
    """Scoreboard display screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        
        # Title
        title = Label(
            text='TOP 10 SCORES',
            font_size=dp(32),
            bold=True,
            size_hint_y=0.12,
            color=(0.95, 0.77, 0.06, 1)
        )
        layout.add_widget(title)
        
        # Scrollable scores list
        scroll = ScrollView(size_hint_y=0.78)
        self.scores_layout = GridLayout(cols=1, spacing=dp(8), size_hint_y=None)
        self.scores_layout.bind(minimum_height=self.scores_layout.setter('height'))
        scroll.add_widget(self.scores_layout)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = ModernButton(text='BACK TO MENU', size_hint_y=0.1)
        back_btn.set_color(1, 0.33, 0.33)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def on_enter(self):
        """Refresh scores when entering screen"""
        self.load_scores()
    
    def load_scores(self):
        """Load and display scores"""
        self.scores_layout.clear_widgets()
        
        game_data.load_scores()
        
        if not game_data.top_scores:
            no_scores = Label(
                text='No scores yet. Be the first!',
                font_size=dp(16),
                size_hint_y=None,
                height=dp(50),
                color=(0.74, 0.76, 0.79, 1)
            )
            self.scores_layout.add_widget(no_scores)
            return
        
        for i, entry in enumerate(game_data.top_scores):
            # Determine color based on rank
            if i == 0:
                color = (0.95, 0.77, 0.06, 1)  # Gold
            elif i == 1:
                color = (0.55, 0.91, 0.99, 1)  # Silver
            elif i == 2:
                color = (1, 0.72, 0.42, 1)  # Bronze
            else:
                color = (0.97, 0.97, 0.95, 1)  # White
            
            # Score entry
            score_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(60),
                padding=[dp(10), dp(5)]
            )
            
            rank = Label(
                text=f'{i+1}.',
                font_size=dp(16),
                bold=True,
                size_hint_x=0.1,
                color=color
            )
            score_box.add_widget(rank)
            
            info = BoxLayout(orientation='vertical', size_hint_x=0.9)
            
            name_score = Label(
                text=f'{entry["name"]} - {entry["score"]}/{entry["total"]}',
                font_size=dp(16),
                bold=True,
                halign='left',
                color=color
            )
            name_score.bind(size=name_score.setter('text_size'))
            info.add_widget(name_score)
            
            details = Label(
                text=f'{entry["difficulty"]} • {entry["date"]} {entry["time"]}',
                font_size=dp(12),
                halign='left',
                color=(0.74, 0.76, 0.79, 1)
            )
            details.bind(size=details.setter('text_size'))
            info.add_widget(details)
            
            score_box.add_widget(info)
            self.scores_layout.add_widget(score_box)
            
            # Separator line
            if i < len(game_data.top_scores) - 1:
                separator = Label(size_hint_y=None, height=dp(1))
                with separator.canvas:
                    Color(0.27, 0.28, 0.35, 1)
                    Line(points=[0, 0, 1000, 0], width=1)
                self.scores_layout.add_widget(separator)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'


class SettingsScreen(Screen):
    """Settings screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Title
        title = Label(
            text='SETTINGS',
            font_size=dp(36),
            bold=True,
            size_hint_y=0.15,
            color=(0.55, 0.91, 0.99, 1)
        )
        layout.add_widget(title)
        
        # Settings buttons
        settings_layout = BoxLayout(orientation='vertical', spacing=dp(12), size_hint_y=0.7)
        
        self.sound_btn = ModernButton(text='Sound: ON')
        self.sound_btn.set_color(0.31, 0.98, 0.48)
        self.sound_btn.bind(on_press=self.toggle_sound)
        settings_layout.add_widget(self.sound_btn)
        
        info = Label(
            text='Tap buttons to toggle settings',
            font_size=dp(14),
            size_hint_y=0.5,
            color=(0.74, 0.76, 0.79, 1)
        )
        settings_layout.add_widget(info)
        
        layout.add_widget(settings_layout)
        
        # Back button
        back_btn = ModernButton(text='BACK TO MENU', size_hint_y=0.15)
        back_btn.set_color(1, 0.33, 0.33)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def toggle_sound(self, instance):
        """Toggle sound effects"""
        game_data.sound_on = not game_data.sound_on
        self.sound_btn.text = f'Sound: {"ON" if game_data.sound_on else "OFF"}'
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'


class CreditsScreen(Screen):
    """Credits screen"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # Title
        title = Label(
            text='CREDITS',
            font_size=dp(36),
            bold=True,
            size_hint_y=0.15,
            color=(0.31, 0.98, 0.48, 1)
        )
        layout.add_widget(title)
        
        # Credits content
        scroll = ScrollView(size_hint_y=0.7)
        credits_text = Label(
            text='\n\n[b]MATH HUNTER[/b]\n\n'
                 'Android Version\n\n\n'
                 '[b]Developed by:[/b]\n'
                 'Azwan Azli\n\n\n'
                 '[b]Background Music:[/b]\n'
                 'Jungle Waves by DimmySad\n\n\n'
                 '[b]Framework:[/b]\n'
                 'Kivy - Python Mobile Framework\n\n\n'
                 'Thanks for playing!\n\n',
            markup=True,
            font_size=dp(16),
            color=(0.97, 0.97, 0.95, 1)
        )
        scroll.add_widget(credits_text)
        layout.add_widget(scroll)
        
        # Back button
        back_btn = ModernButton(text='BACK TO MENU', size_hint_y=0.15)
        back_btn.set_color(1, 0.33, 0.33)
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def go_back(self, instance):
        self.manager.current = 'main_menu'


# ============================================================================
# MAIN APP
# ============================================================================

class MathHunterApp(App):
    """Main application class"""
    
    def build(self):
        # Set window background color
        Window.clearcolor = (0.10, 0.10, 0.14, 1)
        
        # Create screen manager
        sm = ScreenManager(transition=FadeTransition())
        
        # Add all screens
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(DifficultyScreen(name='difficulty'))
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(ResultsScreen(name='results'))
        sm.add_widget(ScoreboardScreen(name='scoreboard'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(CreditsScreen(name='credits'))
        
        return sm


if __name__ == '__main__':
    MathHunterApp().run()
