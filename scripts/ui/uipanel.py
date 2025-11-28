from arcade.types import Color
from arcade import Texture
from arcade.gui import NinePatchTexture
from typing import Self, Union, Optional
import arcade.gui as gui
import arcade

class UIPanel:
    def __init__(
        self,
        *,
        x: float = 0,
        y: float = 0,
        width: float = 100,
        height: float = 100,
    ):
        self.root = gui.UIAnchorLayout(x=x, y=y, width=width, height=height)

    @property
    def visible(self) -> bool:
        return self.root.visible

    @visible.setter
    def visible(self, value: bool):
        self.root.visible = value

    def with_padding(
        self,
        *,
        top: Optional[int] = None,
        right: Optional[int] = None,
        bottom: Optional[int] = None,
        left: Optional[int] = None,
        all: Optional[int] = None,
    ) -> Self:
        """Changes the padding to the given values if set. Returns itself

        Returns:
            self
        """
        self.root.with_padding(top=top, right=right, bottom=bottom, left=left, all=all)
        return self
    
    def with_border(self, *, width=2, color: Color | None = arcade.color.GRAY) -> Self:
        """Sets border properties

        Args:
            width: border width
            color: border color

        Returns:
            self
        """
        self.root.with_border(width=width, color=color)
        return self
        
    def with_background(
        self,
        *,
        color: Union[None, Color] = ...,    # type: ignore
        texture: Union[None, Texture, NinePatchTexture] = ...,   # type: ignore
    ) -> Self:
        """Set widgets background.

        A color or texture can be used for background,
        if a texture is given, start and end point can be added to use the texture as ninepatch.

        Args:
            color: A color used as background
            texture: A texture or ninepatch texture used as background

        Returns:
            self
        """
        self.root.with_background(color=color, texture=texture)
        return self
    
