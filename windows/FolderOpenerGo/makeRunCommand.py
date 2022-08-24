#!/usr/bin/env python3

LIMIT=3

for i in range(1, LIMIT+1):
    if i != LIMIT:
        print("  if cmd_array_len == " + f"{i}" + " {")

    print("    return exec.Command(", end="")
    for j in range(0, i):
        print(f"cmd_array[{j}]", end="")
        if j == i -1 :
            print(")")
        else:
            print(", ", end="")


    # print("")
    if i != LIMIT:
        print("  }")

    print("")
