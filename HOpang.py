#!/usr/bin/env python3
"""
🌟 HO_GAME - 매치-3 퍼즐 게임 & 테트리스 🌟
5세 남자아이를 위한 귀여운 게임 모음
"""

import pygame
import random
import math
import sys
import os

# ─── 초기화 ───
pygame.init()

# ─── 화면 설정 ───
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 850
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🌟 HO_GAME 🌟")

# ─── 게임 상태 ───
GAME_STATE = "menu"  # menu, anipang, hotris

# ─── 색상 ───
WHITE = (255, 255, 255)
BG_COLOR = (255, 245, 230)  # 따뜻한 크림색 배경
GRID_BG = (255, 253, 245)
HIGHLIGHT_COLOR = (255, 200, 50)
SCORE_COLOR = (255, 120, 80)
TITLE_COLOR = (255, 100, 130)
COMBO_COLORS = [
    (255, 100, 100),
    (255, 165, 0),
    (255, 215, 0),
    (0, 200, 100),
    (100, 150, 255),
]
SHADOW_COLOR = (0, 0, 0, 30)

# ─── 보드 설정 ───
COLS = 7
ROWS = 7
CELL_SIZE = 80
BOARD_PADDING = 8
BOARD_X = (SCREEN_WIDTH - COLS * CELL_SIZE) // 2
BOARD_Y = 200

# ─── 공룡 캐릭터 ───
ANIMALS = ["🦕", "🦖", "🦎", "🐊", "🥚", "🦴", "🌋"]
ANIMAL_NAMES = ["티라노", "트리케라", "브라키오", "스테고", "프테라", "안킬로", "아기공룡"]
ANIMAL_COLORS = [
    (130, 200, 130),  # 티라노 - 초록
    (140, 180, 230),  # 트리케라 - 파랑
    (240, 220, 130),  # 브라키오 - 노랑
    (190, 150, 220),  # 스테고 - 보라
    (255, 180, 200),  # 프테라 - 분홍
    (240, 180, 120),  # 안킬로 - 주황
    (240, 140, 140),  # 아기공룡 - 빨강
]

# ─── 폰트 설정 ───
def get_korean_font(size):
    """한글 폰트 로드 (파일 경로 방식)"""
    font_paths = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except:
                continue
    return pygame.font.Font(None, size)


def get_font(size):
    """일반 폰트 로드 (파일 경로 방식)"""
    font_paths = [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/System/Library/Fonts/Supplemental/AppleGothic.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return pygame.font.Font(path, size)
            except:
                continue
    return pygame.font.Font(None, size)


emoji_font = get_font(48)
title_font = get_korean_font(48)
score_font = get_korean_font(36)
small_font = get_korean_font(24)
combo_font = get_korean_font(60)
message_font = get_korean_font(28)

# ─── 공룡 / 현오 스프라이트 ───
DINOSAUR_SPRITES = []
HYUNO_SPRITES = []

# 개별 공룡 아이콘 이미지 경로들 (6종) - 공룡팡 모드
DINOSAUR_IMAGE_PATHS = [
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-43c9ed41-1a1b-4699-a7fb-c7fc8228e542.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-4e88f852-9c97-4aa9-8cba-1d901a72e444.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-4bd9558a-a785-4f02-8ad0-216a8c3d0486.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-3ce74f8b-1b88-42d1-ac58-7a608a9c3dbd.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-1ff5360f-3686-4f8d-a4b5-feda37ea207c.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-64b98373-3cab-432d-b15a-8fa25140a30a.png",
]

# 현오 얼굴 아이콘 이미지 경로들 (6종) - 현오팡 모드
HYUNO_IMAGE_PATHS = [
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-26c45160-0310-4cd7-8898-e90c2fe19e41.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-edcc5d83-c717-4761-812d-c96d20deb328.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-f8ff3f44-f67c-430f-a570-5aabd4f66193.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-2c54d084-3510-4dfe-927b-60c9511c2674.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-b68c44fe-cba0-4ec3-ad86-8801175a4144.png",
    "/Users/sy.im/.cursor/projects/Users-sy-im-anipang-game/assets/image-a97428dc-1edb-4bbe-b526-1fd06ba74748.png",
]

try:
    target_size = CELL_SIZE - 8  # 셀 안에서 최대한 크게 보이도록
    for path in DINOSAUR_IMAGE_PATHS:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            scaled = pygame.transform.smoothscale(img, (target_size, target_size))
            DINOSAUR_SPRITES.append(scaled)
    for path in HYUNO_IMAGE_PATHS:
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            scaled = pygame.transform.smoothscale(img, (target_size, target_size))
            HYUNO_SPRITES.append(scaled)
except:
    DINOSAUR_SPRITES = []
    HYUNO_SPRITES = []


# ─── 파티클 클래스 ───
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.5, 1.2)
        self.max_life = self.life
        self.size = random.randint(4, 12)
        self.shape = random.choice(["circle", "star", "heart"])

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += 5 * dt  # 약한 중력
        self.life -= dt
        return self.life > 0

    def draw(self, surface):
        alpha = max(0, self.life / self.max_life)
        size = int(self.size * alpha)
        if size < 1:
            return

        r, g, b = self.color
        color = (r, g, b)

        if self.shape == "circle":
            pygame.draw.circle(surface, color, (int(self.x), int(self.y)), size)
        elif self.shape == "star":
            self._draw_star(surface, color, int(self.x), int(self.y), size)
        elif self.shape == "heart":
            self._draw_heart(surface, color, int(self.x), int(self.y), size)

    def _draw_star(self, surface, color, cx, cy, size):
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            r = size if i % 2 == 0 else size // 2
            points.append((cx + r * math.cos(angle), cy - r * math.sin(angle)))
        if len(points) >= 3:
            pygame.draw.polygon(surface, color, points)

    def _draw_heart(self, surface, color, cx, cy, size):
        pygame.draw.circle(surface, color, (cx - size // 3, cy - size // 4), size // 2)
        pygame.draw.circle(surface, color, (cx + size // 3, cy - size // 4), size // 2)
        points = [
            (cx - size // 1.5, cy),
            (cx, cy + size // 1.2),
            (cx + size // 1.5, cy),
        ]
        pygame.draw.polygon(surface, color, points)


# ─── 떠다니는 메시지 ───
class FloatingText:
    def __init__(self, text, x, y, color, size=40):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life = 1.5
        self.max_life = 1.5
        self.font = get_korean_font(size)
        self.scale = 0.5

    def update(self, dt):
        self.y -= 40 * dt
        self.life -= dt
        if self.life > self.max_life * 0.7:
            self.scale = min(1.2, self.scale + 4 * dt)
        else:
            self.scale = max(0, self.scale - 0.5 * dt)
        return self.life > 0

    def draw(self, surface):
        alpha = max(0, min(255, int(255 * (self.life / self.max_life))))
        text_surface = self.font.render(self.text, True, self.color)
        w = int(text_surface.get_width() * self.scale)
        h = int(text_surface.get_height() * self.scale)
        if w > 0 and h > 0:
            scaled = pygame.transform.scale(text_surface, (w, h))
            surface.blit(scaled, (self.x - w // 2, self.y - h // 2))


# ─── 게임 클래스 ───
class AnipangGame:
    def __init__(self):
        self.board = [[0] * COLS for _ in range(ROWS)]
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.state = "playing"  # playing, swapping, removing, falling, gameover
        self.particles = []
        self.floating_texts = []
        self.swap_progress = 0
        self.swap_cells = None
        self.remove_cells = []
        self.remove_progress = 0
        self.fall_data = []
        self.fall_progress = 0
        self.time_left = 90  # 90초
        self.bg_hue = 0
        self.star_positions = [
            (random.randint(0, SCREEN_WIDTH), random.randint(0, 180))
            for _ in range(20)
        ]
        self.star_twinkle = [random.uniform(0, math.pi * 2) for _ in range(20)]
        self.moves = 0
        self.encouragements = [
            "잘했어! ⭐",
            "대단해! 🌟",
            "최고야! 🎉",
            "멋져! ✨",
            "와아! 🌈",
            "굉장해! 🎊",
            "짝짝짝! 👏",
        ]

        # 배경 음악 채널
        self.bgm_channel = None

        # 모드: "dino" (공룡팡), "hyuno" (현오팡)
        self.mode = "dino"

        # 게임 시작 여부 및 버튼
        self.game_started = False
        button_w, button_h = 130, 44
        gap = 18
        center_x = SCREEN_WIDTH // 2
        button_y = 150
        self.start_button = pygame.Rect(center_x - button_w // 2, button_y, button_w, button_h)
        self.restart_button = pygame.Rect(
            center_x - button_w - gap - button_w // 2, button_y, button_w, button_h
        )
        self.quit_button = pygame.Rect(
            center_x + button_w // 2 + gap, button_y, button_w, button_h
        )

        # 모드 선택 버튼 (상단 양쪽)
        mode_button_w, mode_button_h = 120, 34
        self.dino_mode_button = pygame.Rect(30, 30, mode_button_w, mode_button_h)
        self.hyuno_mode_button = pygame.Rect(
            SCREEN_WIDTH - 30 - mode_button_w, 30, mode_button_w, mode_button_h
        )

        # 드래그 관련 상태
        self.dragging = False
        self.drag_start = None       # (row, col)
        self.drag_start_pos = None   # (px_x, px_y)
        self.drag_current_pos = None # 드래그 중 현재 마우스 픽셀 좌표

        # 보드 초기화 (매치 없이)
        self.init_board()

        # 현재 버전에서는 소리를 사용하지 않으므로 빈 딕셔너리만 유지
        self.sounds = {}

    def play_sound(self, name):
        # 현재 버전에서는 소리를 사용하지 않음
        return

    def start_bgm(self):
        """배경 음악 비활성화 상태"""
        return

    def stop_bgm(self):
        """배경 음악 비활성화 상태"""
        return

    def init_board(self):
        """매치 없이 보드 초기화"""
        for row in range(ROWS):
            for col in range(COLS):
                choices = list(range(len(ANIMALS)))
                # 왼쪽 2칸 확인
                if col >= 2:
                    if self.board[row][col - 1] == self.board[row][col - 2]:
                        val = self.board[row][col - 1]
                        if val in choices:
                            choices.remove(val)
                # 위쪽 2칸 확인
                if row >= 2:
                    if self.board[row - 1][col] == self.board[row - 2][col]:
                        val = self.board[row - 1][col]
                        if val in choices:
                            choices.remove(val)
                self.board[row][col] = random.choice(choices)

    def get_cell(self, mx, my):
        """마우스 좌표 → 셀 좌표"""
        col = (mx - BOARD_X) // CELL_SIZE
        row = (my - BOARD_Y) // CELL_SIZE
        if 0 <= row < ROWS and 0 <= col < COLS:
            return row, col
        return None

    def find_matches(self):
        """매치 찾기"""
        matched = set()
        # 가로 매치
        for row in range(ROWS):
            for col in range(COLS - 2):
                val = self.board[row][col]
                if val is not None and val == self.board[row][col + 1] == self.board[row][col + 2]:
                    matched.add((row, col))
                    matched.add((row, col + 1))
                    matched.add((row, col + 2))
        # 세로 매치
        for row in range(ROWS - 2):
            for col in range(COLS):
                val = self.board[row][col]
                if val is not None and val == self.board[row + 1][col] == self.board[row + 2][col]:
                    matched.add((row, col))
                    matched.add((row + 1, col))
                    matched.add((row + 2, col))
        return matched

    def handle_mouse_down(self, mx, my):
        """드래그 시작"""
        # 모드 선택 버튼 먼저 확인
        if self.dino_mode_button.collidepoint(mx, my):
            self.mode = "dino"
            return
        if self.hyuno_mode_button.collidepoint(mx, my):
            self.mode = "hyuno"
            return

        # 게임 컨트롤 버튼 확인
        if self.start_button.collidepoint(mx, my):
            if self.state != "gameover":
                self.game_started = True
                self.start_bgm()
            return
        if self.restart_button.collidepoint(mx, my):
            self.restart()
            return
        if self.quit_button.collidepoint(mx, my):
            pygame.quit()
            sys.exit()

        if self.state != "playing" or not self.game_started:
            return

        cell = self.get_cell(mx, my)
        if cell is None:
            return

        self.dragging = True
        self.drag_start = cell
        self.drag_start_pos = (mx, my)
        self.drag_current_pos = (mx, my)
        self.play_sound("select")

    def handle_mouse_up(self, mx, my):
        """드래그 종료 → 방향 판정 후 스왑"""
        if not self.dragging or self.drag_start is None:
            self.dragging = False
            self.drag_start = None
            self.drag_start_pos = None
            return

        self.dragging = False
        start_row, start_col = self.drag_start
        sx, sy = self.drag_start_pos

        dx = mx - sx
        dy = my - sy
        threshold = CELL_SIZE // 3

        self.drag_start = None
        self.drag_start_pos = None
        self.drag_current_pos = None

        # 드래그 거리가 충분한지 확인
        if abs(dx) < threshold and abs(dy) < threshold:
            return

        # 상하좌우 중 가장 큰 축 방향으로 스왑
        if abs(dx) >= abs(dy):
            # 좌우
            target_col = start_col + (1 if dx > 0 else -1)
            target_row = start_row
        else:
            # 상하
            target_row = start_row + (1 if dy > 0 else -1)
            target_col = start_col

        # 보드 범위 확인
        if 0 <= target_row < ROWS and 0 <= target_col < COLS:
            self.start_swap((start_row, start_col), (target_row, target_col))

    def handle_mouse_move(self, mx, my):
        """드래그 중 마우스 위치 업데이트"""
        if self.dragging:
            self.drag_current_pos = (mx, my)

    def start_swap(self, cell1, cell2):
        """스왑 애니메이션 시작"""
        self.state = "swapping"
        self.swap_cells = (cell1, cell2)
        self.swap_progress = 0

    def do_swap(self, cell1, cell2):
        """실제 스왑 수행"""
        r1, c1 = cell1
        r2, c2 = cell2
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]

    def start_remove(self, matched):
        """제거 애니메이션 시작"""
        self.state = "removing"
        self.remove_cells = list(matched)
        self.remove_progress = 0

        # 점수 계산
        self.combo += 1
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        points = len(matched) * 10 * self.combo
        self.score += points

        # 파티클 & 텍스트 효과
        for row, col in matched:
            cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
            cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
            animal_idx = self.board[row][col]
            color = ANIMAL_COLORS[animal_idx] if animal_idx is not None else (255, 200, 100)
            for _ in range(8):
                self.particles.append(Particle(cx, cy, color))

        # 콤보 또는 격려 메시지
        center_x = BOARD_X + COLS * CELL_SIZE // 2
        center_y = BOARD_Y + ROWS * CELL_SIZE // 2

        if self.combo >= 2:
            combo_text = f"{self.combo} 콤보!"
            color = COMBO_COLORS[min(self.combo - 1, len(COMBO_COLORS) - 1)]
            self.floating_texts.append(
                FloatingText(combo_text, center_x, center_y - 30, color, 55)
            )
            self.play_sound("combo")
        else:
            if random.random() < 0.4:
                msg = random.choice(self.encouragements)
                self.floating_texts.append(
                    FloatingText(msg, center_x, center_y - 30, (255, 150, 50), 40)
                )
                # "짝짝짝!" 문구일 때는 박수 소리 재생
                if "짝짝짝" in msg:
                    self.play_sound("clap")

        self.play_sound("match")
        self.moves += 1

    def apply_gravity(self):
        """블록 떨어뜨리기"""
        self.fall_data = []
        for col in range(COLS):
            empty_rows = []
            for row in range(ROWS - 1, -1, -1):
                if self.board[row][col] is None:
                    empty_rows.append(row)
                elif empty_rows:
                    target_row = empty_rows.pop(0)
                    self.fall_data.append((row, col, target_row, col, self.board[row][col]))
                    self.board[target_row][col] = self.board[row][col]
                    self.board[row][col] = None
                    empty_rows.append(row)

            # 새 블록 생성
            for i, row in enumerate(sorted(empty_rows)):
                new_val = random.randint(0, len(ANIMALS) - 1)
                self.board[row][col] = new_val
                from_row = -(len(empty_rows) - i)
                self.fall_data.append((from_row, col, row, col, new_val))

        if self.fall_data:
            self.state = "falling"
            self.fall_progress = 0
        else:
            self.check_after_fall()

    def check_after_fall(self):
        """떨어진 후 매치 확인"""
        matched = self.find_matches()
        if matched:
            self.start_remove(matched)
        else:
            self.combo = 0
            self.state = "playing"

    def update(self, dt):
        """게임 상태 업데이트"""
        # 배경 효과
        self.bg_hue = (self.bg_hue + 10 * dt) % 360
        for i in range(len(self.star_twinkle)):
            self.star_twinkle[i] += random.uniform(1, 3) * dt

        # 파티클 업데이트
        self.particles = [p for p in self.particles if p.update(dt)]

        # 떠다니는 텍스트 업데이트
        self.floating_texts = [t for t in self.floating_texts if t.update(dt)]

        # 타이머 (시작 버튼을 누른 뒤부터 감소)
        if self.state == "playing" and self.time_left > 0 and self.game_started:
            self.time_left -= dt
            if self.time_left <= 0:
                self.time_left = 0
                self.state = "gameover"
                # 시간 종료 시 배경 음악 정지
                self.stop_bgm()

        # 스왑 애니메이션
        if self.state == "swapping":
            self.swap_progress += dt * 4
            if self.swap_progress >= 1:
                self.swap_progress = 1
                cell1, cell2 = self.swap_cells
                self.do_swap(cell1, cell2)
                matched = self.find_matches()
                if matched:
                    self.start_remove(matched)
                else:
                    # 매치 없으면 되돌리기
                    self.do_swap(cell1, cell2)
                    self.state = "playing"
                self.swap_cells = None

        # 제거 애니메이션
        if self.state == "removing":
            self.remove_progress += dt * 4
            if self.remove_progress >= 1:
                for row, col in self.remove_cells:
                    self.board[row][col] = None
                self.remove_cells = []
                self.apply_gravity()

        # 낙하 애니메이션
        if self.state == "falling":
            self.fall_progress += dt * 5
            if self.fall_progress >= 1:
                self.fall_progress = 1
                self.fall_data = []
                self.check_after_fall()

    def draw_rounded_rect(self, surface, color, rect, radius):
        """둥근 사각형 그리기"""
        x, y, w, h = rect
        pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
        pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
        pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)

    def draw_cute_animal(self, surface, animal_idx, cx, cy, size=40, alpha=1.0):
        """귀여운 캐릭터 그리기 (스프라이트 우선 사용)"""
        sprites = None
        if self.mode == "hyuno" and HYUNO_SPRITES:
            sprites = HYUNO_SPRITES
        elif DINOSAUR_SPRITES:
            sprites = DINOSAUR_SPRITES

        if sprites:
            sprite = sprites[animal_idx % len(sprites)]
            # 요청된 사이즈와 셀 크기에 맞게 크기 조정 (너무 커서 잘리지 않도록 제한)
            max_size = CELL_SIZE - 8  # 셀 내부보다 약간 작게
            scale = max(24, min(int(size), max_size))
            img = pygame.transform.smoothscale(sprite, (scale, scale))
            rect = img.get_rect(center=(cx, cy))
            surface.blit(img, rect)
            return

        # 스프라이트 로딩에 실패했을 때만 기존 벡터 공룡 사용
        s = int(size * 0.85)
        if s < 2:
            return

        if animal_idx == 0:  # 티라노 (초록)
            body_color = (100, 180, 100)
            belly_color = (160, 220, 160)
            dark = (70, 140, 70)
            # 몸통
            pygame.draw.ellipse(surface, body_color, (cx - s, cy - s + 4, s * 2, s * 2))
            # 배
            pygame.draw.ellipse(surface, belly_color, (cx - s // 2, cy - s // 3, s, s))
            # 작은 팔
            pygame.draw.ellipse(surface, body_color, (cx - s - 6, cy - 4, 10, 6))
            pygame.draw.ellipse(surface, body_color, (cx + s - 4, cy - 4, 10, 6))
            # 이빨 (아래로 삐죽)
            for tx in [-7, -2, 3, 8]:
                pygame.draw.polygon(surface, WHITE, [
                    (cx + tx - 2, cy + 6),
                    (cx + tx + 2, cy + 6),
                    (cx + tx, cy + 11),
                ])
            # 눈
            pygame.draw.circle(surface, WHITE, (cx - 10, cy - 10), 7)
            pygame.draw.circle(surface, (50, 50, 50), (cx - 9, cy - 9), 4)
            pygame.draw.circle(surface, WHITE, (cx - 7, cy - 11), 2)
            pygame.draw.circle(surface, WHITE, (cx + 10, cy - 10), 7)
            pygame.draw.circle(surface, (50, 50, 50), (cx + 11, cy - 9), 4)
            pygame.draw.circle(surface, WHITE, (cx + 13, cy - 11), 2)
            # 콧구멍
            pygame.draw.circle(surface, dark, (cx - 4, cy + 2), 2)
            pygame.draw.circle(surface, dark, (cx + 4, cy + 2), 2)
            # 등 돌기
            for dx_off in [-8, 0, 8]:
                pygame.draw.polygon(surface, dark, [
                    (cx + dx_off - 4, cy - s + 6),
                    (cx + dx_off + 4, cy - s + 6),
                    (cx + dx_off, cy - s - 3),
                ])
            # 볼 홍조
            pygame.draw.circle(surface, (255, 180, 180), (cx - 18, cy + 2), 5)
            pygame.draw.circle(surface, (255, 180, 180), (cx + 18, cy + 2), 5)

        elif animal_idx == 1:  # 트리케라 (파랑)
            body_color = (120, 160, 210)
            frill_color = (100, 140, 200)
            dark = (80, 120, 170)
            horn_color = (230, 220, 180)
            # 프릴 (머리 뒤 방패)
            pygame.draw.circle(surface, frill_color, (cx, cy - s + 2), s - 2)
            # 프릴 장식 (작은 원들)
            for angle_deg in [-40, -15, 10, 35]:
                rad = math.radians(angle_deg - 90)
                px = cx + int((s - 6) * math.cos(rad))
                py = (cy - s + 2) + int((s - 6) * math.sin(rad))
                pygame.draw.circle(surface, (90, 130, 190), (px, py), 4)
                pygame.draw.circle(surface, (150, 180, 230), (px, py), 2)
            # 얼굴
            pygame.draw.circle(surface, body_color, (cx, cy + 4), s - 4)
            # 배
            pygame.draw.ellipse(surface, (160, 200, 240), (cx - s // 2 + 2, cy + 2, s - 4, s - 6))
            # 뿔 3개
            pygame.draw.polygon(surface, horn_color, [
                (cx - 3, cy - s + 8), (cx + 3, cy - s + 8), (cx, cy - s - 8)
            ])
            pygame.draw.polygon(surface, horn_color, [
                (cx - 12, cy - 6), (cx - 10, cy - 2), (cx - 18, cy - 14)
            ])
            pygame.draw.polygon(surface, horn_color, [
                (cx + 12, cy - 6), (cx + 10, cy - 2), (cx + 18, cy - 14)
            ])
            # 눈
            pygame.draw.circle(surface, WHITE, (cx - 9, cy + 2), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx - 8, cy + 3), 3)
            pygame.draw.circle(surface, WHITE, (cx - 6, cy + 1), 1)
            pygame.draw.circle(surface, WHITE, (cx + 9, cy + 2), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx + 10, cy + 3), 3)
            pygame.draw.circle(surface, WHITE, (cx + 12, cy + 1), 1)
            # 입
            pygame.draw.arc(surface, dark, (cx - 6, cy + 10, 12, 8), 3.14, 6.28, 2)
            # 볼 홍조
            pygame.draw.circle(surface, (255, 180, 200), (cx - 18, cy + 8), 5)
            pygame.draw.circle(surface, (255, 180, 200), (cx + 18, cy + 8), 5)

        elif animal_idx == 2:  # 브라키오 (노랑)
            body_color = (220, 200, 100)
            belly_color = (245, 235, 170)
            dark = (180, 160, 70)
            # 긴 목
            pygame.draw.ellipse(surface, body_color, (cx - 7, cy - s - 12, 14, s + 4))
            # 몸통 (아래쪽, 둥근)
            pygame.draw.ellipse(surface, body_color, (cx - s + 2, cy - 2, s * 2 - 4, s + 8))
            # 배
            pygame.draw.ellipse(surface, belly_color, (cx - s // 2, cy + 2, s, s - 2))
            # 머리 (작고 둥근)
            head_y = cy - s - 8
            pygame.draw.circle(surface, body_color, (cx, head_y), s // 2 + 2)
            # 눈
            pygame.draw.circle(surface, WHITE, (cx - 6, head_y - 2), 5)
            pygame.draw.circle(surface, (50, 50, 50), (cx - 5, head_y - 1), 3)
            pygame.draw.circle(surface, WHITE, (cx - 3, head_y - 3), 1)
            pygame.draw.circle(surface, WHITE, (cx + 6, head_y - 2), 5)
            pygame.draw.circle(surface, (50, 50, 50), (cx + 7, head_y - 1), 3)
            pygame.draw.circle(surface, WHITE, (cx + 9, head_y - 3), 1)
            # 콧구멍
            pygame.draw.circle(surface, dark, (cx - 3, head_y + 4), 2)
            pygame.draw.circle(surface, dark, (cx + 3, head_y + 4), 2)
            # 입 (미소)
            pygame.draw.arc(surface, dark, (cx - 5, head_y + 4, 10, 6), 3.14, 6.28, 2)
            # 다리 (짧은 4개)
            for lx in [cx - s + 8, cx - 6, cx + 6, cx + s - 8]:
                pygame.draw.ellipse(surface, dark, (lx - 4, cy + s - 2, 8, 8))
            # 볼 홍조
            pygame.draw.circle(surface, (255, 190, 180), (cx - 13, head_y + 2), 4)
            pygame.draw.circle(surface, (255, 190, 180), (cx + 13, head_y + 2), 4)

        elif animal_idx == 3:  # 스테고 (보라)
            body_color = (170, 130, 200)
            belly_color = (200, 180, 230)
            dark = (130, 90, 160)
            plate_color = (200, 160, 230)
            # 몸통
            pygame.draw.ellipse(surface, body_color, (cx - s, cy - s // 2, s * 2, s + s // 2))
            # 배
            pygame.draw.ellipse(surface, belly_color, (cx - s // 2, cy, s, s // 2 + 4))
            # 등판 (삼각형 판들)
            plate_positions = [-14, -7, 0, 7, 14]
            plate_sizes = [6, 9, 11, 9, 6]
            for i, (px, ps) in enumerate(zip(plate_positions, plate_sizes)):
                pygame.draw.polygon(surface, plate_color, [
                    (cx + px - ps // 2, cy - s // 2 + 2),
                    (cx + px + ps // 2, cy - s // 2 + 2),
                    (cx + px, cy - s // 2 - ps + 2),
                ])
                pygame.draw.polygon(surface, dark, [
                    (cx + px - ps // 2, cy - s // 2 + 2),
                    (cx + px + ps // 2, cy - s // 2 + 2),
                    (cx + px, cy - s // 2 - ps + 2),
                ], 1)
            # 꼬리 가시
            pygame.draw.polygon(surface, plate_color, [
                (cx + s - 4, cy - 2), (cx + s + 8, cy - 10), (cx + s + 2, cy + 2)
            ])
            pygame.draw.polygon(surface, plate_color, [
                (cx + s - 2, cy + 4), (cx + s + 10, cy), (cx + s + 4, cy + 8)
            ])
            # 눈
            pygame.draw.circle(surface, WHITE, (cx - 12, cy - 4), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx - 11, cy - 3), 3)
            pygame.draw.circle(surface, WHITE, (cx - 9, cy - 5), 1)
            pygame.draw.circle(surface, WHITE, (cx + 4, cy - 4), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx + 5, cy - 3), 3)
            pygame.draw.circle(surface, WHITE, (cx + 7, cy - 5), 1)
            # 입
            pygame.draw.arc(surface, dark, (cx - 8, cy + 4, 12, 8), 3.14, 6.28, 2)
            # 볼 홍조
            pygame.draw.circle(surface, (255, 180, 200), (cx - 20, cy + 2), 5)
            pygame.draw.circle(surface, (255, 180, 200), (cx + 12, cy + 2), 5)

        elif animal_idx == 4:  # 프테라 (분홍)
            body_color = (240, 160, 180)
            wing_color = (250, 190, 210)
            dark = (200, 120, 140)
            # 날개 (큰 삼각형)
            pygame.draw.polygon(surface, wing_color, [
                (cx - 8, cy - 2),
                (cx - s - 14, cy - s + 2),
                (cx - 6, cy + 8),
            ])
            pygame.draw.polygon(surface, wing_color, [
                (cx + 8, cy - 2),
                (cx + s + 14, cy - s + 2),
                (cx + 6, cy + 8),
            ])
            # 날개 테두리
            pygame.draw.polygon(surface, dark, [
                (cx - 8, cy - 2),
                (cx - s - 14, cy - s + 2),
                (cx - 6, cy + 8),
            ], 2)
            pygame.draw.polygon(surface, dark, [
                (cx + 8, cy - 2),
                (cx + s + 14, cy - s + 2),
                (cx + 6, cy + 8),
            ], 2)
            # 몸통
            pygame.draw.ellipse(surface, body_color, (cx - s // 2 - 2, cy - s // 2, s + 4, s + 6))
            # 머리 볏 (뒤로 뻗는 볏)
            pygame.draw.polygon(surface, body_color, [
                (cx + 2, cy - s // 2 - 2),
                (cx + 16, cy - s - 6),
                (cx + 8, cy - s // 2 + 4),
            ])
            # 부리
            pygame.draw.polygon(surface, (240, 200, 100), [
                (cx - 4, cy + 2),
                (cx + 4, cy + 2),
                (cx, cy + 12),
            ])
            # 눈
            pygame.draw.circle(surface, WHITE, (cx - 8, cy - 4), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx - 7, cy - 3), 3)
            pygame.draw.circle(surface, WHITE, (cx - 5, cy - 5), 1)
            pygame.draw.circle(surface, WHITE, (cx + 8, cy - 4), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx + 9, cy - 3), 3)
            pygame.draw.circle(surface, WHITE, (cx + 11, cy - 5), 1)
            # 볼 홍조
            pygame.draw.circle(surface, (255, 160, 170), (cx - 16, cy + 2), 4)
            pygame.draw.circle(surface, (255, 160, 170), (cx + 16, cy + 2), 4)

        elif animal_idx == 5:  # 안킬로 (주황)
            body_color = (220, 165, 100)
            armor_color = (200, 145, 80)
            belly_color = (240, 210, 170)
            dark = (170, 120, 60)
            # 몸통 (넓적한 타원)
            pygame.draw.ellipse(surface, body_color, (cx - s - 2, cy - s // 2 - 2, s * 2 + 4, s + 8))
            # 배
            pygame.draw.ellipse(surface, belly_color, (cx - s // 2, cy + 2, s, s // 2))
            # 갑옷 무늬 (육각 패턴)
            armor_spots = [(-10, -8), (0, -10), (10, -8), (-6, -2), (6, -2)]
            for ax, ay in armor_spots:
                pygame.draw.circle(surface, armor_color, (cx + ax, cy + ay), 5)
                pygame.draw.circle(surface, dark, (cx + ax, cy + ay), 5, 1)
            # 옆 가시
            for side in [-1, 1]:
                for sy_off in [-6, 0, 6]:
                    spike_x = cx + side * (s + 2)
                    pygame.draw.polygon(surface, armor_color, [
                        (spike_x, cy + sy_off - 3),
                        (spike_x, cy + sy_off + 3),
                        (spike_x + side * 7, cy + sy_off),
                    ])
            # 꼬리 곤봉
            pygame.draw.line(surface, body_color, (cx + s, cy + 4), (cx + s + 10, cy + 6), 4)
            pygame.draw.circle(surface, armor_color, (cx + s + 13, cy + 6), 7)
            pygame.draw.circle(surface, dark, (cx + s + 13, cy + 6), 7, 1)
            # 눈
            pygame.draw.circle(surface, WHITE, (cx - 12, cy - 2), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx - 11, cy - 1), 3)
            pygame.draw.circle(surface, WHITE, (cx - 9, cy - 3), 1)
            pygame.draw.circle(surface, WHITE, (cx + 4, cy - 2), 6)
            pygame.draw.circle(surface, (50, 50, 50), (cx + 5, cy - 1), 3)
            pygame.draw.circle(surface, WHITE, (cx + 7, cy - 3), 1)
            # 입
            pygame.draw.arc(surface, dark, (cx - 8, cy + 6, 12, 6), 3.14, 6.28, 2)
            # 볼 홍조
            pygame.draw.circle(surface, (255, 190, 180), (cx - 20, cy + 4), 4)
            pygame.draw.circle(surface, (255, 190, 180), (cx + 12, cy + 4), 4)

        elif animal_idx == 6:  # 아기공룡 (빨강)
            body_color = (230, 120, 120)
            belly_color = (250, 180, 180)
            dark = (190, 80, 80)
            shell_color = (245, 240, 220)
            shell_crack = (200, 195, 175)
            # 알 껍데기 (하반부)
            pygame.draw.ellipse(surface, shell_color, (cx - s - 4, cy - 2, s * 2 + 8, s + 10))
            # 알 껍데기 갈라진 모양 (지그재그 상단)
            crack_points = []
            for i in range(9):
                px = cx - s - 4 + i * (s * 2 + 8) // 8
                py = cy - 2 + ((-5 if i % 2 == 0 else 3))
                crack_points.append((px, py))
            crack_points.append((cx + s + 4, cy + s + 8))
            crack_points.append((cx - s - 4, cy + s + 8))
            pygame.draw.polygon(surface, shell_color, crack_points)
            # 알 껍데기 갈라진 선
            for i in range(8):
                px1 = cx - s - 4 + i * (s * 2 + 8) // 8
                py1 = cy - 2 + ((-5 if i % 2 == 0 else 3))
                px2 = cx - s - 4 + (i + 1) * (s * 2 + 8) // 8
                py2 = cy - 2 + ((-5 if (i + 1) % 2 == 0 else 3))
                pygame.draw.line(surface, shell_crack, (px1, py1), (px2, py2), 2)
            # 몸통 (알 위로 나온 상반신)
            pygame.draw.ellipse(surface, body_color, (cx - s // 2 - 4, cy - s - 2, s + 8, s + 6))
            # 배
            pygame.draw.ellipse(surface, belly_color, (cx - s // 3, cy - s // 2, s // 2 + 4, s // 2))
            # 작은 뿔 2개
            pygame.draw.polygon(surface, (240, 180, 100), [
                (cx - 8, cy - s), (cx - 5, cy - s - 10), (cx - 2, cy - s),
            ])
            pygame.draw.polygon(surface, (240, 180, 100), [
                (cx + 2, cy - s), (cx + 5, cy - s - 10), (cx + 8, cy - s),
            ])
            # 눈 (큰 눈 - 아기라서)
            pygame.draw.circle(surface, WHITE, (cx - 10, cy - s // 2 - 2), 7)
            pygame.draw.circle(surface, (50, 50, 50), (cx - 9, cy - s // 2 - 1), 4)
            pygame.draw.circle(surface, WHITE, (cx - 7, cy - s // 2 - 3), 2)
            pygame.draw.circle(surface, WHITE, (cx + 10, cy - s // 2 - 2), 7)
            pygame.draw.circle(surface, (50, 50, 50), (cx + 11, cy - s // 2 - 1), 4)
            pygame.draw.circle(surface, WHITE, (cx + 13, cy - s // 2 - 3), 2)
            # 입 (작은 미소)
            pygame.draw.arc(surface, dark, (cx - 5, cy - s // 2 + 6, 10, 6), 3.14, 6.28, 2)
            # 볼 홍조
            pygame.draw.circle(surface, (255, 170, 170), (cx - 18, cy - s // 2 + 2), 5)
            pygame.draw.circle(surface, (255, 170, 170), (cx + 18, cy - s // 2 + 2), 5)

    def draw_cell_bg(self, surface, row, col, highlight=False):
        """셀 배경 그리기"""
        x = BOARD_X + col * CELL_SIZE
        y = BOARD_Y + row * CELL_SIZE
        margin = 3

        if highlight:
            # 선택된 셀 - 반짝이는 효과
            glow_size = 4 + 2 * math.sin(pygame.time.get_ticks() / 200)
            glow_rect = (x + margin - glow_size, y + margin - glow_size,
                        CELL_SIZE - margin * 2 + glow_size * 2, CELL_SIZE - margin * 2 + glow_size * 2)
            self.draw_rounded_rect(surface, HIGHLIGHT_COLOR, glow_rect, 14)

        bg_color = (255, 255, 255) if (row + col) % 2 == 0 else (250, 248, 240)
        cell_rect = (x + margin, y + margin, CELL_SIZE - margin * 2, CELL_SIZE - margin * 2)
        self.draw_rounded_rect(surface, bg_color, cell_rect, 10)

    def draw(self):
        """화면 그리기"""
        # 배경
        screen.fill(BG_COLOR)

        # 상단 배경 그라데이션
        for i in range(180):
            alpha = 1 - i / 180
            r = int(255 * alpha + BG_COLOR[0] * (1 - alpha))
            g = int(220 * alpha + BG_COLOR[1] * (1 - alpha))
            b = int(240 * alpha + BG_COLOR[2] * (1 - alpha))
            pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))

        # 반짝이는 별
        for i, (sx, sy) in enumerate(self.star_positions):
            twinkle = (math.sin(self.star_twinkle[i]) + 1) / 2
            size = int(2 + 3 * twinkle)
            brightness = int(200 + 55 * twinkle)
            color = (brightness, brightness, min(255, brightness + 30))
            pygame.draw.circle(screen, color, (sx, sy), size)
            if twinkle > 0.7:
                pygame.draw.line(screen, color, (sx - size - 2, sy), (sx + size + 2, sy), 1)
                pygame.draw.line(screen, color, (sx, sy - size - 2), (sx, sy + size + 2), 1)

        # 제목
        title_text = "HOpang - 공룡팡" if self.mode == "dino" else "HOpang - 현오팡"
        title = title_font.render(title_text, True, TITLE_COLOR)
        title_shadow = title_font.render(title_text, True, (200, 80, 100))
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 2, 22))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))

        # 모드 선택 버튼 UI
        def draw_mode_button(rect, text, active):
            base_color = (200, 230, 255) if active else (235, 235, 235)
            border_color = (80, 140, 200) if active else (170, 170, 170)
            self.draw_rounded_rect(screen, base_color, rect, 12)
            pygame.draw.rect(
                screen,
                border_color,
                (rect.x, rect.y, rect.w, rect.h),
                2,
                border_radius=12,
            )
            label = small_font.render(text, True, (80, 80, 80))
            screen.blit(
                label,
                (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2),
            )

        draw_mode_button(self.dino_mode_button, "공룡팡", self.mode == "dino")
        draw_mode_button(self.hyuno_mode_button, "현오팡", self.mode == "hyuno")

        # 점수
        score_text = score_font.render(f"점수: {self.score}", True, SCORE_COLOR)
        screen.blit(score_text, (30, 85))

        # 타이머
        time_color = (255, 80, 80) if self.time_left < 15 else (100, 180, 100)
        minutes = int(self.time_left) // 60
        seconds = int(self.time_left) % 60
        time_text = score_font.render(f"시간: {minutes}:{seconds:02d}", True, time_color)
        screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 30, 85))

        # 콤보 표시
        if self.combo >= 2:
            combo_text = small_font.render(f"콤보 x{self.combo}", True, (255, 150, 0))
            screen.blit(combo_text, (SCREEN_WIDTH // 2 - combo_text.get_width() // 2, 90))

        # 버튼들 (시작 / 다시시작 / 종료)
        def draw_button(rect, text, base_color, text_color, enabled=True):
            color = base_color if enabled else (200, 200, 200)
            shadow_rect = (rect.x + 3, rect.y + 3, rect.w, rect.h)
            self.draw_rounded_rect(screen, (210, 200, 190), shadow_rect, 14)
            self.draw_rounded_rect(screen, color, rect, 14)
            label = small_font.render(text, True, text_color)
            screen.blit(
                label,
                (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2),
            )

        draw_button(
            self.start_button,
            "시작",
            (140, 200, 255),
            (40, 80, 120),
            enabled=not self.game_started and self.state != "gameover",
        )
        draw_button(
            self.restart_button,
            "다시시작",
            (180, 230, 160),
            (50, 110, 60),
            enabled=True,
        )
        draw_button(
            self.quit_button,
            "종료",
            (255, 180, 170),
            (140, 60, 60),
            enabled=True,
        )

        # 타이머 바
        bar_width = SCREEN_WIDTH - 60
        bar_height = 16
        bar_x = 30
        bar_y = 135
        # 배경
        self.draw_rounded_rect(screen, (220, 220, 220), (bar_x, bar_y, bar_width, bar_height), 8)
        # 진행률
        progress = max(0, self.time_left / 90)
        if progress > 0:
            fill_width = int(bar_width * progress)
            fill_color = (100, 200, 100) if progress > 0.3 else ((255, 200, 50) if progress > 0.15 else (255, 80, 80))
            self.draw_rounded_rect(screen, fill_color, (bar_x, bar_y, fill_width, bar_height), 8)

        # 보드 배경
        board_bg_rect = (
            BOARD_X - BOARD_PADDING,
            BOARD_Y - BOARD_PADDING,
            COLS * CELL_SIZE + BOARD_PADDING * 2,
            ROWS * CELL_SIZE + BOARD_PADDING * 2,
        )
        # 그림자
        shadow_rect = (board_bg_rect[0] + 4, board_bg_rect[1] + 4, board_bg_rect[2], board_bg_rect[3])
        self.draw_rounded_rect(screen, (200, 195, 185), shadow_rect, 16)
        self.draw_rounded_rect(screen, GRID_BG, board_bg_rect, 16)
        # 테두리
        pygame.draw.rect(screen, (230, 220, 200),
                        (board_bg_rect[0], board_bg_rect[1], board_bg_rect[2], board_bg_rect[3]),
                        3, border_radius=16)

        # 셀 배경 그리기 (드래그 중인 셀 하이라이트)
        for row in range(ROWS):
            for col in range(COLS):
                is_dragging = self.dragging and self.drag_start == (row, col)
                self.draw_cell_bg(screen, row, col, is_dragging)

        # 공룡 그리기
        falling_positions = {}
        if self.state == "falling" and self.fall_data:
            for from_row, from_col, to_row, to_col, val in self.fall_data:
                t = min(1, self.fall_progress)
                # ease-out bounce
                t2 = 1 - (1 - t) ** 2
                cur_row = from_row + (to_row - from_row) * t2
                falling_positions[(to_row, to_col)] = (cur_row, to_col, val)

        swap_positions = {}
        if self.state == "swapping" and self.swap_cells:
            (r1, c1), (r2, c2) = self.swap_cells
            t = min(1, self.swap_progress)
            # ease-in-out
            t2 = t * t * (3 - 2 * t)
            swap_positions[(r1, c1)] = (r1 + (r2 - r1) * t2, c1 + (c2 - c1) * t2)
            swap_positions[(r2, c2)] = (r2 + (r1 - r2) * t2, c2 + (c1 - c2) * t2)

        for row in range(ROWS):
            for col in range(COLS):
                val = self.board[row][col]
                if val is None:
                    continue

                # 제거 애니메이션 중인 셀
                if (row, col) in self.remove_cells:
                    scale = max(0, 1 - self.remove_progress)
                    cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
                    cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
                    self.draw_cute_animal(screen, val, cx, cy, int(34 * scale))
                    continue

                # 낙하 중인 셀
                if (row, col) in falling_positions:
                    cur_row, cur_col, fval = falling_positions[(row, col)]
                    cx = BOARD_X + int(cur_col * CELL_SIZE) + CELL_SIZE // 2
                    cy = BOARD_Y + int(cur_row * CELL_SIZE) + CELL_SIZE // 2
                    self.draw_cute_animal(screen, fval, cx, cy)
                    continue

                # 스왑 중인 셀
                if (row, col) in swap_positions:
                    sr, sc = swap_positions[(row, col)]
                    cx = BOARD_X + int(sc * CELL_SIZE) + CELL_SIZE // 2
                    cy = BOARD_Y + int(sr * CELL_SIZE) + CELL_SIZE // 2
                    self.draw_cute_animal(screen, val, cx, cy)
                    continue

                # 드래그 중인 셀은 나중에 최상위 레이어로 그림
                if self.dragging and self.drag_start == (row, col) and self.drag_current_pos:
                    # 원래 위치에 반투명 잔상 표시
                    cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
                    cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
                    self.draw_cute_animal(screen, val, cx, cy, 60, alpha=0.3)
                    continue

                # 일반 셀
                cx = BOARD_X + col * CELL_SIZE + CELL_SIZE // 2
                cy = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

                # 살짝 통통 튀는 느낌
                bounce = math.sin(pygame.time.get_ticks() / 500 + row * 0.3 + col * 0.5) * 2
                cy += int(bounce)

                self.draw_cute_animal(screen, val, cx, cy, 60)

        # 드래그 중인 아이콘을 최상위 레이어로 그림 (마우스 커서 위치)
        if self.dragging and self.drag_start and self.drag_current_pos:
            dr, dc = self.drag_start
            drag_val = self.board[dr][dc]
            if drag_val is not None:
                dmx, dmy = self.drag_current_pos
                self.draw_cute_animal(screen, drag_val, dmx, dmy, 70)

        # 파티클
        for p in self.particles:
            p.draw(screen)

        # 떠다니는 텍스트
        for ft in self.floating_texts:
            ft.draw(screen)

        # 하단 안내
        if self.state == "playing":
            if not self.game_started:
                hint_msg = "위의 시작 버튼을 눌러 게임을 시작해요!"
            else:
                hint_msg = "같은 공룡 3개를 맞춰보세요!"
            hint = small_font.render(hint_msg, True, (180, 160, 140))
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 45))

        # 게임 오버
        if self.state == "gameover":
            self.draw_gameover()

    def draw_gameover(self):
        """게임 오버 화면"""
        # 반투명 오버레이
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        # 결과 패널
        panel_w, panel_h = 400, 350
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        self.draw_rounded_rect(screen, WHITE, (panel_x, panel_y, panel_w, panel_h), 20)
        self.draw_rounded_rect(screen, (255, 240, 220), (panel_x + 5, panel_y + 5, panel_w - 10, panel_h - 10), 18)

        # 텍스트
        y = panel_y + 30
        end_title = title_font.render("참 잘했어요!", True, TITLE_COLOR)
        screen.blit(end_title, (SCREEN_WIDTH // 2 - end_title.get_width() // 2, y))

        y += 70
        score_text = score_font.render(f"점수: {self.score}", True, SCORE_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y))

        y += 50
        combo_text = small_font.render(f"최대 콤보: {self.max_combo}x", True, (150, 130, 200))
        screen.blit(combo_text, (SCREEN_WIDTH // 2 - combo_text.get_width() // 2, y))

        y += 50
        # 별 등급
        stars = 1
        if self.score >= 500:
            stars = 2
        if self.score >= 1500:
            stars = 3
        if self.score >= 3000:
            stars = 4
        if self.score >= 5000:
            stars = 5

        # 일부 환경에서 이모지가 깨져 보이는 것을 막기 위해 일반 별 문자 사용
        star_text = "★" * stars
        star_surface = get_korean_font(40).render(star_text, True, (255, 215, 0))
        screen.blit(star_surface, (SCREEN_WIDTH // 2 - star_surface.get_width() // 2, y))

        y += 60
        retry_text = message_font.render("다시 하려면 스페이스 바를 누르세요!", True, (150, 150, 150))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, y))

    def restart(self):
        """게임 재시작"""
        self.__init__()


# ─── HOtris (테트리스) 게임 클래스 ───
class HOtrisGame:
    """5세 아이를 위한 테트리스 게임"""
    
    TETRIS_COLS = 10
    TETRIS_ROWS = 15
    CELL_SIZE = 35
    BOARD_X = (SCREEN_WIDTH - TETRIS_COLS * CELL_SIZE) // 2
    BOARD_Y = 180
    
    TETRIS_SHAPES = [
        [[1,1,1,1]],  # I
        [[1,1],[1,1]],  # O
        [[1,1,1],[0,1,0]],  # T
        [[1,1,1],[1,0,0]],  # L
        [[1,1,1],[0,0,1]],  # J
        [[1,1,0],[0,1,1]],  # S
        [[0,1,1],[1,1,0]],  # Z
    ]
    
    TETRIS_COLORS = [
        (100, 200, 255),  # 파랑
        (255, 200, 50),   # 노랑
        (180, 100, 255),  # 보라
        (255, 150, 50),   # 주황
        (50, 200, 150),   # 초록
        (255, 100, 100),  # 빨강
        (100, 150, 255),  # 파랑2
    ]
    
    def __init__(self):
        self.board = [[None] * self.TETRIS_COLS for _ in range(self.TETRIS_ROWS)]
        self.score = 0
        self.game_over = False
        self.game_started = False
        
        self.current_piece = None
        self.current_color = None
        self.current_row = 0
        self.current_col = 0
        
        self.next_piece = None
        self.next_color = None
        
        self.drop_timer = 0
        self.drop_speed = 800  # 5세 아이를 위해 느린 속도
        
        self.particles = []
        self.floating_texts = []
        
        # 버튼
        button_w, button_h = 130, 44
        gap = 18
        center_x = SCREEN_WIDTH // 2
        button_y = 550
        self.start_button = pygame.Rect(center_x - button_w // 2, button_y, button_w, button_h)
        self.restart_button = pygame.Rect(
            center_x - button_w - gap - button_w // 2, button_y, button_w, button_h
        )
        self.quit_button = pygame.Rect(
            center_x + button_w // 2 + gap, button_y, button_w, button_h
        )
        self.back_button = pygame.Rect(30, 30, 80, 36)
        
        # 테트리스 블록 스프라이트
        self.block_sprites = []
        self.load_block_sprites()
        
        # 새 게임 시작 시 첫 블록 생성
        self.next_piece = random.choice(self.TETRIS_SHAPES)
        self.next_color = random.choice(self.TETRIS_COLORS)
        self.spawn_piece()
        
    def load_block_sprites(self):
        """테트리스 블록 스프라이트 로드"""
        tetress_path = "/Users/sy.im/HO_GAME/assets/tetress.png"
        if os.path.exists(tetress_path):
            try:
                img = pygame.image.load(tetress_path).convert_alpha()
                # 7개의 블록 색상에 대한 스프라이트 생성 (약간 다른 색상으로)
                for i, color in enumerate(self.TETRIS_COLORS):
                    # 원본 이미지에서 잘라서 사용하거나 색상 적용
                    sprite = pygame.Surface((self.CELL_SIZE - 2, self.CELL_SIZE - 2), pygame.SRCALPHA)
                    # 색상填充
                    pygame.draw.rect(sprite, color + (200,), (0, 0, self.CELL_SIZE - 2, self.CELL_SIZE - 2))
                    # 테두리
                    pygame.draw.rect(sprite, (255, 255, 255, 150), (0, 0, self.CELL_SIZE - 2, self.CELL_SIZE - 2), 2)
                    # 내부 하이라이트
                    pygame.draw.rect(sprite, (255, 255, 255, 80), (2, 2, 8, 8))
                    self.block_sprites.append(sprite)
            except:
                self.block_sprites = []
        else:
            self.block_sprites = []
    
    def spawn_piece(self):
        """새 블록 생성"""
        self.current_piece = self.next_piece
        self.current_color = self.next_color
        
        self.next_piece = random.choice(self.TETRIS_SHAPES)
        self.next_color = random.choice(self.TETRIS_COLORS)
        
        self.current_row = 0
        self.current_col = (self.TETRIS_COLS - len(self.current_piece[0])) // 2
        
        # 충돌 검사
        if self.check_collision(self.current_row, self.current_col, self.current_piece):
            self.game_over = True
    
    def check_collision(self, row, col, shape):
        """충돌 검사"""
        for r in range(len(shape)):
            for c in range(len(shape[r])):
                if shape[r][c]:
                    new_row = row + r
                    new_col = col + c
                    if new_col < 0 or new_col >= self.TETRIS_COLS:
                        return True
                    if new_row >= self.TETRIS_ROWS:
                        return True
                    if new_row >= 0 and self.board[new_row][new_col] is not None:
                        return True
        return False
    
    def rotate_piece(self):
        """블록 회전"""
        rotated = [list(row) for row in zip(*self.current_piece[::-1])]
        if not self.check_collision(self.current_row, self.current_col, rotated):
            self.current_piece = rotated
    
    def move_piece(self, d_row, d_col):
        """블록 이동"""
        if not self.check_collision(self.current_row + d_row, self.current_col + d_col, self.current_piece):
            self.current_row += d_row
            self.current_col += d_col
            return True
        return False
    
    def lock_piece(self):
        """블록 고정"""
        for r in range(len(self.current_piece)):
            for c in range(len(self.current_piece[r])):
                if self.current_piece[r][c]:
                    row = self.current_row + r
                    col = self.current_col + c
                    if row >= 0:
                        self.board[row][col] = self.current_color
        
        self.clear_lines()
        self.spawn_piece()
    
    def clear_lines(self):
        """줄 삭제"""
        lines_cleared = 0
        for row in range(self.TETRIS_ROWS - 1, -1, -1):
            if None not in self.board[row]:
                # 줄 삭제
                del self.board[row]
                self.board.insert(0, [None] * self.TETRIS_COLS)
                lines_cleared += 1
                # 효과
                for c in range(self.TETRIS_COLS):
                    cx = self.BOARD_X + c * self.CELL_SIZE + self.CELL_SIZE // 2
                    cy = self.BOARD_Y + row * self.CELL_SIZE + self.CELL_SIZE // 2
                    for _ in range(5):
                        self.particles.append(Particle(cx, cy, self.TETRIS_COLORS[random.randint(0, 6)]))
        
        if lines_cleared > 0:
            self.score += lines_cleared * 100 * lines_cleared
            # 콤보 텍스트
            if lines_cleared >= 2:
                center_x = self.BOARD_X + self.TETRIS_COLS * self.CELL_SIZE // 2
                center_y = self.BOARD_Y + self.TETRIS_ROWS * self.CELL_SIZE // 2
                self.floating_texts.append(
                    FloatingText(f"{lines_cleared}줄!", center_x, center_y - 30, (255, 200, 50), 50)
                )
    
    def update(self, dt):
        """업데이트"""
        # 파티클 업데이트
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # 떠다니는 텍스트 업데이트
        self.floating_texts = [t for t in self.floating_texts if t.update(dt)]
        
        if not self.game_started or self.game_over:
            return
        
        # 블록 자동下落
        self.drop_timer += dt * 1000
        if self.drop_timer >= self.drop_speed:
            self.drop_timer = 0
            if not self.move_piece(1, 0):
                self.lock_piece()
    
    def draw_rounded_rect(self, surface, color, rect, radius):
        """둥근 사각형 그리기"""
        x, y, w, h = rect
        pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
        pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))
        pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + radius), radius)
        pygame.draw.circle(surface, color, (x + radius, y + h - radius), radius)
        pygame.draw.circle(surface, color, (x + w - radius, y + h - radius), radius)
    
    def draw_block(self, surface, color_idx, cx, cy, size=None):
        """블록 그리기"""
        if size is None:
            size = self.CELL_SIZE - 2
        
        if self.block_sprites and color_idx < len(self.block_sprites):
            sprite = pygame.transform.scale(self.block_sprites[color_idx], (size, size))
            rect = sprite.get_rect(center=(cx, cy))
            surface.blit(sprite, rect)
        else:
            # 폴백: 기본 사각형
            color = self.TETRIS_COLORS[color_idx % len(self.TETRIS_COLORS)]
            pygame.draw.rect(surface, color, (cx - size//2, cy - size//2, size, size), border_radius=4)
            pygame.draw.rect(surface, (255, 255, 255, 150), (cx - size//2, cy - size//2, size, size), 2, border_radius=4)
    
    def draw(self):
        """그리기"""
        # 배경
        screen.fill((255, 248, 240))
        
        # 상단 그라데이션
        for i in range(150):
            alpha = 1 - i / 150
            r = int(255 * alpha + BG_COLOR[0] * (1 - alpha))
            g = int(200 * alpha + BG_COLOR[1] * (1 - alpha))
            b = int(220 * alpha + BG_COLOR[2] * (1 - alpha))
            pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))
        
        # 제목
        title_text = "HOtris - 테트리스"
        title = title_font.render(title_text, True, (100, 150, 255))
        title_shadow = title_font.render(title_text, True, (80, 120, 200))
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 2, 22))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
        
        # 뒤로 가기 버튼
        def draw_small_button(rect, text, base_color):
            self.draw_rounded_rect(screen, base_color, rect, 10)
            label = small_font.render(text, True, (80, 80, 120))
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
        
        draw_small_button(self.back_button, "뒤로", (220, 230, 250))
        
        # 점수
        score_text = score_font.render(f"점수: {self.score}", True, SCORE_COLOR)
        screen.blit(score_text, (30, 80))
        
        # 버튼들
        def draw_button(rect, text, base_color, text_color, enabled=True):
            color = base_color if enabled else (200, 200, 200)
            shadow_rect = (rect.x + 3, rect.y + 3, rect.w, rect.h)
            self.draw_rounded_rect(screen, (210, 200, 190), shadow_rect, 14)
            self.draw_rounded_rect(screen, color, rect, 14)
            label = small_font.render(text, True, text_color)
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.centery - label.get_height() // 2))
        
        draw_button(self.start_button, "시작", (140, 255, 180), (40, 120, 80), enabled=not self.game_started and not self.game_over)
        draw_button(self.restart_button, "다시하기", (180, 230, 160), (50, 110, 60))
        draw_button(self.quit_button, "종료", (255, 180, 170), (140, 60, 60))
        
        # 보드 배경
        board_rect = (
            self.BOARD_X - 8,
            self.BOARD_Y - 8,
            self.TETRIS_COLS * self.CELL_SIZE + 16,
            self.TETRIS_ROWS * self.CELL_SIZE + 16,
        )
        self.draw_rounded_rect(screen, (180, 180, 200), board_rect, 12)
        self.draw_rounded_rect(screen, (240, 245, 255), board_rect, 10)
        
        # 보드 그리드
        for r in range(self.TETRIS_ROWS):
            for c in range(self.TETRIS_COLS):
                x = self.BOARD_X + c * self.CELL_SIZE
                y = self.BOARD_Y + r * self.CELL_SIZE
                bg_color = (255, 255, 255) if (r + c) % 2 == 0 else (248, 252, 255)
                pygame.draw.rect(screen, bg_color, (x + 1, y + 1, self.CELL_SIZE - 2, self.CELL_SIZE - 2), border_radius=3)
        
        # 고정된 블록 그리기
        for r in range(self.TETRIS_ROWS):
            for c in range(self.TETRIS_COLS):
                if self.board[r][c] is not None:
                    color_idx = self.TETRIS_COLORS.index(self.board[r][c]) if self.board[r][c] in self.TETRIS_COLORS else 0
                    cx = self.BOARD_X + c * self.CELL_SIZE + self.CELL_SIZE // 2
                    cy = self.BOARD_Y + r * self.CELL_SIZE + self.CELL_SIZE // 2
                    self.draw_block(screen, color_idx, cx, cy)
        
        # 현재 블록 그리기
        if self.current_piece and not self.game_over:
            for r in range(len(self.current_piece)):
                for c in range(len(self.current_piece[r])):
                    if self.current_piece[r][c]:
                        row = self.current_row + r
                        col = self.current_col + c
                        if 0 <= row < self.TETRIS_ROWS and 0 <= col < self.TETRIS_COLS:
                            cx = self.BOARD_X + col * self.CELL_SIZE + self.CELL_SIZE // 2
                            cy = self.BOARD_Y + row * self.CELL_SIZE + self.CELL_SIZE // 2
                            color_idx = self.TETRIS_COLORS.index(self.current_color) if self.current_color in self.TETRIS_COLORS else 0
                            self.draw_block(screen, color_idx, cx, cy)
        
        # 다음 블록 미리보기
        next_x = SCREEN_WIDTH - 150
        next_y = 250
        next_label = small_font.render("다음", True, (100, 150, 200))
        screen.blit(next_label, (next_x - next_label.get_width() // 2, next_y - 30))
        
        if self.next_piece:
            for r in range(len(self.next_piece)):
                for c in range(len(self.next_piece[r])):
                    if self.next_piece[r][c]:
                        cx = next_x + c * 25 + 25
                        cy = next_y + r * 25 + 25
                        color_idx = self.TETRIS_COLORS.index(self.next_color) if self.next_color in self.TETRIS_COLORS else 0
                        self.draw_block(screen, color_idx, cx, cy, 23)
        
        # 조작법
        controls_y = 450
        controls = [
            "← → : 이동",
            "↓ : 빠르게 내리기",
            "↑ : 회전",
        ]
        for i, ctrl in enumerate(controls):
            ctrl_text = small_font.render(ctrl, True, (150, 150, 180))
            screen.blit(ctrl_text, (SCREEN_WIDTH - 180, controls_y + i * 30))
        
        # 파티클
        for p in self.particles:
            p.draw(screen)
        
        # 떠다니는 텍스트
        for ft in self.floating_texts:
            ft.draw(screen)
        
        # 게임 오버
        if self.game_over:
            self.draw_gameover()
        
        # 하단 안내
        if not self.game_started and not self.game_over:
            hint = small_font.render("시작 버튼을 눌러 게임을 시작하세요!", True, (180, 160, 140))
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 45))
    
    def draw_gameover(self):
        """게임 오버 화면"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))
        
        panel_w, panel_h = 350, 280
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        self.draw_rounded_rect(screen, WHITE, (panel_x, panel_y, panel_w, panel_h), 20)
        
        y = panel_y + 30
        end_title = title_font.render("게임 끝!", True, (100, 150, 255))
        screen.blit(end_title, (SCREEN_WIDTH // 2 - end_title.get_width() // 2, y))
        
        y += 70
        score_text = score_font.render(f"점수: {self.score}", True, SCORE_COLOR)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, y))
        
        y += 50
        retry_text = message_font.render("다시 하려면 스페이스 바!", True, (150, 150, 150))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, y))
    
    def handle_input(self, event):
        """입력 처리"""
        if event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key == pygame.K_SPACE:
                    self.__init__()
                return
            
            if not self.game_started:
                return
            
            if event.key == pygame.K_LEFT:
                self.move_piece(0, -1)
            elif event.key == pygame.K_RIGHT:
                self.move_piece(0, 1)
            elif event.key == pygame.K_DOWN:
                self.move_piece(1, 0)
            elif event.key == pygame.K_UP:
                self.rotate_piece()
    
    def handle_mouse(self, mx, my, button_type):
        """마우스 처리"""
        if button_type == "down":
            # 뒤로 가기
            if self.back_button.collidepoint(mx, my):
                global GAME_STATE
                GAME_STATE = "menu"
                return True
            
            # 시작 버튼
            if self.start_button.collidepoint(mx, my) and not self.game_started and not self.game_over:
                self.game_started = True
                return True
            
            # 다시하기
            if self.restart_button.collidepoint(mx, my):
                self.__init__()
                return True
            
            # 종료
            if self.quit_button.collidepoint(mx, my):
                pygame.quit()
                sys.exit()
        
        return False


# ─── 메뉴 화면 클래스 ───
class MenuScreen:
    """게임 선택 화면"""
    
    def __init__(self):
        self.title_font = get_korean_font(56)
        self.button_font = get_korean_font(36)
        
        # 게임 선택 버튼
        btn_w, btn_h = 250, 100
        center_x = SCREEN_WIDTH // 2
        gap = 80
        
        # HOpang 버튼 (위)
        self.anipang_btn = pygame.Rect(center_x - btn_w // 2, 300, btn_w, btn_h)
        # HOtris 버튼 (아래)
        self.tris_btn = pygame.Rect(center_x - btn_w // 2, 300 + btn_h + gap, btn_w, btn_h)
        
    def draw(self):
        """메뉴 화면 그리기"""
        # 배경
        screen.fill((255, 248, 240))
        
        # 상단 그라데이션
        for i in range(200):
            alpha = 1 - i / 200
            r = int(255 * alpha + 255 * (1 - alpha))
            g = int(200 * alpha + 248 * (1 - alpha))
            b = int(220 * alpha + 240 * (1 - alpha))
            pygame.draw.line(screen, (r, g, b), (0, i), (SCREEN_WIDTH, i))
        
        # 별装饰
        for i in range(15):
            x = 50 + i * 45
            y = 80 + (i % 3) * 30
            size = 3 + (i % 3)
            twinkle = math.sin(pygame.time.get_ticks() / 500 + i) * 0.5 + 0.5
            color = (255, 220 + int(35 * twinkle), 100)
            pygame.draw.circle(screen, color, (x, y), size)
        
        # 제목
        title = self.title_font.render("HO_GAME", True, (255, 100, 150))
        title_shadow = self.title_font.render("HO_GAME", True, (200, 80, 120))
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title.get_width() // 2 + 3, 53))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        # 부제목
        subtitle = get_korean_font(28).render("다양한 게임을 즐기자!", True, (150, 150, 180))
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 110))
        
        # 버튼 그리기
        self.draw_game_button(
            self.anipang_btn,
            "🎮 HOpang",
            "공룡 / 현오 매칭",
            (140, 220, 255),
            (80, 150, 220)
        )
        
        self.draw_game_button(
            self.tris_btn,
            "🧱 HOtris",
            "테트리스 블록",
            (255, 180, 100),
            (220, 140, 60)
        )
        
        # 하단 텍스트
        hint = get_korean_font(20).render("버튼을 클릭해서 게임을 선택하세요!", True, (180, 180, 180))
        screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 40))
    
    def draw_game_button(self, rect, title, desc, color, border_color):
        """게임 버튼 그리기"""
        # 그림자
        shadow_rect = (rect.x + 4, rect.y + 4, rect.w, rect.h)
        pygame.draw.rect(screen, (200, 190, 180), shadow_rect, border_radius=20)
        
        # 배경
        pygame.draw.rect(screen, color, rect, border_radius=20)
        
        # 테두리
        pygame.draw.rect(screen, border_color, rect, 3, border_radius=20)
        
        # 제목
        title_surf = self.button_font.render(title, True, (60, 60, 100))
        screen.blit(title_surf, (rect.centerx - title_surf.get_width() // 2, rect.centery - 25))
        
        # 설명
        desc_surf = get_korean_font(20).render(desc, True, (100, 100, 140))
        screen.blit(desc_surf, (rect.centerx - desc_surf.get_width() // 2, rect.centery + 15))
    
    def handle_click(self, mx, my):
        """클릭 처리"""
        if self.anipang_btn.collidepoint(mx, my):
            return "anipang"
        if self.tris_btn.collidepoint(mx, my):
            return "hotris"
        return None


# ─── 메인 루프 ───
def main():
    global GAME_STATE
    
    clock = pygame.time.Clock()
    
    anipang_game = None
    hotris_game = None
    menu = MenuScreen()
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        dt = min(dt, 0.05)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if GAME_STATE != "menu":
                        GAME_STATE = "menu"
                elif event.key == pygame.K_SPACE:
                    if GAME_STATE == "anipang" and anipang_game and anipang_game.state == "gameover":
                        anipang_game.restart()
                    elif GAME_STATE == "hotris" and hotris_game and hotris_game.game_over:
                        hotris_game.__init__()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    
                    if GAME_STATE == "menu":
                        result = menu.handle_click(mx, my)
                        if result == "anipang":
                            GAME_STATE = "anipang"
                            anipang_game = AnipangGame()
                        elif result == "hotris":
                            GAME_STATE = "hotris"
                            hotris_game = HOtrisGame()
                    
                    elif GAME_STATE == "anipang" and anipang_game:
                        anipang_game.handle_mouse_down(mx, my)
                    
                    elif GAME_STATE == "hotris" and hotris_game:
                        if hotris_game.handle_mouse(mx, my, "down"):
                            pass
            
            elif event.type == pygame.MOUSEMOTION:
                if GAME_STATE == "anipang" and anipang_game:
                    mx, my = event.pos
                    anipang_game.handle_mouse_move(mx, my)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and GAME_STATE == "anipang" and anipang_game:
                    mx, my = event.pos
                    anipang_game.handle_mouse_up(mx, my)
        
        # 화면 그리기
        if GAME_STATE == "menu":
            menu.draw()
        
        elif GAME_STATE == "anipang":
            if anipang_game:
                anipang_game.update(dt)
                anipang_game.draw()
        
        elif GAME_STATE == "hotris":
            if hotris_game:
                hotris_game.update(dt)
                hotris_game.draw()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
