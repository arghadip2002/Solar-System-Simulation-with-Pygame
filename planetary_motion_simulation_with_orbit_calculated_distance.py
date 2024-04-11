import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1000, 630
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # Display size

# caption on the head of the display
pygame.display.set_caption("Planetary Simulation")

WHITE = (255, 255, 255)  # RGB values of White colour
YELLOW = (255, 255, 0)  # RGB values of yellow colour
BLUE = (100, 149, 237)  # RGB values of blue colour
RED = (188, 39, 50)  # RGB values of red colour
DARK_GREY = (80, 78, 81)  # RGB values of DARK_GREY colour

FONT = pygame.font.SysFont("comicsans", 20)


class planet:

    AU = 149.6e6 * 1000  # Astronomical unit
    G = 6.67428e-11  # Gravitational Constant
    SCALE = 200/AU  # 1 AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 Day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x*self.SCALE + WIDTH/2
                y = y*self.SCALE + HEIGHT/2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun/1000,1)}Km", 1, WHITE)
            win.blit(distance_text, (x - 0.5*distance_text.get_width() /
                     2, y - 0.5*distance_text.get_width()/2))

    def attraction(self, other):
        other_x = other.x
        other_y = other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def main():
    run = True

    # .Clock() --> running the animation w.r.t the clock speed of the comp processor
    clock = pygame.time.Clock()

    sun = planet(0, 0, 30, YELLOW, 1.98892*10**30)
    sun.sun = True

    mercury = planet(-0.387*planet.AU, 0, 5, DARK_GREY, 0.3*10**23)
    mercury.y_vel = 47.4*1000

    venus = planet(-0.723*planet.AU, 0, 12, WHITE, 4.8685*10**24)
    venus.y_vel = -35.02*1000

    earth = planet(-1*planet.AU, 0, 16, BLUE, 5.97219*10**24)
    earth.y_vel = 29.783*1000

    mars = planet(-1.524*planet.AU, 0, 10, RED, 6.29*10*10**23)
    mars.y_vel = 24.007*1000

    planets = [sun, earth, mars, mercury,
               venus]

    while run:
        clock.tick(60)  # runs at max 60 fps
        WIN.fill((0, 0, 0))

        # WIN.fill(WHITE)
        # pygame.display.update()  # updates the display

        for i in planets:
            i.update_position(planets)
            i.draw(WIN)

        # running a loop so that display ends only when the user click on the x icon.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


main()
