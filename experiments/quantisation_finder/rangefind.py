import numpy as np
import colours

if __name__ == '__main__':
    max_l = []
    max_m = []
    max_s = []

    min_l = []
    min_m = []
    min_s = []

    count = 0
    for r in range(256):
        for g in range(256):
            rgb = np.zeros([256, 3])

            rgb[:, 0] = np.ones(256) * r
            rgb[:, 1] = np.ones(256) * g
            rgb[:, 2] = np.arange(256)

            xyz = colours.SRGB.to_xyz(rgb)
            csp = colours.OKLAB.from_xyz(xyz)

            l = csp[:, 0]
            m = csp[:, 1]
            s = csp[:, 2]

            max_l.append(np.max(l))
            max_m.append(np.max(m))
            max_s.append(np.max(s))

            min_l.append(np.min(l))
            min_m.append(np.min(m))
            min_s.append(np.min(s))

            count += 1

            print(count)

    print(min(min_l), min(min_m), min(min_s))
    print(max(max_l), max(max_m), max(max_s))


    print(max(max_l) - min(min_l))
    print(max(max_m) - min(min_m))
    print(max(max_s) - min(min_s))