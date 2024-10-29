import flet as ft
from dotenv import load_dotenv
import os
from time import sleep
import json
from flet.auth.providers import GoogleOAuthProvider, GitHubOAuthProvider
import random
import string
# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

login = os.getenv("ADM_ESTUDO_GUITARRA")



# class Login(ft.Container):
#     def __init__(self, func = None, tipo = 'login'):
#         super().__init__()
#         self.func = func
#         self._tipo = tipo
#         self.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK)
#         self.shadow=ft.BoxShadow(
#                 blur_radius = 300,
#                 blur_style = ft.ShadowBlurStyle.OUTER,
#                 color = ft.colors.with_opacity(0.3,ft.colors.CYAN)
#         )
#         self.border= ft.border.all(3, ft.colors.CYAN_500)
#         self.border_radius=12
#         self.padding= 8
#         self.width = 250
#         self.height = 260

#         # with open('assets\senhas.txt', 'r') as arq:
#         #    self.senhas = arq.read() 
#         # self.senhas = login.split('\n')
#         self.senhas = self.ler_json2(r'assets\senhas.json')
#         # print(self.senhas)


#         self.username_input = ft.TextField(
#             hint_text="Usuário",  
#             border_color=ft.colors.BLUE_400,
#             border_radius=15,
#             dense = True,
            
#             helper_style=ft.TextStyle(
#                 color = '#77bf70'
#             ),
#             prefix_icon=ft.icons.PERSON,
#             keyboard_type=ft.KeyboardType.NAME,
   

#             prefix_style=ft.TextStyle(
#                 color = 'primary,0.7'
#             )
#         )
#         self.password_input = ft.TextField(
#             hint_text="Senha", 
#             password=True, 
#             dense = True,
#             border_color=ft.colors.BLUE_400, 
#             border_radius=15,
#             prefix_icon=ft.icons.LOCK,
#             keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,   
#             can_reveal_password=True,         
#             on_submit=self.login_clicked,
#         )
#         self.login_button = ft.ElevatedButton(text="Login", on_click=self.login_clicked)
#         self.cadastro_button = ft.ElevatedButton(text="Cadastrar", on_click=self.Cadastrar)
#         valor = False

#         self.salvar_login = ft.Checkbox(
#             scale=0.8,
#             label="Salvar",
#             label_style = ft.TextStyle(
#                 color=ft.colors.PRIMARY
#             ),
#             value = False, 
#             on_change=self.Chenge_valor_salvar_login,
#         )

#         self.telalogin = ft.Column(
#                 [
#                             ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
#                             self.username_input,
#                             self.password_input,
#                             ft.Row([self.login_button,self.salvar_login], alignment='center'),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                 tight=True,
#                 )
        

#         self.telacadastro = ft.Column(
#                 [
#                             ft.Text("Crie um Usuário e senha", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
#                             self.username_input,
#                             self.password_input,
#                             ft.Row([self.cadastro_button], alignment='center'),
#                 ],
#                 alignment=ft.MainAxisAlignment.CENTER,
#                 horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#                 tight=True,
#                 )
        
#         self.tela = ft.Column(
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#             tight=True,
#             )

#         if self._tipo == 'login':
#             self.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK)
#             self.tela.controls =  [
#                 ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
#                 self.username_input,
#                 self.password_input,
#                 ft.Row([self.login_button,self.salvar_login], alignment='center'),
#             ]
     
#         elif self._tipo == 'cadastro':
#             self.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLUE)
#             self.tela.controls =  [
#                 ft.Text("Crie um Usuário e senha", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
#                 self.username_input,
#                 self.password_input,
#                 ft.Row([self.cadastro_button], alignment='center'),
#             ] 
        
#         self.content =  self.tela

#     def did_mount(self):
#         try:
#             l = False
#             l = self.page.client_storage.get("login")
#             v = self.page.client_storage.get("salvar_login")
#             if l and v:
#                 self.salvar_login.value = v
#                 self.salvar_login.update()
#                 if self.func:   
#                     # sleep(2)                 
#                     if v:
#                         self.func(2)
#         except:
#             pass



#     def valor_salvar_login(self):
#         try:
#             v = self.page.client_storage.get("salvar_login")
#             print('valor', v)
#             if not v is None:
#                 return v
#         except:
#             return False
        
#     async def Chenge_valor_salvar_login(self, e):
#         await self.page.client_storage.set_async("salvar_login", self.salvar_login.value)
                              
#     async def login_clicked(self, e):
#         username = self.username_input.value 
#         password = self.password_input.value       
#         # print(f'{username},{password}')
#         # print(self.senhas)
#         if f'{username},{password}' in self.senhas:
#             dialog = ft.AlertDialog(title=ft.Text("Login bem-sucedido!"))
#             await self.page.client_storage.set_async("login", True)
#             e.data = 'logado'
#             if self.func:
#                 self.func(e)
#         else:
#             dialog = ft.AlertDialog(title=ft.Text("Credenciais inválidas!"))

#             dialog.open = True
#             self.page.overlay.append(dialog)
#             self.page.update()

#     def Cadastrar(self, e):
#         username = self.username_input.value 
#         password = self.password_input.value       
#         usuarios = list(self.senhas.keys())
#         # print(usuarios)
#         if not username in usuarios:
#             self.senhas[username] = password
#             self.escrever_json(self.senhas, 'assets\senhas.json' )
#             self.telacadastro.controls = [ft.Text(
#                                             'Cadastro realizado com sucesso!', 
#                                             weight='BOLD' ,
#                                             size = 20,
#                                             text_align='center'
#                                             )
#             ]
#             self.height = 100
#             self.telacadastro.update()
#             self.update()
#             sleep(1)
#             e.data = 'login'
#             # await self.page.client_storage.set_async("login", True)
#             if self.func:
#                 self.func(e)
#         else:
#             # dialog = ft.AlertDialog(title=ft.Text("Usuário já cadastrado"))
#             self.username_input.helper_text = 'Usuário já cadastrado'
#             self.username_input.update()
#             # dialog.open = True
#             # self.page.overlay.append(dialog)
#             # self.page.update()

#     def escrever_json(self, data, filename):
#         if not filename.endswith('.json'):
#             filename += '.json'
#         with open(filename, 'w') as f:
#             json.dump(data, f, indent=4)

#     def ler_json2(self, filename, default=None):
#         if not filename.endswith('.json'):
#             filename += '.json'
#         try:
#             with open(filename, 'r') as f:
#                 return json.load(f)
#         except (FileNotFoundError, json.JSONDecodeError):
#             try:
#                 self.escrever_json(default, filename)
#             except:
#                 pass
#             return default or {}

#     @property
#     def tipo(self):
#         return self._tipo
    
#     @tipo.setter
#     def tipo(self, tipo):
#         self._tipo = tipo
#         if self._tipo == 'login':
#             self.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK)
#             self.tela.controls =  [
#                 ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
#                 self.username_input,
#                 self.password_input,
#                 ft.Row([self.login_button,self.salvar_login], alignment='center'),
#             ]
#             self.tela.update()
     
#         elif self._tipo == 'cadastro':
#             self.bgcolor = '#190426,0.8'
#             self.tela.controls =  [
#                 ft.Text("Crie um Usuário e senha", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
#                 self.username_input,
#                 self.password_input,
#                 ft.Row([self.cadastro_button], alignment='center'),
#             ] 
#             self.tela.update()




class LoginG(ft.Container):
    def __init__(self, 
               app = None  
    ):
        super().__init__()
        self.alignment=ft.alignment.center  
        self.expand = True
        self.image = ft.DecorationImage(
            src =  "git.png",  # URL da imagem de fundo
            fit = ft.ImageFit.FILL
        )
        # self.image_src = "git.png"
        # self.image_fit = ft.ImageFit.FILL
        self.app = app
        self._provider_google = GoogleOAuthProvider(
            client_id=os.getenv('GITHUB_CLIENT_ID_G'),
            client_secret=os.getenv('GITHUB_CLIENT_SECRET_G'),
            redirect_url='http://127.0.0.1:5000/oauth_callback'
        )
        self._provider_git = GitHubOAuthProvider(
            client_id=os.getenv('GITHUB_CLIENT_ID'),
            client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
            redirect_url='http://127.0.0.1:5000/api/oauth/redirect'
        ) 
        self.btn_log_google = ft.IconButton(
            content = ft.Image(
                src='logo_google.png',
                width = 120,
                height = 25,
                border_radius = 20,
                fit = ft.ImageFit.FILL,
            ),
            data = 'google',
            on_click = self.fazerlogin,
            style = ft.ButtonStyle(
                padding=ft.Padding(0,0,0,0),
            ),

        )
        self.btn_log_github =  ft.IconButton(
            content = ft.Image(
                src='logo_github.png',
                width = 120,
                height = 25,
                border_radius = 20,
                fit = ft.ImageFit.FILL,
            ),
            data = 'Github',
            on_click = self.fazerlogin,
            style = ft.ButtonStyle(
                padding=ft.Padding(0,0,0,0),
            ),

        )  
        self.linha_botoes_bigs = ft.Row(
            controls = [self.btn_log_google ,self.btn_log_github],
            tight=True,
            alignment='center',
            vertical_alignment='center',
        )
        self.linha_btn_cadastro_login = ft.Row([
            ft.TextButton(
                'Fazer login',
                height = 20,
                style = ft.ButtonStyle(
                    color = {
                        ft.ControlState.HOVERED:'#ede8fd',
                        ft.ControlState.DEFAULT:'blue',
                    },
                    bgcolor = 'black,0.8',
                    padding = ft.Padding(5,0,5,0),
                ),
                data = 'telalogin',
                on_click=self.abrirtela,
            ),  
                
            ft.TextButton(
                'Cadastre-se',
                height = 20,
                style = ft.ButtonStyle(
                    color = {
                        ft.ControlState.HOVERED:'#ede8fd',
                        ft.ControlState.DEFAULT:'blue',
                    },
                    bgcolor = 'black,0.8',
                    padding = ft.Padding(5,0,5,0),
                ),
                data = 'telacadastro',
                on_click=self.abrirtela,
            ),        
            ],
            tight=True,
            alignment='center',
            vertical_alignment='center',
        
        )

        self.senhas = self.ler_json2(r'assets\senhas.json')
                
        # self.caixalogin = Login(self.entrar, 'login')





        self.username_input = ft.TextField(
            hint_text="Usuário",  
            border_color=ft.colors.BLUE_400,
            border_radius=15,
            dense = True,
            
            helper_style=ft.TextStyle(
                color = '#77bf70'
            ),
            prefix_icon=ft.icons.PERSON,
            keyboard_type=ft.KeyboardType.NAME,
   

            prefix_style=ft.TextStyle(
                color = 'primary,0.7'
            )
        )
        self.password_input = ft.TextField(
            hint_text="Senha", 
            password=True, 
            dense = True,
            border_color=ft.colors.BLUE_400, 
            border_radius=15,
            prefix_icon=ft.icons.LOCK,
            keyboard_type=ft.KeyboardType.VISIBLE_PASSWORD,   
            can_reveal_password=True,         
            on_submit=self.login_clicked,
        )
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login_clicked)
        self.cadastro_button = ft.ElevatedButton(text="Cadastrar", on_click=self.Cadastrar)
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


        self.tela = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
            )

        # if self._tipo == 'login':
            # self.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK)
        self.tela.controls =  [
            ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
            self.username_input,
            self.password_input,
            ft.Row([self.login_button,self.salvar_login], alignment='center'),
        ]
     
        # elif self._tipo == 'cadastro':
        #     self.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLUE)
        #     self.tela.controls =  [
        #         ft.Text("Crie um Usuário e senha", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
        #         self.username_input,
        #         self.password_input,
        #         ft.Row([self.cadastro_button], alignment='center'),
        #     ] 
        
        





        self.caixalogin = ft.Container(
            bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK),
            shadow=ft.BoxShadow(
                    blur_radius = 300,
                    blur_style = ft.ShadowBlurStyle.OUTER,
                    color = ft.colors.with_opacity(0.3,ft.colors.CYAN)
            ),
            border= ft.border.all(3, ft.colors.CYAN_500),
            border_radius=12,
            padding= 8,
            data = 'login',
            width = 250,
            height = 260,
            content =  self.tela
        )

        self.content = ft.Column(
            controls = [                
                self.linha_botoes_bigs,
                self.caixalogin,
                self.linha_btn_cadastro_login,
            ],
            alignment='center',
            horizontal_alignment='center', 
        )



    def did_mount(self):
        self.page.on_login = self.onlogin
        if self.page.client_storage.get("login"):
            sleep(2)
            if not self.app is None:
                self.page.controls = [self.app] 
                self.page.update()      


    async def onlogin(self, e):
        self.content.visible = False
        # cadastrar_user.content.visible = False
        self.page.update()        
        if self.caixalogin.data == 'cadastro':
            usuario = self.page.auth.user['email']
            usuarios = list(self.senhas.keys())
            if not usuario in usuarios:
                senha = self.gerar_senha()
                self.senhas[usuario] = senha
                self.escrever_json(self.senhas, 'assets\senhas.json' )
                e.data = 'login'
                self.entrar(e)              
            else:
                dialog = ft.AlertDialog(title=ft.Text("Usuário já cadastrado"))
                dialog.open = True
                self.page.overlay.append(dialog)
                self.page.update()    

            self.content.visible = True
            
            # self.page.update()

        elif self.caixalogin.data == 'login':
            usuario = self.page.auth.user['email']
            usuarios = list(self.senhas.keys())
            # print(usuarios)
            if usuario in usuarios:
                await self.page.client_storage.set_async("login", True)
                e.data = 'logado'
                self.entrar(e)
            else:
                dialog = ft.AlertDialog(title=ft.Text("Usuário não cadastrado"))
                dialog.open = True
                self.page.overlay.append(dialog)
                self.content.visible = True
                self.page.update()
               
        self.update()
            
        #     print('login')
        # print(page.auth.user)

    def fazerlogin(self,e):
        match e.control.data:
            case 'google':
                self.page.login(provider = self._provider_google)
            case 'Github':
                self.page.login(provider = self._provider_git)   

    def entrar(self, e):
        match e.data:
            case 'login':
                # self.page.remove(cadastrar_user)
                # self.page.add(loggg)
                self.caixalogin.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK)
                self.caixalogin.data = 'login'
                self.caixalogin.height = 260

                self.tela.controls =  [
                    ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
                    self.username_input,
                    self.password_input,
                    ft.Row([self.login_button,self.salvar_login], alignment='center'),
                ]
                self.tela.update()
                self.caixalogin.update()              
                self.page.update()
                self.update()

            case 'logado':
                # print('aqui')
                # self.page.remove(loggg)
                # self.page.add(p)
                if not self.app is None:
                    self.page.controls = [self.app] 
                    self.page.update()

    def abrirtela(self, e):
        match e.control.data:
            case 'telacadastro':
                self.caixalogin.bgcolor = ft.colors.with_opacity(0.78, ft.colors.BLACK)
                self.caixalogin.data = 'cadastro'
                self.tela.controls =  [
                    ft.Text("Crie um Usuário e senha", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
                    self.username_input,
                    self.password_input,
                    ft.Row([self.cadastro_button], alignment='center'),
                ]   
                self.caixalogin.update()              
                self.update()   

            case 'telalogin':                     
                self.caixalogin.bgcolor = ft.colors.with_opacity(0.8, ft.colors.BLACK)
                self.caixalogin.data = 'login'
                self.tela.controls =  [
                    ft.Text("Por favor, faça login", size=20, weight=ft.FontWeight.BOLD, text_align='center'),
                    self.username_input,
                    self.password_input,
                    ft.Row([self.login_button,self.salvar_login], alignment='center'),
                ]
            
        self.caixalogin.update()              
        self.update()



    def gerar_senha(self):
        # Lista de caracteres especiais
        caracteres_especiais = '!@#$%^&*()'
        
        # Gera um caractere maiúsculo aleatório
        letra_maiuscula = random.choice(string.ascii_uppercase)
        
        # Gera um caractere especial aleatório
        caractere_especial = random.choice(caracteres_especiais)
        
        # Gera 4 caracteres aleatórios (podem ser letras minúsculas, maiúsculas ou dígitos)
        caracteres_aleatorios = random.choices(string.ascii_letters + string.digits, k=4)
        
        # Combina todos os caracteres
        senha = [letra_maiuscula, caractere_especial] + caracteres_aleatorios
        
        # Embaralha os caracteres para garantir aleatoriedade
        random.shuffle(senha)
        
        # Converte a lista para string e retorna
        return ''.join(senha)



    def valor_salvar_login(self):
        try:
            v = self.page.client_storage.get("salvar_login")
            # print('valor', v)
            if not v is None:
                return v
        except:
            return False
        
    async def Chenge_valor_salvar_login(self, e):
        await self.page.client_storage.set_async("salvar_login", self.salvar_login.value)
                              
    async def login_clicked(self, e):
        usuario = self.username_input.value 
        password = self.password_input.value       
        usuarios = list(self.senhas.keys())


        if usuario in usuarios:
            await self.page.client_storage.set_async("login", True)
            e.data = 'logado'
            self.entrar(e)
        else:
            dialog = ft.AlertDialog(title=ft.Text("Usuário não cadastrado"))
            dialog.open = True
            self.page.overlay.append(dialog)
            self.content.visible = True
            self.page.update()

    def Cadastrar(self, e):
        usuario = self.username_input.value 
        senha = self.password_input.value       
        usuarios = list(self.senhas.keys())
        # print(usuarios)
        if not usuario in usuarios:
            self.senhas[usuario] = senha
            self.escrever_json(self.senhas, 'assets\senhas.json' )
            self.tela.controls = [
                ft.Text(
                    'Cadastro realizado com sucesso!', 
                    weight='BOLD' ,
                    size = 20,
                    text_align='center'
                )
            ]
            
            self.caixalogin.height = 100
            self.update()
            sleep(1)
            e.data = 'login'
            self.entrar(e) 
        else:
            # dialog = ft.AlertDialog(title=ft.Text("Usuário já cadastrado"))
            self.username_input.helper_text = 'Usuário já cadastrado'
            self.username_input.update()
            # dialog.open = True
            # self.page.overlay.append(dialog)
            # self.page.update()


    
    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json2(self, filename, default=None):
        if not filename.endswith('.json'):
            filename += '.json'
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                self.escrever_json(default, filename)
            except:
                pass
            return default or {}














def main(page: ft.Page):
    page.title = "Tela de Login"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    page.add(Login())
if __name__ == '__main__': 
    ft.app(target=main)



