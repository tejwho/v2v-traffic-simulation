import pygame
import math
import random

pygame.init()

# ================= SETTINGS =================
ROAD_AREA_WIDTH = 1000
DASHBOARD_WIDTH = 400
WIDTH = ROAD_AREA_WIDTH + DASHBOARD_WIDTH
HEIGHT = 700

CENTER = (ROAD_AREA_WIDTH // 2, HEIGHT // 2)
FPS = 60
NUM_VEHICLES = 8

SAFE_DISTANCE = 60
FOG_SAFE_DISTANCE = 110

ROAD_RX = 420
ROAD_RY = 250

fog_on = True

# ================= COLORS =================
WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK = (20, 20, 20)
BLUE = (0, 170, 255)
RED = (255, 70, 70)
YELLOW = (255, 255, 0)
CYAN = (0, 200, 255)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚗 V2V Smart Traffic Simulation")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 22)
big_font = pygame.font.SysFont("arial", 36)

def draw_text(text, x, y, color=WHITE):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# ================= VEHICLE =================
class Vehicle:
    def __init__(self, vid, angle):
        self.id = vid
        self.angle = angle
        self.speed = 0.9 + (vid % 4) * 0.15
        self.alert = False

    def update(self):
        self.angle += self.speed * 0.008
        if self.angle > 2 * math.pi:
            self.angle -= 2 * math.pi

    def position(self):
        x = CENTER[0] + ROAD_RX * math.cos(self.angle)
        y = CENTER[1] + ROAD_RY * math.sin(self.angle)
        return int(x), int(y)

# ================= GAME =================
class Game:
    def __init__(self):
        self.vehicles = [
            Vehicle(i + 1, i * (2 * math.pi / NUM_VEHICLES))
            for i in range(NUM_VEHICLES)
        ]
        self.closest_pair = None
        self.closest_distance = 9999
        self.running = True

    def draw_road(self):
        pygame.draw.ellipse(
            screen, GRAY,
            (CENTER[0] - ROAD_RX, CENTER[1] - ROAD_RY,
             ROAD_RX * 2, ROAD_RY * 2), 70
        )
        pygame.draw.ellipse(
            screen, WHITE,
            (CENTER[0] - ROAD_RX, CENTER[1] - ROAD_RY,
             ROAD_RX * 2, ROAD_RY * 2), 3
        )

    def v2v_logic(self):
        for v in self.vehicles:
            v.alert = False

        threshold = FOG_SAFE_DISTANCE if fog_on else SAFE_DISTANCE
        avg_radius = (ROAD_RX + ROAD_RY) / 2

        sorted_vehicles = sorted(self.vehicles, key=lambda v: v.angle)
        self.closest_distance = 9999
        self.closest_pair = None

        for i in range(len(sorted_vehicles)):
            v1 = sorted_vehicles[i]
            v2 = sorted_vehicles[(i + 1) % len(sorted_vehicles)]

            angular_gap = (v2.angle - v1.angle) % (2 * math.pi)
            distance = angular_gap * avg_radius

            if distance < self.closest_distance:
                self.closest_distance = distance
                self.closest_pair = (v1, v2)

            if distance < threshold:
                v1.alert = True
                v2.alert = True

    def draw_vehicles(self):
        for v in self.vehicles:
            x, y = v.position()
            color = RED if v.alert else BLUE
            pygame.draw.rect(screen, color, (x - 12, y - 6, 24, 12), border_radius=4)
            draw_text(f"V{v.id}", x - 10, y - 22)

    def draw_hud(self):
        draw_text(f"Fog: {'ON' if fog_on else 'OFF'} (Press F)", 20, 20, YELLOW)
        if any(v.alert for v in self.vehicles):
            banner = big_font.render("⚠ V2V ALERT ACTIVE", True, RED)
            screen.blit(banner, (300, 20))

    def draw_dashboard(self):
        pygame.draw.rect(screen, (30, 30, 30), (ROAD_AREA_WIDTH, 0, DASHBOARD_WIDTH, HEIGHT))
        pygame.draw.line(screen, (120, 120, 120), (ROAD_AREA_WIDTH, 0), (ROAD_AREA_WIDTH, HEIGHT), 2)

        y = 30
        draw_text("V2V MONITORING DASHBOARD", ROAD_AREA_WIDTH + 20, y, CYAN)
        y += 40

        draw_text(f"Fog Status: {'ON' if fog_on else 'OFF'}", ROAD_AREA_WIDTH + 20, y)
        y += 25

        threshold = FOG_SAFE_DISTANCE if fog_on else SAFE_DISTANCE
        draw_text(f"Safe Distance: {threshold} m", ROAD_AREA_WIDTH + 20, y)
        y += 40

        if self.closest_pair:
            v1, v2 = self.closest_pair
            draw_text("Closest Vehicles", ROAD_AREA_WIDTH + 20, y, YELLOW)
            y += 30

            draw_text(f"Vehicle V{v1.id} Speed: {v1.speed:.2f} m/s", ROAD_AREA_WIDTH + 20, y)
            y += 25
            draw_text(f"Vehicle V{v2.id} Speed: {v2.speed:.2f} m/s", ROAD_AREA_WIDTH + 20, y)
            y += 25
            draw_text(f"Distance (V{v1.id} ↔ V{v2.id}): {self.closest_distance:.2f} m", ROAD_AREA_WIDTH + 20, y)
            y += 30

            if self.closest_distance < threshold:
                draw_text("V2V State: WARNING", ROAD_AREA_WIDTH + 20, y, RED)
            else:
                draw_text("V2V State: NORMAL", ROAD_AREA_WIDTH + 20, y, GREEN)

    def run(self):
        global fog_on
        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    fog_on = not fog_on

            for v in self.vehicles:
                v.update()

            self.v2v_logic()

            screen.fill(DARK)
            self.draw_road()
            self.draw_vehicles()
            self.draw_hud()
            self.draw_dashboard()

            pygame.display.flip()

        pygame.quit()

# ================= MAIN =================
Game().run()