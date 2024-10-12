import flet as ft
from dotenv import load_dotenv
import os
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

login = os.getenv("ADM_ESTUDO_GUITARRA")



class Login(ft.Container):
    def __init__(self, func = None):
        super().__init__()
        self.func = func
        self.shadow=ft.BoxShadow(
                blur_radius = 300,
                blur_style = ft.ShadowBlurStyle.OUTER,
                color = ft.colors.with_opacity(0.3,ft.colors.CYAN)
        )
        self.border= ft.border.all(3, ft.colors.CYAN_500)
        self.border_radius=8
        self.padding= 8



        l = login.split(',')
        self.user = 'leo' 
        self.senha = l[1]


        self.username_input = ft.TextField(label="Usuário", width=300, border_color=ft.colors.BLUE_400)
        self.password_input = ft.TextField(label="Senha", password=True, width=300, border_color=ft.colors.BLUE_400, on_submit=self.login_clicked)
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login_clicked)
        
        self.content =  ft.Column(
            [
                ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD),
                self.username_input,
                self.password_input,
                self.login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        )
        
    # def did_mount(self):
    #     ConfirmarSaidaeResize(self.page,exibir=False,  width_max=723,height_max=656)

    def login_clicked(self, e):
        username = self.username_input.value 
        password = self.password_input.value       

        if username == self.user and password == self.senha:
            dialog = ft.AlertDialog(title=ft.Text("Login bem-sucedido!"))
            # dialog.open = True
            # self.page.overlay.append(dialog)
            # self.page.update()
            if self.func:
                self.func(e)
        else:
            dialog = ft.AlertDialog(title=ft.Text("Credenciais inválidas!"))

            dialog.open = True
            self.page.overlay.append(dialog)
            self.page.update()

def main(page: ft.Page):
    page.title = "Tela de Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.add(Login())
if __name__ == '__main__': 
    ft.app(target=main)



