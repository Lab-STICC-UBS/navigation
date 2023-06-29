# %%
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.transforms as transforms

TOPMARKS_LIST =['green', 'green_bis', 'red', 'red_bis', 'north', 'south', 'east', 'west', 
                'danger', 'special', 'safe_water', 'emergency']
LANDMARKS_LIST = ['lighthouse', 'major_lighthouse', 'land_tower', 'water_tower', 'church']
DANGERS_LIST = ['wreck', 'wreck_depth', 'danger','rock_covers','rock_depth']

class PlotMark:
    """ Plot mark """
    text_shift = 0.0002
    markersize = 30
    
    def __init__(self, position_x, position_y, mark_type, light_color=None, name = None ):
        self.position_x = position_x
        self.position_y = position_y
        self.mark_type = mark_type.lower()
        self.name = name
        self.light_color = light_color
        if self.mark_type in DANGERS_LIST:
            self.plot_danger_mark()
        if self.mark_type in LANDMARKS_LIST:
            self.plot_land_mark()
        if light_color is not None:
            self.plot_light_mark(light_color)
        if self.name is not None:
            plt.text(self.position_x + self.text_shift, self.position_y + self.text_shift, self.name)


    def plot_light_mark(self, color, angle = None):
        """ Plot light mark """
        if angle is None:
            angle = -0.45
        marker = build_light_path(angle)
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle= None, 
                 markeredgecolor=color,
                markerfacecolor=color, markersize=self.markersize)

    def plot_danger_mark(self):
        """ plot danger marks """
        marker_size = self.markersize/2
        
        if self.mark_type == 'danger':
            facecolor ='skyblue'
        else:
            facecolor='k'
        match self.mark_type:
            case 'wreck':
                marker = build_wreck_path()
            case 'wreck_depth':
                marker = build_wreck_depth_path()
            case 'danger':
                marker = Path.unit_circle()
            case 'rock_covers':
                # plt.plot(position_x, position_y,'xk', markersize=markersize,)
                marker = (8,2,0.5)
                marker_size = marker_size/2
            case 'rock_depth':
                marker = '+'
                marker_size = marker_size/2
            case _:
                print('not defined danger')
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle='solid',
            markerfacecolor=facecolor, markeredgecolor='k',
            markeredgewidth=0.5,
            markersize=marker_size, label=type)
        if self.mark_type == 'wreck':
            self.plot_white_circle(10)

    def plot_land_mark(self):
        """ plot land_marks """
        markersize = self.markersize
        match self.mark_type:
            case 'lighthouse':
                marker = Path.unit_regular_star(5,0.3)
                facecolor='k'
                markersize = markersize/4
            case 'major_lighthouse':
                marker = Path.unit_regular_star(5,0.3)
                facecolor='k'
                markersize = markersize/3
            case 'land_tower':
                marker = build_land_tower_path(10,3)
                facecolor='none'
                self.plot_white_circle(10)
            case 'water_tower':
                marker = build_water_tower_path(10,3)
                facecolor='none'
                self.plot_white_circle(10)
            case 'church':
                marker = build_church_path()
                facecolor ='k'
                markersize = markersize/4
            case _:
                print('not defined landmark!')
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle='solid',
                markerfacecolor=facecolor, markeredgecolor='k',
                markersize=markersize, label=type)
        if self.mark_type.lower() == 'major_lighthouse':
            plt.plot(self.position_x, self.position_y, marker='o', linestyle='solid',
                markerfacecolor=self.light_color, markeredgecolor=self.light_color,
                markersize=markersize/6, label=type)
            

    def plot_sea_mark(self, top_mark_type = None, show_top_mark = True, floating = False):
        """ plot nautical symbol """
        shape_height = 12
        topmark_size = 2
        color, color2 = select_color(top_mark_type)
        markersize = self.markersize
        shape_marker, shape_marker2 = self.select_shape(top_mark_type, shape_height)
        if show_top_mark is not True:
            symbol_marker = shape_marker
            symbol_marker2 = shape_marker2
            markersize = 2*markersize/3
        else:
            topmark_marker = select_topmark_marker(top_mark_type, topmark_size, shift_up=shape_height + 2)
            symbol_marker = Path.make_compound_path(shape_marker, topmark_marker)
            symbol_marker2 = Path.make_compound_path(shape_marker2, topmark_marker)

        if floating:
            symbol_marker = symbol_marker.transformed(transforms.Affine2D().rotate(-0.3))
            symbol_marker2 = symbol_marker2.transformed(transforms.Affine2D().rotate(-0.3))

        if self.mark_type == 'spar':
            self.plot_ref_line(self.markersize/4)
        else:
            self.plot_ref_line(self.markersize/2)
        
        plt.plot(self.position_x, self.position_y, marker=symbol_marker, linestyle='solid',
                markerfacecolor=color,
                markeredgecolor='k',markeredgewidth=0.5,
                markersize=markersize)
        plt.plot(self.position_x, self.position_y, marker=symbol_marker2, linestyle='solid',
                markerfacecolor=color2,
                markeredgecolor='k',markeredgewidth=0.5,
                markersize=markersize)
        
        self.plot_white_circle(shape_height)
        
        
    def plot_ref_line(self,size):
        """ Build point path """
        marker = Path([(-1,0), (1,0)],[1,2])
        plt.plot(self.position_x, self.position_y, marker=marker, 
                markeredgecolor='k',
                markeredgewidth=0.5,
                markersize=size)
        
    def plot_white_circle(self,circle_size):
        """ plot white circle"""
        circle_path = build_circle_path(circle_size,0)
        plt.plot(self.position_x, self.position_y, marker=circle_path,
                markerfacecolor='white', markeredgecolor='k',
                markeredgewidth=0.2,
                markersize=self.markersize/12)

    def select_shape(self, top_mark_type, shape_height):
        """ select shape """
        width = 10
        match self.mark_type:
            case 'spar':
                shape_marker = build_rectangle_path(shape_height, width/5, 0)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = build_rectangle_path(shape_height/3, width/5, 0)
                        marker_tmp2 = build_rectangle_path(shape_height/3, width/5, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = build_rectangle_path(shape_height/2, width/5, shape_height/2)
                    case 'south':
                        shape_marker2 = build_rectangle_path(shape_height/2, width/5, 0)   
                    case 'west':
                        shape_marker2 = build_rectangle_path(shape_height/3, width/5, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = build_rectangle_path(shape_height, width/15, 0)
                    case 'emergency':
                        shape_marker2 = build_rectangle_path(shape_height, width/15, 0)
                    case _:
                        shape_marker2 = shape_marker
            case 'can':
                shape_marker = build_rectangle_path(shape_height, width,0)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = build_rectangle_path(shape_height/3, width, 0)
                        marker_tmp2 = build_rectangle_path(shape_height/3, width, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = build_rectangle_path(shape_height/2, width, shape_height/2)
                    case 'south':
                        shape_marker2 = build_rectangle_path(shape_height/2, width, 0)   
                    case 'west':
                        shape_marker2 = build_rectangle_path(shape_height/3, width, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = build_rectangle_path(shape_height, width/3, 0)
                    case 'emergency':
                        shape_marker2 = build_rectangle_path(shape_height, width/3, 0)
                    case _:
                        shape_marker2 = shape_marker
                
                
            case 'spherical':
                shape_marker = build_spherical(width*3/4, -30, 210, width*3/8)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = build_spherical(width*3/4, 30, 150, width*3/8)
                        marker_tmp2 = build_tower_path(width/3, 5*width/8, width*3/4, 0)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = build_spherical(width*3/4, 0, 180, width*3/8)
                    case 'south':
                        shape_marker2 = build_tower_path(width/3, 5*width/8, width*3/4, 0)
                    case 'west':
                        shape_marker2 = build_tower_path(width/3, width*3/4, 5*width/8, width/3)
                    case 'safe_water':
                        shape_marker2 = build_triangle_path(width/2, shape_height, 0)
                    case 'emergency':
                        shape_marker2 = build_triangle_path(width/2, shape_height, 0)
                    case _:
                        shape_marker2 = shape_marker
            case 'conical':
                shape_marker = build_conical_path(shape_height, width)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = build_tower_path(shape_height/3, width/2, 3*width/8, 0)
                        marker_tmp2 = build_triangle_path(  width/2 ,shape_height/3, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = build_triangle_path(3*width/4, 2*shape_height/3, shape_height/3)
                    case 'south':
                        shape_marker2 = build_tower_path(shape_height/3, width/2, 3*width/8, 0)
                    case 'west':
                        shape_marker2 = build_tower_path(shape_height/3, width/2, width/4, shape_height/4)
                    case 'safe_water':
                        shape_marker2 = build_triangle_path(shape_height/2, shape_height, 0)
                    case 'emergency':
                        shape_marker2 = build_triangle_path(shape_height/2, shape_height, 0)
                    case _:
                        shape_marker2 = shape_marker
                
            case 'pillar':
                shape_marker = build_pillar_path(shape_height, width)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = build_tower_path(shape_height/3, width/2, width/4,0)
                        marker_tmp2 = build_tower_path(shape_height/3, width/6, width/8, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'south':
                        shape_marker2 = build_tower_path(shape_height/3, width/2, width/4,0)
                    case 'north':
                        shape_marker2 = build_tower_path(2*shape_height/3, width/4, width/8, shape_height/3)
                    case 'west':
                        shape_marker2 = build_tower_path(shape_height/3, width/4, width/6, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = build_rectangle_path(shape_height, width/8, 0)
                    case 'emergency':
                        shape_marker2 = build_rectangle_path(shape_height, width/8, 0)
                    case _:
                        shape_marker2 = shape_marker
            case 'tower':
                shape_marker = build_tower_path(shape_height, width, 3*width/4, 0)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = build_tower_path(shape_height/3, width, 10*width/12, 0)
                        marker_tmp2 = build_tower_path(shape_height/3, 10*width/12, 3*width/4, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = build_tower_path(shape_height/2, 10*width/12, 3*width/4, shape_height/2)
                    case 'south':
                        shape_marker2 = build_tower_path(shape_height/2, width, 10*width/12, 0)
                    case 'west':
                        shape_marker2 = build_tower_path(shape_height/3, 11*width/12, 10*width/12, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = build_rectangle_path(shape_height, width/3, 0)
                    case 'emergency':
                        shape_marker2 = build_rectangle_path(shape_height, width/3, 0)
                    case _:
                        shape_marker2 = shape_marker
            case _:
                print('not defined shape')
        return shape_marker, shape_marker2

def select_color(top_mark_type):
    """ select color """
    match top_mark_type.lower():
        case 'green':
            color = 'green'
            color2 = 'green'
        case 'green_bis':
            color = 'red'
            color2 = 'green'
        case 'red' :
            color = 'red'
            color2 = 'red'
        case 'red_bis':
            color = 'green'
            color2 = 'red'
        case 'special':
            color ='yellow'
            color2 ='yellow'
        case 'safe_water':
            color ='white'
            color2 ='red'
        case 'danger':
            color ='red'
            color2 = 'black'
        case 'emergency':
            color = 'blue'
            color2 = 'yellow'
        case _:
            color = 'yellow'
            color2 = 'black'
    return color, color2



def select_topmark_marker(top_mark_type, size, shift_up):
    """ select topmark marker """
    match top_mark_type.lower():
        case 'green':
            topmark_marker = green_topmark(size, shift_up)
        case 'green_bis':
            topmark_marker = green_topmark(size, shift_up)
        case 'red':
            topmark_marker = red_topmark(height=size*2, width=size*2, shift_up=shift_up)
        case 'red_bis':
            topmark_marker = red_topmark(height=size*2, width=size*2, shift_up=shift_up)
        case 'south':
            topmark_marker = south_topmark(size, shift_up)
        case 'north':
            topmark_marker = north_topmark(size, shift_up)
        case 'east':
            topmark_marker = east_topmark(size, shift_up)
        case 'west':
            topmark_marker = west_topmark(size, shift_up)
        case 'danger':
            topmark_marker = danger_topmark(size, shift_up)
        case 'special':
            topmark_marker = build_cross_path(shift_up + size, size)
        case 'safe_water':
            topmark_marker = build_circle_path(size, shift_up + size)
        case 'emergency':
            topmark_marker = build_cross_path2(shift_up + size, size)
        case _:
            print(' Not a valid topmark')
    return topmark_marker

def build_triangle_path(width, height, shift_up):
    """ Build a triangle path """
    vertices = [(-width/2, shift_up), (0, shift_up + height), (width/2, shift_up), (-width/2, shift_up)]
    codes = [1, 2, 2, 79]
    triangle_path = Path(vertices,codes)
    return triangle_path 

def build_triangle_down_path(size, shift_up):
    """ Build a triangle path """
    vertices = [(0, shift_up), (-size, shift_up + 2*size), (size, shift_up + 2*size), (0, shift_up)]
    codes = [1, 2, 2, 79]
    triangle_path = Path(vertices,codes)
    return triangle_path 

def build_rectangle_path(height, width, shift_up):
    """ Build a rectangle path """
    vertices = [(-width/2, shift_up), (-width/2, height + shift_up), 
                (width/2, height + shift_up), (width/2, shift_up), (-width/2, shift_up)]
    codes = [1, 2, 2, 2, 79]
    rectangle_path = Path(vertices,codes)
    return rectangle_path

def build_conical_path(height, width):
    """ Buils conocal curved path"""
    vertices =[(-width/2,0), (-width/2, height/3), (0,height), (width/2, height/3), (width/2,0),(-width/2,0)]
    codes = [1,3,2,3,2,79]
    conical_path = Path(vertices,codes)
    return conical_path

def build_pillar_path(height, width):
    """ Buils pillar path"""
    vertices =[(-width/2,0), (-width/4, height/3), (-width/8,height),(width/8,height), (width/4, height/3), (width/2,0),(-width/2,0)]
    codes = [1,2,2,2,2,2,79]
    pillar_path = Path(vertices,codes)
    return pillar_path

def build_cross_path(height, width):
    """ Build diagonal cross path """
    vertices = [(width/3*0, width/3*1 + height), (width/3*2, width/3*3 + height), (width/3*3, width/3*2 + height),
        (width/3*1, width/3*0 + height), (width/3*3, width/3*-2 + height), (width/3*2, width/3*-3 + height),
        (width/3*0, width/3*-1 + height), (width/3*-2, width/3*-3 + height), (width/3*-3, width/3*-2 + height),
        (width/3*-1, width/3*0 + height), (width/3*-3, width/3*2 + height), (width/3*-2, width/3*3 + height), (width/3*0, width/3*1 + height)]
    codes = [1,2,2,2,2,2,2,2,2,2,2,2,79]
    cross_path = Path(vertices, codes)
    return cross_path

def build_cross_path2(height, width):
    """ Build horizontal cross path """
    vertices = [(width/4, width/4 + height), (width, width/4 + height), (width, -width/4 + height), (width/4, -width/4 + height),
        (width/4, -width + height), (-width/4, -width + height), (-width/4, -width/4 + height),
        (-width, -width/4 + height), (-width, width/4 + height), (-width/4, width/4 + height),
        (-width/4, width/4 + height), (-width/4, width + height), (width/4, width + height), (width/4, width/4 + height)]
    codes = [1,2,2,2,2,2,2,2,2,2,2,2,2,79]
    cross_path = Path(vertices, codes)
    return cross_path

def build_tower_path(height, width_botton, width_top, shift_up):
    """ build tower path """
    vertices = [(-width_botton, shift_up), (-width_top, height + shift_up), (width_top, height + shift_up), (width_botton,shift_up), (-width_botton,shift_up)]
    codes = [1, 2, 2, 2, 79]
    tower_path = Path(vertices, codes)
    return tower_path

def build_church_path():
    """ Build church path """
    vertices = [(0,0), (0,2), (-1,3), (1,3), (0,2), (0,0), (2,0), (3,1), (3,-1), (2,0),
        (0,0), (0,-2), (1,-3), (-1,-3), (0,-2), (0,0), (-2,0), (-3,-1), (-3,1), (-2,0), (0,0)]
    codes=[1,3,2,2,3, 2,3,2,2,3, 2,3,2,2,3, 2,3,2,2,3, 79]
    church_path = Path(vertices, codes)
    return church_path

def build_land_tower_path(height, width):
    """ build tower path """
    botton_tower_path = build_tower_path(height*3/4, width, width/2, 0)
    top_tower_path = build_rectangle_path(height/4,width,height*3/4)
    land_tower_path = Path.make_compound_path(botton_tower_path, top_tower_path)
    return land_tower_path

def build_water_tower_path(height, width):
    """ build tower path """
    botton_tower_path = build_tower_path(height*3/4, width, width/2, 0)
    top_tower_path = build_rectangle_path(height/4, 2*width, height*3/4)
    land_tower_path = Path.make_compound_path(botton_tower_path, top_tower_path)
    return land_tower_path

def build_wreck_path():
    """ build wreck path"""
    vertices =[(-2,0), (-3,2), (3,0), (-2,0)]
    codes = [1,2,2,79]
    boat_path = Path(vertices, codes)
    mast_path = Path([(0,0), (1,3)], [1,2])
    ref_line_path = Path([(-3,0), (3.5,0) ],[1,2])
    wreck_path = Path.make_compound_path(boat_path, mast_path, ref_line_path)
    return wreck_path

def build_wreck_depth_path():
    """ build wreck path"""
    vertices =[(-2,0), (2,0), (0,1), (0,-1), (-1,0.5), (-1,-0.5), (1,0.5), (1,-0.5)]
    codes = [1,2,1,2,1,2,1,2]
    wreck_depth_path = Path(vertices, codes)
    return wreck_depth_path


def build_light_path(angle):
    """ build light path """
    vertices = [(1,0), (6,1), (6.5, 0.9), (6.8,0.7), (7,0), (6.8,-0.7 ), (6.5, -0.9), (6,-1),(6,0)]
    codes = [1,2,3,3,2,3,3,2,79]
    light_path = Path(vertices,codes)
    light_path = light_path.transformed(transforms.Affine2D().rotate(angle))
    return light_path

def build_spherical(width, angle_start, angle_stop, shift_up):
    """ Build spherical path"""
    tmp = Path.arc(angle_start,angle_stop)
    vertices = tmp.vertices*width
    for vertice in vertices:
        vertice[1]=vertice[1] + shift_up
    codes = tmp.codes
    spherical_path = Path(vertices, codes)
    return spherical_path

def build_circle_path(size, shift_up):
    """ Build circle path """
    circle = Path.circle([0.0, shift_up], size)
    return circle

def green_topmark(size, shift_up):
    """ plot green beacon """
    triangle_marker = build_triangle_path(2*size, 2*size, shift_up)
    return triangle_marker

def red_topmark(height, width, shift_up):
    """ Plot red beacon """
    red_marker = build_rectangle_path(height,width,shift_up)
    return red_marker

def north_topmark(size, shift_up):
    """ Plot north beacon """
    triangle_marker1 = build_triangle_path(2*size, 2*size, shift_up)
    triangle_marker2 = build_triangle_path(2*size, 2*size, shift_up + 2*size + 2)
    north_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return north_marker

def south_topmark(size, shift_up):
    """ Plot north beacon """
    triangle_marker1 = build_triangle_down_path(size, shift_up)
    triangle_marker2 = build_triangle_down_path(size, shift_up + 2*size + 2)
    south_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return south_marker

def east_topmark(size, shift_up):
    """ Plot east beacon """
    triangle_marker1 = build_triangle_down_path(size, shift_up)
    triangle_marker2 = build_triangle_path(2*size, 2*size, shift_up + 2*size + 2)
    east_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return east_marker

def west_topmark(size, shift_up):
    """ Plot west beacon """
    triangle_marker1 = build_triangle_path(2*size, 2*size, shift_up)
    triangle_marker2 = build_triangle_down_path(size, shift_up + 2*size + 2)
    west_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return west_marker

def danger_topmark(size, shift_up):
    """ Plot danger beacon """
    circle_marker1 = build_circle_path(size, shift_up + size)
    circle_marker2 = build_circle_path(size, shift_up + 3*size + 2)
    danger_marker = Path.make_compound_path(circle_marker1, circle_marker2)
    return danger_marker

if __name__ == "__main__":

    
    shape_type_list =['conical','can','spherical','spar','pillar','tower']
    
    PlotMark.markersize = 50

    plt.figure(1,figsize=(10,5) )
    for j, shape in enumerate(shape_type_list):
        plt.text(1,j*2,shape.capitalize(), horizontalalignment='center')

    for i, topmark in enumerate(TOPMARKS_LIST):
        plt.text(i+2,len(shape_type_list)*2, topmark.capitalize(),
                 horizontalalignment='left', rotation = 30)
        for j, shape in enumerate(shape_type_list):
            sea_mark = PlotMark(i+2, j*2,shape)
            sea_mark.plot_sea_mark(top_mark_type=topmark, floating=False)
    plt.title('Sea marks as a function of shape and topmark')
    
    
    plt.plot(1,13,'*')
    plt.axis('off')
    #plt.show(block="True")
    plt.draw()

    plt.figure(2)
    

    plt.text(1,15,'Land marks')
    for i, mark in enumerate(LANDMARKS_LIST):
        plt.text(i*2 + 4,16,mark.capitalize(), horizontalalignment='left', rotation = 30)
        land_mark = PlotMark(i*2+4, 15, mark)
    
    plt.text(1,19,'Danger marks')
    for i, mark in enumerate(DANGERS_LIST):
        plt.text(i*2 + 4,20,mark.capitalize(), horizontalalignment='left', rotation = 30)
        danger_mark = PlotMark(i*2+4,19,mark)
    plt.text(1,23,'Light')
    
    
    light1 = PlotMark(3, 23,'Spar',light_color='yellow')
    light1.plot_sea_mark('East',floating=True)
    
    light2 = PlotMark(5, 23,'Can', light_color='green')
    light2.plot_sea_mark('Green', floating=False)
    
    light3 = PlotMark(7, 23, 'lighthouse',light_color='red')
    
    plt.plot(1,25,'*')
    

    plt.axis('off')
    plt.title('Nautical symbols')
    plt.show()
