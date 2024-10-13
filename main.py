

import flet as ft
import os
import json
from login import Login
from bancodadosmysql import DatabaseManager
from temaselectsysten import TemaSelectSysten
from time import sleep
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()
# Acessa a variável de ambiente
connection_string = os.getenv("MYSQL_CONNECTION_STRING")
login = os.getenv("ADM_ESTUDO_GUITARRA")



#rciar uma janela para edtar o json dos dados


class ConfirmarSaidaeResize:
    def __init__(self,page, funcao = None, exibir = True, width_max = None, height_max = None):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.width_max = width_max
        self.height_max = height_max
        self.confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirme!"),
            content=ft.Text("Deseja realmente fechar o App?"),
            actions=[
                ft.ElevatedButton("Sim", on_click=self.yes_click),
                ft.OutlinedButton("Não", on_click=self.no_click),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.window.on_event = self.window_event
        self.page.window.prevent_close = True 

        self.page.on_resized = self.page_resize
        # self.page.window.on_event = self.page_resize
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados() 


    def window_event(self, e):
            self.page_resize(e)
            if e.data == "close":
                self.page.overlay.append(self.confirm_dialog)
                
                self.confirm_dialog.open = True
                self.page.update()

    def yes_click(self,e):
        if self.funcao not in ['', None]:
            self.funcao(e)
        self.page.window.destroy()

    def no_click(self,e):
        self.confirm_dialog.open = False
        self.page.update()



    def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
            self.pw.update()
        valores = [self.page.window.width,self.page.window.height,self.page.window.top,self.page.window.left]
        for i in valores:
            if i < 0:
                i = 0
        if valores[1]< self.height_max:
            valores[1] = self.height_max
        with open('assets/tamanho.txt', 'w') as arq:
            arq.write(f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')

  

    def Ler_dados(self):
        try:
            with open('assets/tamanho.txt', 'r') as arq:
                po = arq.readline()
            p1 = po.split(',')
            p = [int(float(i)) for i in p1]
            po = p[:4] 
            for i in po:
                if i < 0:
                    i = 0
            if po[1]< self.height_max:
                po[1] = self.height_max       
            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po
            # print('acerto')
        except:
            # print('erro!')
            with open('assets/tamanho.txt', 'w') as arq:
                arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')
            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = 500,self.height_max,0,0



# class Resize:
#     def __init__(self,page):
#         self.page = page
#         self.page.on_resized = self.page_resize
#         self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
#         self.page.overlay.append(self.pw)   

#     def page_resize(self, e):
#         self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
#         self.pw.update()


class Resize:
    def __init__(self,page, exibir = True):
        self.page = page
        self.page.on_resized = self.page_resize
        self.page.window.on_event = self.page_resize
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados()  

    def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
            self.pw.update()
        with open('assets/tamanho.txt', 'w') as arq:
            arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')

  

    def Ler_dados(self):
        try:
            with open('assets/tamanho.txt', 'r') as arq:
                po = arq.readline()
        except:
            with open('assets/tamanho.txt', 'w') as arq:
                arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')
        po = po.split(',')
        po = [int(float(i)) for i in po]
        
        self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po


class Saida:
    def __init__(self,  page = None):
        self.page = page
        self.snac = ft.SnackBar(
                    content = ft.Text('', selectable=True, color=ft.colors.BROWN_100),
                    open=True,
                    bgcolor=ft.colors.GREY_900,
                )
 
    
    def pprint(self, *texto):
        for i in list(texto):
            self.snac.content.value = f"{i}"
            self.page.open(
                self.snac
            )            
        try:
            self.page.update()
        except:
            pass



    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, height):
        self._height = height
        try:
            self.controls[0].content.height = self._height
            # print(self.controls[0])
            self.page.update()
        except:
            pass

            
            
# class TemaSelectSysten(ft.IconButton):
#     def __init__(self, page = None):
#         super().__init__()    
#         self.pastalocal = 'assets'
#         # self.verificar_pasta()
#         if page:
#             self.page = page
#         self.col = 2
#         self.db = DatabaseManager(connection_string, 'temas', pprint=print)
#         self.EditarTema = self.JanelaEditarTema()
#         self.icon = ft.icons.PALETTE
#         self.sair = ft.FilledTonalButton('Sair', on_click=self.RestaurarJanela)
#         self.em_edicao = False
#         self.on_click = self.Edit


#     def did_mount(self):
#         self.ct_old = self.page.controls.copy() 
#         try:       
#             with open('mytheme.txt', 'r') as arq:
#                 tema = arq.read()
#         except:
#             tema = None
#         if tema:
#             self.page.bgcolor = 'surface'
#             self.dic_atributos = self.arquiv[tema].copy()

#         #     cores_claras = ["white","deeppurple","indigo","lightblue","lightgreen","lime"
#         # "yellow","bluegrey","grey"]
#         #     cc = []
#         #     for i in cores_claras:
#         #         cc.extend([f"{i}{j}" for j in range(100, 600,100)])
#         #     cores_claras += cc

#             if self.dic_atributos.get("light", False):
#                 self.page.theme_mode = ft.ThemeMode.LIGHT
#             else:
#                 self.page.theme_mode = ft.ThemeMode.DARK


#             self.page.theme = ft.Theme(
#                 color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
#                 color_scheme=ft.ColorScheme(
#                     primary = self.dic_atributos["primary"],
#                     on_primary = self.dic_atributos["on_primary"],
#                     on_secondary_container = self.dic_atributos["on_secondary_container"],
#                     outline = self.dic_atributos["outline"],
#                     shadow = self.dic_atributos["shadow"],
#                     on_surface_variant = self.dic_atributos["on_surface_variant"],
#                     surface_variant = self.dic_atributos["surface_variant"],
#                     primary_container = self.dic_atributos["primary_container"],
#                     on_surface = self.dic_atributos["on_surface"],
#                     surface = self.dic_atributos["surface"],
#                     # on_primary_container = self.dic_atributos["on_primary_container"],
#                     # secondary = self.dic_atributos["secondary"],
#                     # on_secondary = self.dic_atributos["on_secondary"],
#                     # tertiary = self.dic_atributos["tertiary"],
#                     # on_tertiary = self.dic_atributos["on_tertiary"],
#                     # tertiary_container = self.dic_atributos["tertiary_container"],
#                     # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
#                     # error = self.dic_atributos["error"],
#                     # on_error = self.dic_atributos["on_error"],
#                     # error_container = self.dic_atributos["error_container"],
#                     # on_error_container = self.dic_atributos["on_error_container"],
#                     # background = self.dic_atributos["background"],
#                     # on_background = self.dic_atributos["on_background"],
#                     # outline_variant = self.dic_atributos["outline_variant"],
#                     # scrim = self.dic_atributos["scrim"],
#                     # inverse_surface = self.dic_atributos["inverse_surface"],
#                     # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
#                     # inverse_primary = self.dic_atributos["inverse_primary"],
#                     # surface_tint = self.dic_atributos["surface_tint"],
#                 )
#             )
                
#             for i in list(self.dic_atributos.keys()):
#             #     self.icones[i].color = self.dic_atributos[i]
#                 try:
#                     self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
#                 except:
#                     pass
#             self.menus.update()                  
#             self.page.update()
        


#     def verificar_pasta(self):
#         # user_profile = os.environ.get('USERPROFILE')
#         # print(user_profile)
#         # if not user_profile:
#         #     # return False  # USERPROFILE não está definido
#         #     self.local = None

#         # caminho = os.path.join(user_profile, self.pastalocal)
#         caminho = self.pastalocal
        
#         if os.path.exists(caminho):
#             self.local = caminho
#             # return self.caminho
#         else:
#             os.mkdir(caminho)
#             # print(caminho)
#             if os.path.exists(caminho):
#                 self.local = caminho
#                 # return self.caminho
#             # else:
#                 # return None
    
#     def caminho(self, nome):
#         # self.verificar_pasta()
#         return os.path.join(self.local, nome)


#     def Caixa(self, ct):
#         return ft.Container(
#             content = ct,
#             shadow=ft.BoxShadow(
#                 blur_radius = 300,
#                 blur_style = ft.ShadowBlurStyle.OUTER,
#                 color = ft.colors.with_opacity(0.5,ft.colors.CYAN)
#             ),
#             border= ft.border.all(3, ft.colors.CYAN_500),
#             border_radius=8,
#             # alignment=ft.Alignment(0, 0),
#             expand = True,
#             padding= 8,

#         ) 

#     def Edit(self, e):
#         if not self.em_edicao:
#             self.em_edicao = True
#             self.tamanho_old = self.page.window.width,self.page.window.height
#             # self.page.window.width = 700
#             # self.page.window.height = 750
#             self.page.controls = [self.Caixa(ft.ListView([self.EditarTema,self.sair], width = 700, expand=True))]
#             self.page.update()

#     def RestaurarJanela(self, e):
#         # e.page.window.width,e.page.window.height = self.tamanho_old
#         e.page.controls = self.ct_old
#         e.page.update()
#         self.em_edicao = False


#     def GerarMenus(self, i):
#         return ft.PopupMenuButton(
#             content = ft.Container(
#                 ft.Text(self.funcoes[i], no_wrap=False,), 
#                 border=ft.border.all(5,'blue'),
#                 padding = ft.Padding(5,0,5,0),
#                 margin=0,
#                 border_radius=12,
#             ),                                      
#             splash_radius = 0,
#             tooltip = '',
#             items=[
#                 ft.PopupMenuItem(
#                     content = self.paleta(i), 
                                            
#                 ),
#                 ft.PopupMenuItem(
#                     content = self.GerarCores(i),                          
#                 ),                            
                
#             ],
#             col = 1 if len(self.funcoes[i]) <= len('labels, cor da caixa do checkbox e cor do check do popMenubutton') else 3
        
        
#         ) 



#     def Change_dark_light(self, e):
#         match e.data:
#             case "DARK":
#                 e.page.theme_mode = ft.ThemeMode.DARK
#                 self.dic_atributos["light"] = False
#             case "LIGHT":
#                 e.page.theme_mode = ft.ThemeMode.LIGHT
#                 self.dic_atributos["light"] = True
#         e.page.update()

#     def JanelaEditarTema(self):
#         self.cores = [
#             "white","black","red","pink","purple",
#             "deeppurple","indigo", "blue","lightblue",
#             "cyan","teal","green","lightgreen","lime"
#         "yellow", "amber", "orange", "deeporange",
#         "brown","bluegrey","grey"

#         ]
#         self.funcoes = {
#             'primary': 'primary: texto principal, fundo filledbutton, texto outlinedbutton, slider,  preenchimento do switch e checkbox, icone,  texto do elevatebuton',
#             'on_primary': 'on_primary: texto filledbutton e bolinha do swicth com True',
#             'on_secondary_container': 'on_secondary_container: texto filledtonalbutton',
#             'outline': 'outline: borda do outliedbutton',
#             'shadow': 'shadow: sombras',
#             'on_surface_variant': 'on_surface_variant: labels, cor da caixa do checkbox e cor do check do popMenubutton',
#             'surface_variant': 'surface_variant: slider e fundo do texfield e do dropbox',
#             'primary_container': 'primary_container: HOVERED da bolinha do switch',
#             'on_surface': 'on_surface: HOVERED do checkbox e cor dos items do popmenubuton',
#             'surface': 'surface: cor de fundo',
#             'color_scheme_seed':'color_scheme_seed',

#         }
#         self.atributos_ColorScheme = list(self.funcoes.keys())
        
#         self.dic_atributos = {i:None for i in self.atributos_ColorScheme}
#         self.icones = {i:ft.Icon(name = ft.icons.SQUARE, data = [i, False], color = 'white') for i in self.atributos_ColorScheme}
        
#         self.nome_tema = ft.TextField(hint_text='Digite o nome do tema', col = 24)
#         self.conf = False
#         self.confirmar = ft.FilledButton('Confirmar', on_click= self.Salvar)
#         self.cancelar = ft.FilledButton('Cancelar', on_click= self.Cancelar)
#         self.linha_salve = ft.ResponsiveRow([self.nome_tema, self.confirmar, self.cancelar], columns={'xs':24, 'sm':48 },visible = False, col =96)
#         self.btn_save = ft.FilledButton('Salvar Tema', on_click=self.TornarVizivel, col = {'xs':96, 'sm':48 })
#         # self.color_scheme_seed = self.GerarMenus('color_scheme_seed', 50)
               
#         self.select_dark_light = ft.RadioGroup(
#             content=ft.Row(
#                 [
#                     ft.Radio(value='DARK', label="DARK",label_style= ft.TextStyle(weight='BOLD')),
#                     ft.Radio(value="LIGHT", label="LIGHT",label_style= ft.TextStyle(weight='BOLD')),
                
#                 ]
#             ),
#         on_change=self.Change_dark_light,
#         )

        
  
#         # self.arquivo_temas = self.caminho('Tema')
#         self.arquiv = self.ler_json(user_id = 'adm', 
#         default=  {
#                 "black": {
#                     "background": None,
#                     "error": None,
#                     "error_container": None,
#                     "inverse_primary": None,
#                     "inverse_surface": None,
#                     "on_background": None,
#                     "on_error": None,
#                     "on_error_container": None,
#                     "on_inverse_surface": None,
#                     "on_primary": "limeyellow",
#                     "on_primary_container": None,
#                     "on_secondary": None,
#                     "on_secondary_container": "grey",
#                     "on_surface": "cyan",
#                     "on_surface_variant": "lightgreen",
#                     "on_tertiary": None,
#                     "on_tertiary_container": None,
#                     "outline": "bluegrey",
#                     "outline_variant": None,
#                     "primary": "lightblue",
#                     "primary_container": "grey",
#                     "scrim": None,
#                     "secondary": None,
#                     "secondary_container": "white",
#                     "shadow": "bluegrey",
#                     "surface": "limeyellow",
#                     "surface_tint": None,
#                     "surface_variant": "limeyellow",
#                     "tertiary": None,
#                     "tertiary_container": None
#     }
# }                       
#         )
#         self.tema_escolhido = ft.Dropdown(
#             label='Selecione um tema',
#             col = 3,
#             options = [
#                 ft.dropdown.Option(i)
#                 for i in sorted(list(self.arquiv.keys()))
#             ],
#             on_change=self.CarregarTema
#         )

#         self.menus = {i:self.GerarMenus(i) for i in self.atributos_ColorScheme}
#         self.ferramentas = ft.Container(
#             bgcolor=ft.colors.SURFACE,           
#             expand=True,
#             content = ft.ResponsiveRow(
#                 [

#                     ft.ElevatedButton('Botão',
#                         # color = self.cor3            
#                     ),
#                     ft.FilledButton(
#                         text = 'Botão1',
#                         # style = ft.ButtonStyle(
#                         #     bgcolor = ft.colors.ON_PRIMARY,
#                         #     color = ft.colors.ON_INVERSE_SURFACE
#                         # )
#                         # ,
#                     ),
#                     # ft.FilledButton(
#                     #     text = 'Botão2',
#                     #     style = ft.ButtonStyle(
#                     #         bgcolor = ft.colors.ON_SECONDARY,
#                     #         color = ft.colors.ON_INVERSE_SURFACE
#                     #     )
#                     #     ,
#                     # ),
#                     # ft.FilledButton(
#                     #     text = 'Botão3',
#                     #     style = ft.ButtonStyle(
#                     #         bgcolor = ft.colors.ON_TERTIARY,
#                     #         color = ft.colors.ON_INVERSE_SURFACE
#                     #     )
#                     #     ,
#                     # ),                                        
#                     ft.FilledTonalButton(
#                         text = 'FilledTonalButton'
#                     ),
#                     ft.OutlinedButton(
#                         text = 'OutlinedButton'
#                     ),
#                     ft.TextField('ksajgh',label='texto', 
#                                 filled=True, dense = True,
            
#                                 ),
#                     ft.Dropdown(label='drop', 
#                                 options=[ft.dropdown.Option(i) for i in range(10)],
#                                 dense = True,
#                                 filled = True,
#                                 # color = ft.colors.ON_PRIMARY,
#                                 # fill_color =ft.colors.,
#                                 # text_style = ft.TextStyle(
#                                 #     color=ft.colors.PRIMARY,
#                                 # )
#                                 # bgcolor = 'black,0.7',
#                     ),
#                     ft.Slider(
#                         min = 1,
#                         max = 100,
#                         divisions = 100,
#                         label='casa',
#                         value=50,

#                     ),
#                     ft.Switch(label = 'valor swith') ,
#                     ft.Checkbox(label ='checkbox'),
#                     ft.Icon(name = ft.icons.BOOK),
#                     ft.PopupMenuButton(
#                         content=ft.Text('TEMA', weight=ft.FontWeight.W_900),
#                         items = [
#                             ft.PopupMenuItem('dark',checked=False),
#                             ft.PopupMenuItem('light',checked=True ),
#                         ],
#                     ),   
#                     ft.Text('título',
#                             color=ft.colors.PRIMARY,
                            
#                     ),              
                    

#                 ],
                
#                 columns={'xs':24, 'sm':50 },
#                 spacing = 0,
#                 run_spacing = 10,
#                 alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
#                 vertical_alignment=ft.CrossAxisAlignment.START,            

#             )
#         )

#         self.cts = [self.ferramentas, self.tema_escolhido, self.select_dark_light,]


           

#         self.cts += [self.menus[i] for i in self.atributos_ColorScheme]
        
#         self.cts += [ft.ResponsiveRow([self.btn_save, self.linha_salve], columns=96, spacing=0, run_spacing=0)]
    
#         return ft.ResponsiveRow(self.cts,
#                            columns={'xs':1, 'sm':3 },
#                            spacing=20,
#                         #    expand = True,
#                            run_spacing = 0,
                           
#             )

#     def GerarCores(self, data):
#         return ft.GridView(
#             [
#                 # ft.IconButton(icon = ft.icons.SQUARE, icon_color = i, col = 0.2,splash_radius=0, padding = 0, on_focus=self.SelecColor) 
#                 ft.Container(bgcolor = i, data = data,col = 0.2, padding = 20, on_click=self.definirCor ) 
#                 for i in ft.colors.colors_list[ft.colors.colors_list.index('scrim')+1:]
#             ],
#             col = 2, 
#             # columns=5,
#             width=200,
#             height=100,
#             runs_count = 8,
#             padding = 0,
#             # aspect_ratio=1,
#             run_spacing=0, 
#             spacing=0
#         )        

#     def TornarVizivel(self, e):
#         self.btn_save.visible = False
#         self.linha_salve.visible = True
#         self.linha_salve.update()
#         self.btn_save.update()


#     def Salvar(self, e):
#         nome_tema = self.nome_tema.value
#         if nome_tema not in ['', ' ', None]+list(self.arquiv.keys()):
#             self.arquiv[nome_tema] = self.dic_atributos
#             # self.escrever_json(self.arquiv, self.arquivo_temas)
#             self.db.EditarJson(
#                 user_id='adm', 
#                 novos_dados_json=self.arquiv,
#                 tabela = 'temas'
#             )            
#             self.linha_salve.visible = False
#             self.btn_save.visible = True
#         else:
#             self.nome_tema.hint_text = 'Digite um nome de Tema válido ou clique em Cancelar'
#             # self.nome_tema.hint_style = ft.TextStyle(size = 10)

#         e.page.update()


#     def CarregarTema(self, e):
#         tema = self.tema_escolhido.value
#         if tema:
#             e.page.bgcolor = 'surface'

#             self.dic_atributos = self.arquiv[tema].copy()
#             # print(self.dic_atributos["surface"])
#         #     cores_claras = ["white","deeppurple","indigo","lightblue","lightgreen","lime"
#         # "yellow","bluegrey","grey"]
#         #     cc = []
#         #     for i in cores_claras:
#         #         cc.extend([f"{i}{j}" for j in range(100, 600,100)])
#         #     cores_claras += cc
#         #     if self.dic_atributos["surface"] in cores_claras:
#         #         e.page.theme_mode = ft.ThemeMode.LIGHT
#         #     else:
#         #         e.page.theme_mode = ft.ThemeMode.DARK

      

#             if self.dic_atributos.get("light", False):
#                 e.page.theme_mode = ft.ThemeMode.LIGHT
#             else:
#                 e.page.theme_mode = ft.ThemeMode.DARK


#             e.page.theme = ft.Theme(
#                 color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
#                 color_scheme=ft.ColorScheme(
#                     primary = self.dic_atributos["primary"],
#                     on_primary = self.dic_atributos["on_primary"],
#                     on_secondary_container = self.dic_atributos["on_secondary_container"],
#                     outline = self.dic_atributos["outline"],
#                     shadow = self.dic_atributos["shadow"],
#                     on_surface_variant = self.dic_atributos["on_surface_variant"],
#                     surface_variant = self.dic_atributos["surface_variant"],
#                     primary_container = self.dic_atributos["primary_container"],
#                     on_surface = self.dic_atributos["on_surface"],
#                     surface = self.dic_atributos["surface"],
#                     # on_primary_container = self.dic_atributos["on_primary_container"],
#                     # secondary = self.dic_atributos["secondary"],
#                     # on_secondary = self.dic_atributos["on_secondary"],
#                     # tertiary = self.dic_atributos["tertiary"],
#                     # on_tertiary = self.dic_atributos["on_tertiary"],
#                     # tertiary_container = self.dic_atributos["tertiary_container"],
#                     # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
#                     # error = self.dic_atributos["error"],
#                     # on_error = self.dic_atributos["on_error"],
#                     # error_container = self.dic_atributos["error_container"],
#                     # on_error_container = self.dic_atributos["on_error_container"],
#                     # background = self.dic_atributos["background"],
#                     # on_background = self.dic_atributos["on_background"],
#                     # outline_variant = self.dic_atributos["outline_variant"],
#                     # scrim = self.dic_atributos["scrim"],
#                     # inverse_surface = self.dic_atributos["inverse_surface"],
#                     # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
#                     # inverse_primary = self.dic_atributos["inverse_primary"],
#                     # surface_tint = self.dic_atributos["surface_tint"],
#                 )
#             )
                
#             for i in list(self.dic_atributos.keys()):
#             #     self.icones[i].color = self.dic_atributos[i]
#                 try:
#                     self.menus[i].content.border = ft.border.all(5,self.dic_atributos[i])
#                 except:
#                     pass
#             # self.menus[i].update()  

#             with open('mytheme.txt', 'w') as arq:
#                 arq.write(tema)

#             # self.icones[i].update()                
#             e.page.update()
            
#     def Cancelar(self, e):
#         self.nome_tema.clean()
#         self.linha_salve.visible = False
#         self.btn_save.visible = True

#         self.nome_tema.update()
#         self.linha_salve.update()
#         self.btn_save.update()

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
        
#     def ler_json(self, user_id = 'adm', default=None):
#         r = self.db.LerJson(user_id=user_id)
#         if isinstance(r, dict):
#             return r
#         else:
#             return default or {}     



#     def definirCor(self, e):
#         # print('bgcolor = ',e.control.bgcolor,'---', 'data =',e.control.data )
#         # self.icones[e.control.data].color = e.control.bgcolor
#         # self.icones[e.control.data].data[1] = True
#         # self.icones[e.control.data].update()

#         self.menus[e.control.data].content.border = ft.border.all(5,e.control.bgcolor)
#         self.menus[e.control.data].update()

#         if e.control.data == 'surface':
#             self.page.bgcolor = e.control.bgcolor

#         # for i in self.atributos_ColorScheme:
#         #     if self.icones[i].data[1] and self.icones[i].data[0] == e.control.data:
#         #         self.dic_atributos[i] = e.control.bgcolor


#         self.dic_atributos[e.control.data] = e.control.bgcolor


#         self.page.theme = ft.Theme(
#             color_scheme_seed=self.dic_atributos.get("color_scheme_seed",None),
#             color_scheme=ft.ColorScheme(
#                 primary = self.dic_atributos["primary"],
#                 on_primary = self.dic_atributos["on_primary"],
#                 on_secondary_container = self.dic_atributos["on_secondary_container"],
#                 outline = self.dic_atributos["outline"],
#                 shadow = self.dic_atributos["shadow"],
#                 on_surface_variant = self.dic_atributos["on_surface_variant"],
#                 surface_variant = self.dic_atributos["surface_variant"],
#                 primary_container = self.dic_atributos["primary_container"],
#                 on_surface = self.dic_atributos["on_surface"],
#                 surface = self.dic_atributos["surface"],
#                 # on_primary_container = self.dic_atributos["on_primary_container"],
#                 # secondary = self.dic_atributos["secondary"],
#                 # on_secondary = self.dic_atributos["on_secondary"],
#                 # tertiary = self.dic_atributos["tertiary"],
#                 # on_tertiary = self.dic_atributos["on_tertiary"],
#                 # tertiary_container = self.dic_atributos["tertiary_container"],
#                 # on_tertiary_container = self.dic_atributos["on_tertiary_container"],
#                 # error = self.dic_atributos["error"],
#                 # on_error = self.dic_atributos["on_error"],
#                 # error_container = self.dic_atributos["error_container"],
#                 # on_error_container = self.dic_atributos["on_error_container"],
#                 # background = self.dic_atributos["background"],
#                 # on_background = self.dic_atributos["on_background"],
#                 # outline_variant = self.dic_atributos["outline_variant"],
#                 # scrim = self.dic_atributos["scrim"],
#                 # inverse_surface = self.dic_atributos["inverse_surface"],
#                 # on_inverse_surface = self.dic_atributos["on_inverse_surface"],
#                 # inverse_primary = self.dic_atributos["inverse_primary"],
#                 # surface_tint = self.dic_atributos["surface_tint"],
#             )
#         )

#         self.page.update()

#     def paleta(self, data):
#         return ft.GridView(
#             [
#                 ft.Container(bgcolor = i, data = data,col = 0.2, padding = 20, on_click=self.definirCor) 
#                 for i in self.cores
#             ],
#             col = 2, 
            
#             runs_count = 6,
#             padding = 0,
#             # aspect_ratio=16/9,
#             run_spacing=0, 
#             spacing=0
#         )

#     def Atributos(self, classe):
#         return [attr for attr in dir(classe) if not attr.startswith('__')]



# class Verificar_pasta:
#     def __init__(self,pastalocal = 'Guitarra'):
#         self.pastalocal = pastalocal
#         self.verificar_pasta()

#     def verificar_pasta(self):
#         user_profile = os.environ.get('USERPROFILE')
#         # print(user_profile)
#         if not user_profile:
#             # return False  # USERPROFILE não está definido
#             self.local = None

#         caminho = os.path.join(user_profile, self.pastalocal)
        
#         if os.path.exists(caminho):
#             self.local = caminho
#             # return self.caminho
#         else:
#             os.mkdir(caminho)
#             # print(caminho)
#             if os.path.exists(caminho):
#                 self.local = caminho
#                 # return self.caminho
#             # else:
#                 # return None
    

#     def caminho(self, nome):
#         # self.verificar_pasta()
#         return os.path.join(self.local, nome)





larguras = {
    "Ano": 80,
    "Mês": 90,
    "item_de_estudo": 180,
    "técnica": 80,
    "Articulação": 80,
    "tempo": 80,
    "NOTAS_TEMPO": 80,
    "meta": 80,
    "velocidade_palhetada": 130,
    "bpm_semana": 80,
    "evolução": 80,
    "NOTAS_S": 80,
    "dias_para_aumentar_1_bpm": 130,
    "tempo_para_conseguir": 130,
    "bpm_máximas": 80,
    "dias":40,    
}

def Calc_larg(i):
    dias = [d for d in list(range(1,32))]
    if i in [ "velocidade_palhetada", 'velocidade palhetada(n/s)','dias para aumentar 1 bpm','tempo para conseguir (dias)', "tempo_para_conseguir", "dias_para_aumentar_1_bpm"]:
        return larguras["velocidade_palhetada"]
  
    elif i in dias:
        return larguras.get('dias', 80)
    elif i in ['item de estudo',"item_de_estudo"]:
        return larguras.get("item_de_estudo", 180)    
    
    else:
        return larguras.get(i, 80) 

def MeuCampoTexto(nome = None, width = None,on_change = None, bold = False):
    if width:
        larg = width
    else:
        larg = Calc_larg(nome)
    if bold:
        b = "bold"
    else: 
        b = "normal"
    return ft.TextField(
        value = nome,
        width=larg,
        content_padding=ft.Padding(4,0,4,0),
        # height=35,
        # dense=True,
        text_style=ft.TextStyle(weight=b),
        text_align=ft.TextAlign.CENTER,
        multiline=True,
        max_lines = 2,
        expand = True,
        on_change=on_change,
    )




class Estudo(ft.Container):
    def __init__(self,                
        Ano = None,
        Mês = None,
        dias = [None for i in range(32)],
        meta = None, 
        Articulação = None,
        técnica = None,
        bpm_semana = None,
        NOTAS_TEMPO = None,
        tempo = None,
        item_de_estudo = None,
        func = None,               
        ):
        super().__init__()
        self.expand_loose = True


        self.func = func


        self.Ano = MeuCampoTexto(nome = Ano, width = larguras.get("Ano", 80))
        self.Mês = MeuCampoTexto(nome = Mês, width = larguras.get("Mês", 80))
        self.item_de_estudo = MeuCampoTexto(nome = item_de_estudo, width = larguras.get("item_de_estudo", 100), bold=True)
        self.técnica = MeuCampoTexto(nome = técnica, width = larguras.get("técnica", 80))
        self.Articulação = MeuCampoTexto(nome = Articulação, width = larguras.get("Articulação", 80))
        self.tempo = MeuCampoTexto(nome = tempo, width = larguras.get("tempo", 80))
        self.NOTAS_TEMPO = MeuCampoTexto(nome = NOTAS_TEMPO, width = larguras.get("NOTAS_TEMPO", 80))
        self.meta = MeuCampoTexto(nome = meta, width = larguras.get("meta", 80))
        self.bpm_semana = MeuCampoTexto(nome = bpm_semana, width = larguras.get("bpm_semana", 80))


        self.velocidade_palhetada = self.MeuCampoTexto1(width=larguras["velocidade_palhetada"])
        self.evolução = self.MeuCampoTexto1()
        self.NOTAS_S = self.MeuCampoTexto1()
        self.dias_pata_aumentar_1_bpm = self.MeuCampoTexto1(width=larguras["dias_para_aumentar_1_bpm"],)
        self.tempo_para_conseguir = self.MeuCampoTexto1(width=larguras["tempo_para_conseguir"])
        self.bpm_máximas = self.MeuCampoTexto1()  
  
        self.dias = [self.MeuCampoTexto1(nome = dias[i-1], width=Calc_larg(i), on_change = self.Calc_max, somente_leitura=False, data = 'dias') for i in range(1,32)]
        
        self.Calc_max(1)


        self.content = ft.Row(
            expand = True,
            # scroll = ft.ScrollMode.AUTO,
            spacing=1,
            run_spacing=0,
            controls = [
                self.Ano,
                self.Mês,
                self.item_de_estudo,
                self.técnica,
                self.Articulação,
                self.tempo,
                self.NOTAS_TEMPO,
                self.meta,
                self.bpm_semana,
                self.velocidade_palhetada,
                self.evolução,
                self.NOTAS_S,
                self.dias_pata_aumentar_1_bpm,
                self.tempo_para_conseguir,
                self.bpm_máximas,
            ]+self.dias   
        )

    def Calc_max(self, e):
        valores_dias = [int(v.value) if v.value else 0  for v in self.dias]
        maximo = max(valores_dias)
        self.bpm_máximas.value = maximo if maximo > 0 else None
        try:
            self.bpm_máximas.update()
        except:
            pass


        if self.bpm_máximas.value and self.NOTAS_TEMPO.value:
            ns = int(self.NOTAS_TEMPO.value) * int(self.bpm_máximas.value)/60
            self.NOTAS_S.value = round(ns,1)
            try:
                self.NOTAS_S.update()
            except:
                pass

        
        if self.NOTAS_S.value and self.técnica.value in ['palhetada', 'Palhetada', 'P.A']:
            self.velocidade_palhetada.value = round(self.NOTAS_S.value, 1)
            try:
                self.velocidade_palhetada.update()
            except:
                pass

        if self.bpm_semana.value:
            self.dias_pata_aumentar_1_bpm.value = round(int(7/int(self.bpm_semana.value)),0)
            try:
                self.dias_pata_aumentar_1_bpm.update()
            except:
                pass  


        if self.dias_pata_aumentar_1_bpm.value and self.bpm_máximas.value:
            if int(self.meta.value) <= int(self.bpm_máximas.value):
                self.tempo_para_conseguir.value = 'Parabéns'
            else:
                self.tempo_para_conseguir.value = round(int((int(self.meta.value) - int(self.bpm_máximas.value))/int(self.dias_pata_aumentar_1_bpm.value)),0)
            
            try:
                self.tempo_para_conseguir.update()
            except:
                pass 

            valores_dias1 = [int(v.value) if v.value else 999  for v in self.dias]
            minimo = min(valores_dias1)
            self.evolução.value = maximo - minimo
            try:
                self.evolução.update()
            except:
                pass 


        #salvar alteração dos bpm
        # try:
        #     # print(e.control.data)
        #     if e.control.data == 'dias':
        #         if self.func:
        #             self.func(e)
        # except:
        #     pass 







    def Savar(self, e):
        if self.func:
            self.func(e)

    def MeuCampoTexto1(self, nome = None, width = None,on_change = None, somente_leitura = True, data = None):
        if width:
            larg = width
        else:
            larg = Calc_larg(nome)
        return ft.TextField(
            value = nome,
            data = data,
            width=larg,
            content_padding=ft.Padding(4,0,4,0),
            # height=35,
            # dense=True,
            text_align=ft.TextAlign.CENTER,
            multiline=True,
            max_lines = 2,
            expand = True,
            on_change=on_change,
            input_filter = ft.NumbersOnlyInputFilter(),
            read_only= somente_leitura,
            selection_color = ft.colors.TRANSPARENT if somente_leitura else None,
            focused_border_color = ft.colors.TRANSPARENT if somente_leitura else None,
        )            

    # @property
    # def bgcolor(self):
    #     return self._bgcolor

    # @bgcolor.setter
    # def bgcolor(self, bgcolor):
    #     self._bgcolor = bgcolor

class ClassName(ft.Row):
    def __init__(self, pprint):
        super().__init__()

        self.pprint = pprint
        self.expand = True
        self.run_spacing = 0
        self.scroll = ft.ScrollMode.AUTO 
        # self.on_scroll = self.Ocultar
        self.vertical_alignment = ft.CrossAxisAlignment.START

        self.db = DatabaseManager(connection_string, 'estudoguitarra', pprint=self.pprint)
        self.nomes_colunas = [
            'Ano', 
            'Mês', 
            'item de estudo',
            'técnica'	,
            'Articulação'	,
            'tempo (min)'	,
            'NOTAS/ TEMPO'	,
            'meta'	,
            'bpm/semana',
            'velocidade palhetada(n/s)'	,
            'evolução (bpm)'	,
            'NOTAS /S'	,
            'dias para aumentar 1 bpm'	,
            'tempo para conseguir (dias)'	,
            'bpm máximas'
        ]
        self.nomes_colunas += list(range(1,32))
        self.style_text = ft.TextStyle(
            weight = 'BOLD',
        )

        # self.caminho_arquivo = Verificar_pasta('Guitarra').caminho('estudoguitarra.json')
        self.arquiv = self.ler_json(
            user_id = 1,
            default={
                "manu": {
                    "0": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "1NPC_MD",
                        "t\u00e9cnica": "P.A",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "4",
                        "meta": "150",
                        "bpm_semana": "7",
                        "dias": [
                            "10",
                            "80",
                            "120",
                            "5",
                            "10",
                            "100",
                            "101",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "1": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "3NPC_MD",
                        "t\u00e9cnica": "sweep",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "6",
                        "meta": "150",
                        "bpm_semana": "7",
                        "dias": [
                            "150",
                            "120",
                            "2",
                            "3",
                            "",
                            "120",
                            "121",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "2": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "ligados - roger franco",
                        "t\u00e9cnica": "ligados",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "",
                        "meta": "",
                        "bpm_semana": "",
                        "dias": [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "120",
                            "121",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "3": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "tapping penta",
                        "t\u00e9cnica": "tapping",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "",
                        "meta": "",
                        "bpm_semana": "",
                        "dias": [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "150",
                            "151",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "4": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "arpegios",
                        "t\u00e9cnica": "sweep",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "",
                        "meta": "",
                        "bpm_semana": "",
                        "dias": [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "105",
                            "106",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "5": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "penta 2NPC",
                        "t\u00e9cnica": "P.A",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "",
                        "meta": "",
                        "bpm_semana": "",
                        "dias": [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "110",
                            "111",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "6": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "escala 3NPC",
                        "t\u00e9cnica": "P.A",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "",
                        "meta": "",
                        "bpm_semana": "",
                        "dias": [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "130",
                            "131",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "7": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "nos alcan\u00e7ou - frase1",
                        "t\u00e9cnica": "ecnomic",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "8",
                        "meta": "",
                        "bpm_semana": "",
                        "dias": [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "120",
                            "121",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "8": {
                        "Ano": "2024",
                        "M\u00eas": "setembro",
                        "item_de_estudo": "nos alcan\u00e7ou - frase2",
                        "t\u00e9cnica": "ecnomic",
                        "Articula\u00e7\u00e3o": "",
                        "tempo": "",
                        "NOTAS_TEMPO": "8",
                        "meta": "",
                        "bpm_semana": "",
                        "dias": [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "120",
                            "121",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ""
                        ]
                    },
                    "visiv": [
                        True,
                        True,
                        True,
                        True,
                        True,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False,
                        False
                    ]
                }
            }
            )
        self.lista_estudos = list(self.arquiv.keys())
        
        self.estudo_mais_recente = self.Nome_estudo_mais_recente()
        self.salvos = self.Gerar_lista_salvos(self.estudo_mais_recente)

        # print(self.salvos)
        self.linha = ft.Row(
            expand_loose = True,
            # scroll = ft.ScrollMode.AUTO,
            spacing=1,
            run_spacing=0, 
            controls = [
                ft.Container(
                    content = ft.Column(
                        spacing = 0,
                        run_spacing=0,
                        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        alignment = ft.MainAxisAlignment.START,
                        controls = [
                            ft.Checkbox(
                                data='dias',
                                splash_radius = 0,
                                shape = ft.CircleBorder(),
                                scale= 0.5,                   
                                label_position = ft.LabelPosition.LEFT,
                                visual_density = ft.VisualDensity.COMPACT,
                                on_change=self.Salvar
                            ),
                            ft.Text(
                                value = i, 
                                style=self.style_text,
                                text_align=ft.TextAlign.CENTER
                            ), 
                        ],
                        # wrap = True,
                        width=Calc_larg(i),
                        height=80,
                    ),
                    

                    bgcolor=ft.colors.SURFACE_VARIANT,
                    alignment = ft.alignment.center,
                    padding=0,
                    
                   
                ) 
                for i in self.nomes_colunas
            ]
        )

        
        self.estudos = ft.Column(
            expand = True,
            scroll = ft.ScrollMode.AUTO,
            spacing=0,
            run_spacing=0, 
            alignment = ft.MainAxisAlignment.START,               
            controls = [
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '1NPC_MD asdasd a  asd as asd asdd s',
                #     func=self.Salvar,
                # ),
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '3NPC_MD',
                #     func=self.Salvar,
                # ), 
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '4NPC_MD',
                #     func=self.Salvar,
                # ),
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '5NPC_MD',
                #     func=self.Salvar,
                # ),
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '3NPC_MD',
                #     func=self.Salvar,
                # ),
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '6NPC_MD',
                #     func=self.Salvar,
                # ),
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '7NPC_MD',
                #     func=self.Salvar,
                # ),
                
                # Estudo(
                #     Ano = '2024',
                #     Mês = 'setembro',
                #     item_de_estudo = '8NPC_MD',
                #     func=self.Salvar,

                # ), 
                Estudo(*i)   
                for i in self.salvos                                                                                                                                                                                          
            ]
        ) 
        self.lgg = Login(func=self.Entrar)
        self.controls1 = [
            ft.Column(
                expand = True,
                # scroll = ft.ScrollMode.AUTO,
                spacing=0,
                run_spacing=0, 
                alignment = ft.MainAxisAlignment.START,
                controls = [
                    self.linha,                                             
                    self.estudos,
                 
                ] 
            )
        ]

        self.controls = [ft.Container(content = self.lgg, alignment=ft.alignment.center,  width=500,expand = True)]


        for n,i in enumerate(self.estudos.controls):
            i.bgcolor = ft.colors.SURFACE if n%2 == 0 else ft.colors.with_opacity(0.15,ft.colors.SURFACE_VARIANT)




            
        # print(estudo_mais_recente)
        self.drop_estudos = ft.Dropdown(
            hint_text='Lista de Estudos',
            value = self.estudo_mais_recente,
            # expand_loose = True,
            width=200,            
            padding = ft.Padding(0,0,2,0),
            height = 20,
            filled=True,
            dense=True,
            alignment = ft.alignment.center,
            text_size = 18,
            col = 4,
            border_radius=5,
            content_padding = ft.Padding(3,0,0,0),
            label = 'Lista de Estudos:',
            # icon_content = ft.Icon(name = ft.icons.FILTER_LIST),
            options=[ft.dropdown.Option(i)
                for i in self.lista_estudos[::-1]
            ],
            on_change=self.Carregar
        )
    
    def Entrar(self, e):
        self.controls = self.controls1
        self.page.floating_action_button = ft.FloatingActionButton(
            text = 'Exibir',
            data = False,
            bgcolor=ft.colors.SURFACE_VARIANT,

            on_click=self.Ocultar
        )

        self.Appbar(mostrar=True)
        self.navigation_bar(mostrar = False)

        # ConfirmarSaidaeResize(self.page,exibir=False,  width_max=723,height_max=656)

        self.page.update()
        self.update()

        for i,j in zip(self.linha.controls[15:],self.arquiv.get(self.estudo_mais_recente, None)['visiv']):
            i.content.controls[0].value = j
     
        self.Ocultacao(False)
    
    def Appbar(self, mostrar = True): 
        if mostrar:   
            # self.page.appbar = ft.AppBar(
            #     actions = [
            #         TemaSelectSysten(),  
            #         ft.FilledButton(
            #             text = 'Salvar',
            #             height=20,
            #             data = 'dias',
            #             style=ft.ButtonStyle(
            #                 padding=ft.Padding(4,0,4,0)
            #             ),
            #             on_click=self.Salvar
                        
            #         ),                           
            #         self.drop_estudos,

            #         ft.FilledButton(
            #             text = 'Add. linha',
            #             height=20,
            #             style=ft.ButtonStyle(
            #                 padding=ft.Padding(4,0,4,0)
            #             ),
            #             on_click=self.Add_nova_linha
                        
            #         ),             
            #         ft.OutlinedButton(
            #             text = 'Novos estudos',
            #             height=20,
            #             style=ft.ButtonStyle(
            #                 padding=ft.Padding(4,0,4,0)
            #             ),
            #             on_click=self.Criar_novo_estudo
                        
            #         ),
            #     ],
                
                
            #     # leading = TemaSelectSysten(),
            #     title=ft.Text(
            #         value = '', 
            #         weight='BOLD', 
            #         color=ft.colors.GREEN_600,
            #         style=ft.TextStyle(
            #             shadow = ft.BoxShadow(
            #                 blur_radius = 300,
            #                 # blur_style = ft.ShadowBlurStyle.OUTER,
            #                 color = ft.colors.WHITE
            #             ),                
            #         )
            #         ),
            #     shadow_color=ft.colors.BLUE,
            #     elevation=8,
            #     toolbar_height = 30,
            #     bgcolor=ft.colors.BLACK38,
            #     automatically_imply_leading=False,
            # )     


            self.page.appbar = ft.Container(
                padding=ft.Padding(5,2,5,3),
                border_radius=3,
                gradient = ft.LinearGradient(
                    end=ft.alignment.bottom_center,
                    begin = ft.alignment.top_center,
                    colors=[                        
                        ft.colors.with_opacity(i/8, ft.colors.SURFACE_VARIANT) for i in  [1,2]
                    ]
                ),
                content = ft.ResponsiveRow(
                    columns={'xs':10, 'sm':18},
                    # expand_loose=True,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing= 10,
                    run_spacing=2,
                    controls = [
                        TemaSelectSysten(),  
                        self.drop_estudos,
                        ft.OutlinedButton(
                            text = 'Novos estudos',
                            height=20,
                            style=ft.ButtonStyle(
                                padding=ft.Padding(4,0,4,0)
                            ),
                            on_click=self.Criar_novo_estudo,
                            col = 4,
                        ), 
                        ft.FilledTonalButton(
                            text = 'Salvar',
                            height=20,
                            data = 'dias',
                            style=ft.ButtonStyle(
                                padding=ft.Padding(4,0,4,0)
                            ),
                            on_click=self.Salvar,
                            col = {'xs':5, 'sm':4},
                            
                        ),                           

                        ft.FilledTonalButton(
                            text = 'Add. linha',
                            height=20,
                            style=ft.ButtonStyle(
                                padding=ft.Padding(4,0,4,0)
                            ),
                            on_click=self.Add_nova_linha,
                            col = {'xs':5, 'sm':4},
                            
                        ),             

                            
                    ]
                ),
            )

    def navigation_bar(self, mostrar = True):
        if mostrar:
            self.page.navigation_bar = ft.CupertinoNavigationBar(
                    bgcolor= ft.colors.BLACK38,
                    inactive_color=ft.colors.GREY,
                    active_color=ft.colors.GREEN_800,
                    on_change=lambda e: print("Selected tab:", e.control.selected_index),
                    destinations=[
                        ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                        ft.NavigationBarDestination(icon=ft.icons.COMMUTE, label="Commute"),
                        ft.NavigationBarDestination(
                            icon=ft.icons.BOOKMARK_BORDER,
                            selected_icon=ft.icons.BOOKMARK,
                            label="Explore",
                        ),
                    ]
                )


    def did_mount(self):
        # for k in list(self.arquiv.get(nome, None).keys())[-1]
        # for i in self.linha.controls[15:]:
        #         i.visible = True

        # for k in self.estudos.controls:
        #     for i in k.content.controls[15:]:                  
        #         i.visible = True

        # print(self.arquiv.get(self.estudo_mais_recente, None)['visiv'])
        for i,j in zip(self.linha.controls[15:],self.arquiv.get(self.estudo_mais_recente, None)['visiv']):
            i.content.controls[0].value = j

        # for k in self.estudos.controls:
        #     for i in k.content.controls[15:]:                  
        #         i.visible = True            



        # self.Ocultacao(False)
        # self.Entrar(1)


    def Ocultar(self,e):
        e.control.data = not e.control.data
        self.Ocultacao(e.control.data)
        if e.control.data:
            e.control.text = 'Ocultar'
            e.control.bgcolor=ft.colors.SURFACE_VARIANT   
        else:
            e.control.text = 'Exibir'
            e.control.bgcolor=ft.colors.with_opacity(0.3,ft.colors.SURFACE_VARIANT)
        e.control.update()



    def Ocultacao(self, sinal):     
        if sinal:
            for i in self.linha.controls[:2]+self.linha.controls[3:15]:
                i.visible = True

            for i in self.linha.controls[15:]:
                  i.visible = True

            for k in self.estudos.controls:
                for i in k.content.controls[15:]:                  
                  i.visible = True


            for k in self.estudos.controls:
                for i in k.content.controls[:2]+k.content.controls[3:15]:
                    i.visible = True                
   
        else:
            for i in self.linha.controls[:2]+self.linha.controls[3:15]:
                i.visible = False


            for i in self.linha.controls[15:]:
                if i.content.controls[0].value:
                    i.visible = False
                else:
                    i.visible = True

            for k in self.estudos.controls:
                for n,i in enumerate(k.content.controls[15:]):
                    if self.linha.controls[15+n].content.controls[0].value:
                        i.visible = False
                    else:
                        i.visible = True


            for k in self.estudos.controls:
                for i in k.content.controls[:2]+k.content.controls[3:15]:
                    i.visible = False



        
        self.linha.update()
        self.estudos.update()
        # return sinal




    def Nome_estudo_mais_recente(self):
        try:
            with open('assets/nestrec.txt', 'r')as arq:
                er = arq.readline()
            return er
        except:
            with open('assets/nestrec.txt', 'w')as arq:
                arq.write('padrão')
            return 'padrão'


    def Criar_novo_estudo(self, e):
        old_actions = self.page.appbar.actions.copy()
        texto = ft.TextField(
                label='Digite o nome da lista',
                # hint_text='Nome da lista de estudos',
                content_padding=ft.Padding(4,0,0,0),
                height=30,


            )
        def Criar(e):
            self.estudos.controls = []
            self.estudos.update()
            self.estudos.controls.append(Estudo(func=self.Salvar))
            self.estudos.controls.append(Estudo(func=self.Salvar))
            for n,i in enumerate(self.estudos.controls):
                i.bgcolor = ft.colors.SURFACE if n%2 == 0 else ft.colors.with_opacity(0.15,ft.colors.SURFACE_VARIANT)

            self.estudos.update()
            # drop_estudos.update()
            self.page.appbar.actions = old_actions
            self.page.appbar.update()
            # page.appbar.actions[0].value = 'leo'
            e.control.data = texto.value
            self.Salvar(e)

            self.lista_estudos = list(self.arquiv.keys())
            self.drop_estudos.options=[ft.dropdown.Option(i)
                for i in self.lista_estudos[::-1]
            ]
            self.drop_estudos.value = texto.value
            self.drop_estudos.update()
            # print(self.page.appbar.actions[0].value )

        def Cancelar(e):
            self.page.appbar.actions = old_actions
            self.page.appbar.update()            


        self.page.appbar.actions = [
            texto,
            ft.FilledButton(
                text='Criar',
                on_click=Criar,
            ),
            ft.OutlinedButton(
                text='Cancelar',
                on_click=Cancelar,
            ),            
        ]
        self.page.appbar.update()



    def Gerar_lista_salvos(self, nome = 'padrão'):         
         return [[i for j,i in list(self.arquiv.get(nome, None).get(k, None).items())+[(None,self.Salvar)]] for k in list(self.arquiv.get(nome, None).keys())[:-1]]
         

    async def Add_nova_linha(self, e):
        self.estudos.controls.append(Estudo(func=self.Salvar))
        for n,i in enumerate(self.estudos.controls):
            i.bgcolor = ft.colors.SURFACE if n%2 == 0 else ft.colors.with_opacity(0.15,ft.colors.SURFACE_VARIANT)

        self.estudos.update()

    def Salvar(self, e):
        # print(e.control.data)
        dic = {}
        for n,i in enumerate(self.estudos.controls):
            dic[n] = {
                'Ano': i.Ano.value,
                'Mês': i.Mês.value,
                'item_de_estudo': i.item_de_estudo.value,
                'técnica': i.técnica.value,
                'Articulação': i.Articulação.value,
                'tempo': i.tempo.value,
                'NOTAS_TEMPO': i.NOTAS_TEMPO.value,
                'meta': i.meta.value,
                'bpm_semana': i.bpm_semana.value,
                'dias': [d.value for d in i.dias]
            }

        dic['visiv'] = []
        for i in self.linha.controls[15:]:
            if i.content.controls[0].value:
                dic['visiv'].append(True)
            else:
                dic['visiv'].append(False)


        if e.control.data and e.control.data != 'dias':
            nome = e.control.data
        else:
            nome = self.drop_estudos.value
        self.arquiv = self.ler_json(
            user_id = 1,

            )  
        self.arquiv[nome] = dic        
        # self.escrever_json(self.arquiv, self.caminho_arquivo)
        sleep(0.7)
        self.db.EditarJson(
            user_id=1, 
            novos_dados_json=self.arquiv,
            tabela = 'estudoguitarra'
        )

        # print('dados salvos')
        # print({'padrão':dic})


    def Carregar(self, e):
        nome  = e.control.value
        lista = self.Gerar_lista_salvos(nome)
        # print(lista)
        self.estudos.controls = [ Estudo(*i)    for i in lista ]
        with open('nestrec.txt', 'w') as arq:
            arq.write(nome)        
        self.estudos.update()

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


    def ler_json(self, user_id = 1, default=None):
        r = self.db.LerJson(user_id=user_id)
        if isinstance(r, dict):
            return r
        else:
            return default or {}     

def main(page: ft.Page):
    # Definindo o titulo da pagina
    page.title = 'Estudo de Guitarra'
    page.window.width = 500  # Define a largura da janela como 800 pixels
    page.window.height = 385  # 
    page.spacing=2
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.theme = ft.Theme(
        scrollbar_theme = ft.ScrollbarTheme(
            thickness = {
                ft.ControlState.HOVERED:20,
                ft.ControlState.DRAGGED:20, 
                ft.ControlState.SCROLLED_UNDER:20
                  },
        ),
        use_material3 = True,
        color_scheme=ft.ColorScheme(
            primary = ft.colors.WHITE70, # cor fundo filledbutton e cor texto outlinedbutton
            on_primary = ft.colors.BLACK, #cor texto filledbutton e cor da bolinha do swicth com True
            secondary_container = ft.colors.GREY_700, # cor de fundo filledtonalbutton
            on_secondary_container = ft.colors.WHITE, # cor de tecto filledtonalbutton
            outline = ft.colors.GREY_600, #cor de borda do outliedbutton
            shadow = ft.colors.BLUE_300, # cor das sombras
            on_surface_variant = ft.colors.WHITE, #cor dos labela
            surface_variant = ft.colors.GREY_600, #cor do slider e cor de fundo do texfield
            primary_container = ft.colors.WHITE70, #cor da bolinha do switch
            on_surface = ft.colors.WHITE, #cor HOVERED do checkbox

        ),
        divider_theme=ft.DividerTheme(
            color=ft.colors.with_opacity(0.5, ft.colors.GREY_800),      # Cor do divisor
            thickness=1,               # Espessura da linha divisória
            leading_indent=1,                 # Recuo inicial
            trailing_indent=1              # Recuo final
        ),
        text_theme=ft .TextTheme(
            title_large=ft.TextStyle(
                size = 20,
                weight=ft.FontWeight.W_800,
            )
        ),
        slider_theme=ft.SliderTheme(
            thumb_color = ft.colors.GREY_700,
        ),
        switch_theme= ft.SwitchTheme(
            thumb_color = {
                ft.ControlState.DEFAULT:ft.colors.GREY_400,
                ft.ControlState.HOVERED:None,
                ft.ControlState.SELECTED:ft.colors.GREY_300,

            },
            track_color = {
                ft.ControlState.DEFAULT:ft.colors.GREY_700,
                ft.ControlState.HOVERED:ft.colors.GREY_700,
            },
            overlay_color = {
                ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
            },
            track_outline_color= {
                ft.ControlState.DEFAULT:ft.colors.WHITE,
                ft.ControlState.HOVERED:ft.colors.WHITE,
            },
            track_outline_width= {
                ft.ControlState.DEFAULT:0,
                ft.ControlState.HOVERED:0
            },
        ),
        checkbox_theme = ft.CheckboxTheme(
            overlay_color = {
                ft.ControlState.DEFAULT:ft.colors.TRANSPARENT,
                ft.ControlState.HOVERED:ft.colors.TRANSPARENT,
            },                
        ),
    )    


    saida = Saida(page)
    # print = saida.pprint 
    # Resize2(page)
    # Resize(page, exibir=False)
    page.update()
    p = ClassName( pprint = saida.pprint)
    def sair(e):
        p.Salvar(e)
        p.db.fechar_conexao(e)
    ConfirmarSaidaeResize(page,exibir=False, funcao=sair, width_max=723,height_max=656)
    # ConfirmarSaidaeResize(page,exibir=False, funcao=sair)
    page.update()
    # page.on_window_event = 
    page.add(p)


if __name__ == '__main__': 
    ft.app(target=main)

