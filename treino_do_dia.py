
import flet as ft
import datetime
from treinos import Treinos

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
        self.nome = ft.Text(value=nome, weight='BOLD', size=25, col = 9)  
        self.b = ft.TextField(
            hint_text='bpm',
            value=bpm,
            dense=True,
            # width=60,
            col = 3,
            border_width=1,
            content_padding=5,
            text_align='center',
            text_style=ft.TextStyle(
                weight=ft.FontWeight.W_600
            ),
            input_filter = ft.NumbersOnlyInputFilter()          
        )
        self.content = ft.ResponsiveRow(
            spacing = 5,
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN,
            controls = [self.nome,self.b],
        )
        
    @property
    def bpm(self):
        return self.b.value
    
    @bpm.setter
    def bpm(self, bpm):
        self.b.value = bpm


class TreinosDiarios(ft.Column):
    def __init__(self,page):
        super().__init__()
        self.page = page
        self.expand = True
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.data_atual = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
        self.treinos = Treinos(self.page)
        self.treino_hoje = self.treinos.exercicio_do_dia()

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
        self.nome_arq_treino = r'assets/treinos.json'
        self.nome_arq_estudos = r'assets/estudos.json'
        self.arquiv = self.treinos.ler_json(
            self.nome_arq_treino,
            default=self.default
            )  
        self.default_estudos  = {
            "None do Treino2":{
                "29-10-2024 22:40":[100,120,105],
                "30-10-2024 22:40":[101,121,106]
            }
        }   
        self.arquiv_estudos = self.treinos.ler_json(
            self.nome_arq_estudos,
            default=self.default_estudos
            )             

        self.btn_salvar = ft.FilledButton(
            text= 'Salvar',
            on_click=self.SalvarEstudoFeito,
        )
        self.modoedicao = ft.FilledButton(
            text= 'Modo Edição',
            on_click=self.AbrirModoEdicao,
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

            col = 8,
            border_width=1,
            dense = True,
            options=self.treinos.materia.options,
            on_change=self.EscolherMateria,
            value = self.treinos.materia.value
        )
           
        self.controls1 = [
            self.materia,
            ft.Container(
                content = ft.Text(
                    f'{self.data_atual}',
                    weight=ft.FontWeight.W_900, 
                    color = ft.colors.PRIMARY,
                    size=20,
                ),
                gradient=ft.LinearGradient(
                    colors = [ft.colors.BLUE_900, ft.colors.GREEN_900],
                    begin = ft.alignment.top_center,
                    end=ft.alignment.bottom_center,
                    # stops=[0,0.3],
                ),
                shadow=ft.BoxShadow(
                    color = ft.colors.with_opacity(0.7,ft.colors.BLUE),
                    spread_radius = 3,
                    blur_radius = 100,
                    blur_style = ft.ShadowBlurStyle.NORMAL,
                ),
                border_radius=12,
                padding=ft.Padding(10,5,10,5),
                alignment=ft.alignment.center,
                width=300
            ) ,
            ft.Row(
                [
                    ft.Text(f'{self.treino_hoje}', size=15, italic = True, weight=ft.FontWeight.W_500),

                ],
                alignment='center'
            ),
            self.Estudos_exibidos,
            ft.Row(
                [
                    self.btn_salvar,
                    self.modoedicao,

                ],
                alignment='center'
            ),            
        ]

        self.controls = self.controls1


    def did_mount(self):
        self.page.window.width = 400
        self.page.update()

    def EscolherMateria(self, e):
        self.page.client_storage.set(f'{self.page.title}_materia',e.control.value)
        self.treinos.materia.value = e.control.value
        self.treinos.lista_treinos = list(self.arquiv[e.control.value]['treinos'].keys())
        self.treino_hoje = self.treinos.exercicio_do_dia()
        self.CarregarListaEstudos()
        self.Estudos_exibidos.controls = self.lista_estudos
        self.Estudos_exibidos.update()

    def CarregarListaEstudos(self):
        self.lista_treinos = self.arquiv[self.treinos.materia.value]['treinos'][self.treino_hoje]
        try:
            self.lista_valores_estudos =  self.arquiv_estudos[self.treino_hoje][-1][1]
            self.lista_estudos = [Estudos(i,b) for i,b in zip(self.lista_treinos,self.lista_valores_estudos)]
        except:
            self.lista_estudos = [Estudos(i,None) for i in self.lista_treinos]




    def SalvarEstudoFeito(self, e):
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


    def AbrirModoEdicao(self, e):

        self.controls = [Treinos(self.page), ft.OutlinedButton('Voltar', on_click=self.Voltar, expand_loose=True , width=300)]
        self.page.window.width = 700
        self.page.update()
        self.update()

    def Voltar(self, e):
        self.controls = self.controls1
        self.page.window.width = 400
        self.page.update()
        self.update()     
        self.CarregarListaEstudos()   
        self.Estudos_exibidos.update()
def main(page: ft.Page):
    # Definindo o t�tulo da p�gina
    page.title = 'Treinos'
    page.window.width = 400  # Define a largura da janela como 800 pixels
    page.window.height = 700  # 
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
