import pygame
import sys
import os
import array
from config import *
from ball import CueBall, ObjectBall
from table import Table
from cue import Cue
from physics import PhysicsEngine

# --- CLASS SOUND GENERATOR ---
class SoundGenerator:
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.sounds = {}
            self.sounds['hit'] = self._generate_beep(400, 0.1)    
            self.sounds['pocket'] = self._generate_beep(800, 0.2) 
            self.has_mixer = True
        except Exception as e:
            print(f"Audio init failed: {e}")
            self.has_mixer = False

    def _generate_beep(self, frequency, duration):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buffer = array.array('h', [0] * n_samples)
        amplitude = 4000 
        period = sample_rate / frequency
        for i in range(n_samples):
            if (i // (period / 2)) % 2 == 0: buffer[i] = amplitude
            else: buffer[i] = -amplitude
        return pygame.mixer.Sound(buffer)

    def play(self, name):
        if self.enabled and self.has_mixer and name in self.sounds:
            self.sounds[name].play()

# --- CLASS BUTTON UI ---
class Button:
    def __init__(self, x, y, w, h, text, color=ACCENT_COLOR):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = BUTTON_HOVER
        self.is_hovered = False
        self.font = pygame.font.SysFont('Arial', 20, bold=True)

    def draw(self, surface):
        color = self.color if not self.is_hovered else self.hover_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False

# --- GAME MANAGER ---
class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Billiard Master v2.5 (Widescreen & Pause)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.ball_font = pygame.font.SysFont('Arial', 10, bold=True)
        self.ui_ball_font = pygame.font.SysFont('Arial', 12, bold=True)
        
        self.state = STATE_MENU
        self.sound_manager = SoundGenerator()

        self.ball_colors = {
            1: YELLOW, 2: BLUE, 3: RED, 4: PURPLE, 5: ORANGE, 6: GREEN, 7: MAROON,
            9: YELLOW, 10: BLUE, 11: RED, 12: PURPLE, 13: ORANGE, 14: GREEN, 15: MAROON,
            8: BLACK
        }

        self.reset_game()
        
        # --- UI BUTTONS ---
        # Main Menu
        cx = SCREEN_WIDTH // 2
        self.btn_start = Button(cx - 100, 300, 200, 50, "PLAY GAME")
        self.btn_tutorial = Button(cx - 100, 370, 200, 50, "TUTORIAL")
        self.btn_settings = Button(cx - 100, 440, 200, 50, "SETTINGS")
        self.btn_quit = Button(cx - 100, 510, 200, 50, "QUIT")
        
        # Others
        self.btn_back = Button(50, SCREEN_HEIGHT - 60, 100, 40, "BACK", GREY)
        self.btn_toggle_sound = Button(cx - 100, 300, 200, 50, "SOUND: ON")
        
        # In-Game UI
        self.btn_reset_match = Button(cx - 60, SCREEN_HEIGHT - 60, 120, 40, "RESET", RED)
        # Tombol Menu di pojok kanan atas (dalam top bar)
        self.btn_pause_game = Button(SCREEN_WIDTH - 120, 20, 100, 40, "MENU", GREY)
        
        # Pause Menu Buttons
        self.btn_resume = Button(cx - 100, SCREEN_HEIGHT//2 - 30, 200, 50, "RESUME", ACCENT_COLOR)
        self.btn_exit_to_menu = Button(cx - 100, SCREEN_HEIGHT//2 + 40, 200, 50, "MAIN MENU", GREY)
        
        # Game Over Buttons
        self.btn_play_again = Button(cx - 100, 380, 200, 50, "PLAY AGAIN", ACCENT_COLOR)
        self.btn_main_menu = Button(cx - 100, 450, 200, 50, "MAIN MENU", GREY)

    def reset_game(self):
        self.table = Table()
        self.cue_ball = CueBall(TABLE_X + 200, TABLE_Y + PLAY_HEIGHT // 2)
        self.balls = [self.cue_ball]
        self.cue = Cue(self.cue_ball)
        
        start_x = TABLE_X + 600
        start_y = TABLE_Y + PLAY_HEIGHT // 2
        
        colors = [YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, MAROON, BLACK, 
                  YELLOW, BLUE, RED, PURPLE, ORANGE, GREEN, MAROON]
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        
        ball_idx = 0
        rows = 5
        for col in range(rows):
            for row in range(col + 1):
                x = start_x + (col * (BALL_RADIUS * 2 + 1))
                y = start_y - (col * BALL_RADIUS) + (row * (BALL_RADIUS * 2 + 1))
                
                num = numbers[ball_idx]
                if num == 8: c = BLACK
                elif num <= 7: c = colors[num-1]
                else: c = colors[num-9]
                
                self.balls.append(ObjectBall(x, y, c, num))
                ball_idx += 1
                if ball_idx >= 15: break
        
        self.turn = 1
        self.player_assignments = {1: None, 2: None}
        self.scores = {1: [], 2: []}
        self.is_moving = False
        self.ball_potted_this_turn = False
        self.message = "Break Shot!"
        self.message_timer = 120
        self.winner_text = ""

    def run(self):
        while True:
            mouse_pos = pygame.mouse.get_pos()
            events = pygame.event.get()
            
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # --- STATE HANDLING ---
                if self.state == STATE_MENU:
                    if self.btn_start.is_clicked(event): self.state = STATE_PLAYING
                    if self.btn_tutorial.is_clicked(event): self.state = STATE_TUTORIAL
                    if self.btn_settings.is_clicked(event): self.state = STATE_SETTINGS
                    if self.btn_quit.is_clicked(event): pygame.quit(); sys.exit()
                
                elif self.state == STATE_SETTINGS:
                    if self.btn_back.is_clicked(event): self.state = STATE_MENU
                    if self.btn_toggle_sound.is_clicked(event):
                        self.sound_manager.enabled = not self.sound_manager.enabled
                        status = "ON" if self.sound_manager.enabled else "OFF"
                        self.btn_toggle_sound.text = f"SOUND: {status}"
                        
                elif self.state == STATE_TUTORIAL:
                    if self.btn_back.is_clicked(event): self.state = STATE_MENU
                
                elif self.state == STATE_PLAYING:
                    # Tombol Pause Menu
                    if self.btn_pause_game.is_clicked(event):
                        self.state = STATE_PAUSED
                    
                    if self.btn_reset_match.is_clicked(event):
                        self.reset_game()

                    # Logic Stik hanya jalan jika tidak klik tombol
                    if not self.btn_pause_game.is_hovered and not self.btn_reset_match.is_hovered:
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            if not self.is_moving:
                                shot_fired = self.cue.handle_click()
                                if shot_fired: 
                                    self.is_moving = True
                                    self.sound_manager.play('hit')
                        
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                            self.cue.cancel_shot()
                
                elif self.state == STATE_PAUSED:
                    if self.btn_resume.is_clicked(event):
                        self.state = STATE_PLAYING
                    if self.btn_exit_to_menu.is_clicked(event):
                        self.reset_game()
                        self.state = STATE_MENU

                elif self.state == STATE_GAME_OVER:
                    if self.btn_play_again.is_clicked(event):
                        self.reset_game()
                        self.state = STATE_PLAYING
                    if self.btn_main_menu.is_clicked(event):
                        self.reset_game()
                        self.state = STATE_MENU

            # --- HOVER UPDATE & DRAW ---
            self.screen.fill(UI_BG)
            
            if self.state == STATE_MENU:
                self.btn_start.check_hover(mouse_pos)
                self.btn_tutorial.check_hover(mouse_pos)
                self.btn_settings.check_hover(mouse_pos)
                self.btn_quit.check_hover(mouse_pos)
                self.draw_menu()
                
            elif self.state == STATE_PLAYING:
                self.btn_pause_game.check_hover(mouse_pos)
                self.btn_reset_match.check_hover(mouse_pos)
                self.update_game_logic(mouse_pos)
                self.draw_game(mouse_pos)
                
            elif self.state == STATE_PAUSED:
                self.btn_resume.check_hover(mouse_pos)
                self.btn_exit_to_menu.check_hover(mouse_pos)
                self.draw_game(mouse_pos) # Draw game bg
                self.draw_paused() # Draw overlay
                
            elif self.state == STATE_TUTORIAL:
                self.btn_back.check_hover(mouse_pos)
                self.draw_tutorial()
                
            elif self.state == STATE_SETTINGS:
                self.btn_back.check_hover(mouse_pos)
                self.btn_toggle_sound.check_hover(mouse_pos)
                self.draw_settings()
                
            elif self.state == STATE_GAME_OVER:
                self.btn_play_again.check_hover(mouse_pos)
                self.btn_main_menu.check_hover(mouse_pos)
                self.draw_game_over()

            self.clock.tick(FPS)
            pygame.display.flip()

    def update_game_logic(self, mouse_pos):
        if not self.is_moving:
            self.cue.update(mouse_pos)
        
        moving_count = 0
        for ball in self.balls:
            if ball.potted: continue
            
            prev_vel = ball.velocity.length()
            ball.update()
            
            if ball.check_wall_collision(self.table.rect) and prev_vel > 2:
                pass
            
            if ball.check_pocket_collision(self.table.pockets):
                self.sound_manager.play('pocket')
                self.handle_pot(ball)
            
            if ball.velocity.length() > 0:
                moving_count += 1
        
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                b1 = self.balls[i]
                b2 = self.balls[j]
                if PhysicsEngine.resolve_collision(b1, b2):
                    impact = (b1.velocity - b2.velocity).length()
                    if impact > 1:
                        self.sound_manager.play('hit')

        if self.is_moving and moving_count == 0:
            self.is_moving = False
            self.cue.state = 0
            if self.state != STATE_GAME_OVER:
                self.switch_turn()
            
        if self.message_timer > 0: self.message_timer -= 1

    def handle_pot(self, ball):
        if ball.type == "cue":
            self.ball_potted_this_turn = False
            self.message = "FOUL! Cue Ball Potted"
            ball.reset()
        elif ball.type == "eight":
            current_player = self.turn
            p_type = self.player_assignments[current_player]
            has_won = False
            if p_type:
                target_nums = list(range(1, 8)) if p_type == 'solid' else list(range(9, 16))
                remaining = [b for b in self.balls if b.number in target_nums and not b.potted]
                if not remaining: has_won = True
                else: has_won = False
            else:
                has_won = False
            
            if has_won:
                self.winner_text = f"VICTORY! PLAYER {current_player} WINS!"
            else:
                winner = 2 if current_player == 1 else 1
                self.winner_text = f"GAME OVER! PLAYER {current_player} LOSE!"
            self.state = STATE_GAME_OVER
        else:
            if self.player_assignments[1] is None:
                if self.turn == 1:
                    self.player_assignments[1] = ball.type
                    self.player_assignments[2] = "stripe" if ball.type == "solid" else "solid"
                else:
                    self.player_assignments[2] = ball.type
                    self.player_assignments[1] = "stripe" if ball.type == "solid" else "solid"
            
            if self.player_assignments[self.turn] == ball.type or self.player_assignments[self.turn] is None:
                self.scores[self.turn].append(ball)
                self.ball_potted_this_turn = True
            else:
                opponent = 2 if self.turn == 1 else 1
                self.scores[opponent].append(ball)
                self.ball_potted_this_turn = False

    def switch_turn(self):
        if not self.ball_potted_this_turn:
            self.turn = 2 if self.turn == 1 else 1
            self.message = f"Turn: Player {self.turn}"
        else:
            self.message = f"Continue: Player {self.turn}"
        self.message_timer = 60
        self.ball_potted_this_turn = False

    # --- DRAW FUNCTIONS ---
    def draw_menu(self):
        title = self.title_font.render("BILLIARD SIMULATION", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        self.btn_start.draw(self.screen)
        self.btn_tutorial.draw(self.screen)
        self.btn_settings.draw(self.screen)
        self.btn_quit.draw(self.screen)

    def draw_settings(self):
        title = self.title_font.render("SETTINGS", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        self.btn_toggle_sound.draw(self.screen)
        self.btn_back.draw(self.screen)

    def draw_tutorial(self):
        title = self.title_font.render("HOW TO PLAY", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        lines = [
            "1. ARAHKAN mouse untuk membidik.",
            "2. KLIK KIRI sekali untuk MENGUNCI ARAH.",
            "3. TARIK MOUSE ke belakang untuk POWER.",
            "4. KLIK KIRI lagi untuk MENEMBAK.",
            "5. KLIK KANAN untuk membatalkan bidikan.",
        ]
        y = 150
        for line in lines:
            txt = self.font.render(line, True, TEXT_COLOR)
            self.screen.blit(txt, (SCREEN_WIDTH//2 - 200, y))
            y += 35
        self.btn_back.draw(self.screen)

    def draw_remaining_balls(self, player_num, start_x, start_y, align_left=True):
        p_type = self.player_assignments[player_num]
        if p_type is None:
            target_nums = list(range(1, 8)) if player_num == 1 else list(range(9, 16))
        else:
            target_nums = list(range(1, 8)) if p_type == 'solid' else list(range(9, 16))
            
        balls_to_draw = []
        for num in target_nums:
            ball_obj = next((b for b in self.balls if b.number == num), None)
            if ball_obj and not ball_obj.potted: balls_to_draw.append(num)

        spacing = 25
        for i, num in enumerate(balls_to_draw):
            color = self.ball_colors.get(num, WHITE)
            if align_left: pos_x = start_x + (i * spacing)
            else: pos_x = start_x - (i * spacing)
            
            pygame.draw.circle(self.screen, color, (pos_x, start_y), 10)
            if num > 8:
                pygame.draw.circle(self.screen, WHITE, (pos_x, start_y), 7)
                pygame.draw.rect(self.screen, color, (pos_x - 8, start_y - 3, 16, 6))

            txt = self.ui_ball_font.render(str(num), True, BLACK)
            txt_rect = txt.get_rect(center=(pos_x, start_y))
            self.screen.blit(txt, txt_rect)

    def draw_game(self, mouse_pos):
        pygame.draw.rect(self.screen, DARK_GREY, (0, 0, SCREEN_WIDTH, 80))
        
        p1_type = self.player_assignments[1] if self.player_assignments[1] else "OPEN"
        p1_color = ACCENT_COLOR if self.turn == 1 else GREY
        p1_text = self.font.render(f"PLAYER 1 ({p1_type.upper()})", True, p1_color)
        self.screen.blit(p1_text, (50, 20))
        self.draw_remaining_balls(1, 50, 55, align_left=True)
            
        p2_type = self.player_assignments[2] if self.player_assignments[2] else "OPEN"
        p2_color = ACCENT_COLOR if self.turn == 2 else GREY
        p2_text = self.font.render(f"PLAYER 2 ({p2_type.upper()})", True, p2_color)
        p2_rect = p2_text.get_rect(topright=(SCREEN_WIDTH - 150, 20)) # Geser sedikit agar muat tombol pause
        self.screen.blit(p2_text, p2_rect)
        self.draw_remaining_balls(2, SCREEN_WIDTH - 150, 55, align_left=False)

        # Power Bar
        bar_x, bar_y = SCREEN_WIDTH // 2 - 100, 25
        bar_w, bar_h = 200, 30
        pygame.draw.rect(self.screen, BLACK, (bar_x, bar_y, bar_w, bar_h), border_radius=5)
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=5)
        
        ratio = self.cue.power / self.cue.max_power
        if ratio > 0:
            fill_w = int((bar_w - 4) * ratio)
            fill_color = (255, int(255 * (1 - ratio)), 0) 
            pygame.draw.rect(self.screen, fill_color, (bar_x + 2, bar_y + 2, fill_w, bar_h - 4), border_radius=3)
        
        pow_txt = self.ball_font.render("POWER", True, WHITE)
        self.screen.blit(pow_txt, (bar_x + bar_w // 2 - pow_txt.get_width() // 2, bar_y + 8))

        self.table.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen, self.ball_font)
            
        if not self.is_moving and self.state != STATE_PAUSED:
            self.cue.draw(self.screen, self.balls, self.table.rect)
            
        if self.message_timer > 0:
            msg_surf = self.title_font.render(self.message, True, WHITE)
            msg_rect = msg_surf.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            bg_rect = msg_rect.inflate(40, 20)
            pygame.draw.rect(self.screen, (0,0,0,180), bg_rect, border_radius=10)
            self.screen.blit(msg_surf, msg_rect)
            
        self.btn_reset_match.draw(self.screen)
        self.btn_pause_game.draw(self.screen)

    def draw_paused(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        
        text = self.title_font.render("GAME PAUSED", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(text, rect)
        
        self.btn_resume.draw(self.screen)
        self.btn_exit_to_menu.draw(self.screen)

    def draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        
        color = GREEN if "WINS" in self.winner_text else RED
        text = self.title_font.render(self.winner_text, True, color)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
        self.screen.blit(text, rect)
        
        self.btn_play_again.draw(self.screen)
        self.btn_main_menu.draw(self.screen)

if __name__ == "__main__":
    game = GameManager()
    game.run()