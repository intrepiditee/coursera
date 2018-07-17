"""
Program template for Spaceship

Copy to codeskulptor.com and run.
"""

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
is_started = False
rock_group = set([])
missile_group = set([])
explosion_group = set([])

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
thrusting_info = ImageInfo([135, 45], [90, 90], 35)
thrusting_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, thrusting_image, info, thrusting_info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.thrusting_image = thrusting_image
        self.thrusting_image_center = thrusting_info.get_center()
        self.thrusting_image_size = thrusting_info.get_size()
        self.thrusting_radius = thrusting_info.get_radius()
        self.acceleration = [0, 0]
        self.direction = 0

    def draw(self,canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.thrusting_image, self.thrusting_image_center, self.thrusting_image_size, self.pos, self.thrusting_image_size, self.angle)
    def update(self):
        self.angle += self.angle_vel
        self.vel[0] = 0.995 * self.vel[0] + self.acceleration[0]
        self.vel[1] = 0.995 * self.vel[1] + self.acceleration[1]
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.direction = angle_to_vector(self.angle)
        if self.thrust == True:
            self.acceleration[0] = self.direction[0] * 0.1
            self.acceleration[1] = self.direction[1] * 0.1
        else:
            self.acceleration[0] = 0
            self.acceleration[1] = 0
            
    def thrust_ship(self):
        if self.thrust == False:
            self.thrust = True
            ship_thrust_sound.play()
    
    def cancel_thrust_ship(self):
        self.thrust = False
        ship_thrust_sound.pause()

    def rotate_ship_left(self):
        self.angle_vel += -0.05

    def rotate_ship_right(self):
        self.angle_vel += 0.05

    def shoot(self):
        direction = angle_to_vector(self.angle)
        a_missile = Sprite([self.pos[0] + direction[0] * self.radius, self.pos[1] + direction[1] * self.radius], [self.vel[0] + direction[0] * 5, self.vel[1] + direction[1] * 5], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)

    def get_radius(self):
    	return self.radius

    def get_position(self):
    	return self.pos
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
        	if is_started:
	            sound.rewind()
	            sound.play()
   
    def draw(self, canvas):
    	if self.animated == True:
    		canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0] * self.age, self.image_center[1]], self.image_size, self.pos, self.image_size)
    		self.age += 1
    	else:
        	canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.pos[0] = self.pos[0] % WIDTH
        self.pos[1] = self.pos[1] % HEIGHT
        self.angle += self.angle_vel
        self.age += 1
        if self.age <= self.lifespan:
        	return True
        else:
        	return False

    def get_position(self):
    	return self.pos

    def get_radius(self):
    	return self.radius

    def collide(self, object):
    	if dist(self.pos, object.get_position()) < self.radius + object.get_radius():
    		return True
    	else:
    		return False

def group_collide(object, the_set):
	global explosion_group
	for sprite in set(the_set):
		if sprite.collide(object):
			explosion = Sprite(sprite.get_position(), [0, 0], 0, 0, explosion_image, explosion_info, explosion_sound)
			explosion_group.add(explosion)
			the_set.discard(sprite)
			return True

def group_group_collide(set1, set2):
	number_of_collision = 0
	for sprite1 in set(set1):
		if group_collide(sprite1, set2):
			number_of_collision += 1
			set1.discard(sprite1)
	return number_of_collision

def process_sprite_group(canvas, set):
	for sprite in set:
		if sprite.update():
			sprite.draw(canvas)
		else:
			set.discard(sprite)

           
def draw(canvas):
    global time, lives, score, rock_group, missile_group, is_started, my_ship, explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text('Lives = ' + str(lives), [30, 45], 30, 'Yellow')
    canvas.draw_text('Score = ' + str(score), [WIDTH - 140, 45], 30, 'Yellow')
    
    if lives == 0:
    	my_ship.cancel_thrust_ship()
    	is_started = False
    	explosion_group = set([])
    	score = 0
    	timer.stop()
    	rock_group = set([])
    	my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, thrusting_image, ship_info, thrusting_info)

    if is_started:
    	soundtrack.play()
    	# draw ship and sprites
	    my_ship.draw(canvas)
	    
	    # update ship and sprites
	    my_ship.update()
	    process_sprite_group(canvas, rock_group)
	    process_sprite_group(canvas, missile_group)
	    process_sprite_group(canvas, explosion_group)
	    if group_collide(my_ship, rock_group):
	    	lives -= 1
	    score += group_group_collide(missile_group, rock_group)
	else:
		soundtrack.rewind()
		canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    if len(rock_group) < 20:
    	if score < 30:
	    	a_rock = Sprite([random.randint(0, WIDTH), random.randint(0, HEIGHT)], [random.choice([-1, 1]) * random.random(), random.choice([-1, 1]) * random.random()], 0, random.randint(-10, 10) * 0.01, asteroid_image, asteroid_info)
	    elif  30 <= score < 60:
	    	a_rock = Sprite([random.randint(0, WIDTH), random.randint(0, HEIGHT)], [4 * random.choice([-1, 1]) * random.random(), 4 * random.choice([-1, 1]) * random.random()], 0, random.randint(-10, 10) * 0.01, asteroid_image, asteroid_info)
	    elif score >= 60:
	    	a_rock = Sprite([random.randint(0, WIDTH), random.randint(0, HEIGHT)], [6 * random.choice([-1, 1]) * random.random(), 6 * random.choice([-1, 1]) * random.random()], 0, random.randint(-10, 10) * 0.01, asteroid_image, asteroid_info)
	if dist(a_rock.get_position(), my_ship.get_position()) > 100:
	    rock_group.add(a_rock)

def keydown(key):
	if is_started:
	    if key == simplegui.KEY_MAP['up']:
	        my_ship.thrust_ship()
	    elif key == simplegui.KEY_MAP['left']:
	        my_ship.rotate_ship_left()
	    elif key == simplegui.KEY_MAP['right']:
	        my_ship.rotate_ship_right()
	    elif key == simplegui.KEY_MAP['space']:
	        my_ship.shoot()

def keyup(key):
	if is_started:
	    if key == simplegui.KEY_MAP['up']:
	        my_ship.cancel_thrust_ship()
	    elif key == simplegui.KEY_MAP['left']:
	        my_ship.rotate_ship_right()
	    elif key == simplegui.KEY_MAP['right']:
	        my_ship.rotate_ship_left()

def click(pos):
	global is_started, lives
	if is_started == False:
		if WIDTH / 2 - splash_info.get_size()[0] / 2 <= pos[0] <= WIDTH / 2 + splash_info.get_size()[0] / 2:
			if HEIGHT / 2 - splash_info.get_size()[1] / 2 <= pos[1] <= HEIGHT / 2 + splash_info.get_size()[1] / 2:
				is_started = True
				lives = 3
				timer.start()


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, thrusting_image, ship_info, thrusting_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)


# get things rolling
timer.start()
frame.start()