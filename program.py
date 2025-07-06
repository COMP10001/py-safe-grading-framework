def remove_player(grid, coord):
    row, col = coord 
    # Zero indexing
    row -= 1
    col -= 1
    current_value = grid[row][col]
    if current_value == '|x ':
        grid[row][col] = '|'
    elif current_value == ' x': 
        grid[row][col] = ' '
    return grid