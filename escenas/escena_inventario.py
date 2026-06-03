from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from escenas.escena_base import EscenaBase
from core.fuente import Fuente

if TYPE_CHECKING:
    from core.juego import Juego


class EscenaInventario(EscenaBase):
    def __init__(self, juego: Juego) -> None:
        super().__init__(juego)
        self.fuente_titulo = Fuente.obtener(24)
        self.fuente_seccion = Fuente.obtener(20)
        self.fuente_item = Fuente.obtener(18)
        self.fuente_detalle = Fuente.obtener(16)
        self.fuente_pista = Fuente.obtener(14)

        # Sections: we'll define the sections we want to show
        self.sections = ["Laptops", "Componentes"]  # Can add more like "Herramientas", "NS-E", etc.
        self.section_seleccionado = 0  # Index of selected section

        # For item selection within the current section
        self.item_seleccionado = 0
        self.scroll_offset = 0  # For scrolling the item list if needed
        self.visible_items = 12  # Number of items visible in the list

    def _get_items_for_section(self, section_name: str) -> list:
        """Return the list of items for the given section name."""
        inventario = self.juego.jugador.inventario
        if section_name == "Laptops":
            return inventario.laptops
        elif section_name == "Componentes":
            return inventario.componentes
        # Add more sections as needed
        return []

    def _get_item_name(self, item) -> str:
        """Get a display name for an item."""
        if hasattr(item, 'modelo'):
            return item.modelo
        elif hasattr(item, 'nombre'):
            return item.nombre
        elif isinstance(item, dict) and 'nombre' in item:
            return item['nombre']
        else:
            return str(item)

    def _get_item_description(self, item) -> str:
        """Get a detailed description for an item."""
        desc_parts = []
        if hasattr(item, 'modelo'):
            desc_parts.append(f"Modelo: {item.modelo}")
        if hasattr(item, 'marca'):
            desc_parts.append(f"Marca: {item.marca}")
        if hasattr(item, 'tipo'):
            desc_parts.append(f"Tipo: {item.tipo}")
        # For laptops, we might have more specs
        if hasattr(item, 'procesador'):
            desc_parts.append(f"Procesador: {item.procesador}")
        if hasattr(item, 'ram'):
            desc_parts.append(f"RAM: {item.ram}")
        if hasattr(item, 'almacenamiento'):
            desc_parts.append(f"Almacenamiento: {item.almacenamiento}")
        if hasattr(item, 'grafica'):
            desc_parts.append(f"Gráfica: {item.grafica}")

        # For components, we might have different attributes
        if hasattr(item, 'capacidad'):
            desc_parts.append(f"Capacidad: {item.capacidad}")
        if hasattr(item, 'velocidad'):
            desc_parts.append(f"Velocidad: {item.velocidad}")
        if hasattr(item, 'tipo_componente'):
            desc_parts.append(f"Tipo de componente: {item.tipo_componente}")

        # If we don't have any specific attributes, fall back to string representation
        if not desc_parts:
            desc_parts.append(str(item))

        return " | ".join(desc_parts)

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    from escenas.escena_juego import EscenaJuego
                    self.juego.manejador_escenas.cambiar_escena(EscenaJuego(self.juego))
                elif evento.key == pygame.K_LEFT:
                    # Previous section
                    self.section_seleccionado = (self.section_seleccionado - 1) % len(self.sections)
                    self.item_seleccionado = 0  # Reset item selection when changing section
                    self.scroll_offset = 0
                elif evento.key == pygame.K_RIGHT:
                    # Next section
                    self.section_seleccionado = (self.section_seleccionado + 1) % len(self.sections)
                    self.item_seleccionado = 0
                    self.scroll_offset = 0
                elif evento.key == pygame.K_UP:
                    # Previous item in current section
                    items = self._get_items_for_section(self.sections[self.section_seleccionado])
                    if items:
                        self.item_seleccionado = (self.item_seleccionado - 1) % len(items)
                        # Adjust scroll if needed
                        if self.item_seleccionado < self.scroll_offset:
                            self.scroll_offset = self.item_seleccionado
                elif evento.key == pygame.K_DOWN:
                    # Next item in current section
                    items = self._get_items_for_section(self.sections[self.section_seleccionado])
                    if items:
                        self.item_seleccionado = (self.item_seleccionado + 1) % len(items)
                        # Adjust scroll if needed
                        if self.item_seleccionado >= self.scroll_offset + self.visible_items:
                            self.scroll_offset = self.item_seleccionado - self.visible_items + 1
                elif evento.key == pygame.K_a:
                    # Use/select item (placeholder for future implementation)
                    pass

    def actualizar(self, dt: float):
        pass

    def dibujar(self, pantalla: pygame.Surface):
        pantalla.fill((30, 30, 40))  # dark background

        # Calculate layout - more authentic Pokemon style
        screen_width, screen_height = pantalla.get_size()

        # Left panel: sections (25% width)
        section_width = int(screen_width * 0.25)
        # Right panel: item list (75% width)
        item_panel_width = screen_width - section_width

        # Split right panel: item list (70% height), description area (30% height)
        item_list_height = int(screen_height * 0.7)
        desc_height = screen_height - item_list_height

        section_x = 0
        item_panel_x = section_width
        desc_y = item_list_height

        # Draw sections (vertical tabs on the left)
        self._dibujar_secciones(pantalla, section_x, 0, section_width, item_list_height)

        # Draw item list for selected section (top-right)
        self._dibujar_lista_items(pantalla, item_panel_x, 0, item_panel_width, item_list_height)

        # Draw description area (bottom)
        self._dibujar_descripcion(pantalla, 0, desc_y, screen_width, desc_height)

    def _dibujar_secciones(self, pantalla: pygame.Surface, x: int, y: int, width: int, height: int):
        """Draw the section tabs on the left side."""
        # Background for sections
        s = pygame.Surface((width, height))
        s.fill((40, 40, 50))
        pantalla.blit(s, (x, y))

        # Draw each section name
        item_height = 32  # Slightly smaller for more sections
        for i, section_name in enumerate(self.sections):
            item_y = y + i * item_height
            # Highlight selected section
            if i == self.section_seleccionado:
                highlight_s = pygame.Surface((width, item_height))
                highlight_s.fill((70, 130, 180))  # Blue highlight like Pokemon
                pantalla.blit(highlight_s, (x, item_y))
                text_color = (255, 255, 255)
            else:
                text_color = (200, 200, 200)

            # Draw section name
            text_surf = self.fuente_seccion.render(section_name, False, text_color)
            text_rect = text_surf.get_rect(midleft=(x + 10, item_y + item_height // 2))
            pantalla.blit(text_surf, text_rect)

            # Draw separator line (except for last item)
            if i < len(self.sections) - 1:
                pygame.draw.line(pantalla, (60, 60, 70),
                               (x, item_y + item_height),
                               (x + width, item_y + item_height), 1)

    def _dibujar_lista_items(self, pantalla: pygame.Surface, x: int, y: int, width: int, height: int):
        """Draw the list of items for the selected section."""
        # Background for item list
        s = pygame.Surface((width, height))
        s.fill((40, 40, 50))
        pantalla.blit(s, (x, y))

        # Get items for current section
        section_name = self.sections[self.section_seleccionado]
        items = self._get_items_for_section(section_name)

        if not items:
            # Show empty message centered
            empty_surf = self.fuente_item.render(f"No hay {section_name.lower()} en el inventario", False, (180, 180, 180))
            empty_rect = empty_surf.get_rect(center=(x + width // 2, y + height // 2))
            pantalla.blit(empty_surf, empty_rect)
            return

        # Draw each visible item
        item_height = 24
        start_idx = self.scroll_offset
        end_idx = min(start_idx + self.visible_items, len(items))

        for i in range(start_idx, end_idx):
            item = items[i]
            item_y = y + (i - start_idx) * item_height

            # Highlight selected item
            if i == self.item_seleccionado:
                # Draw selection highlight (like Pokemon cursor)
                highlight_s = pygame.Surface((width, item_height))
                highlight_s.fill((70, 130, 180))  # Blue highlight
                pantalla.blit(highlight_s, (x, item_y))
                name_color = (255, 255, 255)
                # Draw a small triangle cursor like in Pokemon
                cursor_points = [
                    (x + 4, item_y + item_height // 2),
                    (x + 8, item_y + item_height // 2 - 3),
                    (x + 8, item_y + item_height // 2 + 3)
                ]
                pygame.draw.polygon(pantalla, (255, 255, 255), cursor_points)
                text_x_offset = 16  # Offset text to make room for cursor
            else:
                name_color = (200, 200, 200)
                text_x_offset = 0

            # Draw item image placeholder (left)
            image_size = 20
            image_x = x + 4 + text_x_offset
            image_y = item_y + (item_height - image_size) // 2
            # Draw a placeholder rectangle for the image
            pygame.draw.rect(pantalla, (60, 60, 80), (image_x, image_y, image_size, image_size))
            pygame.draw.rect(pantalla, (100, 100, 120), (image_x, image_y, image_size, image_size), 1)

            # Draw item name
            item_name = self._get_item_name(item)
            name_x = image_x + image_size + 4
            name_surf = self.fuente_item.render(item_name, False, name_color)
            pantalla.blit(name_surf, (name_x, item_y + (item_height - name_surf.get_height()) // 2))

        # Draw scroll indicators if needed
        if len(items) > self.visible_items:
            # Up arrow (top right)
            if self.scroll_offset > 0:
                pygame.draw.polygon(pantalla, (100, 100, 120),
                                  [(x + width - 12, y + 6),
                                   (x + width - 4, y + 14),
                                   (x + width - 20, y + 14)])
            # Down arrow (bottom right)
            if self.scroll_offset + self.visible_items < len(items):
                pygame.draw.polygon(pantalla, (100, 100, 120),
                                  [(x + width - 20, y + height - 14),
                                   (x + width - 4, y + height - 6),
                                   (x + width - 12, y + height - 14)])

    def _dibujar_descripcion(self, pantalla: pygame.Surface, x: int, y: int, width: int, height: int):
        """Draw the item description area at the bottom."""
        # Background for description
        s = pygame.Surface((width, height))
        s.fill((40, 40, 50))
        pantalla.blit(s, (x, y))

        # Get items for current section
        section_name = self.sections[self.section_seleccionado]
        items = self._get_items_for_section(section_name)

        # Draw description (with padding)
        desc_x = x + 10
        desc_y = y + 10
        max_width = width - 20

        if items and 0 <= self.item_seleccionado < len(items):
            selected_item = items[self.item_seleccionado]
            description = self._get_item_description(selected_item)

            # Word wrap description
            words = description.split(' ')
            lines = []
            current_line = []
            space_width = self.fuente_detalle.render(" ", False, (255, 255, 255)).get_width()

            for word in words:
                word_surf = self.fuente_detalle.render(word, False, (255, 255, 255))
                word_width = word_surf.get_width()
                current_line_width = sum(self.fuente_detalle.render(w, False, (255, 255, 255)).get_width() for w in current_line) + (len(current_line) * space_width if current_line else 0)

                if current_line_width + word_width <= max_width:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            if current_line:
                lines.append(' '.join(current_line))

            # Draw lines
            line_height = self.fuente_detalle.get_height() + 2
            for i, line in enumerate(lines[:4]):  # Show up to 4 lines
                line_surf = self.fuente_detalle.render(line, False, (255, 255, 255))
                pantalla.blit(line_surf, (desc_x, desc_y + i * line_height))

            # If there are more lines, show an indicator
            if len(lines) > 4:
                more_surf = self.fuente_detalle.render("...", False, (180, 180, 180))
                pantalla.blit(more_surf, (desc_x, desc_y + 4 * line_height))
        else:
            # Show hint when no item selected
            hint_surf = self.fuente_detalle.render("Seleccione un ítem para ver los detalles", False, (180, 180, 180))
            pantalla.blit(hint_surf, (desc_x, desc_y))