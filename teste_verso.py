
import flet as ft


class ClassName(ft.Column):
    def __init__(self):
        super().__init__()
        self.controls = [ft.Text('Meu ovo')]


def main(page: ft.Page):
    # Definindo o t�tulo da p�gina
    page.title = 'Título'
    page.window.width = 500  # Define a largura da janela como 800 pixels
    page.window.height = 385  # 
    page.theme_mode = ft.ThemeMode.DARK
 
    p = ClassName()
    page.add(p)

if __name__ == '__main__': 
    ft.app(target=main)
