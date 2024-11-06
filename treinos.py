import flet as ft
import datetime
import json
from os import path, environ,mkdir
# from time import sleep

'''
o drop treinos vai selecionar os treinos - ok
colocar um botão para salvar os treinos abaixo de trienos - ok
on_chenge de treinos deve alterar a exibição de tela dos treinos - ok 
adicinar movimento aos estudos (gestos)





'''

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


class SelecionarData(ft.Row):
    def __init__(self, on_change = None):
        super().__init__() 
        self.on_change = on_change
        self.d = ft.DatePicker(
            cancel_text="Cancelar",
            confirm_text= 'Ok',
            error_format_text= 'Data inválida!',
            field_hint_text= 'MM/DD/YYYY',
            field_label_text= 'Digite uma data',
            help_text= 'Selecione uma data no calendário',
            date_picker_mode=ft.DatePickerMode.DAY,
            date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR,
            value = datetime.date(2024,10,30),
            on_change = self.Change
        )
        # self.on_click = self.AbrirData
        self.tooltip = 'Selecionar data inicial'
        self.btn = ft.IconButton(
                icon=ft.icons.DATE_RANGE,
                on_click=lambda _: self.page.open(self.d),
        )

        self.controls = [
                self.btn,
                self.d
        ]

    def did_mount(self):
        self.page.overlay.append(self.d)

    def Change(self, e):
        if self.on_change:   
            e.valor = e.control.value.strftime("%d-%m-%Y")
            self.on_change(e)

    @property
    def value(self):
        return self.d.value.strftime("%d-%m-%Y")

    @value.setter
    def value(self, value):
        self.d.value = value
        self.update()



class Linha(ft.Row):
    def __init__(self, value = None, on_click = None, data = None):
        super().__init__()  
        self.on_click = on_click
        self.campo = ft.TextField(
            hint_text='Nome do estudo',
            # suffix= self.btn_add_novo_treino,
            dense = True,
            # width=270,
            expand=True,
            border_width=1,
            content_padding=8,
            value = value,
            border_radius=12,
        )
        self.controls = [
            ft.Container(
                content = ft.Icon(name = ft.icons.DELETE),
                padding=0,
                margin=0,
                on_click=self.Deletar,
                tooltip='deletar linha',
                data = data,
            ),
            self.campo
        ]

            

    @property
    def value(self):
        return self.campo.value 
    
    @value.setter
    def value(self, value):
        self.campo.value = value

    def Deletar(self, e):
        if self.on_click:
            self.on_click(self)
    



class Gestos(ft.Stack):
    def __init__(self,nome_json):
        super().__init__()
        self.nome_json = nome_json
        def colun(x=1):
            return {"xs":x,"sm": x, "md": x, "lg": x, "xl": x,"xxl": x}
        self.expand=True
        self._movimento = True
        self.controls = []

    @property
    def movimento(self):
        return self._movimento
    
    @movimento.setter
    def movimento(self, movimento:bool):
        if isinstance(movimento, bool):            
            self._movimento = movimento
            if self._movimento:
                for i in self.controls:
                    i.on_vertical_drag_update = self.on_pan_update
                self.update()
        else:
            print(f'o valor dado para "movimento" não é booleano')


    def Add_control(self,nome, control ):
        self.arquiv = self.ler_json(self.nome_json, default={nome:{'left':0,'top':0}})
        try: 
            self.arquiv[nome] == 5
            
        except KeyError:
            v = len(self.controls)*50
            self.arquiv[nome] = {'left':0,'top':v}
        self.escrever_json(self.arquiv,self.nome_json)

        if self._movimento:
            self.controls.append(
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_vertical_drag_update=self.on_pan_update if self._movimento else None,
                    
                    # left=self.arquiv[nome]['left'],
                    top=self.arquiv[nome]['top'],               
                    content= control ,
                    data = nome
                )
            )
        else:
            try:
                # control.left=self.arquiv[nome]['left']
                control.top=self.arquiv[nome]['top']              
                control.data = nome
                self.controls.append(control)
            except:
                self.controls.append(
                    ft.Column(
                        controls = [control],
                        # left=self.arquiv[nome]['left'],
                        top=self.arquiv[nome]['top'],
                        data = nome   
                        )
                )
                
    def on_pan_update(self, e: ft.DragUpdateEvent):
        e.control.top = max(0, e.control.top + e.delta_y)
        # e.control.left = max(0, e.control.left + e.delta_x)
        # self.arquiv[e.control.data]['left'] = e.control.left
        self.arquiv[e.control.data]['top'] = e.control.top
        self.escrever_json(self.arquiv,self.nome_json)
        e.control.update()
        
    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
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




class Verificar_pasta:
    def __init__(self,pastalocal = 'Guitarra'):
        self.pastalocal = pastalocal
        self.verificar_pasta()

    def verificar_pasta(self):
        user_profile = environ.get('USERPROFILE')
        # print(user_profile)
        if not user_profile:
            # return False  # USERPROFILE não está definido
            self.local = None

        caminho = path.join(user_profile, self.pastalocal)
        
        if path.exists(caminho):
            self.local = caminho
            # return self.caminho
        else:
            mkdir(caminho)
            # print(caminho)
            if path.exists(caminho):
                self.local = caminho
                # return self.caminho
            # else:
                # return None
    

    def caminho(self, nome):
        # self.verificar_pasta()
        return path.join(self.local, nome)


class Poupup:
    def __init__(self, 
                 title = None, 
                 funcao = None,
                 page = None,
                 texto =None,
                 nomes_botoes = ['Sim', 'Não'],
                content = None
                 ):
        super().__init__()
        self.page = page
        self.title = title
        self._content = content
        self._funcao = funcao
        self._texto = texto
        self.dialogo1 = ft.AlertDialog(
            modal=False,
            open = True,
            title=ft.Row([ft.Text(self.title, weight='BOLD')],alignment='center'),
            shadow_color = ft.colors.TRANSPARENT,
            content_padding = ft.Padding(15,0,15,0),
            actions_padding = ft.Padding(0,10,0,0),
            title_padding = ft.Padding(4,0,4,0),
            
            bgcolor=ft.colors.GREY_900,
            actions_alignment=ft.MainAxisAlignment.CENTER,
            alignment =ft.alignment.top_center,
        )
        if self._content != None:
            if isinstance(self._content, list):
                self.dialogo1.content = ft.Column([ft.Text(self._texto)], tight=True)
                self.dialogo1.content.controls += [i for i in self._content]

            else:
                self.dialogo1.content = ft.Column([ft.Text(self._texto)], tight=True)
                self.dialogo1.content.controls += [self._content]  
        


        
        if self._funcao != None:
            self.dialogo1.modal=True

            self.dialogo1.actions = [
                ft.Row([
                    ft.Container(
                        bgcolor = ft.colors.with_opacity(1, ft.colors.GREY_500),
                        border_radius = ft.BorderRadius(0,0,20,0),
                        on_click=self.yes_click,
                        padding= ft.Padding(0,10,0,10),
                        content = ft.Text(
                            nomes_botoes[0], 
                            weight = "BOLD", 
                            text_align='center',
                            size = 15,
                             color=ft.colors.PRIMARY,
                        ),
                        expand=True,
                    ),
                    ft.Container(
                        bgcolor = ft.colors.with_opacity(1, ft.colors.RED),
                        border_radius = ft.BorderRadius(0,0,0,20),
                        on_click=self.no_click,
                        padding= ft.Padding(0,10,0,10),
                        content = ft.Text(
                            nomes_botoes[1],
                              weight = "BOLD", 
                              text_align='center',
                              size = 15,
                              color=ft.colors.PRIMARY,
                            ),
                        expand=True,
                    ),
                                     
                ],
                spacing = 0,
                expand= True)
        
            ]

        self.page.overlay.append(self.dialogo1)
        self.page.update()

    @property
    def content(self):
        return self._content
    @content.setter
    def content(self, valor):
        self._content = valor
        if self._content != None and isinstance(self._content, list):
            self.dialogo1.content = ft.Column([ft.Text(self._texto)])
            self.dialogo1.content.controls += [i for i in self._content]
        elif isinstance(self._content, str) | isinstance(self._content, int):
            self.dialogo1.content.controls[0].value = self._texto
        
        self.dialogo1.update() 



    @property
    def texto(self):
        return self._texto
    @texto.setter
    def texto(self, valor):
        self._texto = valor
        if isinstance(self._content, str) | isinstance(self._content, int):
            self.dialogo1.content.controls[0].value = self._texto        
            self.dialogo1.update() 
        

        

    @property
    def funcao(self):
        return self._funcao
    @funcao.setter
    def funcao(self, valor):
        self._funcao = valor
        if self._funcao != None:
            self.dialogo1.modal=True
            self.dialogo1.actions = [
                ft.CupertinoDialogAction(
                'Sim',
                text_style=ft.TextStyle(italic=True),
                is_destructive_action=True,
                on_click=self.yes_click
            ),
                ft.CupertinoDialogAction(text='Não', is_default_action=False, on_click=self.no_click),

            ]
        self.dialogo1.update() 





    def yes_click(self,e):
        if self._funcao != None:
            self._funcao(e)
        # sleep(0.5)
        self.dialogo1.open = False
        self.page.update()


    def no_click(self,e):
        self.dialogo1.open = False
        self.page.update()
    

    def print_in_dialog(self, texto):
        # self.saida_dialog.value = texto
        # self.dialogo1.Content.update()
        self.dialogo1.content.controls[0].value = texto
        self.dialogo1.update() 
    


    def Escrever_json(self, nomedodicionario, nomedoarquivo):
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'w') as f2:
            json.dump(nomedodicionario, f2, indent=4)

    def Ler_json(self, nomedoarquivo):  # retorna um dicionário
        if nomedoarquivo[-4:] != 'json':
            nomedoarquivo = nomedoarquivo+'.json'
        with open(nomedoarquivo, 'r') as f2:
            try:
                a = json.load(f2)
                return a
            except json.JSONDecodeError as e:
                print(f'Erro ao decodificar JSON: {e}')
                return {}


class Treinos(ft.Column):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.expand = True
        self.cont = 0
        self.default = {
            "materia1":{
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
                },
                'data':'31-10-2024'   
            }
        }
        pasta = Verificar_pasta()
        self.nome_arq_treino = pasta.caminho('treinos.json')        
        # self.nome_arq_treino = r'assets/treinos.json'

        style_btn = ft.ButtonStyle(
            color='#92BBEA',
            bgcolor = '#41444b',
            text_style = ft.TextStyle(
                size=12,
                weight='BOLD',
                
            ),
        )
        self.btn_add_materia =  ft.FilledButton(
            text='Add',
            on_click=self.AddMateria,
            col = {'xs':6, 'sm':2},
            style=style_btn,
        )
        self.btn_del_materia =  ft.FilledButton(
            text='Del',
            col ={'xs':6, 'sm':2},
            on_click=self.DeletarMateria,
            style=style_btn,

        )

        self.novo_nome_materia = ft.TextField(
            hint_text='Nome da matéria',
            dense = True,
            width=300,
            border_width=1,
            content_padding=8,
            text_align=ft.alignment.center,
            visible=False,
            suffix= ft.Row(
                spacing=0,
                run_spacing=0,
                tight=True,
                controls=[
                    ft.IconButton(
                        icon=ft.icons.SAVE,
                        tooltip='Salvar',
                        on_click=self.SalvarMateria,
                        
                    ),
                    ft.IconButton(
                        icon=ft.icons.CANCEL,
                        tooltip='Cancelar',
                        on_click=self.CancelarNovaMateria                        
                    ),
                ]
            ),
        )

        self.materia = ft.Dropdown(
            label = 'Materias',
            # width=150,
            col = {'xs':12, 'sm':8},
            border_width=1,
            dense = True,
            on_change=self.EscolherMateria,
            border_radius=12,
        )

        self.treinos = ft.Dropdown(
            label = 'Treinos',
            # width=150,
            border_width=1,
            dense = True,
            on_change=self.EscolherTreino,
            border_radius=12,
            
        )

        self.nome_novo_treino = ft.TextField(
            hint_text='Nome do Treino',
            # suffix= self.btn_add_novo_treino,
            dense = True,
            # width=265,
            expand=True,
            border_width=1,
            content_padding=12,
            border_radius=12,
        )

        self.modo_automatico = ft.Checkbox(
            label='Modo Automático',
            on_change=self.Modo_operacao,
            value = True,
        )
        self.modo_manual = ft.Checkbox(
            label='Modo Manual',
            on_change=self.Modo_operacao,
            value = False,
        )

        self.dias = {
            i:ft.Dropdown(
                label = i,
                width=280,
                border_width=1,
                dense = True,
                content_padding=5,
                alignment=ft.alignment.center_left,
                on_change=self.SelecionarTreinoDia,
                border_radius=8,
            )

            for i in ['dom','seg', 'ter', 'qua', 'qui', 'sex', 'sab']
        }
        self.linha_dias_da_semana = ft.Column(
            controls = [i  for _,i in self.dias.items() ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            # wrap=True,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            run_spacing=5,
            spacing=8,
            
        )

        self.data_select = SelecionarData(self.Set_data_inicial)
        
        self.data_inicial = ft.Text('27-10-2024')
        self.btn_add_linha = ft.IconButton(
            icon=ft.icons.ADD,
            tooltip='Adicionar linha',
            on_click=self.Add_linha_de_treino,
        )

        self.linhas = ft.Column(
            spacing=8,
            run_spacing=0,
            scroll=ft.ScrollMode.AUTO,
            # height=280,
            # tight=True,
            expand=True
        )
        # self.linhas = Gestos('posicoes.json')

        self.btn_novo_treino = ft.FilledTonalButton(
            text='Criar treino',
            on_click=self.Add_Novo_treino,
            style=style_btn,
            col = {'xs':12, 'sm':6},

        )
        self.btn_salvar_treino = ft.FilledButton(
            text='Salvar treino',
            on_click=self.SalvarTreino,
            style=style_btn,
            col = {'xs':12, 'sm':6},
        )
        # self.btn_add_novo_treino = ft.FilledButton(
        #     text = 'Add.',
        # )        

        self.barra_lateral = ft.Column(
            controls = [
                self.treinos,
                ft.Row(
                    [ft.Text('Data inicial:'),self.data_inicial,self.data_select],
                    alignment='center',
                ),
                self.modo_automatico,                
                self.modo_manual,
                self.linha_dias_da_semana, 
                ft.ResponsiveRow(
                    [self.btn_novo_treino,  self.btn_salvar_treino,],
                    alignment='center',
                ),
                             

            ],
            width=270,
            # expand=True,
            spacing=5,

        )

        self.tela_treinos = ft.Column(
             controls = [
                ft.Row([self.nome_novo_treino,self.btn_add_linha],),
                self.linhas,                 
            ],
            width=245,
            alignment=ft.MainAxisAlignment.START,
            # expand_loose=True,
        )


        self.Carregar_treinos()
        self.CarregarModos()


        self.controls = [
            ft.Container(              
                ft.ResponsiveRow(
                    [ 
                        self.materia,
                        self.novo_nome_materia,
                        self.btn_add_materia,
                        self.btn_del_materia,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True,
                ),
                gradient = ft.LinearGradient(
                    end=ft.alignment.center_left,
                    begin = ft.alignment.center_right,
                    colors=[                        
                        ft.colors.with_opacity(i/12, ft.colors.GREY_200) for i in  [1,2]
                    ]
                ),
                padding=ft.Padding(10,10,10,10),
                border_radius=20,

            ),            
            ft.ResponsiveRow(
               [ 
                    ft.Container(              
                        self.barra_lateral,
                        gradient = ft.LinearGradient(
                            end=ft.alignment.center_left,
                            begin = ft.alignment.center_right,
                            colors=[                        
                                ft.colors.with_opacity(i/9, ft.colors.GREY_400) for i in  [1,2]
                            ]
                        ),
                        padding=ft.Padding(10,10,10,10),
                        border_radius=20,
                        col = 6,
                    ),
                    ft.Container(              
                        self.tela_treinos,
                        gradient = ft.LinearGradient(
                            end=ft.alignment.center_left,
                            begin = ft.alignment.center_right,
                            colors=[                        
                                ft.colors.with_opacity(i/15, ft.colors.GREY_400) for i in  [1,2]
                            ]
                        ),
                        padding=ft.Padding(10,10,10,10),
                        border_radius=20,
                        col = 6,

                    ),                    
                ],
                expand=True,

            ),
        ]



    # def did_mount(self):
    #     self.CarregarModos()

    def CarregarModos(self):
        try:
            valor_modo = self.page.client_storage.get(f'{self.page.title}_Modo_Automatico')
            # print('valor_modo', valor_modo)
        except:
            valor_modo = True
        # sleep(1)
        self.modo_automatico.value = valor_modo
        self.modo_manual.value = not valor_modo
        try:
            self.modo_automatico.update()
            self.modo_manual.update()       
        except:
            pass



       
    def Add_Novo_treino(self, e):
        self.nome_novo_treino.value = None
        self.linhas.controls = [] 
        self.linhas.update()
        self.nome_novo_treino.update()

       
    def SalvarTreino(self, e):
        nome = self.nome_novo_treino.value
        estudos = [i.value for i in self.linhas.controls]
  
        self.arquiv = self.ler_json(
            self.nome_arq_treino,
            default=self.default
            )
        self.arquiv[self.materia.value]['treinos'][nome] = estudos

        self.arquiv[self.materia.value]['data'] = self.data_inicial.value
        self.escrever_json(self.arquiv, self.nome_arq_treino)
        self.Carregar_treinos()
        self.treinos.update()
        self.linha_dias_da_semana.update()
        # print('nome:', nome)
        # print(estudos)


    def SalvarMateria(self, e):
        nome_materia = self.novo_nome_materia.value
        if nome_materia not in ['', None]:
            self.arquiv = self.ler_json(
                self.nome_arq_treino,
                default=self.default
                )

            nome = self.nome_novo_treino.value
            estudos = [i.value for i in self.linhas.controls]
    
           
            dic = {
                       'treinos':{nome:estudos},
                       'dias':{ 
                            "dom": self.dias["dom"].value,
                           "seg": self.dias["seg"].value,
                            "ter": self.dias["ter"].value,
                            "qua": self.dias["qua"].value,
                            "qui": self.dias["qui"].value,
                            "sex": self.dias["sex"].value,
                            "sab": self.dias["sab"].value,
                            }
                   }
            
            self.arquiv[nome_materia] = dic
            self.escrever_json(self.arquiv, self.nome_arq_treino)
            self.Carregar_treinos()
            self.treinos.update()
            self.linha_dias_da_semana.update()  
        self.CancelarNovaMateria(1)


    def Modo_operacao(self, e):
        if e.control.label == 'Modo Automático':
            self.modo_manual.value = not self.modo_automatico.value
        else:
            self.modo_automatico.value = not self.modo_manual.value
        self.page.client_storage.set(f'{self.page.title}_Modo_Automatico', self.modo_automatico.value)
        self.modo_manual.update()
        self.modo_automatico.update()

    def Escrever_treino_noarquivo(self, treino):
        with open(r'assets/treinos.txt', 'a') as arq:
            arq.write(f'{treino}\n')

    def Carregar_treinos(self):
        # with open(r'assets/treinos.txt', 'r') as arq:
        #     treinos = arq.read()    
        self.arquiv = self.ler_json(
            self.nome_arq_treino,
            default=self.default
            )     
        self.lista_materias =  list(self.arquiv.keys())  
        self.materia.options = [] 
        for materia in self.lista_materias:
            if materia not in ['', None]:
                self.materia.options.append(ft.dropdown.Option(materia)) 

        if self.materia.value == None:
            try:
                value_materia = self.page.client_storage.get(f'{self.page.title}_materia')
                if value_materia and value_materia in self.lista_materias:
                    self.materia.value = value_materia
                else:
                    self.materia.value = self.lista_materias[0]
            except:
                self.materia.value = self.lista_materias[0]
 
        # self.materia.update()

        self.lista_treinos = list(self.arquiv[self.materia.value]['treinos'].keys())
        self.treinos.options = []
        for _,t in self.dias.items():
            t.options = []         
        for i in self.lista_treinos:
            if i not in ['', None]:
                self.treinos.options.append(ft.dropdown.Option(i))
                for _,t in self.dias.items():
                    t.options.append(ft.dropdown.Option(i)) 

        if self.treinos.value == None:
            try:
                valor_treino = self.page.client_storage.get(f'{self.page.title}_treino')
                if valor_treino not in ['', None] and valor_treino in self.lista_treinos:
                    self.treinos.value = valor_treino
                else:
                    self.treinos.value = self.lista_treinos[0]
            except:
                self.treinos.value = self.lista_treinos[0]


        nomes_dias = [ 'dom','seg', 'ter', 'qua', 'qui', 'sex', 'sab']    
        for i in nomes_dias: 
            self.dias[i].value = self.arquiv[self.materia.value]['dias'][i]

        treino = self.treinos.value
        estudos = self.arquiv[self.materia.value]['treinos'].get(treino, None)
        if not estudos is None:
            self.linhas.controls = [Linha(i, self.Deletar) for i in estudos]
            self.nome_novo_treino.value = treino
        self.data_inicial.value = self.arquiv[self.materia.value].get('data','01-10-2024')

    def EscolherMateria(self, e):
        materia = self.materia.value
        self.page.client_storage.set(f'{self.page.title}_materia', materia)
        self.Carregar_treinos()
        # treinos = list(self.arquiv.get(materia, None).keys())
        # estudos = self.arquiv[materia]['treinos'].get(treinos[0], None)

        # self.linhas.controls = [Linha(i, self.Deletar) for i in estudos]
        # self.nome_novo_treino.value = treinos[0]
        # self.nome_novo_treino.update()
        self.treinos.value = list(self.arquiv[self.materia.value]['treinos'].keys())[0]
        print(self.treinos.value)
        self.EscolherTreino(1)
        self.update()

    def EscolherTreino(self, e):
        treino = self.treinos.value
        self.page.client_storage.set(f'{self.page.title}_treino', treino)
        estudos = self.arquiv[self.materia.value]['treinos'].get(treino, None)
        self.linhas.controls = [Linha(i, self.Deletar) for i in estudos]
        self.nome_novo_treino.value = treino
        self.nome_novo_treino.update()
        self.linhas.update()
        # self.data_inicial.value = self.arquiv[self.materia.value]['data'].get('data','01-10-2024')
        # self.data_inicial.update()

    def SelecionarTreinoDia(self, e):
        dia = e.control.label
        self.arquiv = self.ler_json(
            self.nome_arq_treino,
            default=self.default
            )
        self.arquiv[self.materia.value]['dias'][dia] = e.control.value
        self.escrever_json(self.arquiv, self.nome_arq_treino)


    def Set_data_inicial(self, e):
        data_inicial = e.valor
        self.data_inicial.value = data_inicial
        self.data_inicial.update()
        # print(data_inicial)
        # print(self.exercicio_do_dia())

    def exercicio_do_dia(self):
        # Converte a data inicial e a data atual para o formato datetime
        self.Carregar_treinos()

        if self.modo_automatico.value == True:
            data_inicial = self.data_inicial.value
            data_inicial = datetime.datetime.strptime(data_inicial, "%d-%m-%Y")
            data_atual = datetime.datetime.now()

            # Calcula a diferença em dias entre as datas
            diferenca_dias = (data_atual - data_inicial).days

            # Determina o índice do exercício baseado na diferença de dias
            indice = diferenca_dias % len(self.lista_treinos)

            # Retorna o exercício do dia
            return self.lista_treinos[indice]

        else:
            dia_hoje = (datetime.datetime.now().weekday() + 1) % 7
            # print('dia hoje:',dia_hoje )
            nomes_dias = ['dom','seg', 'ter', 'qua', 'qui', 'sex', 'sab' ]
            return self.dias.get(nomes_dias[dia_hoje], 'Não definido').value

    def Add_linha_de_treino(self, e):
        # linha = ft.Row(
        #     controls = [
        #         ft.Container(
        #             content = ft.Icon(name = ft.icons.DELETE),
        #             padding=0,
        #             margin=0,
        #             on_click=self.Deletar,
        #             tooltip='deletar linha',
        #         ),

        #         ft.TextField(
        #             hint_text='Nome do estudo',
        #             # suffix= self.btn_add_novo_treino,
        #             dense = True,
        #             width=265,
        #             border_width=1,
        #             content_padding=8,
        #         )

        #     ]
        # )
        
        self.linhas.controls.append(Linha(on_click = self.Deletar))
        # nome = f'{self.materia.value}_{self.nome_novo_treino.value}_{self.cont}'
        # self.cont +=1
        # self.linhas.Add_control(nome, Linha(on_click = self.Deletar,data = nome))
        self.linhas.update()

    def AddMateria(self, e):
        self.novo_nome_materia.visible = True
        self.novo_nome_materia.update()
        self.btn_add_materia.visible = False
        self.btn_del_materia.visible = False 
        self.btn_add_materia.update()
        self.btn_del_materia.update()             
        self.materia.visible = False
        self.materia.update()


        self.treinos.value = None
        self.treinos.update()
        self.nome_novo_treino.value = None
        self.nome_novo_treino.update()
        for _,i in self.dias.items():
            i.value = None
        self.linha_dias_da_semana.update()

    def DeletarMateria(self, e):
        valor = self.materia.value
        pop = ft.AlertDialog(
            open = True,
            modal = False,
            title = ft.Row([ft.Text('CUIDADO!', weight='BOLD')]),
            content = ft.Column([ft.Text(  'meu poau')]),
            # actions: List[Control] | None = None,
            # on_dismiss: OptionalControlEventCallable = None,
            # ref: Ref | None = None,
            # disabled: bool | None = None,
            # visible: bool | None = None,
            # data: Any = None
        )
  


        # for i in self.materia.options:
        #     if i.key == valor:
        #         self.materia.options.remove(i)    
        # self.materia.update()
        # self.arquiv = self.ler_json(
        #     self.nome_arq_treino,
        #     default=self.default
        #     )
        # del self.arquiv[valor]      
            

    def CancelarNovaMateria(self, e):
        self.novo_nome_materia.visible = False
        self.novo_nome_materia.update()
        self.btn_add_materia.visible = True
        self.btn_del_materia.visible = True 
        self.btn_add_materia.update()
        self.btn_del_materia.update()             
        self.materia.visible = True
        self.materia.update()        

    def Deletar(self, e):
        self.linhas.controls.remove(e)
        # for n,i in enumerate(self.linhas.controls):
        #     if i.data == e.control.data:
        #         del self.linhas.controls[n]
        self.linhas.update()



    def escrever_json(self, data, filename):
        if not filename.endswith('.json'):
            filename += '.json'
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def ler_json(self, filename, default=None):
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
    # Definindo o t�tulo da p�gina
    page.title = 'Treinos'
    page.window.width = 685  # Define a largura da janela como 800 pixels
    page.window.height = 683  # 
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


    p = Treinos(page)
    page.add(p)

if __name__ == '__main__': 
    ft.app(target=main)
