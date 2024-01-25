import os
import numpy as np
from os import getcwd
from sys import platform
import pandas as pd

from Drow import Drow
from flet import (
    ElevatedButton,
    Page,
    Row,
    Text,
    icons,
    TextField,
    Checkbox,
    Dropdown,
    IconButton,
    MainAxisAlignment,
    dropdown,
    RadioGroup,
    Radio,
    app,
    VerticalDivider,
    Column,
    FloatingActionButton,
    NavigationRail,
    NavigationRailLabelType,
    Icon,
    NavigationRailDestination,
    AlertDialog,
)

Mac = False
path = ''
if Mac == True:
    splitter = '/'
else:
    splitter = '\\'
for item in getcwd().split(splitter):
    path += item + '/'
if platform == 'win32':
    splitter = '/'
else:
    splitter = '/'


def get_buttons():
    pass


But_list = get_buttons()


class Interface():
    "Этот класс для..."

    def __init__(self, page):
        self.splitter = splitter
        self.page = page
        self.selected_index = 0
        self.LaserBlue_nm = TextField(value='410', width=100, label="Laser_BLUE nm")
        self.LaserRed_nm = TextField(value='659', width=100, label="Laser_RED nm")
        self.AddExample = Checkbox(label='Добавить на график', value=True, visible=False)
        self.Standartaligment = MainAxisAlignment.START
        self.Label_k_b = Text('fff', visible=False)
        self.ChooseLaser_BLUE = Dropdown(
            label="ChooseLaser_BLUE",
            on_change=self.ImportDataLaser_BLUE,
            width=350,
        )
        self.ChooseLaser_RED = Dropdown(
            label="ChooseLaser_RED",
            on_change=self.ImportDataLaser_RED,
            width=350,
        )
        self.ChooseFile = Dropdown(
            label="Выберите файл для просмотра",
            on_change=self.ReadExperiment,
            visible=False
        )
        self.ChooseExample = Dropdown(
            label="Выберите спект для сравнения",
            # on_change=self.ReadExperiment,
            visible=False
        )
        self.ON_OFF_Radio = RadioGroup(
            on_change=self.ObrabON_OFF_Radio,
            value='ON',
            content=Row(
                [Text('ON/OFF'),
                 Radio(value="ON", label="ON"),
                 Radio(value="OFF", label="OFF"),
                 ]
            )
        )
        self.GetBlueLaserButton = ElevatedButton('Считать Laser_BLUE', on_click=self.GetBlueLaserData)
        self.GetREDLaserButton = ElevatedButton('Считать Laser_RED  ', on_click=self.GetREDLaserData)
        self.Calc_k_b_button = ElevatedButton('Рассчитать k b', on_click=self.Calc_k_b)
        self.DrowIconButton = IconButton(icon=icons.TASK_ALT_OUTLINED, on_click=self.GetBlueLaserData,
                                         icon_color='green')
        self.Label = Text('On', visible=True)
        self.StartPicNumber = 0
        self.DisplayedPic = 260
        self.Name = TextField(visible=False)
        self.AlertIndex = 0
        self.JesusButton = IconButton(icon=icons.ACCESSIBILITY_SHARP, icon_color='red', on_click=self.Alert)

    def DrowFullCsvSpectr(self, df):
        drow = Drow(self)
        drow.DrowFullCsvSpectr(df)

    def LoadCsvSpectr(self, file):
        print('path:', f'./Эксперимент/{file}')
        df = pd.read_csv(f'./Эксперимент/{file}', sep=';', decimal=',').drop(columns=['Unnamed: 0'])
        return df

    def ImportDataLaser_BLUE(self, e):
        df = self.LoadCsvSpectr(self.ChooseLaser_BLUE.value)
        self.DrowFullCsvSpectr(df)
        self.XBlue = np.argmax(df.b)
        print('X Laser_BLUE', self.XBlue)

    def ImportDataLaser_RED(self, e):
        df = self.LoadCsvSpectr(self.ChooseLaser_RED.value)
        self.DrowFullCsvSpectr(df)
        self.XRed = np.argmax(df.r)
        print('X Laser_RED', self.XRed)

    def Calc_k_b(self, e):
        self.k = (float(self.LaserBlue_nm.value) - float(self.LaserRed_nm.value)) / (int(self.XBlue) - int(self.XRed))
        self.b = float(self.LaserBlue_nm.value) - self.k * int(self.XBlue)
        print(f'k= {self.k} b = {self.b}')
        self.Label_k_b.value = f'k= {self.k} b = {self.b}'
        self.Label_k_b.visible = True
        self.Label_k_b.update()
        self.AddExample.visible = True
        self.AddExample.update()
        self.CheckExperimentFiles()
        self.LoadExamples()

    def LoadExamples(self):
        sheet_names = ['led', 'cfl', 'ln', 'mg']
        self.df_list = []
        self.DeviceNames = []
        self.ChooseExample.options = []
        for i, sheetName in enumerate(sheet_names):
            self.DeviceNames.append(sheetName)
            # self.df_list[i] = pd.read_excel('Examples.xlsx', sheet_name=sheetName).fillna(0)
            df_tmp = pd.read_excel('Examples.xlsx', sheet_name=sheetName)
            for Device in df_tmp.columns[1:]:
                self.df_list.append(pd.DataFrame(data={'nm':df_tmp['nm'],f'{Device}':df_tmp[Device]}).dropna())
                self.ChooseExample.options.append(dropdown.Option(Device))
        self.ChooseExample.visible = True
        self.ChooseExample.update()

        pass

    def CheckExperimentFiles(self):
        self.files = []
        self.ChooseFile.options = []
        for file in os.listdir('./Эксперимент/'):
            if ('csv' in file) and ('._' not in file):
                self.files.append(file)
                self.ChooseFile.options.append(dropdown.Option(file))
        self.ChooseFile.visible = True
        self.ChooseFile.update()

    def ReadExperiment(self, e):
        df = self.LoadCsvSpectr(self.ChooseFile.value)
        drow = Drow(self)
        drow.DrowSpectr(df, self.ChooseFile.value)
        print(df)

    def Alert(self, e):
        self.AlertIndex += 1
        self.page.dialog = AlertDialog(
            modal=True,
            title=Text(f'{self.AlertIndex}'),
            actions=[self.JesusButton])
        self.page.dialog.open = True
        self.page.update()

    def Obrab_ViewGraphs(self, e):
        if e.control.value:
            self.ChooseFunction.visible = True
            self.InputA.visible = True
            self.DrowButton.visible = True
            self.DrowIconButton.visible = True
            self.Label.visible = True
            self.ON_OFF_Radio.visible = True
        else:
            self.ChooseFunction.visible = False
            self.InputA.visible = False
            self.DrowButton.visible = False
            self.DrowIconButton.visible = False
            self.Label.visible = False
            self.ON_OFF_Radio.visible = False
        self.ChooseFunction.update()
        self.InputA.update()
        self.DrowButton.update()
        self.DrowIconButton.update()
        self.Label.update()
        self.ON_OFF_Radio.update()

    def ObrabON_OFF_Radio(self, e):
        if e.control.value == 'ON':
            self.Label.value = e.control.value
        else:
            self.Label.value = e.control.value
        self.Label.update()

    def GetBlueLaserData(self, e):
        path = './Эксперимент/'
        for file in os.listdir(path):
            if ('csv' in file) and ('._' not in file):
                if 'Laser_BLUE' in file:
                    self.ChooseLaser_BLUE.options.append(dropdown.Option(file))
        self.ChooseLaser_BLUE.update()

    def GetREDLaserData(self, e):
        path = './Эксперимент/'
        for file in os.listdir(path):
            if ('csv' in file) and ('._' not in file):
                if 'Laser_RED' in file:
                    self.ChooseLaser_RED.options.append(dropdown.Option(file))
        self.ChooseLaser_RED.update()

    def rebuildSetup(self, e):
        self.rebuild('Setup')
        return 'Setup'

    def get_menu(self):

        rail = NavigationRail(
            selected_index=self.selected_index,
            label_type=NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            leading=FloatingActionButton(icon=icons.CREATE, text="Run", on_click=self.GetBlueLaserData),
            group_alignment=-0.9,
            destinations=[
                NavigationRailDestination(
                    icon_content=Icon(icons.SETTINGS),
                    selected_icon=icons.SETTINGS,
                    label="Setup"
                ),
                NavigationRailDestination(
                    icon_content=Icon(icons.BOOKMARK_BORDER),
                    selected_icon_content=Icon(icons.BOOKMARK),
                    label="Buttons",
                ),
            ],
            on_change=self.rebuild,
        )
        return rail

    def get_Setup(self):
        row01 = Row([self.GetBlueLaserButton, self.ChooseLaser_BLUE, self.LaserBlue_nm])
        row02 = Row([self.GetREDLaserButton, self.ChooseLaser_RED, self.LaserRed_nm])
        row03 = Row([self.Calc_k_b_button, self.Label_k_b])
        row04 = Row([self.ChooseFile, self.ChooseExample, self.AddExample])
        row2 = Row([self.DrowIconButton, self.JesusButton],
                   alignment=self.Standartaligment)
        row3 = Row([self.Label], alignment=self.Standartaligment)
        row4 = Row([self.ON_OFF_Radio], alignment=self.Standartaligment)
        body = Column([Row([Text('Setup')]),
                       row01,
                       row02,
                       row03,
                       row04,
                       row2,
                       row3,
                       row4,
                       ])
        return body

    def Plus(self, e):
        self.StartPicNumber += self.DisplayedPic
        self.rebuild('Buttons')

    def Minus(self, e):
        if self.StartPicNumber >= self.DisplayedPic:
            self.StartPicNumber -= self.DisplayedPic
            self.rebuild('Buttons')

    def Set_StartPicNumber(self, e):
        self.StartPicNumber = (int(e.control.value) // self.DisplayedPic) * self.DisplayedPic
        self.rebuild('Buttons')

    def PrintName(self, e):
        self.Name.value = e.control.icon
        self.Name.visible = True
        self.Name.update()

    def get_Buttons(self):
        row0 = Row([ElevatedButton('Left', on_click=self.Minus),
                    ElevatedButton('Right', on_click=self.Plus),
                    TextField(value=self.StartPicNumber, on_submit=self.Set_StartPicNumber),
                    self.Name])
        row1 = Row([], alignment=self.Standartaligment)
        row2 = Row([], alignment=self.Standartaligment)
        row3 = Row([], alignment=self.Standartaligment)
        row4 = Row([], alignment=self.Standartaligment)
        row5 = Row([], alignment=self.Standartaligment)
        row6 = Row([], alignment=self.Standartaligment)
        row7 = Row([], alignment=self.Standartaligment)
        row8 = Row([], alignment=self.Standartaligment)
        row9 = Row([], alignment=self.Standartaligment)
        row10 = Row([], alignment=self.Standartaligment)
        row11 = Row([], alignment=self.Standartaligment)
        row12 = Row([], alignment=self.Standartaligment)
        for button in But_list[int(self.StartPicNumber):int(self.StartPicNumber) + 20]:
            row1.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[20 + int(self.StartPicNumber):int(self.StartPicNumber) + 40]:
            row2.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[40 + int(self.StartPicNumber):int(self.StartPicNumber) + 60]:
            row3.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[60 + int(self.StartPicNumber):int(self.StartPicNumber) + 80]:
            row4.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[80 + int(self.StartPicNumber):int(self.StartPicNumber) + 100]:
            row5.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[100 + int(self.StartPicNumber):int(self.StartPicNumber) + 120]:
            row6.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[120 + int(self.StartPicNumber):int(self.StartPicNumber) + 140]:
            row7.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[140 + int(self.StartPicNumber):int(self.StartPicNumber) + 160]:
            row8.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[160 + int(self.StartPicNumber):int(self.StartPicNumber) + 180]:
            row9.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[180 + int(self.StartPicNumber):int(self.StartPicNumber) + 200]:
            row10.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[220 + int(self.StartPicNumber):int(self.StartPicNumber) + 240]:
            row11.controls.append(IconButton(icon=button, on_click=self.PrintName))
        for button in But_list[240 + int(self.StartPicNumber):int(self.StartPicNumber) + 260]:
            row12.controls.append(IconButton(icon=button, on_click=self.PrintName))

        body = Column([Row([Text('Setup')]),
                       row0,
                       row1,
                       row2,
                       row3,
                       row4,
                       row5,
                       row6,
                       row7,
                       row8,
                       row9,
                       row10,
                       row11,
                       row12,
                       ])
        return body

    def get_body(self, e):
        if isinstance(e, str):  # Обработка вызова из класса
            if e == 'Setup':
                return self.get_Setup()
            # elif e == 'Buttons':
            #     return self.get_Buttons()
        elif isinstance(e.control, NavigationRail):  # Обработка вызова из Навигационного меню
            if e.control.selected_index == 0:
                return self.get_Setup()
            # elif e.control.selected_index == 1:
            #     return self.get_Buttons()

    def rebuild(self, e):
        self.page.clean()
        body = self.get_body(e)
        self.page.add(
            Row(
                [
                    self.get_menu(), VerticalDivider(width=1),
                    Column([body], alignment=MainAxisAlignment.START, expand=True),
                ], expand=True,
            )
        )
        self.page.update()
        pass


if __name__ == "__main__":
    def main(page: Page):
        Window = Interface(page)
        Window.rebuild('Setup')
        page.window_center()
        page.window_width = 1000
        page.window_height = 600
        page.update()


    app(target=main)
