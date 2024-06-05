import pygame
from typing import Tuple


class ProgresBar:
    def __init__(
        self,
        pos: Tuple[int, int],
        size: Tuple[int, int],
        total: int = 0
    ) -> None:
        self.rect = pygame.Rect(pos, size)
        self.progress = 0
        self.total = total
        self.stage = ""
        self.font = pygame.font.SysFont("Arial", round(size[1] * 0.5))

    def update(self, progress: int, total: int, stage: str = "") -> None:
        self.progress = progress
        self.total = total
        self.stage = stage

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (50, 50, 50), self.rect)
        width = (self.rect.width - 2) * self.progress / self.total
        progress_rect = pygame.Rect(
            self.rect.left + 1,
            self.rect.top + 1,
            width,
            self.rect.height - 2,
        )
        pygame.draw.rect(surface, (96, 219, 55), progress_rect)
        stage_img = self.font.render(self.stage, True, (255, 255, 255))
        surface.blit(
            stage_img, (self.rect.left, self.rect.top - stage_img.get_height())
        )
        pp = round(self.progress / self.total * 100, 2)
        progress_img = self.font.render(str(pp) + "%", True, (255, 255, 255))
        surface.blit(progress_img, (
            self.rect.left + self.rect.width/2 - progress_img.get_width() / 2,
            self.rect.top + self.rect.height/2 - progress_img.get_height() / 2,
        ))
