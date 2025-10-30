# -*- coding: utf-8 -*-
"""
Created on Thu Oct 16 17:12:48 2025

@author: OMARS
"""
"""Práctica 3

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Lugo Valenzuela Liliana Fernanda
Número de control: 21212165
Correo institucional: l21212165@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Librerías necesarias
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0, t0, tF, dt, w, h = 0, 0, 10, 1E-3, 6, 3
N = round((tF - t0) / dt) + 1
t = np.linspace(t0, tF, N)
u = np.zeros(N)
u[round(1 / dt):round(2 / dt)] = 1  # Impulso

# Colores personalizados
mycolors = np.array([
    [1.000, 0.902, 0.902],
    [0.882, 0.686, 0.820],
    [0.678, 0.533, 0.776],
    [0.455, 0.412, 0.714],
    [0.392, 0.498, 0.737],
    [0.568, 0.678, 0.784]
])

# Componentes del modelo eléctrico (control)
a = 0.25
R = 100
L = 22E-6
Cs = 10E-6
Cp = 100E-6
numControl = [R * Cs, 1 - a]
denControl = [R * (Cp + Cs), 1]
sysControl = ctrl.tf(numControl, denControl)
print(sysControl)

# Componentes del modelo eléctrico (caso)
R = 10E3
numCaso = [R * Cs, 1 - a]
denCaso = [R * (Cp + Cs), 1]
sysCaso = ctrl.tf(numCaso, denCaso)
print(sysCaso)

# Componentes del controlador
Rr = 716.59
Re = 443.08
Cr = 1E-6
Ce = 0
numPID = [-Rr * Cr, 1]
denPID = [Re * Cr, 0]
PID = ctrl.tf(numPID, denPID)
print(PID)

# Sistema de control en lazo cerrado
X = ctrl.series(PID, sysCaso)
sysPID = ctrl.feedback(X, 1, sign=-1)
print(sysPID)
sysTratamiento = ctrl.series(sysControl, sysPID)

# =====================================================
# Función para graficar con y sin tratamiento
# =====================================================
def plotsignals(u, sysControl, sysCaso, sysTratamiento):
    # ---------- FIGURA 1: Con tratamiento (lazo cerrado) ----------
    fig1 = plt.figure()
    plt.plot(t, u, '-', color=mycolors[0], label='$F(t)$')

    ts, PAx = ctrl.forced_response(sysControl, t, u, x0)
    plt.plot(t, PAx, '-', color=mycolors[1], label='$F_{sx}$')

    ts, PAy = ctrl.forced_response(sysCaso, t, u, x0)
    plt.plot(t, PAy, '-', color=mycolors[2], label='$F_{sy}(t)$')

    ts, PAz = ctrl.forced_response(sysTratamiento, t, u, x0)
    plt.plot(t, PAz, ':', linewidth=3, color=mycolors[3], label='$F_{sz}$')

    plt.grid(False)
    plt.xlim(0, 10); plt.xticks(np.arange(0,1,10))
    plt.ylim(0, 1.1); plt.yticks(np.arange(0,1.2,0.1))
    plt.xlabel('$t$ [s]', fontsize=11)
    plt.ylabel('$V_i(t)$ [V]', fontsize=11)
    plt.title('Respuesta con tratamiento (lazo cerrado)')
    plt.legend(bbox_to_anchor=(0.5, -0.35), loc='center', ncol=4, fontsize=8, frameon=False)

    fig1.set_size_inches(w, h)
    fig1.tight_layout()
    fig1.savefig('SistemaMusculoesquelético_LazoCerrado.png', dpi=600, bbox_inches='tight')
    plt.show()

    # ---------- FIGURA 2: Sin tratamiento (lazo abierto) ----------
    fig2 = plt.figure()
    plt.plot(t, u, '-', color=mycolors[0], label='$F(t)$')

    ts, PAx = ctrl.forced_response(sysControl, t, u, x0)
    plt.plot(t, PAx, '-', color=mycolors[1], label='$F_{sx}$')

    ts, PAy = ctrl.forced_response(sysCaso, t, u, x0)
    plt.plot(t, PAy, '-', color=mycolors[2], label='$F_{sy}(t)$')

    plt.grid(False)
    plt.xlim(0, 10); plt.xticks(np.arange(0,1,10))
    plt.ylim(0, 1.1); plt.yticks(np.arange(0,1.2,0.1))
    plt.xlabel('$t$ [s]', fontsize=11)
    plt.ylabel('$V_i(t)$ [V]', fontsize=11)
    plt.title('Respuesta sin tratamiento (lazo abierto)')
    plt.legend(bbox_to_anchor=(0.5, -0.35), loc='center', ncol=3, fontsize=8, frameon=False)

    fig2.set_size_inches(w, h)
    fig2.tight_layout()
    fig2.savefig('SistemaMusculoesquelético_LazoAbierto.png', dpi=600, bbox_inches='tight')
    plt.show()

# =====================================================
# Ejecución de ambas gráficas
# =====================================================
plotsignals(u, sysControl, sysCaso, sysTratamiento)



