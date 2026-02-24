import hashlib
import io
import pycdlib
import tempfile
import tkinter as tk, tkinter.filedialog
import traceback
import shutil

import consts

iso = pycdlib.PyCdlib()

def _md5_check(file):
    print("Confirming MD5")
    md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5.update(chunk)
    return md5.hexdigest()

def _handle(file_path, tmpdir):
    print("Copying file into temp")
    shutil.copyfile(file_path, tmpdir + "/SPYROAHT.iso")

    iso.open(tmpdir + "/SPYROAHT.iso", mode="rb+")

    outfile = io.BytesIO()
    try:
        iso.get_file_from_iso_fp(outfile, iso_path=f'/{consts.IDN};1')
    except pycdlib.pycdlibexception.PyCdlibInvalidInput:
        raise ValueError("Invalid ISO selected or file not found")

    for addr, cur, over in consts.NOP_ADDR:
        print(f'Modifying {addr:x}')
        outfile.seek(addr)
        b = outfile.read(4)
        if b != cur:
            raise ValueError(f"Unexpected op code at address {addr:x}, expected {cur}, got {b}")
        outfile.seek(addr)
        outfile.write(over)
    outfile.seek(0)
    print("Writing result")
    iso.modify_file_in_place(outfile, len(outfile.getvalue()), f'/{consts.IDN};1')

    saveas = tk.filedialog.asksaveasfilename(title="Save ISO file", filetypes=[("ISO file", "*.iso")], defaultextension=".iso")

    iso.write(saveas)

def main():

    root = tk.Tk()
    root.withdraw()
    file_path = tk.filedialog.askopenfilename(title="Select ISO file", filetypes=[('ISO file', '*.iso')])
    if not file_path:
        return

    md5 = _md5_check(file_path)
    if md5 != consts.MD5:
        raise ValueError("MD5 checksum does not match")

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            _handle(file_path, tmpdir)
        except Exception:
            traceback.print_exc()
        finally:
            iso.close()


if __name__ == '__main__':
    main()