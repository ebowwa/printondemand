
class ThemeNotFoundException(Exception):
    """Exception raised when a theme is not found."""
    pass

class ChapterNotFoundException(Exception):
    """Exception raised when a chapter is not found."""
    pass

class DuplicateThemeException(Exception):
    """Exception raised when attempting to create a duplicate theme."""
    pass

class DuplicateChapterException(Exception):
    """Exception raised when attempting to create a duplicate chapter."""
    pass
