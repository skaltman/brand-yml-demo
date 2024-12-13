import yaml
import tempfile
import os
import matplotlib.pyplot as plt

def mplstyle_from_brand(brand_file):
    brand = yaml.safe_load(brand_file.read())
    fd, name = tempfile.mkstemp("mplstyle")
    os.close(fd)
    with open(name, "w") as out:
        out.write("axes.facecolor: \"%s\"\n" % brand["color"]["palette"]["neutral"])
        out.write("axes.edgecolor: \"%s\"\n" % brand["color"]["palette"]["black"])
        out.write("axes.labelcolor: \"%s\"\n" % brand["color"]["palette"]["black"])
        out.write("axes.titlecolor: \"%s\"\n" % brand["color"]["palette"]["black"])
        out.write("figure.facecolor: \"%s\"\n" % brand["color"]["palette"]["neutral"])
        out.write("figure.edgecolor: \"%s\"\n" % brand["color"]["palette"]["black"])
        out.write("text.color: \"%s\"\n" % brand["color"]["palette"]["black"])
        out.write("xtick.color: \"%s\"\n" % brand["color"]["palette"]["black"])
        out.write("ytick.color: \"%s\"\n" % brand["color"]["palette"]["black"])

        colors = [brand["color"]["palette"]["violet"], brand["color"]["palette"]["red"], 'g']
        colors = [s.lstrip('#') for s in colors]
        out.write("axes.prop_cycle: cycler(color=[%s])\n" % ", ".join([f"'{color}'" for color in colors]))
    plt.style.use(name)
    os.unlink(name)
