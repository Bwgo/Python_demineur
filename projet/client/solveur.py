# -*- coding: utf-8 -*-

from typing import List, Tuple
import clauses
import subprocess
import clauses

voc = {'land': 0, 'sea': 1, 'tiger': 2, 'shark': 3 , 'croco': 4}

def write_dimacs_file(dimacs: str, filename: str):
    with open(filename, "w", newline="") as cnf:
        cnf.write(dimacs)


def exec_gophersat(filename: str, cmd: str = "gophersat-1.1.6.exe", encoding: str = "utf8") -> bool:
    result = subprocess.run([cmd, filename], capture_output=True, check=True, encoding=encoding)
    string = str(result.stdout)
    lines = string.splitlines()

    if lines[1] != "s SATISFIABLE":
        return False

    return True


def clauses_to_dimacs(clauses: List[List[int]], nb_vars: int) -> str:
    textDimacs = ""
    textDimacs += "p cnf "+str(nb_vars)+" "+str(len(clauses))+"\n"
    for i in clauses:
        if (isinstance(i, int)):
             textDimacs += str(i)+" "           
        else:
            for j in range(len(i)):
                textDimacs += str(i[j])+" "
        textDimacs += "0\n"
    return textDimacs


def solve(problemClauses: list, height: int, width: int):
    dimacs = clauses_to_dimacs(problemClauses, height*width*5)
    write_dimacs_file(dimacs, "demineur.cnf")
    return exec_gophersat("demineur.cnf")

