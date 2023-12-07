# Shell Typer Main ~ eylon

from term_io import Terminal, ScreenVector

def main():
    Terminal.init()         # initiate the terminal
    Terminal.print(Terminal.get_screen_size())
    return 0

if (__name__ == '__main__'):
    main()