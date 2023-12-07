# Terminal Manager ~ eylon

from .screen_vector import ScreenVector
import tty, sys, termios, os, atexit, select


class Terminal():
    '''
        Terminal is a static class that supply raw mode terminal services.
    '''
   
    input_buffer  = list()                            # initiate the input buffer with an empty list
    __cursor_pos  = ScreenVector()                    # keep track of the cursor's position, there is no other reliable way of doing it in raw mode
    __stdin_fd    = sys.stdin.fileno()                # stdin file descriptor
    __org_setting = None                              # the original terminal setting are beign switch back to at exit

    #-----<Initialization>-----#

    # Initiate the terminal
    @classmethod
    def init(cls) -> None:
        cls.__enable_raw_mode()                     # enable raw mode
        atexit.register(cls.__disable_raw_mode)     # disable raw mode at exit
        cls.set_cursor(ScreenVector(0, 0))          # initiate the cursor to 0, 0

    # Enable raw mode
    @classmethod
    def __enable_raw_mode(cls) -> None:
        cls.__org_setting = termios.tcgetattr(cls.__stdin_fd)   # save original settings
        tty.setraw(sys.stdin)                                   # enable raw mode

    # Disable raw mode :: private method is design to only be called at exit
    @classmethod
    def __disable_raw_mode(cls) -> None:
        termios.tcsetattr(cls.__stdin_fd, termios.TCSADRAIN, cls.__org_setting)


    #-----<Terminal Services>-----#

    # Clear the screen
    @staticmethod
    def clear() -> None:
        Terminal.print('\033[2J')

    # Write to the screen at the current cursor location
    @staticmethod
    def print(text: str) -> None:
        Terminal.write(text, Terminal.get_cursor())

    # Write to screen at a given location
    @staticmethod
    def write(text: str, position: ScreenVector) -> None:
        text = text.__str__()
        Terminal.set_cursor(position, len(text))   # update cursor's position
        sys.stdout.write(text)          # write [text] at the cursor's location
        sys.stdout.flush()              # flush the buffer to update the screen immediately

    # Check if there is input to read from the user :: blocking function takes a timeout parameter
    @staticmethod
    def can_read(timeout:   float) -> bool:
        return select.select([sys.stdin], [], [], timeout) == ([sys.stdin], [], [])
    
    # Read user input :: non blocking :: check for user input and put it in the terminal's buffer
    @classmethod
    def read(cls) -> None:
        # while there is user input in the buffer read it and add it to the terminal's buffer
        while Terminal.can_read(0):
            input: str = sys.stdin.read(1)          # read user input
            sys.stdin.flush()
            cls.input_buffer.append(input)          # add the input to the end of the buffer list


    #-----<Set & Get>-----#

    # Cursor position getter
    @classmethod
    def get_cursor(cls) -> ScreenVector:
        return cls.__cursor_pos
    
    # Cursor position setter :: [IMPORTANT] any change to the cursor's position must happen from this function only!
    @classmethod
    def set_cursor(cls, position: ScreenVector, offset: int = 0) -> None:
        position += ScreenVector(1, 0)                                  # the upper left corner is defined at (1, 0) but I want to refrence it as (0, 0), so I add 1 to the vector's x
        sys.stdout.write(f'\033[{position.row};{position.column}H\b')   # update the cursor position on screen
        sys.stdout.flush()                                              # flush the buffer to update the screen immediately
        cls.__cursor_pos = position #+ ScreenVector(offset, 0)           # save the cursor's position

    # Screen size getter
    @staticmethod
    def get_screen_size() -> ScreenVector:
        __size = os.get_terminal_size()
        return ScreenVector(__size.columns, __size.lines)