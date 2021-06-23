from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QDir
import pandas as pd
import datetime as dt
import random
from .obj_data import FileData, CurveData, CurveType
from .ui_conf import COLORS


def load_file(source):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QDir.Files)
    DATA = None

    if dialog.exec_():
        try:
            file_name = dialog.selectedFiles()
            path = file_name[0]
            if (source == 'LEAP'):
                DATA = load_LEAP_fileData(path)
            elif (source == 'AP'):
                DATA = load_AP_fileData(path)
            elif (source == 'KLIPPEL'):
                DATA = load_KLIPPEL_fileData(path)
            elif (source == 'Comsol'):
                DATA = load_Comsol_fileData(path)
        except Exception as e:
            print("ERROR: ", e)
            DATA = None
    else:
        pass
    return DATA


def load_AP_fileData(path):
    filename = path[path.rfind('/')+1:path.rfind('.')]

    DATA = None

    if path.endswith('.xlsx'):
        data = pd.read_excel(path, engine="openpyxl", sheet_name=None)
        DATA = FileData(filename, source="AP", file_path=path,
                        import_time=dt.datetime.today())
        curve_idx = 0
        for key in data.keys():
            test_name = data[key].columns[0].strip()
            _type = determineTypeByTestName(test_name)
            note = data[key].columns[1].strip()
            curveDatas = []
            isline = True
            if test_name not in DATA.sequence:
                curve_idx = 0

            for _idx in range(int(len(data[key].columns)/2)):
                label = data[key].iloc[0, _idx*2].strip()
                curve_x = pd.Series(
                    data[key].iloc[3:, _idx*2], name='x', dtype=float)
                curve_y = pd.Series(
                    data[key].iloc[3:, _idx*2+1], name='y', dtype=float)
                if (curve_x.dtype != float or curve_y.dtype != float):
                    isline = False
                    continue
                rdm = random.randint(1, 100)

                curveData_new = CurveData(
                    label=label, note=note, xdata=curve_x, ydata=curve_y, _type=_type, color=COLORS[curve_idx % 11])
                curveDatas.append(curveData_new)
                curve_idx += 1

            if (not isline):
                continue
            if test_name in DATA.sequence:
                DATA.sequence[test_name].extend(curveDatas)
            else:
                DATA.sequence[test_name] = curveDatas
    else:
        pass
    return DATA


def load_LEAP_fileData(path):
    DATA = None
    if path.endswith('.txt'):
        with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
            headers = file.readlines()[:11]
            # LEAP_Impedance
            filename = path[path.rfind('/')+1:path.rfind('.')].strip()
            test_name = filename
            DATA = FileData(filename, source="LEAP",
                            file_path=path, import_time=dt.datetime.today())

            # Impedance_PR: T201100003660
            label = headers[4][headers[4].find('=')+1:].strip()

            units = headers[-1]
            units = units.strip().split(" ")
            units = [x for x in units if x][2:]     # ['Hz', 'Ohm', 'Deg']

            data = pd.read_csv(path,  skiprows=11)
            freq = pd.Series(data.iloc[:, 0], name='x', dtype=float)
            val = pd.Series(data.iloc[:, 1], name='y', dtype=float)
            phase = pd.Series(data.iloc[:, 2], name='y', dtype=float)

            note = ""

            _type = determineTypeByTestName(test_name)

            rdm = random.randint(1, 100)
            curveData_val = CurveData(
                label=label, note=note, xdata=freq, ydata=val, _type=_type, color=COLORS[0])

            curveData_phase = CurveData(
                label=label, note=note, xdata=freq, ydata=phase, _type=CurveType.Phase, color=COLORS[1])

            DATA.sequence[test_name] = [curveData_val]
            DATA.sequence["Phase"] = [curveData_phase]
            file.close()
    else:
        pass
    return DATA


def load_KLIPPEL_fileData(path):
    DATA = None
    if path.endswith('.txt'):
        with open(path, 'r', encoding='UTF-8') as file:
            file_dir = path
            filename = path[file_dir.rfind('/')+1:file_dir.rfind('.')]
            DATA = FileData(filename, source="KLIPPEL",
                            file_path=path, import_time=dt.datetime.today())

            headers = file.readlines()[:3]
            if headers[0][0] == '%':
                raise Exception(
                    "file header start with %, it is a comsole file")
            test_name = headers[0].strip().strip('"')
            labels = headers[1].split('\t\t')
            labels = [c.replace('"', '').strip() for c in labels]

            data = pd.read_table(path,  skiprows=2)
            data = data.dropna()
            curveDatas = []
            note = ""

            # freq = data.iloc[:, 0]
            # freq = [float(f.replace(',', '').strip()) for f in freq]
            # freq = pd.Series(freq, name='x', dtype=float)

            _type = determineTypeByTestName(test_name)

            for i in range(int(len(data.columns)/2)):
                val = pd.Series(data.iloc[:, i*2+1], name='y', dtype=float)
                freq = data.iloc[:, i*2]
                freq = [float(f.replace(',', '').strip()) for f in freq]
                freq = pd.Series(freq, name='x', dtype=float)

                rdm = random.randint(1, 100)
                curveData_new = CurveData(
                    label=labels[i], note=note, xdata=freq, ydata=val, _type=_type, color=COLORS[i % 11])

                curveDatas.append(curveData_new)

            if test_name in DATA.sequence:
                pass
            else:
                DATA.sequence[test_name] = []
            DATA.sequence[test_name].extend(curveDatas)
    else:
        pass
    return DATA


def load_Comsol_fileData(path):
    DATA = None
    if path.endswith('.txt'):
        with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
            headers = file.readlines()[:8]
            # LEAP_Impedance
            filename = path[path.rfind('/')+1:path.rfind('.')]
            test_name = filename
            DATA = FileData(filename, source="COMSOL",
                            file_path=path, import_time=dt.datetime.today())

            if test_name in DATA.sequence:
                pass
            else:
                DATA.sequence[test_name] = []

    #         label = headers[4][headers[4].find('=')+1:]   # Impedance_PR: T201100003660

    #         units = headers[-1]
    #         units = units.strip().split(" ")
    #         units = [x for x in units if x][2:]     # ['Hz', 'Ohm', 'Deg']

            data = pd.read_table(path,  skiprows=7, delim_whitespace=True)
    #         print(data.iloc[:,0])
            freq = pd.Series(data.iloc[:, 0], name='x', dtype=float)
            val = pd.Series(data.iloc[:, 1], name='y', dtype=float)
            # print(freq, val)

            curveDatas = []
            note = ""
            rdm = random.randint(1, 100)
            curveData_new = CurveData(
                label=test_name, note=note, xdata=freq, ydata=val, _type=CurveType.SPL, color=COLORS[0])

            curveDatas.append(curveData_new)

            DATA[test_name].extend(curveDatas)
            file.close()
    else:
        pass
    return DATA


def determineTypeByTestName(test_name):
    if ("Phase" in test_name):
        return CurveType.Phase
    elif ("Impedance" in test_name):
        return CurveType.IMP
    elif ("SPL" in test_name or "CEA" in test_name or 'RMS' in test_name):
        return CurveType.SPL
    elif ("THD" in test_name):
        return CurveType.THD
    else:
        return CurveType.NoType


AP_path = "C:/Users/tong.wang/OneDrive - 國立台灣大學/桌面/Matlab tools/python/data/AP_Acoustic Response_all_xlsx.xlsx"
LEAP_path = "C:/Users/tong.wang/OneDrive - 國立台灣大學/桌面/Matlab tools/python/data/LEAP_Impedance.txt"
KLIPPEL_path = "C:/Users/tong.wang/OneDrive - 國立台灣大學/桌面/Matlab tools/python/data/NFS_CEA2034.txt"

# AP_DATA = load_AP_fileData(AP_path)
# LEAP_DATA = load_LEAP_fileData(LEAP_path)
# KLIPPEL_DATA = load_KLIPPEL_fileData(KLIPPEL_path)

# AP_DATA.dumps()
# AP_DATA.print()