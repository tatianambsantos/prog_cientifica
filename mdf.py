import json
import numpy as np
import matplotlib.pyplot as plt


# A função cria uma matriz A que representa o sistema linear de equações resultante do método dos diferenciais finitos. 
# Os elementos dessa matriz dependem das condições de contorno e conectividade da malha. Em seguida, a função resolve esse 
# sistema linear usando a função np.linalg.solve do NumPy e retorna a solução 

def function_mdf(N, connect, cc):
    A = np.zeros((N, N))
    b = np.zeros((N, 1))

    for i in range(len(b)):
        if cc[i][0] == 1:
            b[i] = cc[i][1]    


    for i in range(len(connect)):
        if cc[i][0] == 0:
            if connect[i][0] != 0:
                A[i][connect[i][0]-1] = 1
            if connect[i][1] != 0:
                A[i][connect[i][1]-1] = 1
            if connect[i][2] != 0:
                A[i][connect[i][2]-1] = 1
            if connect[i][3] != 0:
                A[i][connect[i][3]-1] = 1
            if connect[i][4] != 0:
                A[i][connect[i][4]-1] = -4
        else:
            A[i][i] = 1


    T = np.linalg.solve(A,b)


    print(T)

    return (T)

# A função lê o arquivo JSON fornecido (_file) e extrai as informações necessárias para o método dos diferenciais finitos. 
# Retorna as informações relevantes como ne (número de elementos), connect (conectividade entre os elementos) e cc (condições de contorno).

def function_readJSON(_file):
    print(".read")
    with open(_file, "r") as f:
        data = json.load(f)

    if "connection_map" in data and "cc" in data:
        N = len(data["connection_map"])

        connect = np.zeros((N, 5), dtype=int)
        cc = np.zeros((N, 2), dtype=float)

        for i in range(N):
            for j in range(5):
                connect[i, j] = int(data["connection_map"][i][j])

            for k in range(2):
                cc[i, k] = float(data["cc"][i][k])

        return N, connect, cc

# ne: Número de elementos na malha.
# connect: Matriz que descreve a conectividade entre os elementos da malha.
# cc: Matriz que contém as condições de contorno.

N, connect, cc = function_readJSON("teste.json")
y = function_mdf(N, connect, cc)


x = np.arange(1, len(y) + 1)

plt.plot(x, y, label="MDF")
plt.title("Variação de Temperatura")
plt.ylabel("Temperatura °C")
plt.xlabel("Pontos")
plt.legend()
plt.show()