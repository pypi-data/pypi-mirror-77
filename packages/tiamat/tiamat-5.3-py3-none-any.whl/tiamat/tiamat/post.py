# Import python libs
import os
import shutil


def report(hub, bname):
    opts = hub.tiamat.BUILDS[bname]
    art = os.path.join("dist", opts["name"])
    print(f"Executable created in {art}")


def clean(hub, bname):
    opts = hub.tiamat.BUILDS[bname]
    shutil.rmtree(opts["venv_dir"])
    os.remove(opts["spec"])
    os.remove(opts["req"])
    try:
        # try to remove pyinstaller warn-*** file
        os.remove(
            os.path.join(
                opts["dir"], "build", opts["name"], "warn-{}.txt".format(opts["name"])
            )
        )
    except FileNotFoundError:
        pass
