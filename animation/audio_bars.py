def audio_bars(t, coord, ii, n_pixels, random_values):
    x, y, z = coord

    h = int(audio.positionVolume15[x])
    # print("h ", h)

    l = int(audio.lastpositionVolume15[x])
    # print("l ",l)

    if z == l:  # max volume falling
        return (250, 10, 250)
        # return (0,0,0)
    elif z > h and x < 3:  # everything below(above) the current volume
        # return (0,0,0)
        return (250, 250, 250)
    elif z > h and x < 6:
        return (250, 250, 250)
    elif z > h and x < 9:
        return (250, 250, 250)
    elif z > h:
        return (250, 250, 250)
    else:
        return (0, 0, 0)


# def bar(label, value,last):
# string = ""
# count = 0
# if value > 2000:
#     value = 2000
# while value > 0:
#     count+=1
#     string+="-"
#     value-=50
# while count < last - 1: #add space for the memory bar
#     string+=" "
#     count+=1

# string+="|"
# print(label , string)
# return count
