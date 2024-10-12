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
        self.password_input = ft.TextField(label="Senha", password=True, width=300, border_color=ft.colors.BLUE_400)
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
        


    def login_clicked(self, e):
        username = self.username_input.value
        password = self.password_input.value       

        if username == self.user and password == self.senha:
            dialog = ft.AlertDialog(title=ft.Text("Login bem-sucedido!"))
            dialog.open = True
            self.page.overlay.append(dialog)
            self.page.update()
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

    l = login.split(',')
    user = 'leo' 
    senha = l[1]

    def login_clicked(e):
        username = username_input.value
        password = password_input.value
       

        if username == self.user and password == self.senha:
            dialog = ft.AlertDialog(title=ft.Text("Login bem-sucedido!"))
        else:
            dialog = ft.AlertDialog(title=ft.Text("Credenciais inválidas!"))

        dialog.open = True
        page.overlay.append(dialog)
        page.update()

    username_input = ft.TextField(label="Usuário", width=300, border_color=ft.colors.ON_PRIMARY)
    password_input = ft.TextField(label="Senha", password=True, width=300, border_color=ft.colors.ON_PRIMARY)
    login_button = ft.ElevatedButton(text="Login", on_click=login_clicked)


    # Adicionando os widgets na página
    def Caixa(ct):
        return ft.Container(
            content = ct,
            shadow=ft.BoxShadow(
                blur_radius = 300,
                blur_style = ft.ShadowBlurStyle.OUTER,
                color = ft.colors.with_opacity(0.3,ft.colors.CYAN)
            ),
            border= ft.border.all(3, ft.colors.CYAN_500),
            border_radius=8,
            # alignment=ft.Alignment(0, 0),
            # expand= True,
            padding= 8,
            # width=600,
            # image_fit= ft.ImageFit.COVER,   
            # image= ft.DecorationImage(
            #     src =  "carregamento.png",  # URL da imagem de fundo
            #     fit = ft.ImageFit.COVER
            # )
        )     
    # page.add(
    #     Caixa(
    #     ft.Column(
    #         [
    #             ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD),
    #             username_input,
    #             password_input,
    #             login_button,
    #         ],
    #         alignment=ft.MainAxisAlignment.CENTER,
    #         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    #     )
    #     )
    # )

    page.add(Login())
if __name__ == '__main__': 
    ft.app(target=main)



