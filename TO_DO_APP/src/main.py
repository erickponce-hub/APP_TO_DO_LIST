from dataclasses import field
from typing import Callable

import flet as ft


@ft.control
class Task(ft.Column):
    task_name: str = ""
    on_task_delete: Callable[["Task"], None] = field(default=lambda task: None)
    on_task_changed: Callable[[], None] = field(default=lambda: None)
   
    def init(self):
        # Paleta / estilo
        self.SURFACE = "#111B2E"
        self.SURFACE_2 = "#0F172A"
        self.BORDER = "#1F2A44"
        self.ACCENT = "#38BDF8"
        self.OK = "#22C55E"
        self.WARN = "#F59E0B"
        self.DANGER = "#EF4444"
        self.TEXT = "#E5E7EB"
        self.MUTED = "#94A3B8"
       
        self.display_task = ft.Checkbox(value=False, label=self.task_name, on_change=self.on_task_changed)
        self.display_task.label_style = ft.TextStyle(color=self.TEXT)
        self.edit_name = ft.TextField(
            expand=1,
            bgcolor=self.SURFACE_2,
            border_color=self.BORDER,
            focused_border_color=self.ACCENT,
            color=self.TEXT,
            cursor_color=self.ACCENT,
            hint_style=ft.TextStyle(color=self.MUTED),
        )
       
        # Chip estado
        self.state_chip = ft.Container(
            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            border_radius=999,
            bgcolor=self.WARN + "22",
            border=ft.border.all(1, self.WARN + "55"),
            content=ft.Row(
                spacing=6,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=16, color=self.WARN),
                    ft.Text("Pendiente", size=11, color=self.TEXT),
                ],
            ),
        )
       
        # Vista display (card)
        self.display_view = ft.Container(
            padding=ft.Padding.all(14),
            bgcolor=self.SURFACE,
            border_radius=18,
            border=ft.border.all(1, self.BORDER),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Container(
                                width=40,
                                height=40,
                                bgcolor=self.SURFACE_2,
                                border_radius=14,
                                border=ft.Border.all(1, self.BORDER),
                                alignment=ft.Alignment(0,0),
                                content=ft.Icon(ft.Icons.TASK_ALT_ROUNDED, color=self.ACCENT, size=22),
                            ),
                            ft.Column(
                                spacing=6,
                                controls=[
                                    self.display_task,
                                    self.state_chip,
                                ],
                            ),
                        ],
                    ),
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.CREATE_OUTLINED,
                                tooltip="Editar",
                                on_click=self.edit_clicked,
                                icon_color=self.ACCENT,
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE_OUTLINE,
                                tooltip="Eliminar",
                                on_click=self.delete_clicked,
                                icon_color=self.DANGER,
                            ),
                        ],
                    ),
                ],
            ),
        )
       
        # Vista edición (card)
        self.edit_view = ft.Container(
            visible=False,
            padding=ft.Padding.all(14),
            bgcolor=self.SURFACE,
            border_radius=18,
            border=ft.border.all(1, self.BORDER),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.edit_name,
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                                icon_color=self.OK,
                                tooltip="Guardar",
                                on_click=self.save_clicked,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE_ROUNDED,
                                icon_color=self.MUTED,
                                tooltip="Cancelar",
                                on_click=self.cancel_clicked,
                            ),
                        ],
                    ),
                ],
            ),
        )
       
        self.spacing = 10
        self.controls = [self.display_view, self.edit_view]
       
    # -------------- COMPORTAMIENTO IGUAL, SOLO CHIP VISUAL --------------
    def on_check_change(self, e):
        if self.display_task.value:
            self.state_chip.bgcolor = self.OK + "22"
            self.state_chip.border = ft.Border.all(1, self.OK + "55")
            self.state_chip.content.controls[0] = ft.Icon(ft.Icons.CHECK_ROUNDED, size=16, color=self.OK)
            self.state_chip.content.controls[1].value = "Hecha"
        else:
            self.state_chip.bgcolor = self.WARN + "22"
            self.state_chip.border = ft.Border.all(1, self.WARN + "55")
            self.state_chip.content.controls[0] = ft.Icon(ft.Icons.SCHEDULE_ROUNDED, size=16, color=self.WARN)
            self.state_chip.content.controls[1].value = "Pendiente"
           
        self.update()
        self.on_task_changed()
       
    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()
       
    def save_clicked(self, e):
        new_name = (self.edit_name.value or "").strip()
        if new_name:
            self.display_task.label = new_name
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
        self.on_task_changed()
       
    def cancel_clicked(self, e):
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
       
    def delete_clicked(self, e):
        self.on_task_delete(self)
        self.on_task_changed()
        
        
@ft.control
class TodoApp(ft.Column):
    def init(self):
        # Paleta
        self.BG = "#0B1220"
        self.SURFACE = "#111B2E"
        self.SURFACE_2 = "#0F172A"
        self.BORDER = "#1F2A44"
        self.ACCENT = "#38BDF8"
        self.TEXT = "#E5E7EB"
        self.MUTED = "#94A3B8"
        
        self.width = 620
        self.spacing = 12
        
        # Contador (NO llamamos update en init)
        self.counter = ft.Text("Total: 0", size=12, color=self.MUTED)
        
        self.new_task = ft.TextField(
            hint_text="What needs to be done?",
            expand=True,
            bgcolor=self.SURFACE_2,
            border_color=self.BORDER,
            focused_border_color=self.ACCENT,
            color=self.TEXT,
            cursor_color=self.ACCENT,
            hint_style=ft.TextStyle(color=self.MUTED),
        )
        
        self.tasks = ft.Column(spacing=10)
        
        example_task = Task(
            task_name="Ejemplo: Terminar la tarea de informática 🚀",
            on_task_delete=self.task_delete,
            on_task_changed=self.refresh_counter
        )

        self.tasks.controls.append(example_task)
        
        header = ft.Container(
            padding=ft.Padding.all(18),
            bgcolor=self.SURFACE,
            border_radius=18,
            border=ft.Border.all(1, self.BORDER),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        spacing=2,
                        controls=[
                            ft.Text("My Task Manager", size=20, weight=ft.FontWeight.BOLD, color=self.TEXT),
                            ft.Text("Organiza tus tareas fácilmente", size=12, color=self.MUTED),
                        ],
                    ),
                    ft.Container(
                        width=46,
                        height=46,
                        bgcolor=self.SURFACE_2,
                        border_radius=14,
                        border=ft.Border.all(1, self.BORDER),
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(ft.Icons.LIST_ALT_ROUNDED, color=self.ACCENT, size=24),
                    ),
                ],
            ),
        )
        
        form = ft.Container(
            padding=ft.Padding.all(16),
            bgcolor=self.SURFACE,
            border_radius=18,
            border=ft.Border.all(1, self.BORDER),
            content=ft.Column(
                spacing=12,
                controls=[
                    ft.Row(
                        spacing=12,
                        controls=[
                            self.new_task,
                            ft.FloatingActionButton(
                                icon=ft.Icons.ADD,
                                on_click=self.add_clicked,
                                bgcolor=self.ACCENT,
                                foreground_color="#06202B",
                            ),
                        ],
                    ),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            self.counter,
                            ft.Text("Tip: padding + spacing consistentes.", size=11, color=self.MUTED),
                        ],
                    ),
                ],
            ),
        )
        
        self.controls = [
            header,
            form,
            ft.Text("Tasks", size=14, weight=ft.FontWeight.BOLD, color=self.TEXT),
            self.tasks,
        ]
        
        # Solo ponemos el valor inicial SIN update ()
        self.counter.value = f"Total: {len(self.tasks.controls)}"
        
    # ✅ ahora sí: update solo cuando ya está en page
    def refresh_counter(self):
        self.counter.value = f"Total: {len(self.tasks.controls)}"
        if self.page: # ya está montado
            self.update()
            
    def add_clicked(self, e):
        name = (self.new_task.value or "").strip()
        if not name:
            if self.page:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Write a task first ✍️"))
                self.page.snack_bar.open = True
                self.page.update()
            return
        
        task = Task(task_name=name, on_task_delete=self.task_delete, on_task_changed=self.refresh_counter)
        self.tasks.controls.append(task)
        self.new_task.value = ""
        self.refresh_counter()
        
    def task_delete(self, task):
        if task in self.tasks.controls:
            self.tasks.controls.remove(task)
        self.refresh_counter()
        
        
def main(page: ft.Page):
    page.title = "To-Do App"
    page.bgcolor = "#0B1220"
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(color_scheme_seed="#22C55E")
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    
    page.add(TodoApp())
    
    
ft.run(main)
    