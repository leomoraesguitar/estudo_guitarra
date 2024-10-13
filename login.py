import flet as ft
from dotenv import load_dotenv
import os
from time import sleep
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

login = os.getenv("ADM_ESTUDO_GUITARRA")



class Login(ft.Container):
    def __init__(self, func = None):
        super().__init__()
        self.func = func
        self.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK)
        self.shadow=ft.BoxShadow(
                blur_radius = 300,
                blur_style = ft.ShadowBlurStyle.OUTER,
                color = ft.colors.with_opacity(0.3,ft.colors.CYAN)
        )
        self.border= ft.border.all(3, ft.colors.CYAN_500)
        self.border_radius=8
        self.padding= 8
        self.width = 250
        self.height = 240




        l = login.split(',')
        self.user = 'leo' 
        self.senha = l[1]


        self.username_input = ft.TextField(label="Usuário",  border_color=ft.colors.BLUE_400)
        self.password_input = ft.TextField(label="Senha", password=True, border_color=ft.colors.BLUE_400, on_submit=self.login_clicked)
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login_clicked)
        valor = False

        self.salvar_login = ft.Checkbox(
            scale=0.8,
            label="Salvar",
            label_style = ft.TextStyle(
                color=ft.colors.PRIMARY
            ),
            value = False, 
            on_change=self.Chenge_valor_salvar_login,
        )

        self.telalogin = ft.Column(
                [
                            ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
                            self.username_input,
                            self.password_input,
                            ft.Row([self.login_button,self.salvar_login], alignment='center'),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                tight=True,
                )
        
        self.content =  self.telalogin 
        

    def did_mount(self):
        try:
            l = False
            l = self.page.client_storage.get("login")
            v = self.page.client_storage.get("salvar_login")
            if l and v:
                self.salvar_login.value = v
                self.salvar_login.update()
                if self.func:   
                    sleep(2)                 
                    if v:
                        self.func(2)
        except:
            pass
                   
    def valor_salvar_login(self):
        try:
            v = self.page.client_storage.get("salvar_login")
            print('valor', v)
            if not v is None:
                return v
        except:
            return False
        
    async def Chenge_valor_salvar_login(self, e):
        await self.page.client_storage.set_async("salvar_login", self.salvar_login.value)
                        
        

    async def login_clicked(self, e):
        username = self.username_input.value 
        password = self.password_input.value       

        if username == self.user and password == self.senha:
            dialog = ft.AlertDialog(title=ft.Text("Login bem-sucedido!"))
            # dialog.open = True
            # self.page.overlay.append(dialog)
            # self.page.update()
            await self.page.client_storage.set_async("login", True)
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



