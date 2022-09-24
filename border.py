from swamp import Duck, Shrimp, Newt


def map_border_check(creature, width, height, land_height):
    # check left and right boarder for all creature
    if creature.x < 0:
        creature.x = 0
    # "WIDTH - creature.get_size()" --- prevent living cross border at the first time
    if creature.x > width - creature.get_size():
        creature.x = width - creature.get_size()
    # check bottom boarder for all
    # "HEIGHT - creature.get_size()" --- prevent living cross border at the first time
    if creature.y >= height - creature.get_size():
        creature.y = height - creature.get_size()
    # check top boarder for each differently
    # for Duck
    if (isinstance(creature, Duck) or isinstance(creature, Newt)) and creature.y < 0:
        creature.y = 0
    # for Newt
    if isinstance(creature, Shrimp) and creature.y < land_height:
        # stay in water
        creature.y = land_height


def mountains_border_check(pos_x, pos_y, creature, my_map):
    # find the nearst border point before moving
    [n_x, n_y] = min([t for t in my_map.mountains_borders],
                     key=lambda t: pow(t[0] - pos_x, 2) + pow(t[1] - pos_y, 2))
    #  if the rectangle area of passing through contains any mountain points
    # (maybe few points, it is ok,like conor of triangle mountain)
    #  then wrong_way = Ture
    #    x,y-----------
    #    --------------
    #    ----------x2,y2
    wrong_way = False
    for col in range(min(pos_x, creature.x), max(pos_x, creature.x) + 1):
        for row in range(min(pos_y, creature.y), max(pos_y, creature.y) + 1):
            if my_map.mountains_cells[row, col] == 1:
                wrong_way = True
                break
        if wrong_way:
            break
    if wrong_way:
        print(f"{creature} move to boarder of mountain ({n_x},{n_y})")
        # move away from this mountain border point
        for [col, row] in [[n_x, n_y - 1], [n_x, n_y + 1], [n_x - 1, n_y], [n_x + 1, n_y]]:
            if my_map.mountains_cells[row, col] == 0:  # move to this way
                if col > n_x:
                    creature.x = n_x + creature.velocity
                    break
                if col < n_x:
                    creature.x = n_x - creature.velocity
                    break
                if row > n_y:
                    creature.y = n_y + creature.velocity
                    break
                if row < n_y:
                    creature.y = n_y - creature.velocity
                    break
        print(f"new position: {creature.x}, {creature.y}")


def step_check(pos_x, pos_y, creature, my_map):
    #
    map_border_check(creature, my_map.width, my_map.height, my_map.land_height)
    #
    mountains_border_check(pos_x, pos_y, creature, my_map)
