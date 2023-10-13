from views import WIDTH, HEIGHT, SCREEN, BG
from views.main_menu import MainMenu

if __name__ == '__main__':
    m = MainMenu(width=WIDTH, height=HEIGHT, bg=BG, screen=SCREEN)
    m.display()
