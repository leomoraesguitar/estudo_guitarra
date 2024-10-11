import flet as ft

def main(page: ft.Page):
    page.title = "Tela de Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    def login_clicked(e):
        username = username_input.value
        password = password_input.value

        if username == "admin" and password == "admin":
            page.dialog = ft.AlertDialog(title=ft.Text("Login bem-sucedido!"))
        else:
            page.dialog = ft.AlertDialog(title=ft.Text("Credenciais inválidas!"))

        page.dialog.open = True
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
    page.add(
        Caixa(
        ft.Column(
            [
                ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD),
                username_input,
                password_input,
                login_button,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        )
    )

ft.app(target=main)
