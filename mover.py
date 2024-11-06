import flet as ft



class Gestos(ft.Stack):
    def __init__(self, page,control):
        super().__init__()
        self.page = page
        self.expand=True
        self.controls = []
        self.controls.append(
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                on_pan_update=self.on_pan_update, 
                on_pan_start= self.on_pan_start,
                on_pan_end= self.on_pan_end,                               
                left=0,
                top=0,               
                content= control ,
            )
        )

    def Add_control(self, control ):
        self.controls.append(
            ft.GestureDetector(
                mouse_cursor=ft.MouseCursor.MOVE,
                # on_vertical_drag_update=self.on_pan_update,  
                on_pan_start= self.on_pan_start,
                on_pan_end= self.on_pan_end,

                left=0,
                top=0,               
                content= control ,
            )
        )
      

    def on_pan_update(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        e.control.left = max(0, e.control.left + e.delta_x)
        self.x = e.control.left
        self.y = e.control.top
        # self.page.window.top = max(0, e.control.top + e.global_y)
        # self.page.window.left = max(0, e.control.left + e.global_x)        
        e.page.update()

    def on_pan_start(self, e):
        # e.page.window.width = 2500
        # e.page.window.height = 1400
        self.page.window.full_screen = True

        e.page.update()
        
    def on_pan_end(self, e):
        e.page.window.full_screen = False
        e.page.update()

        # e.page.window.width = 500
        # e.page.window.width = 500
        self.SetPosition()
                
    def SetPosition(self):
        print('aqui')
        self.page.window.width = 2500
        self.page.window.height = 1400
        self.page.window.top = 400
        self.page.window.left = 2000
        self.page.update()




def main(page: ft.Page):
    page.window.frameless = True
    page.padding = 0   
    page.window.width = 25 
    page.window.height = 50 
    page.bgcolor = ft.colors.TRANSPARENT
    page.window.bgcolor = ft.colors.TRANSPARENT  
    page.window.title_bar_hidden = True  
    page.window.title_bar_buttons_hidden = True  

    page.add(
        ft.WindowDragArea(
            content=ft.Container(
                on_click = lambda x: print(f'{page.window.left+78}x{page.window.top+25}'),
                
                bgcolor=ft.colors.AMBER, 
                padding=0,
            ), 
            expand=True,
            # width = 25,
            # height=25, 
            maximizable = False,

        ),
    )

ft.app(main)