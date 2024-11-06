
import flet as ft
import datetime
from treinos import Treinos,Verificar_pasta, path

from temaselectsysten import TemaSelectSysten

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
            self.snac.content.value = f'{i}'
            self.page.open(
                self.snac
            )            
        try:
            self.page.update()
        except:
            pass


class Estudos(ft.Container):
    def __init__(self, nome, bpm):
        super().__init__()  
        self.nome = ft.Text(
            value=nome, 
            weight='BOLD', 
            size=25, 
            col = 9,
            color = '#597799',
        )  

        self.b = ft.TextField(
            hint_text='bpm',
            value=bpm,
            dense=True,
            width=80,
            col = 3,
            filled=True,
            border_width=0,
            # focused_border_width = 0,
            fill_color='#503F3F',
            # border_width=1,
            # focused_bgcolor = 'white,0.9',
            border_radius=12,
            content_padding=5,
            text_align='center',
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_900,
                # size = 18,
                color = '#A0BAD7',
            ),
            input_filter = ft.NumbersOnlyInputFilter()          
        )
        self.content = ft.Row(
            spacing = 5,
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.END,
            controls = [
                self.nome,
                ft.Text(
                    value='_'*500, 
                    # weight='BOLD', 
                    size=5, 
                    col = 9,
                    color = '#597799',
                    expand=True,
                    no_wrap=True,
                ),                  
                
                self.b,
            ],
        )
        
    @property
    def bpm(self):
        return self.b.value
    
    @bpm.setter
    def bpm(self, bpm):
        self.b.value = bpm



class ConfirmarSaidaeResize:
    def __init__(self,page, funcao = None, exibir = True, width_min = None, height_min = None, onlyresize = False):
        super().__init__()
        self.page = page
        self.funcao = funcao
        self.width_min = width_min
        self.height_min = height_min
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
        self.onlyresize = onlyresize
        if not onlyresize:
            self.page.window.prevent_close = True 

        self.page.on_resized = self.page_resize
        # self.page.window.on_event = self.page_resize
        self.nome = f'{self.page.title}_tamanho'
        self.exibir = exibir
        if self.exibir:
            self.pw = ft.Text(bottom=10, right=10, theme_style=ft.TextThemeStyle.TITLE_MEDIUM )
            self.page.overlay.append(self.pw) 
        self.Ler_dados() 


    async def window_event(self, e):
            await self.page_resize(e)
            if e.data == "close" and not self.onlyresize:
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



    async def page_resize(self, e):
        if self.exibir:
            self.pw.value = f'{self.page.window.width}*{self.page.window.height} px'
            self.pw.update()
        valores = [self.page.window.width,self.page.window.height,self.page.window.top,self.page.window.left]

        if valores[1]< self.height_min:
            valores[1] = self.height_min
        if valores[0]< self.width_min:
            valores[0] = self.width_min      
        if valores[2] <0:
              valores[2] = 0   
        if valores[3] <0:
              valores[3] = 0                
        # with open('assets/tamanho.txt', 'w') as arq:
        #     arq.write(f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        await self.page.client_storage.set_async(self.nome, f'{valores[0]},{valores[1]},{valores[2]},{valores[3]}')
        

  

    def Ler_dados(self):
        try:
            # with open('assets/tamanho.txt', 'r') as arq:
            #     po = arq.readline()

            po = self.page.client_storage.get(self.nome)

            p1 = po.split(',')
            p = [int(float(i)) for i in p1]
            po = p[:4] 

            if po[0]< self.width_min:
                po[0] = self.width_min   
            if po[1]< self.height_min:
                po[1] = self.height_min 
            if po[2] <0:
                po[2] = 0   
            if po[3] <0:
                po[3] = 0                                   

            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = po
            # print('acerto')
        except:
            # print('erro!')
            # with open('assets/tamanho.txt', 'w') as arq:
            #     arq.write(f'{self.page.window.width},{self.page.window.height},{self.page.window.top},{self.page.window.left}')
            self.page.window.width, self.page.window.height,self.page.window.top,self.page.window.left = self.width_min,self.height_min,0,0




class TreinosDiarios(ft.Column):
    def __init__(self,page):
        super().__init__()
        self.page = page
        # self.page.window.opacity = 0.5
        # self.page.window.width = 685  # Define a largura da janela como 800 pixels
        # self.page.window.height = 683  # 
        # self.page.bgcolor = '#876c6c',
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # self.alignment = ft.MainAxisAlignment.START
        self.data_atual = datetime.datetime.now().strftime("%d-%m-%Y")
        self.treinos = Treinos(self.page)
        # self.treino_hoje = self.treinos.exercicio_do_dia()
        # print('nome_do_treino', self.treino_hoje)

        self.default = {
            'treinos':{
            'None do Treino':['a', 'b', 'c'],
            'None do Treino2':['a2', 'b2', 'c2'],
            },
            'dias':{
                'seg':None,
                'ter':None,
                'qua':None,
                'qui':None,
                'sex':None,
                'sab':None,
                'dom':None
            }
        }
        # self.nome_arq_treino = r'.\assets\treinos.json'
        pasta = Verificar_pasta()
        self.nome_arq_treino = pasta.caminho('treinos.json')
        if not path.exists(self.nome_arq_treino):
            self.page.client_storage.remove(f'{self.page.title}_materia')
        
        # self.nome_arq_estudos = r'.\assets\estudos2.json'
        self.nome_arq_estudos = pasta.caminho('estudos2.json')
        if not path.exists(self.nome_arq_estudos):
            self.page.client_storage.remove(f'{self.page.title}_treino')
                
 
        self.default_estudos  = {
            "None do Treino2":{
                "29-10-2024 22:40":[100,120,105],
                "30-10-2024 22:40":[101,121,106]
            }
        }   
          
        style_btn = ft.ButtonStyle(
            color='#92BBEA',
            bgcolor = '#31343C',
            text_style = ft.TextStyle(
                size=24,
                weight='BOLD',
            ),
        )
        self.btn_salvar = ft.FilledButton(
            text= 'Salvar',
            on_click=self.SalvarEstudoFeito,
            style = style_btn,
        )
        self.modoedicao = ft.FilledButton(
            text= 'Modo Edição',
            on_click=self.AbrirModoEdicao,
            style = style_btn,

        )

        self.CarregarListaEstudos()
        self.Estudos_exibidos = ft.Column(
                self.lista_estudos,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                spacing=5,
        )

        
        # valor_materia = self.page.client_storage.get(f'{self.page.title}_materia')
        self.materia = ft.Dropdown(
            label = 'Materias',
            # width=150,
            border_radius=12,
            border_color='#323232',
            text_style = ft.TextStyle(
                size=20,
                weight='BOLD',
                color='#B0B0B0'
            ),
            label_style =ft.TextStyle(
                color = '#C07F7F',
            ),
            alignment=ft.alignment.center,
            fill_color='#22252e',
            col = 11,
            expand=True,
            border_width=0,
            dense = True,
            options=self.treinos.materia.options,
            on_change=self.EscolherMateria,
            value = self.treinos.materia.value
        )
        tema = TemaSelectSysten(self.page)
        # tema.visible = False
        tema.width = 30
        self.controls1 = [
            ft.Row(
                [
                    self.materia,
                    # tema,
                ], expand_loose=True),
            ft.Container(
                # visible = False,
                content = ft.Text(
                    f'{self.data_atual}',
                    weight=ft.FontWeight.W_900, 
                    color = '#A2AEDA',    #ft.colors.PRIMARY,
                    size=20,
                ),
                # gradient=ft.LinearGradient(
                #     colors = [ft.colors.BLUE_900, ft.colors.GREEN_900],
                #     begin = ft.alignment.top_center,
                #     end=ft.alignment.bottom_center,
                #     # stops=[0,0.3],
                # ),
                # shadow=ft.BoxShadow(
                #     color = ft.colors.with_opacity(0.7,ft.colors.BLUE),
                #     spread_radius = 3,
                #     blur_radius = 100,
                #     blur_style = ft.ShadowBlurStyle.NORMAL,
                # ),
                border_radius=12,
                bgcolor = '#6F5656',
                padding=ft.Padding(10,5,10,5),
                alignment=ft.alignment.center,
                width=300
            ) ,
            ft.Row(
                [
                    ft.Text(
                        f'{self.treino_hoje}', 
                        size=15, 
                        italic = True, 
                        weight=ft.FontWeight.W_500,
                        color = '#A2AEDA',
                    ),

                ],
                alignment='center',
            ),
            self.Estudos_exibidos,
            ft.Row(
                [
                    self.btn_salvar,
                    self.modoedicao,

                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),            
        ]

        self.controls = self.controls1


    def did_mount(self):
    #     self.page.window.width = 400
        self.page.update()

    def EscolherMateria(self, e):
        self.page.client_storage.set(f'{self.page.title}_materia',e.control.value)
        self.treinos.materia.value = e.control.value
        self.treinos.lista_treinos = list(self.arquiv[e.control.value]['treinos'].keys())
        self.treino_hoje = self.treinos.exercicio_do_dia()
        self.CarregarListaEstudos()
        self.Estudos_exibidos.controls = self.lista_estudos
        self.Estudos_exibidos.update()

    def CarregarListaEstudos2(self):
        self.lista_treinos = self.arquiv[self.treinos.materia.value]['treinos'][self.treino_hoje]
        try:
            self.lista_valores_estudos =  self.arquiv_estudos[self.treino_hoje][-1][1]
            self.lista_estudos = [Estudos(i,b) for i,b in zip(self.lista_treinos,self.lista_valores_estudos)]
        except:
            self.lista_estudos = [Estudos(i,None) for i in self.lista_treinos]


    def CarregarListaEstudos(self):
        self.arquiv = self.treinos.ler_json(
            self.nome_arq_treino,
            default=self.default
            )         
        self.arquiv_estudos = self.treinos.ler_json(
            self.nome_arq_estudos,
            default=self.default_estudos
            )      
        
        self.treino_hoje = self.treinos.exercicio_do_dia()  
        # lista_treinos_mais_recente =         
        self.lista_treinos = self.arquiv[self.treinos.materia.value]['treinos'].get(self.treino_hoje, None)
        # try:
        nome_do_treino = self.treino_hoje
        # print('nome_do_treino', nome_do_treino)
        estudos = self.arquiv_estudos.get(nome_do_treino,None)
        if isinstance(estudos, dict):
            data_mais_recente = list(estudos.keys())[-1]
            # print('data_mais_recente',data_mais_recente)
            self.lista_valores_estudos =  estudos[data_mais_recente]
        # print(self.lista_valores_estudos)
            self.lista_estudos = [Estudos(i,b) for i,b in zip(self.lista_treinos,self.lista_valores_estudos)]
        else:
            if isinstance(self.lista_treinos, list):
                self.lista_estudos = [Estudos(i,None) for i in self.lista_treinos]
            else:
                self.lista_estudos = []
        # print(self.lista_estudos)
    def SalvarEstudoFeito2(self, e):
        valores = [int(float(i.bpm)) for i in self.lista_estudos ]
        self.arquiv_estudos = self.treinos.ler_json(
            self.nome_arq_estudos,
            default=self.default_estudos
            )
        try:
            self.arquiv_estudos[self.treino_hoje].append([self.data_atual,valores])
        except:
            self.arquiv_estudos[self.treino_hoje] = []
            self.arquiv_estudos[self.treino_hoje].append([self.data_atual,valores])
    
        self.treinos.escrever_json(self.arquiv_estudos, self.nome_arq_estudos)
        # self.arquiv_estudos

    def SalvarEstudoFeito(self, e):
        valores = [int(float(i.bpm)) for i in self.lista_estudos ]
        self.arquiv_estudos = self.treinos.ler_json(
            self.nome_arq_estudos,
            default=self.default_estudos
            )
        self.arquiv_estudos[self.treino_hoje] = {self.data_atual:valores}    
        self.treinos.escrever_json(self.arquiv_estudos, self.nome_arq_estudos)
        # self.arquiv_estudos





    def AbrirModoEdicao(self, e):
        self.controls = [
            Treinos(self.page), 
            ft.Row(
                [
                    ft.OutlinedButton(
                        'Voltar', 
                        on_click=self.Voltar, 
                        expand=True , 
                        # width=600, 
                        # height=30
                    ),

                ],
                height=30,

            )
        ]
        # self.page.window.width = 800
        # self.page.update()
        self.update()

    def Voltar(self, e):
        self.controls = self.controls1
        self.update()     
        self.CarregarListaEstudos()
        print(self.lista_estudos)
        self.Estudos_exibidos.controls = self.lista_estudos
        self.Estudos_exibidos.update()
        self.arquiv = self.treinos.ler_json(
            self.nome_arq_treino,
            default=self.default
            )         
        self.lista_materias =  list(self.arquiv.keys())  
        self.materia.options = [] 
        for materia in self.lista_materias:
            if materia not in ['', None]:
                self.materia.options.append(ft.dropdown.Option(materia)) 


        self.materia.update()


def main(page: ft.Page):
    # Definindo o t�tulo da p�gina
    page.title = 'Treinos'
    page.window.width = 685  # Define a largura da janela como 800 pixels
    page.window.height = 683  # 
    page.horizontal_alignment = 'center'
    page.theme_mode = ft.ThemeMode.DARK
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
            primary = ft.colors.WHITE70, # fundo filledbutton, texto outlinedbutton, slider,  preenchimento do switch e checkbox, icone, texto, texto do elevatebuton
            on_primary = ft.colors.BLACK, #cor texto filledbutton e cor da bolinha do swicth com True
            secondary_container = ft.colors.GREY_700, # cor de fundo filledtonalbutton
            on_secondary_container = ft.colors.WHITE, # cor de texto filledtonalbutton
            outline = ft.colors.GREY_600, #cor de borda do outliedbutton
            shadow = ft.colors.BLUE_300, # cor das sombras
            on_surface_variant = ft.colors.WHITE, #cor dos labels, cor da caixa do checkbox e cor do check do popmenubutton
            surface_variant = ft.colors.GREY_600, #cor do slider e cor de fundo do texfield e do dropbox
            primary_container = ft.colors.WHITE70, #cor HOVERED da bolinha do switch
            on_surface = ft.colors.WHITE, #cor HOVERED do checkbox e cor dos items do popmenubuton

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


    p = TreinosDiarios(page)
    page.add(p)

if __name__ == '__main__': 
    ft.app(target=main)
