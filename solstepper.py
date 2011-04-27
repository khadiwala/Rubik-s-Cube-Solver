from cube import cube
from solver import solver

cb = solver()
done = False
while(not done):
    ms = raw_input("Scramble String: ")
    ms = ms.upper()
    done = True
    for c in ms:
        done = (done and
        ((c in cb.sides) or (c in ['2','3']) or (c == "'")))
    if not done:
        print "You used an invalid character"

cb.do_string(ms)
cb.solve()
disp = cube()
disp.do_string(ms)

print "Initial cube state:"
disp.print_cube()
for step in cb.solmoves:
    raw_input("next move is: " + step)
    disp.do_string(step)
    disp.print_cube()
