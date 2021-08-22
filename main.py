import time
import cube
import ev3_socket
import threading
from ursina import *

cube = cube.CUBE()

#ev3 = ev3_socket.cube_robot()

def solve_thread():
    engine.action_mode = False
    engine.message.text = "Get Solution..."
    solution = cube.get_solution()
    engine.message.text = "Start Solve"
    start_time = time.time()
    # for rotation in solution:
    #     ev3.rotate(rotation)

    #     time.sleep(0.45)
    engine.action_mode = True
    engine.message.disable()
    for CUBE in engine.CUBES:
        CUBE.disable()
    cube.set_cube()
    engine.load_game()
    engine.message.text = str(round(time.time() - start_time, 3))

def solve_ev3_cube():
    threading.Thread(target=solve_thread,args =()).start()

class main_engine(Ursina):
    def __init__(self):
        super().__init__()
        window.fullscreen = True
        EditorCamera()
        camera.world_position = (0, 0, -15)
        self.model, self.texture = 'src/custom_cube', 'src/rubik_texture'
        self.load_game()
        self.solve_button = Button(text="solve", scale=0.2, x=0.6, text_size=5)
        self.solve_button.on_click = solve_ev3_cube

    def load_game(self):
        self.create_cube_positions()
        self.CUBES = [Entity(model=self.model, texture=self.texture, position=pos) for pos in self.SIDE_POSITIONS]
        self.PARENT = Entity()
        self.rotation_axes = {'L': 'x', 'R': 'x', 'U': 'y', 'D': 'y', 'F': 'z', 'B': 'z'}
        self.cubes_side_positons = {'L': self.L, 'D': self.D, 'R': self.R, 'F': self.F,
                                    'B': self.B, 'U': self.U}
        self.animation_time = 0.3
        self.action_trigger = True
        self.action_mode = False
        self.message = Text(origin=(0, 19), color=color.red, y=0.95, size = 0.07)

        self.toggle_game_mode()
        self.create_sensors()

    def rotate_side_without_animation(self, side_name):
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                exec(f'self.PARENT.rotation_{rotation_axis} = 90')

    def create_sensors(self):
        create_sensor = lambda name, pos, scale: Entity(name=name, position=pos, model='cube', color=color.dark_gray,
                                                        scale=scale, collider='box', visible=False)
        self.L_sensor = create_sensor(name='L', pos=(-0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.F_sensor = create_sensor(name='F', pos=(0, 0, -0.99), scale=(3.01, 3.01, 1.01))
        self.B_sensor = create_sensor(name='B', pos=(0, 0, 0.99), scale=(3.01, 3.01, 1.01))
        self.R_sensor = create_sensor(name='R', pos=(0.99, 0, 0), scale=(1.01, 3.01, 3.01))
        self.U_sensor = create_sensor(name='U', pos=(0, 1, 0), scale=(3.01, 1.01, 3.01))
        self.D_sensor = create_sensor(name='D', pos=(0, -1, 0), scale=(3.01, 1.01, 3.01))

    def toggle_game_mode(self):
        self.action_mode = not self.action_mode


    def toggle_animation_trigger(self):
        self.action_trigger = not self.action_trigger

    def rotate_side(self, side_name, times):
        self.action_trigger = False
        cube_positions = self.cubes_side_positons[side_name]
        rotation_axis = self.rotation_axes[side_name]
        self.reparent_to_scene()
        for cube in self.CUBES:
            if cube.position in cube_positions:
                cube.parent = self.PARENT
                angle = -90*times if side_name in "B D L" else 90*times
                eval(f'self.PARENT.animate_rotation_{rotation_axis}({angle}, duration={self.animation_time*abs(times) - (0.3*(abs(times)-1))})')
        invoke(self.toggle_animation_trigger, delay= (self.animation_time*abs(times)) + 0.11)

    def reparent_to_scene(self):
        for cube in self.CUBES:
            if cube.parent == self.PARENT:
                world_pos, world_rot = round(cube.world_position, 1), cube.world_rotation
                cube.parent = scene
                cube.position, cube.rotation = world_pos, world_rot
        self.PARENT.rotation = 0

    def create_cube_positions(self):
        self.L = {Vec3(-1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.D = {Vec3(x, -1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.F = {Vec3(x, y, -1) for x in range(-1, 2) for y in range(-1, 2)}
        self.B = {Vec3(x, y, 1) for x in range(-1, 2) for y in range(-1, 2)}
        self.R = {Vec3(1, y, z) for y in range(-1, 2) for z in range(-1, 2)}
        self.U = {Vec3(x, 1, z) for x in range(-1, 2) for z in range(-1, 2)}
        self.SIDE_POSITIONS = self.L | self.D | self.F | self.B | self.R | self.U

    def input(self, key):
        if key == 'mouse1' and self.action_mode and self.action_trigger:
            for hitinfo in mouse.collisions:
                collider_name = hitinfo.entity.name
                if collider_name in 'L R F B U D':
                    cube.rotate(collider_name)
                    self.rotate_side(collider_name, 1) 
                    #ev3.rotate(collider_name)
                    break
        
        super().input(key)

engine = main_engine()
engine.run()
