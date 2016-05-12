#!/bin/bash
files=(Prog1_Sorting.txt Prog2_Extra_Call_By_Value.txt Prog3_Extra_Call_By_Reference.txt Prog4_Extra_Recursion.txt Prog6_Extra_Static_Scope.txt Prog7_Extra_Matrices.txt)
for var in ${files[@]}
do
    echo $var
    echo
    echo "SOURCE:"
    echo
    cat $var
    echo
    echo "SOURCE WITH 4 TUPLES:"
    echo
    ./Main.py $var
    echo
    echo "ASSEMBLER LISTINGS WITH 4 TUPLES:"
    echo
    cat ${var%.*}.asm
    nasm -g -f elf32 ${var%.*}.asm
    gcc -g -m32 -o ${var%.*} ${var%.*}.o
    echo
    echo "OUTPUT:"
    echo
    ./${var%.*}
    echo
    echo
    echo
done
