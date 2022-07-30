#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: ZhixinLing
# email: 1069066484@qq.com
import shutil
import os


class Basis:
    """
    Class Basis wraps some C++ basis functions into Python via system calls.
    Note that there must have been a compiled executable Basis binary file.
    """
    def __init__(self,
                 bin_file=r"D:\fduStudy\labZXD\repos\gView\basis\basis_universal\bin\Release\basisu.exe",
                 out=print,
                 valid_im_formats=["png", "jpg", "jpeg"],
                 decompressed_format="png"
                 ):
        """
        :param bin_file: an executable binary file (postfixed by .exe on Windows)
        :param out: output stream
        :param valid_im_formats: valid image formats
        :param decompressed_format: target decompressed format
        """
        self.out = out
        if self.out is None:
            self.out = lambda x: x
        if not os.path.exists(bin_file):
            self.out("warning: basis binary file is not found in {}. Basis format is not supported".format(bin_file))
        else:
            self.out("Find bin file in {}".format(bin_file))
        self.bin_file = os.path.abspath(bin_file)
        self.valid_im_formats = valid_im_formats
        self.decompressed_format = decompressed_format

    def compress(self, im_paths=[], oneByOne=True):
        """
        compress a series of image files
        :param im_paths: a list of image files
        :param oneByOne: process these images one-by-one or once-for-all.
                        In some cases, once-for-all processing might fail.
                        However, once-for-all processing is more efficient.
        """
        if not oneByOne:
            os.system("{} {}".format(self.bin_file, im_paths))
        else:
            for f in im_paths:
                os.system("{} {}".format(self.bin_file, f))

    def decompress(self, basis_paths=[]):
        """
        decompress a series of .basis files
        :param basis_paths: a series of basis-compressed or jpeg files.
                            If there is an basis-compressed file, it would be decompressed into .jpg format.
                            Otherwise, it remains unprocessed.
        """
        ret_fns = []
        # _unpacked_rgb_ETC1_RGB_0000.png
        for p in basis_paths:
            # p = os.path.abspath(p)
            if not p.endswith(".basis"):
                self.out("{} is not a basis file, skip decompressing".format(p))
                if os.path.splitext(p)[-1][1:].lower() in self.valid_im_formats:
                    ret_fns.append(p)
                else:
                    self.out("{} is found to have an unknown postfix, skip".format(p))
            else:
                # no_ktx: we do not need ktx file output
                # etc1_only: only etc1 file is required
                cmd = "{} -no_ktx -etc1_only {}".format(self.bin_file, p)
                ret_sys = os.system(cmd)
                # print("ret_sys = {}".format(ret_sys))

                dst_fn = os.path.splitext(p)[0] + ".{}".format(self.decompressed_format)
                fn_ori = os.path.splitext(p)[0].split("/")[-1].split("\\")[-1]  +\
                         "_unpacked_rgb_ETC1_RGB_0000.png"
                shutil.copy(fn_ori, dst_fn)
                # fn_ori = os.path.abspath(fn_ori)
                self.out("run '{}'. Get file from {} to {}.".format(cmd, fn_ori ,dst_fn))
                # print("{} -no_ktx -etc1_only {} -output_file {}".format(self.bin_file, p, os.path.splitext(p)[0] + ".png"))
                ret_fns.append(dst_fn)
                # ret_fns.append(os.path.splitext(p)[0] + "_unpacked_rgb_ETC1_RGB_0000.png")
        return ret_fns


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
