import pygame
import sys
import os
import array
from config import *
from ball import CueBall, ObjectBall
from table import Table
from cue import Cue
from physics import PhysicsEngine

# Tambahan State untuk Menu Team
STATE_TEAM = "team"

class SoundGenerator:
    """Class untuk menghasilkan efek suara sintetis tanpa file eksternal"""
    def __init__(self):
        self.enabled = True
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.sounds = {}
            self.sounds['hit'] = self._generate_beep(400, 0.1)    
            self.sounds['pocket'] = self._generate_beep(800, 0.2) 
            self.has_mixer = True
        except Exception:
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
        # Shadow effect
        pygame.draw.rect(surface, (10, 10, 10), (self.rect.x + 2, self.rect.y + 2, self.rect.w, self.rect.h), border_radius=8)
        # Main button
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

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Billiard - DPBO Kelompok 8")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 18)
        self.debug_font = pygame.font.SysFont('Consolas', 14) # Font khusus debug
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)
        self.header_font = pygame.font.SysFont('Arial', 28, bold=True) # Font untuk header panel
        self.ball_font = pygame.font.SysFont('Arial', 10, bold=True)
        self.ui_ball_font = pygame.font.SysFont('Arial', 12, bold=True)
        
        self.state = STATE_MENU
        self.sound_manager = SoundGenerator()

        self.ball_colors = {
            1: YELLOW, 2: BLUE, 3: RED, 4: PURPLE, 5: ORANGE, 6: GREEN, 7: MAROON,
            9: YELLOW, 10: BLUE, 11: RED, 12: PURPLE, 13: ORANGE, 14: GREEN, 15: MAROON,
            8: BLACK
        }

        # --- SENSITIVITY SETTINGS ---
        self.sens_values = [0.5, 1.0, 1.5]
        self.sens_names = ["LOW", "NORMAL", "HIGH"]
        self.current_sens_idx = 0 # Default: Low (0.5)

        self.reset_game()
        
        # Inisialisasi Tombol UI
        cx = SCREEN_WIDTH // 2
        
        # --- MENU UTAMA ---
        # Mengatur ulang posisi agar muat tombol Team
        start_y_menu = 280
        gap = 60
        self.btn_start = Button(cx - 100, start_y_menu, 200, 50, "PLAY GAME")
        self.btn_tutorial = Button(cx - 100, start_y_menu + gap, 200, 50, "TUTORIAL")
        self.btn_team = Button(cx - 100, start_y_menu + gap * 2, 200, 50, "OUR TEAM") # Tombol Baru
        self.btn_settings = Button(cx - 100, start_y_menu + gap * 3, 200, 50, "SETTINGS")
        self.btn_quit = Button(cx - 100, start_y_menu + gap * 4, 200, 50, "QUIT")
        
        # --- SUB MENUS (Common Back Button) ---
        # Kita sesuaikan posisi tombol back agar ada di dalam panel nanti
        self.btn_back_panel = Button(cx - 100, 550, 200, 40, "BACK", GREY)
        
        # --- SETTINGS UI ---
        self.btn_toggle_sound = Button(cx - 100, 300, 200, 50, "SOUND: ON")
        current_sens_name = self.sens_names[self.current_sens_idx]
        self.btn_sensitivity = Button(cx - 100, 370, 200, 50, f"SENSITIVITY: {current_sens_name}")
        
        # --- IN GAME UI ---
        # Tombol Pause (Pojok Kanan Atas)
        self.btn_pause_game = Button(SCREEN_WIDTH - 120, 20, 100, 40, "MENU", GREY)
        
        # --- PAUSE MENU UI ---
        self.btn_resume = Button(cx - 100, SCREEN_HEIGHT//2 - 60, 200, 50, "RESUME", ACCENT_COLOR)
        self.btn_restart = Button(cx - 100, SCREEN_HEIGHT//2 + 10, 200, 50, "RESTART MATCH", RED)
        self.btn_exit_to_menu = Button(cx - 100, SCREEN_HEIGHT//2 + 80, 200, 50, "MAIN MENU", GREY)
        
        # --- GAME OVER UI ---
        self.btn_play_again = Button(cx - 100, 380, 200, 50, "PLAY AGAIN", ACCENT_COLOR)
        self.btn_main_menu = Button(cx - 100, 450, 200, 50, "MAIN MENU", GREY)

    def reset_game(self):
        self.table = Table()
        self.cue_ball = CueBall(TABLE_X + 200, TABLE_Y + PLAY_HEIGHT // 2)
        self.balls = [self.cue_ball]
        
        # Create Cue and apply current sensitivity
        self.cue = Cue(self.cue_ball)
        self.cue.sensitivity = self.sens_values[self.current_sens_idx]
        
        start_x = TABLE_X + 600
        start_y = TABLE_Y + PLAY_HEIGHT // 2
        
        # Susunan bola 8-ball (Triangle rack)
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
                
                if self.state == STATE_MENU:
                    if self.btn_start.is_clicked(event): self.state = STATE_PLAYING
                    if self.btn_tutorial.is_clicked(event): self.state = STATE_TUTORIAL
                    if self.btn_team.is_clicked(event): self.state = STATE_TEAM
                    if self.btn_settings.is_clicked(event): self.state = STATE_SETTINGS
                    if self.btn_quit.is_clicked(event): pygame.quit(); sys.exit()
                
                elif self.state == STATE_SETTINGS:
                    if self.btn_back_panel.is_clicked(event): self.state = STATE_MENU
                    
                    if self.btn_toggle_sound.is_clicked(event):
                        self.sound_manager.enabled = not self.sound_manager.enabled
                        status = "ON" if self.sound_manager.enabled else "OFF"
                        self.btn_toggle_sound.text = f"SOUND: {status}"

                    if self.btn_sensitivity.is_clicked(event):
                        self.current_sens_idx = (self.current_sens_idx + 1) % 3
                        val = self.sens_values[self.current_sens_idx]
                        name = self.sens_names[self.current_sens_idx]
                        
                        self.btn_sensitivity.text = f"SENSITIVITY: {name}"
                        if self.cue:
                            self.cue.sensitivity = val
                        
                elif self.state == STATE_TUTORIAL:
                    if self.btn_back_panel.is_clicked(event): self.state = STATE_MENU
                
                elif self.state == STATE_TEAM:
                    if self.btn_back_panel.is_clicked(event): self.state = STATE_MENU

                elif self.state == STATE_PLAYING:
                    if self.btn_pause_game.is_clicked(event):
                        self.state = STATE_PAUSED
                    
                    if not self.btn_pause_game.is_hovered:
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
                    if self.btn_restart.is_clicked(event):
                        self.reset_game()
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

            self.screen.fill(UI_BG)
            
            if self.state == STATE_MENU:
                self.btn_start.check_hover(mouse_pos)
                self.btn_tutorial.check_hover(mouse_pos)
                self.btn_team.check_hover(mouse_pos)
                self.btn_settings.check_hover(mouse_pos)
                self.btn_quit.check_hover(mouse_pos)
                self.draw_menu()
                
            elif self.state == STATE_PLAYING:
                self.btn_pause_game.check_hover(mouse_pos)
                self.update_game_logic(mouse_pos)
                self.draw_game(mouse_pos)
                
            elif self.state == STATE_PAUSED:
                self.btn_resume.check_hover(mouse_pos)
                self.btn_restart.check_hover(mouse_pos)
                self.btn_exit_to_menu.check_hover(mouse_pos)
                self.draw_game(mouse_pos)
                self.draw_paused()
                
            elif self.state == STATE_TUTORIAL:
                self.btn_back_panel.check_hover(mouse_pos)
                self.draw_tutorial()

            elif self.state == STATE_TEAM:
                self.btn_back_panel.check_hover(mouse_pos)
                self.draw_team()
                
            elif self.state == STATE_SETTINGS:
                self.btn_back_panel.check_hover(mouse_pos)
                self.btn_toggle_sound.check_hover(mouse_pos)
                self.btn_sensitivity.check_hover(mouse_pos)
                self.draw_settings()
                
            elif self.state == STATE_GAME_OVER:
                self.btn_play_again.check_hover(mouse_pos)
                self.btn_main_menu.check_hover(mouse_pos)
                self.draw_game_over()

            if DEBUG_MODE:
                self.draw_debug_info()

            self.clock.tick(FPS)
            pygame.display.flip()

    def update_game_logic(self, mouse_pos):
        if not self.is_moving:
            self.cue.update(mouse_pos)
        
        # --- PHYSICS SUB-STEPPING (SOLUSI TUNNELING) ---
        physics_steps = 10 
        
        for _ in range(physics_steps):
            for ball in self.balls:
                if ball.potted: continue
                
                ball.pos += ball.velocity / physics_steps
                
                ball.check_wall_collision(self.table.rect)
                
                if ball.check_pocket_collision(self.table.pockets):
                    self.sound_manager.play('pocket')
                    self.handle_pot(ball)
            
            for i in range(len(self.balls)):
                for j in range(i + 1, len(self.balls)):
                    b1 = self.balls[i]
                    b2 = self.balls[j]
                    if PhysicsEngine.resolve_collision(b1, b2):
                        impact = (b1.velocity - b2.velocity).length()
                        if impact > 1:
                            self.sound_manager.play('hit')

        moving_count = 0
        for ball in self.balls:
            if ball.potted: continue
            
            if ball.velocity.length() > 0.05:
                ball.velocity *= ball.friction
                moving_count += 1
            else:
                ball.velocity = pygame.math.Vector2(0, 0)

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

    def draw_menu(self):
        title = self.title_font.render("BILLIARD SIMULATION", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 120))
        
        self.btn_start.draw(self.screen)
        self.btn_tutorial.draw(self.screen)
        self.btn_team.draw(self.screen) # Draw tombol Team
        self.btn_settings.draw(self.screen)
        self.btn_quit.draw(self.screen)

    # --- Helper Method untuk Panel yang Konsisten ---
    def draw_panel(self, title, height=450):
        # 1. Overlay Gelap Transparan
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        
        # 2. Panel Utama
        panel_w, panel_h = 600, height
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        
        # Shadow
        pygame.draw.rect(self.screen, (10, 10, 10), (panel_x + 5, panel_y + 5, panel_w, panel_h), border_radius=15)
        # Background Panel
        pygame.draw.rect(self.screen, DARK_GREY, (panel_x, panel_y, panel_w, panel_h), border_radius=15)
        # Border Panel
        pygame.draw.rect(self.screen, ACCENT_COLOR, (panel_x, panel_y, panel_w, panel_h), 2, border_radius=15)
        
        # 3. Header Title
        title_surf = self.header_font.render(title, True, ACCENT_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH//2, panel_y + 40))
        self.screen.blit(title_surf, title_rect)
        
        # Garis pemisah di bawah judul
        pygame.draw.line(self.screen, GREY, (panel_x + 50, panel_y + 70), (panel_x + panel_w - 50, panel_y + 70), 2)
        
        return panel_x, panel_y, panel_w, panel_h

    def draw_settings(self):
        self.draw_panel("SETTINGS")
        
        # Tombol-tombol di dalam panel
        self.btn_toggle_sound.draw(self.screen)
        self.btn_sensitivity.draw(self.screen)
        self.btn_back_panel.draw(self.screen)

    def draw_tutorial(self):
        panel_x, panel_y, panel_w, panel_h = self.draw_panel("HOW TO PLAY")
        
        lines = [
            ("Arahkan Mouse", "Untuk membidik bola sasaran."),
            ("Klik Kiri (1x)", "Mengunci arah (Aim Lock)."),
            ("Tarik Mouse", "Mengatur kekuatan (Power)."),
            ("Klik Kiri (2x)", "Melepaskan tembakan."),
            ("Klik Kanan", "Membatalkan tembakan/kunci."),
            ("Tombol Menu", "Pause permainan."),
        ]
        
        start_y_text = panel_y + 100
        for action, desc in lines:
            # Action (Bold/Accent)
            act_surf = self.font.render(action, True, ACCENT_COLOR)
            self.screen.blit(act_surf, (panel_x + 50, start_y_text))
            
            # Description (White)
            desc_surf = self.font.render(f":  {desc}", True, WHITE)
            self.screen.blit(desc_surf, (panel_x + 200, start_y_text))
            
            start_y_text += 40
            
        self.btn_back_panel.draw(self.screen)

    def draw_team(self):
        panel_x, panel_y, panel_w, panel_h = self.draw_panel("OUR TEAM")
        
        # Silakan edit nama-nama di bawah ini sesuai anggota kelompok Anda
        team_members = [
            "Muhammad Daffa Ramdhani (1313624025)",
            "Ricky Darmawan (1313624007)",
            "Muhammad Fabio Usama (1313624054)",
        ]
        
        start_y_text = panel_y + 120
        for member in team_members:
            txt_surf = self.font.render(member, True, WHITE)
            txt_rect = txt_surf.get_rect(center=(SCREEN_WIDTH//2, start_y_text))
            self.screen.blit(txt_surf, txt_rect)
            start_y_text += 45
            
        self.btn_back_panel.draw(self.screen)

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
        
        # Indicator Player 1
        p1_type = self.player_assignments[1] if self.player_assignments[1] else "OPEN"
        p1_color = ACCENT_COLOR if self.turn == 1 else GREY
        p1_text = self.font.render(f"PLAYER 1 ({p1_type.upper()})", True, p1_color)
        self.screen.blit(p1_text, (50, 20))
        # Active Player Marker
        if self.turn == 1:
            pygame.draw.circle(self.screen, ACCENT_COLOR, (30, 30), 5)
        self.draw_remaining_balls(1, 50, 55, align_left=True)
            
        # Indicator Player 2
        p2_type = self.player_assignments[2] if self.player_assignments[2] else "OPEN"
        p2_color = ACCENT_COLOR if self.turn == 2 else GREY
        p2_text = self.font.render(f"PLAYER 2 ({p2_type.upper()})", True, p2_color)
        p2_rect = p2_text.get_rect(topright=(SCREEN_WIDTH - 150, 20))
        self.screen.blit(p2_text, p2_rect)
        # Active Player Marker
        if self.turn == 2:
            pygame.draw.circle(self.screen, ACCENT_COLOR, (SCREEN_WIDTH - 30, 30), 5)
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
            
        self.btn_pause_game.draw(self.screen)

    def draw_paused(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0,0))
        
        text = self.title_font.render("GAME PAUSED", True, WHITE)
        rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120))
        self.screen.blit(text, rect)
        
        self.btn_resume.draw(self.screen)
        self.btn_restart.draw(self.screen)
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

    def draw_debug_info(self):
        """Menampilkan informasi debug (FPS, Jumlah Objek)"""
        fps = int(self.clock.get_fps())
        fps_text = self.debug_font.render(f"FPS: {fps}", True, GREEN)
        obj_text = self.debug_font.render(f"Balls: {len([b for b in self.balls if not b.potted])}", True, GREEN)
        
        self.screen.blit(fps_text, (10, SCREEN_HEIGHT - 30))
        self.screen.blit(obj_text, (10, SCREEN_HEIGHT - 15))

if __name__ == "__main__":
    game = GameManager()
    game.run()