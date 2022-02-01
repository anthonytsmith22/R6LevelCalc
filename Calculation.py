
def get_xp(level):
    xp_total = 0
    xp_requirement = 1000
    counter = 0

    for x in range(level):
        if x == 0:
            xp_requirement = 1000
        elif x == 1:
            xp_requirement = 1500
        elif x == 2 or x == 3:
            xp_requirement = 3500
        elif x == 4 or x == 5:
            xp_requirement = 4000
        elif 6 <= x <= 8:
            xp_requirement = 4500
        elif x == 9 or x == 10:
            xp_requirement = 5500
        if 9 <= x < 37:
            counter += 1
            if counter == 3:
                xp_requirement += 500
                counter = 0
        elif x == 38 or x == 39:
            xp_requirement = 11000
        elif x >= 40:
            xp_requirement += 500
        xp_total += xp_requirement
        # print(f"{x} -> {x + 1} = {xp_requirement}")
    return xp_total


def get_xp2(level):
    counter = 0
    xp_requirement = 0
    for x in range(level):
        if x == 0:
            xp_requirement = 1000
        elif x == 1:
            xp_requirement = 1500
        elif x == 2 or x == 3:
            xp_requirement = 3500
        elif x == 4 or x == 5:
            xp_requirement = 4000
        elif 6 <= x <= 8:
            xp_requirement = 4500
        elif x == 9 or x == 10:
            xp_requirement = 5500
        if 9 <= x < 37:
            counter += 1
            if counter == 3:
                xp_requirement += 500
                counter = 0
        elif x == 38 or x == 39:
            xp_requirement = 11000
        elif x >= 40:
            xp_requirement += 500
    return xp_requirement


def get_level(xp_total):
    current_xp = 0
    level = 0
    xp_requirement = 0
    while current_xp < xp_total:
        xp_requirement = get_xp2(level)
        if current_xp + xp_requirement < xp_total:
            level += 1
            current_xp += xp_requirement
        else:
            break
    return level
