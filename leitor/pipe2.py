"""."""
from os import system
instancias = [
    "albano.svg",
    "blaz1.svg",
    "blaz2.svg",
    "blaz3.svg",
    "dighe1.svg",
    "dighe2.svg",
    "fu.svg",
    "instance_01_2pol.svg",
    "instance_01_3pol.svg",
    "instance_01_4pol.svg",
    "instance_01_5pol.svg",
    "instance_01_6pol.svg",
    "instance_01_7pol.svg",
    "instance_01_8pol.svg",
    "instance_01_9pol.svg",
    "instance_01_10pol.svg",
    "instance_01_16pol.svg",
    "instance_artificial_01_26pol_hole.svg",
    "rco1.svg",
    "rco2.svg",
    "rco3.svg",
    "shapes2.svg",
    "shapes4.svg",
    "spfc_instance.svg",
    "trousers.svg",
]
txt = ''
for i in instancias:
    system(f"echo '\n{i}'")
    system(f"""
    python pipe.py < ../grafos_svg/EJOR/packing/{i}
    """)
    # system(f"""
    # python pipe.py < ../grafos_svg/EJOR/packing/{i} >
    # ../datasets/particao_arestas/ejor/packing/{i.split(".")[0]}.txt
    # """)
    system(f'echo "\nseparado {i.split(".")[0]}.txt"')
    system(f"""
    python pipe.py < ../grafos_svg/EJOR/separated/{i.split(".")[0]}_sep.svg
    """)
    # system(f"""
    # python pipe.py < ../grafos_svg/EJOR/separated/{i.split(".")[0]}_sep.svg >
    # ../datasets/particao_arestas/ejor/separated/{i.split(".")[0]}.txt
    # """)
