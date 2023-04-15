import numpy as np
import colours

if __name__ == '__main__':
    count = 0
    for r in range(256):
        for g in range(256):
            rgb = np.zeros([256, 3])

            rgb[:, 0] = np.ones(256) * r
            rgb[:, 1] = np.ones(256) * g
            rgb[:, 2] = np.arange(256)

            xyz = colours.SRGB.to_xyz(rgb)
            csp = colours.OKLAB.from_xyz(xyz)
            xyz = colours.OKLAB.to_xyz(csp)
            rgb2 = colours.SRGB.from_xyz(xyz)

            try:
                assert np.allclose(rgb, rgb2)
            except:
                print("Didn't match at", count)

                print(rgb2)

                exit()
                # print(rgb2)

            count += 1

            # print(count)
