# D:\fduStudy\labZXD\repos\gView\basis\basis_universal\bin\Release\basisu.exe ex1.basis -no_ktx -etc1_only
# D:\fduStudy\labZXD\repos\gView\basis\basis_universal\bin\Release\basisu.exe VID_20200703_161943_00_010_000321.jpg


import os


class Basis:
    def __init__(self, bin_file=r"D:\fduStudy\labZXD\repos\gView\basis\basis_universal\bin\Release\basisu.exe"):
        """
        :param bin_file: an executable binary file (postfixed by .exe on Windows)
        """
        assert os.path.exists(bin_file)
        self.bin_file = bin_file

    def compress(self, im_paths=[], oneByOne=True):
        if not oneByOne:
            os.system("{} {}".format(self.bin_file, im_paths))
        else:
            for f in im_paths:
                os.system("{} {}".format(self.bin_file, f))

    def decompress(self, basis_paths=[]):
        for p in basis_paths:
            os.system("{} -no_ktx -etc1_only {}".format(self.bin_file, p))


def _test():
    basis = Basis(r"D:\fduStudy\labZXD\repos\gView\basis\basis_universal\bin\Release\basisu.exe")
    c_folder = r"D:\fduStudy\labZXD\repos\gView\PANORAMA"
    basis.compress(
        [os.path.join(c_folder, p) for p in os.listdir(c_folder) if p.endswith(".jpg")]
    )
    d_folder = r"D:\fduStudy\labZXD\repos\gView\compress"
    basis.decompress(
        [os.path.join(d_folder, p) for p in os.listdir(d_folder) if p.endswith(".basis")]
    )


if __name__=="__main__":
    _test()
