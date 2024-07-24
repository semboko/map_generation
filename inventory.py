import pygame
from typing import List, Sequence, Optional
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
import os


class InventoryType:
    name: str


class ClothesHead(InventoryType):
    name = "HEAD"


class ClothesTorso(InventoryType):
    name = "TORSO"


class ClothesBelt(InventoryType):
    name = "BELT"


class ClothesLegs(InventoryType):
    name = "LEGS"


class ClothesFeet(InventoryType):
    name = "FEET"


class ClothesHands(InventoryType):
    name = "HANDS"


inventory_types = (
    ClothesBelt,
    ClothesHead,
    ClothesTorso,
    ClothesBelt,
    ClothesLegs,
    ClothesFeet,
    ClothesHands,
)


def inventory_type_factory(name: str) -> InventoryType | None:
    for t in inventory_types:
        if name == t.name:
            return t


def empty_slot() -> pygame.Surface:
    item_surface = pygame.Surface((64, 64))
    item_surface.fill((200, 200, 200))
    pygame.draw.rect(item_surface, (190, 190, 190), (4, 4, 56, 56), 0, 6)
    pygame.draw.rect(item_surface, (170, 170, 170), (4, 4, 56, 56), 2, 6)
    return item_surface


class InventoryItem:
    def __init__(self, filename: str, inv_type: InventoryType) -> None:
        self.img = pygame.image.load(filename)
        self.icon = self.img.subsurface((0, 0, 64, 64))
        self.inv_type = inv_type

    def display_icon(self, surface: pygame.Surface, coords: Sequence[float]) -> None:
        surface.blit(self.img, coords)


walkcycle: list[InventoryItem] = []
folder = "./assets/character/walkcycle"
for file in os.listdir(folder):
    type_name = file.split("_")[0]
    inventory_type = inventory_type_factory(type_name)
    if inventory_type is None:
        continue
    walkcycle.append(InventoryItem(folder + "/" + file, inventory_type))


class InventorySlot:
    def __init__(self, slot_type: Optional[InventoryType] = None) -> None:
        self.item: Optional[InventoryItem] = None
        self.count = 0
        self.slot_type: None | InventoryType = slot_type


SlotsType = List[List[InventorySlot]]


class PlayerInventory:
    def __init__(self) -> None:
        self.common_slots: SlotsType = [[InventorySlot() for _ in range(6)] for _ in range(6)]
        self.tools: SlotsType = [[InventorySlot() for _ in range(6)]]
        self.clothes: SlotsType = [[
            InventorySlot(ClothesHead),
            InventorySlot(ClothesTorso),
            InventorySlot(ClothesHands),
            InventorySlot(ClothesBelt),
            InventorySlot(ClothesLegs),
            InventorySlot(ClothesFeet),
        ]]
        self.shown = False

        self.moving_item: Optional[tuple[int, int, int]] = None
        self.mouse_position = None

        self.all_slots: List[SlotsType] = [self.common_slots, self.tools, self.clothes]
        self.slot_rects = [
            pygame.Rect(200, 200, 0, 0),
            pygame.Rect(200, 120, 200, 200),
            pygame.Rect(200, 600, 200, 200),
        ]

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for idx, group in enumerate(self.all_slots):
                rect = self.slot_rects[idx]
                if rect.collidepoint(event.pos):
                    i = (event.pos[1] - rect.top) // 64
                    j = (event.pos[0] - rect.left) // 64
                    if group[i][j] is not None:
                        self.moving_item = idx, i, j

        if event.type == pygame.MOUSEBUTTONUP:
            if self.moving_item is not None and self.mouse_position is not None:
                self.apply_move(event.pos)
            self.mouse_position = None
            self.moving_item = None

        if event.type == pygame.MOUSEMOTION and self.moving_item is not None:
            self.mouse_position = event.pos

    def swap_items(self, source_slot: InventorySlot, dest_slot: InventorySlot):
        if dest_slot.slot_type is None:
            source_slot.item, dest_slot.item = dest_slot.item, source_slot.item
        if source_slot.item is None:
            return
        if dest_slot.slot_type == source_slot.item.inv_type:
            source_slot.item, dest_slot.item = dest_slot.item, source_slot.item

    def apply_move(self, mouse_pos: tuple[int, int]):
        idx, mi, mj = self.moving_item
        source_group = self.all_slots[idx]
        for idx, dest_group in enumerate(self.all_slots):
            rect = self.slot_rects[idx]
            if rect.collidepoint(mouse_pos):
                i = (mouse_pos[1] - rect.top) // 64
                j = (mouse_pos[0] - rect.left) // 64
                self.swap_items(source_group[mi][mj], dest_group[i][j])

    def render_slots(self, slots: SlotsType) -> pygame.Surface:
        surface_width = len(slots[0]) * 64
        surface_height = len(slots) * 64
        result = pygame.Surface((surface_width, surface_height))
        for i in range(len(slots)):
            for j in range(len(slots[i])):
                slot = slots[i][j]
                item = slot.item
                item_surface = empty_slot()
                if slot.slot_type is not None:
                    slot_txt = slot.slot_type.name.capitalize()
                    # H/W render and blit this text on the item_surface
                if item is not None:
                    item.display_icon(item_surface, (0, 0))
                result.blit(item_surface, (j * 64, i * 64))
        return result

    def display(self, surface: pygame.Surface) -> None:
        if not self.shown:
            return

        bg_surface = pygame.Surface(
            (WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA, 32
        )
        bg_surface.convert_alpha()
        bg_surface.fill((0, 0, 0, 200))

        for idx, slots_group in enumerate(self.all_slots):
            slots_group_img = self.render_slots(slots_group)
            slots_group_rect = self.slot_rects[idx]
            slots_group_rect.width = slots_group_img.get_width()
            slots_group_rect.height = slots_group_img.get_height()
            bg_surface.blit(slots_group_img, slots_group_rect)

        if self.moving_item is not None and self.mouse_position is not None:
            icon_surface = pygame.Surface((64, 64))
            idx, mi, mj = self.moving_item
            group = self.all_slots[idx]
            moving_item = group[mi][mj].item
            moving_item.display_icon(icon_surface, (0, 0))
            icon_surface.set_colorkey((0, 0, 0))
            bg_surface.blit(icon_surface, pygame.Vector2(self.mouse_position) - pygame.Vector2(32, 32))

        surface.blit(bg_surface, (0, 0))
