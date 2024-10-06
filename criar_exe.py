
import PyInstaller.__main__
from os import path
from shutil  import rmtree


class Criar_exe:
    def __init__(self,
        programas = [
            'main.py',
            ]                 
    ):
        self.limpar_pasta('build')
        
        for i in programas:
            # if not i.endswith('.spec') and i.endswith('.py'):
            sp = i.split('.')[0]+'.spec'
            if  path.exists(sp):
                PyInstaller.__main__.run([
                    sp
                ])  
            elif i.endswith('.py'):
                PyInstaller.__main__.run([
                            i,
                            '--onefile',
                            '--windowed'
                        ])

            self.limpar_pasta('build')

    def limpar_pasta(self, pasta):
        try:
            rmtree(pasta)
            print(f"A pasta {pasta} foi deletada com sucesso.")
        except OSError as e:
            print(f"Erro ao deletar a pasta: ")
            print(OSError)
            
programas = [
'main.py',
            ]  
if __name__ == "__main__":
    Criar_exe(programas)
