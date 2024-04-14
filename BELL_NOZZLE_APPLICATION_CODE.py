### REFFERED FROM A MATLAB CODE BY "VDEngineering" ###

### CODE CONTRIBUTERS : K.HARSHA VARDHAN, B.AKHIL GOUD, SIDDHANTH THAKURI, U.RAJENDAR ###

###****** MAKE SURE TO REFER THE PREVIOUS BELL NOZZLE CONTOUR CODE AND README FILE ******###

'''

 THIS PYTHON CODE WILL POP UP A GUI WINDOW WHERE YOU CAN ENTER ISENTROPIC VALUES MANUALLY AND GET YOUR REQUIRED
 BELL NOZZLE CONTOUR COORDINATES IN EXCEL SHEET, ALSO IT DISPLAYS THE REQUIRED THEORITICAL VALUES WITH
 NOZZLE VISUALIZATION.

'''

'''
 TO CONVERT IT INTO AN APPLICATION I.E.( .exe FILE ), FOLLOW THE PROCEDURE GIVEN IN THE READ ME FILE.
'''

# REQUIRED MODULES-----------------------------------------------------------------------------------
import tkinter as tk
from math import *
from scipy.optimize import brentq
from matplotlib.pyplot import *
from xlwt import Workbook
import numpy as np

#MAIN CODE------------------------------------------------------------------------------------------
try:
#DEFAULT VALUES ------------------------------------------------------------------------------------
    CHAMBER_PRESSURE_DEFAULT = 2267000
    CHAMBER_TEMPERATURE_DEFAULT = 1200
    ALTITUDE_DEFAULT = 7500
    GAMMA_DEFAULT = 1.4
    GAS_CONSTANT_DEFAULT = 288
    MACH_NUMBER_DEFAULT = 3
    THROAT_RADIUS_DEFAULT = 0.0369
    EXIT_PRESSURE_DEFAULT = 39365

#CREATING TKINTER INTERFACE-----------------------------------------------------------------
    root = tk.Tk()
    root.title('BELL NOZZLE CONTOUR GENERATOR')
    canvas1 = tk.Canvas(root,width = 400, height = 300)
    canvas1.pack()

#ADDING DEFAULT VALUES TO THE VALUE BOX-------------------------------------------
    chamber_pressure = tk.StringVar(root, value=str(CHAMBER_PRESSURE_DEFAULT))
    chamber_temperature = tk.StringVar(root, value=str(CHAMBER_TEMPERATURE_DEFAULT))
    altitude = tk.StringVar(root, value=str(ALTITUDE_DEFAULT))
    gamma = tk.StringVar(root, value=str(GAMMA_DEFAULT))
    gas_constant = tk.StringVar(root, value=str(GAS_CONSTANT_DEFAULT))
    mach_number = tk.StringVar(root, value=str(MACH_NUMBER_DEFAULT))
    throat_radius = tk.StringVar(root, value=str(THROAT_RADIUS_DEFAULT))
    exit_pressure = tk.StringVar(root, value=str(EXIT_PRESSURE_DEFAULT))

    entry1 = tk.Entry(root, textvariable=chamber_pressure, font=("Helvetica", 15))
    entry2 = tk.Entry(root, textvariable=chamber_temperature, font=("Helvetica", 15))
    entry3 = tk.Entry(root, textvariable=altitude, font=("Helvetica", 15))
    entry4 = tk.Entry(root, textvariable=gamma, font=("Helvetica", 15))
    entry5 = tk.Entry(root, textvariable=gas_constant, font=("Helvetica", 15))
    entry6 = tk.Entry(root, textvariable=mach_number, font=("Helvetica", 15))
    entry7 = tk.Entry(root, textvariable=throat_radius, font=("Helvetica", 15))
    entry8 = tk.Entry(root, textvariable=exit_pressure, font=("Helvetica", 15))

#LABELS FOR THE DEFAULT VALUES-------------------------------------------------------------------------
    label10 = tk.Label(root, text='CHAMBER_PRESSURE (Pascal)', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 20+80, window=label10)
    label11 = tk.Label(root, text='CHAMBER_TEMPERATURE (K)', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 50+80, window=label11)
    label12 = tk.Label(root, text='ALTITUDE (Meters)', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 80+80, window=label12)
    label13 = tk.Label(root, text='GAMMA', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 110+80, window=label13)
    label14 = tk.Label(root, text='GAS_CONSTANT (J/Kg-K)', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 140+80, window=label14)
    label15 = tk.Label(root, text='MACH_NUMBER', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 170+80, window=label15)
    label16 = tk.Label(root, text='THROAT_RADIUS (m)', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 200+80, window=label16)
    label17 = tk.Label(root, text='EXIT_PRESSURE (Pascal)', fg='#0005FF', font=("Helvetica", 15))
    canvas1.create_window(10, 230+80, window=label17)
    label18 = tk.Label(root, text='(IF DON\'T KNOW THEN JUST ENTER "N")', fg='#0005FF', font=("Helvetica", 9))
    canvas1.create_window(510, 230+80, window=label18)
    canvas1.create_window(280, 20+80, window=entry1)
    canvas1.create_window(280, 50+80, window=entry2)
    canvas1.create_window(280, 80+80, window=entry3)
    canvas1.create_window(280, 110+80, window=entry4)
    canvas1.create_window(280, 140+80, window=entry5)
    canvas1.create_window(280, 170+80, window=entry6)
    canvas1.create_window(280, 200+80, window=entry7)
    canvas1.create_window(280, 230+80, window=entry8)

#SOME TEXTS ---------------------------------------------------------------------------------------------
    my_text = tk.Label(root, text="Bell Nozzle Contour Generator",
                       fg='#6D0092', font=("Helvetica", 23))
    my_text.place(x=280, y=30)
    inst = tk.Label(root, text="INSTRUCTIONS:\n\n\t\t\t\t1) The default values can be changed accordingly"
                               "\n\n\t\t\t\t\t\t   2) The coordinates generated will be saved in your PC as 'nozzlepts.xls'"
                               "\n\n\t\t\t\t\t     3) Check the calculated isentropic values present in the console"
                               "\n\t\t\t\t     *(note down the values before closing the plots.)",
                    fg='black', font=("Helvetica", 15))
    inst.place(x=-450, y=350)


#BUTTON FUNCTIONS TO READ VALUES ON CLICK-------------------------------------------
    def get_chamber_pressure():
        global CHAMBER_PRESSURE
        CHAMBER_PRESSURE = float(entry1.get())
    def get_chamber_temperature():
        global CHAMBER_TEMPERATURE
        CHAMBER_TEMPERATURE = float(entry2.get())
    def get_altitude():
        global ALTITUDE
        ALTITUDE = float(entry3.get())
    def get_gamma():
        global GAMMA
        GAMMA = float(entry4.get())
    def get_gas_constant():
        global GAS_CONSTANT
        GAS_CONSTANT = float(entry5.get())
    def get_mach_number():
        global MACH_NUMBER
        MACH_NUMBER = float(entry6.get())
    def get_throat_radius():
        global THROAT_RADIUS
        THROAT_RADIUS = float(entry7.get())
    def get_exit_pressure():
        global EXIT_PRESSURE
        EXIT_PRESSURE = float(entry8.get())
    def close():
        root.destroy()

#BUTTON----------------------------------------------------------------------------------------------------
    button1 = tk.Button(text='ENTER',
                        width=8,
                        height=4,
                        font=("Helvetica", 13),
                        fg='#0005FF',
                        bg='#F6FF00',
                        command=lambda: [get_chamber_pressure(), get_chamber_temperature(), get_altitude(),
                                         get_gamma(), get_gas_constant(), get_mach_number(), get_throat_radius(),
                                         get_exit_pressure(), close()]
                        )
    button1.place(x=800, y=150)
#GEOMETRY OF THE WINDOW AND DISPLAYING WINDOW---------------------------------
    root.geometry("1100x600")
    root.resizable(width=0, height=0)
    root.mainloop()

    #CODE_STARTS-------------------------------------------------------------------------------------------
    ASTAR = pi * THROAT_RADIUS * THROAT_RADIUS
    At, g, Pc, Tc, R = ALTITUDE, GAMMA, CHAMBER_PRESSURE, CHAMBER_TEMPERATURE, GAS_CONSTANT

    '''THE BELOW LINES ARE USED TO DETERMINE THE PRESSURE AND TEMP AT GIVEN ALTITUDE'''
    if 11000 > ALTITUDE < 25000:
        T_0 = -56.46
        PAMB = 1000 * (22.65 * exp(1.73 - 0.000157 * ALTITUDE))
    elif ALTITUDE >= 25000:
        T_0 = -131.21 + 0.00299 * ALTITUDE
        PAMB = 1000 * (2.488 * ((T_0 + 273.1) / 216.6) ** -11.388)
    else:
        T_0 = 15.04 - 0.00649 * ALTITUDE
        PAMB = 1000 * (101.29 * ((T_0 + 273.1) / 288.08) ** 5.256)
    P_0 = PAMB

#THEORITICAL CALCULATIONS-----------------------------------------------------------------------
    A = ASTAR * (((g + 1) / 2) ** (-((g + 1) / (2 * (g - 1))))) * (((1 + ((g - 1) / 2) * (M ** 2)) ** ((g + 1) / (2 * (g - 1)))) / M)
    print(f'A = {A}')
    print(f'EXIT_PRESSURE = {EXIT_PRESSURE}')
    Te = (EXIT_PRESSURE / Pc) ** ((g - 1) / g) * Tc
    print(f'Te = {Te}')
    Ve = M * sqrt(g * R * Te)
    print(f'Ve = {Ve}')
    Tt = (2 / (g + 1)) * Tc
    print(f'Tt = {Tt}')
    Pt = ((2 / (g + 1)) ** (g / (g - 1))) * Pc
    print(f'Pt = {Pt}')
    m = ((ASTAR * Pt) / sqrt(Tt)) * (sqrt(g / R)) * (((g + 1) / 2) ** (-(g + 1) / (2 * (g - 1))))
    print(f'm = {m}')
    F = (m * Ve) + ((EXIT_PRESSURE - P_0) * A)
    print(f'THEORITICAL THRUST VALUE : {F}(NEWTONS)')
    print()

    #CODE_CONTINUATION--------------------------------------------------------------------------------
    _PR_ = P_0 / CHAMBER_PRESSURE
    PR_2 = (P_0 / CHAMBER_PRESSURE) ** ((GAMMA - 1) / GAMMA)
    T_T = (2 * GAMMA * GAS_CONSTANT * CHAMBER_TEMPERATURE) / (GAMMA - 1)
    P_T = ((2 / (GAMMA + 1)) ** (GAMMA / (GAMMA - 1))) * 2.068
    V_T = sqrt((2 * GAMMA * GAS_CONSTANT * CHAMBER_TEMPERATURE) / (GAMMA + 1))
    V_E = sqrt(T_T * (1 - PR_2))
    T_E = CHAMBER_TEMPERATURE * (P_0 / CHAMBER_PRESSURE) ** ((GAMMA - 1) / GAMMA)
    A_E = sqrt(GAMMA * GAS_CONSTANT * T_E)
    M_e = V_E / A_E
    _RTOD_ = 180 / pi
    _DTOR_ = pi / 180
    _A_ = sqrt((GAMMA + 1) / (GAMMA - 1))
    _B_ = (GAMMA - 1) / (GAMMA + 1)
    V__PM = lambda x: _A_ * atan(sqrt(_B_ * (x ** 2 - 1))) - atan(sqrt(x ** 2 - 1))
    T_MAX = 0.5 * V__PM(M_e) * _RTOD_
    _DT_ = (90 - T_MAX) - round(90 - T_MAX)
    T_0, M, RR, LR, SL, P = [], [0.0000], [0.0000], [0.0000], [0.0000], [0.0000]
    T_0.append(_DT_ * _DTOR_)
    n = T_MAX * 2
    for m in range(1, int(n) + 1):
        T_0.append((_DT_ + m) * _DTOR_)
        X_INT = [1, 1.01 * M_e]
        _FUNC_ = lambda x: T_0[m] - V__PM(x)
        M.append(brentq(_FUNC_, X_INT[0], X_INT[1]))
        P.append(0 + THROAT_RADIUS * tan(T_0[m]))
        RR.append(-THROAT_RADIUS / P[m])
        LR.append(tan(T_0[m] + asin(1 / M[m])))
        SL.append(-RR[m])
    P.pop(0)
    l = len(P)
    for j in range(0, l):
        P1 = [0, THROAT_RADIUS]
        P2 = [P[j], 0]
        plot(P2, P1, 'k')
        xlabel('_CENTERLINE_')
        ylabel('_RADIUS_')
    LR.pop(0)
    SL.pop(0)
    RR.pop(0)
    F = RR[m - 1]
    x, y = [], []
    for c in range(0, len(P) - 1):
        x.append((THROAT_RADIUS + SL[c] * P[c]) / (SL[c] - F))
        y.append(F * x[c] + THROAT_RADIUS)
        X_P = [P[c], x[c]]
        Y_P = [0, y[c]]
        plot(X_P, Y_P, 'b')
    xw, yw, s, b = [], [], [], []
    _TM_ = T_MAX * _DTOR_
    xw.append((THROAT_RADIUS + SL[0] * P[0]) / (SL[0] - tan(_TM_)))
    yw.append(tan(_TM_) * xw[0] + THROAT_RADIUS)
    X_P2 = [P[0], xw[0]]
    Y_P2 = [P[1], yw[0]]
    plot(X_P2, Y_P2, 'g')
    _DTW_ = tan(_TM_) / (len(P) - 1)
    s.append(tan(_TM_))
    b.append(THROAT_RADIUS)
    for k in range(1, len(P) - 1):
        s.append(tan(_TM_) - (k) * _DTW_)
        b.append(yw[k - 1] - s[k] * xw[k - 1])
        xw.append((b[k] + SL[k] * P[k]) / (SL[k] - s[k]))
        yw.append(s[k] * xw[k] + b[k])
        X_P3 = [x[k], xw[k]]
        Y_P3 = [y[k], yw[k]]
        plot(X_P3, Y_P3, 'r')
    xf = (b[len(b) - 1] + SL[len(SL) - 1] * P[len(P) - 1]) / SL[len(SL) - 1]
    yf = b[len(b) - 1]
    X_F = [P[len(P) - 1], xf]
    Y_F = [0, yf]
    plot(X_F, Y_F, 'r')
    xw = [0] + xw
    yw = [THROAT_RADIUS] + yw
    RTHROAT = THROAT_RADIUS
    REXIT = yw[len(yw) - 1]
    AR = (RTHROAT / REXIT) ** 2
#-------------------------------CODE COMPLETION -----------------------------------------------

#OUTPUTS----------------------------------------------------------------------------------------
    print('_ASPECT RATIO_ :', AR)
    print()
    print('YOUR EXCEL SHEET WITH COORDINATES HAS BEEN GENERATED.\nFILE NAME : "nozzlepts.xls".')
    print()
    print('CLOSE THE PLOT AND OPEN THE RESPECTIVE EXCEL SHEET.')
    print()
    savefig('NOZZLE_CONTOUR.png', dpi=300, bbox_inches='tight')
    show()

#TO VISUALIZE BELL NOZZLE IN 2D---------------------------------------------------------------
    throat_radius = THROAT_RADIUS
    x_coordinates, y_coordinates = xw, yw
    vertical_distance = -(y_coordinates[-1] - throat_radius)
    upper_curve_points = []
    distance_per_step = abs(vertical_distance / 30)
    step_count = 0
    current_point_location = vertical_distance
    while True:
        if step_count == 30:
            break
        upper_curve_points.append(current_point_location)
        current_point_location += distance_per_step
        step_count += 1
    
    exit_diameter = y_coordinates[-1]
    lower_curve_points = []
    step_count = 0
    distance_per_step = (exit_diameter - throat_radius) / 30
    current_point_location = exit_diameter
    while True:
        if step_count == 30:
            break
        lower_curve_points.append(current_point_location)
        current_point_location -= distance_per_step
        step_count += 1
    
    x_coordinates = upper_curve_points + x_coordinates
    y_coordinates = lower_curve_points + y_coordinates
    
    additional_points = []
    current_x_coordinate = x_coordinates[0]
    step_size = abs((2.5 * x_coordinates[0]) / 20)
    while current_x_coordinate > -(abs(2.5 * x_coordinates[0])):
        additional_points.insert(0, current_x_coordinate)
        current_x_coordinate -= step_size
    additional_y_coordinates = [y_coordinates[0]] * len(additional_points)
    x_coordinates = additional_points + x_coordinates
    y_coordinates = additional_y_coordinates + y_coordinates
    
    color_palette = ['#151B54', '#000080', '#0000A0', '#0020C0', '#0041C2', '#2554C7', '#1569C7', '#488AC7', '#659EC7', '#87AFC7'
            , '#F75D59', '#E55451', '#FF2400', '#FF0000', '#F70D1A', '#F70D1A', '#F70D1A', '#F70D1A', '#F70D1A']
    
    plot(x_coordinates, y_coordinates, color='black', linewidth=10)
    z_coordinates, v_coordinates = np.array(x_coordinates), np.array(y_coordinates)
    plot(z_coordinates, -v_coordinates, color='black', linewidth=10)
    
    #SCATTER_PLOT --------------------------------------------------------------------
    color_count = ceil(len(y_coordinates) / len(color_palette))
    color_index = 0
    x_range = len(list(range(ceil(x_coordinates[0]), floor(x_coordinates[-1]) + 1)))
    for i in range(len(x_coordinates)):
        x_values = []
        y_values = []
        positive_y = -y_coordinates[i]
        negative_y = y_coordinates[i]
        step_size = ((abs(positive_y) + abs(negative_y)) / 100) * 1
        while positive_y <= negative_y:
            y_values.append(positive_y)
            positive_y += step_size
        x_values = [x_coordinates[i]] * len(y_values)
        scatter(x_values, y_values, color=color_palette[color_index], marker='_', s=y_coordinates[-1] * 2)
        if i % color_count == 0:
            color_index += 1
        if color_index >= len(color_palette):
            color_index = len(color_palette) - 1
    
    xlim([x_coordinates[0], x_coordinates[-1] + (x_coordinates[-1] / 100) * 5])
    ylim([-(y_coordinates[-1]) - ((y_coordinates[-1] / 100) * 5), (y_coordinates[-1]) + ((y_coordinates[-1] / 100) * 5)])
    title('***BELL NOZZLE CONTOUR***')
    xlabel('*LENGTH OF THE NOZZLE*')
    ylabel('*DIAMETER OF THE NOZZLE*')
    tight_layout()
#SAVING THE IMAGE---------------------------------------------------------------------------------------
    savefig('2D_Nozzle_Visualisation.png', dpi=300, bbox_inches='tight')
    show()

#EXPORTING COORDINATES TO EXCEL SHEET--------------------------------------------------
    wb = Workbook()
    sheet1 = wb.add_sheet('points')
    '''xw.insert(0,-(y[-1]-throat))
    yw.insert(0,y[-1])
    xw.insert(0,-80)
    yw.insert(0,y[-1])'''

#CONVERGENT SECTION COORDINATES--------------------------------------------------------
    print()
    print('CONVERGENT SECTION COORDINATES!')
    print()
    print(f'X_coordinate = (0,{-(y[-1]-throat)})')
    print()
    print(f'Y_coordinate = (0,{y[-1]})')
    print()
    for i in range(len(x_coordinates)):
        sheet1.write(i, 0, x_coordinates[i])
        sheet1.write(i, 1, y_coordinates[i])
        sheet1.write(i, 2, 0)
    wb.save('nozzlepts.xls')
except NameError:
    pass
except:
    print('INVALID INPUT!')
    print('TRY AGAIN!')

''' THE POINTS GENERATED WILL BE STORED IN THE EXCEL SHEET('nozzlepts.xls')

----------------------------------------------------END-------------------------------------------------------- '''
