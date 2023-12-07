# Screen Vector ~ eylon

from __future__ import annotations

class ScreenVector():
    ''' 
        Screen Vector stores column (x) and row (y) values
        Both row and column must be above 0 
    '''

    def __init__(self, column: int = 0, row: int = 0) -> None:
        self.column = column
        self.row    = row

    #-----<Dunder Functions>-----#

    def __str__(self) -> str:
        return f'(c: {self.column}, r: {self.row})'

    def __eq__(self, value: ScreenVector) -> bool:
        return self.column == value.column and self.row == value.row

    def __add__(self, value: ScreenVector) -> ScreenVector:
        return ScreenVector(self.column + value.column, self.row + value.row)

    def __sub__(self, value: ScreenVector) -> ScreenVector:
        return ScreenVector(self.column - value.column, self.row - value.row)
    
    def __rsub__(self, value: ScreenVector) -> ScreenVector:
        return ScreenVector(value.column - self.column, value.row - self.row)
    
    def __neg__(self) -> ScreenVector:
        return self * -1
    
    def __mul__(self, value: ScreenVector) -> ScreenVector:
        if isinstance(value, ScreenVector):
            return ScreenVector(self.column * value.column, self.row * value.row)
        if isinstance(value, int | float):
            return ScreenVector(self.column * value, self.row * value)
        
    def __rmul__(self, value: ScreenVector) -> ScreenVector:
        return self.__mul__(value)


    #-----<Get & Set>-----#

    # Column getter
    @property
    def column(self) -> int:
        return self.__column
    
    # Column setter
    @column.setter
    def column(self, value: int) -> None:
        if value < 0:
            raise ValueError('Column in ScreenVector must be above or equal to 0')
        self.__column = value

    # Row getter
    @property
    def row(self) -> int:
        return self.__row
    
    # Row setter
    @row.setter
    def row(self, value: int) -> None:
        if value < 0:
            raise ValueError('Row in ScreenVector must be above or equal to 0')
        self.__row = value