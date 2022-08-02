from math import cos, pi, sin, sqrt

# enum of vision types
FULLCOLOR = 0
PROTANOPIA = 1
DEUTERANOPIA = 2
TRITANOPIA = 3
MONOCHROMATIC = 4
BYR = 5

class Color():
    """Class for returning color of an index and color_spectrum of itself"""
    def __init__(self, numColors, vision_type=FULLCOLOR):
        self.vision_type = vision_type
        self.len = numColors
        
    def __str__(self):
        pallet = self.color_spectrum()
        str_out = ""
        for rgb in pallet:
            str_out += (F"\nR={round(rgb[0],3)}, G={round(rgb[1],3)}, B={round(rgb[2],3)}")
        return str_out

    def color(self, index):
        """returns the rgb values for given index"""
        # create rgb values
        red = self.r(index)
        green = self.g(index)
        blue = self.b(index)
        # return the right mix of RGB calues for the different vistion types and color palettes
        if self.vision_type == FULLCOLOR:
            return red, green, blue
        elif self.vision_type == BYR:
            return (red+green-blue), (green)/1.75, (blue-red)/2
        elif self.vision_type == MONOCHROMATIC:
            return blue/5, blue/3, blue
        elif self.vision_type == PROTANOPIA:
            return (red)/1.5, (red)/1.5, (blue)/1.5
        elif self.vision_type == DEUTERANOPIA: 
            return (red)/1.5, (red)/1.5, (blue)/1.5
        elif self.vision_type == TRITANOPIA: 
            return (red)/3, (blue)/3, (blue)/3

    def color_spectrum(self):
        """return a list of all the colors for self"""
        pallet = []
        for i in range(0,self.len+1):
            pallet.append(self.color(i))
        return pallet

class AttributeColor(Color):
    """Class for specifying vision type and calculting rgb values"""
    def __init__(self, attribute_list, vision_type, numColors=100, max_angle=(7/4)*pi):
        """attribute_list is the list of data from custom attribute of model,
        vision_type is one of the enums,
        numColors is number of colors to use,
        max_angle is the total range of the color wheel used, 2pi would be the entire wheel"""
        super().__init__(numColors, vision_type)
        self.min = min(attribute_list)
        self.max = max(attribute_list)
        # max_angle determines how much of the color wheel to use
        # offset is where to start on the color wheel, 0 is red, and it goes counter-clockwise
        if vision_type == FULLCOLOR:
            max_angle=-(7/4)*pi
            self.offset = (4/8)*pi
        elif vision_type == BYR:
            max_angle=-(6/4)*pi
            self.offset = (5/8)*pi
        elif vision_type == MONOCHROMATIC:
            max_angle = (1/4)*pi
            self.offset = -(6/8)*pi
        elif vision_type == PROTANOPIA:
            max_angle = (9/14)*pi
            self.offset = (11/16)*pi
        elif vision_type == DEUTERANOPIA:
            max_angle = (9/14)*pi
            self.offset = (11/16)*pi
        elif vision_type == TRITANOPIA:
            max_angle = (1/2)*pi
            self.offset = (9/16)*pi
            
        self.theta = max_angle

    # Sean's code for determing rgb values, don't know how it works
    def r(self, index):
        arg = -(self.theta * index / self.len) + self.offset
        return (cos(arg) + 1/2) 
            
    def g(self, index):
        arg = -(self.theta * index / self.len) +(2*pi/3) + self.offset
        return (cos(arg) + 1/2)

    def b(self, index):
        arg = -(self.theta * index / self.len) +(4*pi/3) + self.offset
        return (cos(arg) + 1/2)
    