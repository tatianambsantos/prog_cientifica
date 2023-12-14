import json
import numpy as np
import matplotlib.pyplot as plt

def read_json(file):
    print(".read")
    with open(file, "r") as f:
        data = json.load(f)
        if "coords" in data:
            ne = len(data["coords"])
            x0 = np.zeros(ne)
            y0 = np.zeros(ne)
            for i in range(ne):
                x0[i] = float(data["coords"][i][0])
                y0[i] = float(data["coords"][i][1])
            return ne, x0, y0

def output_res(res):
    output_dict = {"resultado": res.tolist()}
    with open("/home/tatiana/Prog_Cientifica/modelador_grafico/output.json", "w") as f:
        json.dump(output_dict, f)

def main(file):
    print(".DEM")
    # read input file
    N = 600
    h = 0.00004
    ne, x0, y0 = read_json(file)
    ndofs = 2 * ne
    raio = 1.0
    mass = 7850.0
    kspr = 210000000000.0
    conect = np.array([
        [2, 2, 4, 0, 0],
        [3, 1, 3, 5, 0],
        [2, 2, 6, 0, 0],
        [3, 5, 1, 7, 0],
        [4, 4, 6, 2, 8],
        [3, 5, 3, 9, 0],
        [3, 8, 4, 10, 0],
        [4, 7, 9, 5, 11],
        [3, 8, 6, 12, 0],
        [3, 11, 7, 13, 0],
        [4, 10, 12, 8, 14],
        [3, 11, 9, 15, 0],
        [3, 14, 10, 16, 0],
        [4, 13, 15, 11, 17],
        [3, 14, 12, 17, 0],
        [2, 17, 13, 0, 0],
        [3, 16, 17, 14, 0],
        [2, 17, 15, 0, 0]
    ])
    F = np.array([
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [0.0, 0.0],
        [-1000.0, 0.0],
        [-1000.0, 0.0],
        [-1000.0, 0.0]
    ])
    restrs = np.array([
        [1, 1],
        [1, 1],
        [1, 1],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0]
    ])
    F = F.reshape((ndofs, 1))
    restrs = restrs.reshape((ndofs, 1))
    F_list = F.tolist()
    restrs_list = restrs.tolist()

    print("ne:", ne)
    # print("x0:", x0)
    # print("y0:", y0)
    # print("conect:", conect)
    print("F:", F_list)
    # print("restrs:", restrs)

    u = np.zeros((ndofs, 1))
    v = np.zeros((ndofs, 1))
    a = np.zeros((ndofs, 1))
    res = np.zeros(N)

    fi = np.zeros((ndofs, 1))


    a[:] = (F - fi) / mass
    for i in range(N):

        v += a * (0.5 * h)
        
        u += v * h
        # contato
        fi[:] = 0.0
        for j in range(ne):
            if restrs[2 * j] == 1:

                u[2 * j] = 0.0
            if restrs[2 * j + 1] == 1:
                u[2 *j +1] = 0.0
            xj = x0[j] + u[2 * j]
            yj = y0[j] + u[2 * j + 1]
            #percorre os elementos da conect na linha j, na quantidade de elementos nos quais estão conectados, info na pos[0]
            for index in range(conect[j, 0]):
                k = conect[j, index+1]
                xk = x0[k-1] + u[2 * k]
                yk = y0[k-1] + u[2 * k-1]
                dX = xj - xk
                dY = yj - yk
                di = np.sqrt(dX * dX + dY * dY)
                if dX ==0 and dY==0:
                    print(dX, dY)
                d2 = (di - 2 * raio)
                if di != 0:
                    dx = d2 * dX / di
                    dy = d2 * dY / di
                else:
                    dx = 0
                    dy = 0
                fi[2 * j] += kspr * dx
                fi[2 * j+1] += kspr * dy
        a[:] = (F - fi) / mass
        v += a * (0.5 * h)
        # plot
        res[i] = u[33]
    output_res(res)
    x = np.arange(1, N + 1)
    plt.plot(x, res)
    plt.show()

if __name__ == "__main__":
    main("/home/tatiana/Prog_Cientifica/modelador_grafico/input.json")
