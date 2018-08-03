import xml.etree.ElementTree as ET
from shutil import copyfile
from petrinet import *
import sys
import os


# get name of xml-file as command line argument and strip the .xml ending
if len(sys.argv) < 2:
    print("Please specify the xml file name of a network service specification inside the 'xml-files' folder (e.g., 'syncTrans.xml')")
    exit(1)
xml_name = sys.argv[1][:-4]			# cut off .xml file ending
# xml_name = "syncTrans"


# create a new folder for the auto-compiled Omnet++ files, copying the base-files from "omnet-base"
def create_project():
    # create new directory (if it doesn't exist yet)
    directory = "autogen/" + name
    print(f"Creating folder {directory} and copying Omnet basefiles")
    os.makedirs(directory, exist_ok=True)
    os.makedirs(directory + "/images", exist_ok=True)

    # copy omnet base files
    for f in os.listdir("omnet-base"):
        if f != "images":
            copyfile("omnet-base/" + f, directory + "/" + f)
    for f in os.listdir("omnet-base/images"):
        copyfile("omnet-base/images/" + f, directory + "/images/" + f)


# parse xml and store Petri net elements in dicts
def parse_xml():
    print(f"Parsing {xml_name}.xml")
    prefix = "{http://pdv.cs.tu-berlin.de/TimeNET/schema/SCPN}"		# TimeNet 4.4's xml-prefix
    root = ET.parse(f"xml-files/{xml_name}.xml").getroot()
    id2node = {}

    for p in root.iter(prefix + "place"):
        place = Place(p.get("id"), p.find(prefix + "label").get("text"))
        places.append(place)
        id2node[p.get("id")] = place

    for t in root.iter(prefix + "timedTransition"):
        trans = TimedTransition(t.get("id"), t.find(prefix + "label").get("text"), t.get("timeFunction"))
        timed_transitions.append(trans)
        id2node[t.get("id")] = trans

    for it in root.iter(prefix + "immediateTransition"):
        trans = ImmediateTransition(it.get("id"), it.find(prefix + "label").get("text"), it.get("weight"))
        immediate_transitions.append(trans)
        id2node[it.get("id")] = trans

    for a in root.iter(prefix + "arc"):
        src = id2node[a.get("fromNode")]
        dest = id2node[a.get("toNode")]
        arc = Arc(src.name, dest.name, a.find(prefix + "inscription").get("text"))
        arcs.append(arc)
        # add ref to arc at src and dest
        src.out_arcs.append(arc)
        dest.in_arcs.append(arc)
        # if source=Place and dest=immediateTransition, add weights of immediateTransition
        if isinstance(src, Place) and isinstance(dest, ImmediateTransition):
            src.probabilities.append(dest.weight)


# create new .ned-network
def write_ned():
    print(f"Writing to {name}.ned")
    indent = "    "
    with open(f"autogen/{name}/{name}.ned", "w") as ned:
        ned.write(f"network {name} {{\n")
        ned.write(indent + "submodules:\n")
        for p in places:
            ned.write(2*indent + f"{p.name}: Place;\n")
        for t in timed_transitions:
            ned.write(2*indent + f"{t.name}: Transition;\n")
        for it in immediate_transitions:
            ned.write(2*indent + f"{it.name}: ImmTrans;\n")

        ned.write(indent + "connections:\n")
        for a in arcs:
            ned.write(2*indent + f"{a.src}.out++ --> {{ delay = 0ms; }} --> {a.dest}.in++;\n")
        ned.write("}")


# write simple omnetpp.ini with configuration of transitions
def write_ini():
    print(f"Writing omnetpp.ini")
    with open(f"autogen/{name}/omnetpp.ini", "w") as ini:
        ini.write("[General]\n\n")
        ini.write(f"[Config {name}]\n")
        ini.write(f"network = {name}\n")
        for p in places:
            if p.probabilities:
                ini.write(f'{name}.{p.name}.probabilities = "{p.str_probabilities()}"\n')
        for t in timed_transitions:
            ini.write(f"{name}.{t.name}.rate = {t.timing}\n")
            ini.write(f'{name}.{t.name}.coeffs = "{t.coeffs()}"\n')
        for it in immediate_transitions:
            ini.write(f'{name}.{it.name}.coeffs = "{it.coeffs()}"\n')


name = xml_name.capitalize() + "Auto"
places, timed_transitions, immediate_transitions, arcs = [], [], [], []

create_project()
parse_xml()
write_ned()
write_ini()
