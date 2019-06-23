import color_utils
#To use backAndForth
#timer = 0
#reset = 1 ## always start with 1
    #timer, reset = backAndForth(min,max,timer,inc,reset)

def backAndForth(min,max,pos,inc,reset):
    count = pos
    if (count < max) and (reset == 1):
        count = count + inc
    elif count >= min:
        count -= inc
        reset = 0
    else:
        reset = 1
    return (count, reset)

#-------------------------------------------------------------------------------
#Mapping function

def scale(val, src, dst):
    """
    Scale the given value from the scale of src to the scale of dst.
    """
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]




#-----------------------------------------------------------

def count(pos,max,inc):
    if pos < max:
        pos += inc
    return(pos)

#-----------------------------------------------------------

def inverse(x):
    x = int(x)
    var = [8,7,6,5,4,3,2,1,0]
    if x > 8:
        return (0)
    x = var[x]
    return (x)


#-----------------------------------------------------------

def graph(volume,pitch):

    r = 0
    g = 200
    b = 200
    count = 0
    while count < 15:
        #print volume[count]
        volume[count] = volume[count +1]
        pitch[count] = pitch[count +1]
        count += 1

    return(r,g,b,volume,pitch)



#-----------------------------------------------------------


def circle(centerX,centerZ, x, z,color):

      #color = r,g,b
      r = 0
      g = 200
      b = 200
      r,g,b = color

      if centerX == x and centerZ == z:
          b = 200
          r = 200
          g = 200
      elif ((centerX + 1 == (x) or centerX - 1 == (x)) and centerZ == z) or ((centerZ + 1 == (z) or centerZ - 1 == (z)) and centerX == x):
          r *= .8
          g *= .8
          b *= .8
      elif (centerX == (x + 1) or centerX == (x - 1)) and (centerZ == (z + 1) or centerZ == (z - 1)):
          r *= .7
          g *= .7
          b *= .7
      elif ((centerX -2 == x or centerX + 2 == x) and centerZ == z) or ((centerZ + 2 == (z) or centerZ - 2 == (z)) and centerX == x):
          r *= .5
          g *= .5
          b *= .5
      elif (centerX + 2 == (x) or centerX - 2 == (x)) and (centerZ + 1 == (z) or centerZ - 1 == (z)) or (centerZ + 2 == (z) or centerZ - 2 == (z)) and (centerX + 1 == (x) or centerX - 1 == (x)):
          r *= .3
          g *= .3
          b *= .3
      elif (centerX + 2 == (x) or centerX - 2 == (x)) and (centerZ + 2 == (z) or centerZ - 2 == (z)):
          r *= .15
          g *= .15
          b *= .15
      else:
          r = 0
          g = 0
          b = 0

      return(r,g,b)

#----------------------------------------------------------------
#step 1 - 6

def boom(centerX,centerZ, x, z,color,step,total):
    coord = x,z
    center = centerX,centerZ
    r,g,b = 0,0,0
    #print "boom draw loop"
    colorVar = scale(step,(0,total),(0,1))
    

    if step == 0:
        return (r,g,b)
    elif step >= 1 and step < 2:
        if coord == center:
            r,g,b = color
            r *= colorVar
            g *= colorVar
            b *= colorVar
    elif step >= 2 and step < 3:
        if (centerX == x or centerX + 1 == x or centerX - 1 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z):
            r,g,b = color
            r *= colorVar
            g *= colorVar
            b *= colorVar
    elif step >= 3 and step < 4:
        if (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z):
            r,g,b = color
            r *= colorVar
            g *= colorVar
            b *= colorVar
    elif step >= 4 and step < 5:
        if (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x or centerX + 3 == x or centerX - 3 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z or centerZ + 3 == z or centerZ - 3 == z):
            r,g,b = color
            r *= colorVar
            g *= colorVar
            b *= colorVar
    elif step >= 5 and step < 6:
        if (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x or centerX + 3 == x or centerX - 3 == x or centerX + 4 == x or centerX - 4 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z or centerZ + 3 == z or centerZ - 3 == z or centerZ + 4 == z or centerZ - 4 == z):
            r,g,b = color
            r *= colorVar
            g *= colorVar
            b *= colorVar

    elif step >= 6:
        r,g,b = 0,0,0


    return(r,g,b)

#-----------------------------------------------------------
#step 1 - 6


def ripple(centerX,centerZ, x, z,color,step):
    coord = x,z
    center = centerX,centerZ
    r,g,b = 0,0,0
    if step == 1:
        if coord == center:
            r,g,b = color

    elif step == 2:
        if coord == center:
            r,g,b = 0,0,0
        elif (centerX == x or centerX + 1 == x or centerX - 1 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z):
            r,g,b = color

    elif step == 3:
        if (centerX == x or centerX + 1 == x or centerX - 1 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z):
            r,g,b = 0,0,0
        elif (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z):
            r,g,b = color

    elif step == 4:
        if (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z):
            r,g,b = 0,0,0
        elif (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x or centerX + 3 == x or centerX - 3 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z or centerZ + 3 == z or centerZ - 3 == z):
            r,g,b = color

    elif step == 5:
        if (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x or centerX + 3 == x or centerX - 3 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z or centerZ + 3 == z or centerZ - 3 == z):
            r,g,b = 0,0,0
        elif (centerX == x or centerX + 1 == x or centerX - 1 == x or centerX + 2 == x or centerX - 2 == x or centerX + 3 == x or centerX - 3 == x or centerX + 4 == x or centerX - 4 == x) and (centerZ == z or centerZ + 1 == z or centerZ - 1 == z or centerZ + 2 == z or centerZ - 2 == z or centerZ + 3 == z or centerZ - 3 == z or centerZ + 4 == z or centerZ - 4 == z):
            r,g,b = color
    elif step == 6:
        r,g,b = 0,0,0

    return(r,g,b)

#-----------------------------------------------------------

def lineX(centerZ,x,z,color,mod):
    r,g,b = 0,0,0
    x = float(x)
    if z == centerZ + 1 and x % 2 == 0 and mod == 1:
        r,g,b = color
    elif z == centerZ and x % 2 !=0 and mod == 1:
        r,g,b = color
    elif z == centerZ and mod == 0:
        r,g,b = color


    return(r,g,b)

def volumeWave(centerZ,x,z,color,volume,volumeMin,volumeMax):
    r,g,b = 0,0,0
    x = float(x)
    volumeScale = scale(volume, (volumeMin,volumeMax), (centerZ,5))


    if z <= centerZ and volumeScale - 3 <= z:
        r,g,b = color
    if z <= centerZ and int(volumeScale - 1) == z:
        var = volumeScale - int(volumeScale)
        r *= scale(var,(0,1),(1,0))
        g *= scale(var,(0,1),(1,0))
        b *= scale(var,(0,1),(1,0))
        if x % 2 != 0:
            r *= .8
            g *= .8
            b *= .8

    if z <= centerZ and int(volumeScale - 2) == z:
        var = volumeScale - int(volumeScale)
        r *= scale(var,(0,1),(.8,0))
        g *= scale(var,(0,1),(.8,0))
        b *= scale(var,(0,1),(.8,0))
        if x % 2 != 0:
            r *= .2
            g *= .2
            b *= .2

    if z <= centerZ and int(volumeScale - 3) == z:
        var = volumeScale - int(volumeScale)
        r *= scale(var,(0,1),(.7,0))
        g *= scale(var,(0,1),(.7,0))
        b *= scale(var,(0,1),(.7,0))
        if x % 2 != 0:
            r *= .1
            g *= .1
            b *= .1






    return(r,g,b)

#-----------------------------------------------------------

def lineY():
    return()

#-----------------------------------------------------------
