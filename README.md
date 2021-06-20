# Game of Life by astro_tech
*Conway's Game of Life with tkinter*

During development a new branch was created with a name: modify_grid_optimize which included a new method for
incrementing the number of columns. This method changed the canvas size and only created the additional squares
instead of completely redrawing the canvas. Despite this effort the performance dropped. The rendering time
increased +13-18%.