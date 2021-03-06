
import ivy.ivy_module as ivy_module
from ivy.ivy_compiler import ivy_from_string
from ivy.tk_ui import new_ui
import ivy.ivy_utils as iu

prog = """#lang ivy1

type client
type server

relation c(X : client,Y : server)
relation s(X : server)

init (s(W) & ~c(X,Y))
individual x : client,y : server,z : client

derived foo(X:client,Y:server) = c(X,Y) & ~s(Y)

action connect = {
  x := *;
  y := *;
  assume s(y) & ~c(x,Z);
  c(x,y) := true;
  s(y) := false
}

action disconnect = {
  x := *;
  y := *;
  assume c(x,y);
  c(x,y) := false;
  s(y) := true
}

action error = {
  x := *;
  y := *;
  z := *;
  assume x ~= z & c(x,y) & c(z,y)
}

# concept c1(X,Y,Z) = (c(X,Z) * ~X = Y * c(Y,Z))

conjecture (X = Z | ~c(X,Y) | ~c(Z,Y))
"""

with ivy_module.Module():
    main_ui = new_ui()
    ui = main_ui.add(ivy_from_string(prog))
    ui.execute_action(ui.node(0),"connect")
    ui.execute_action(ui.node(1),"connect")
    ui.execute_action(ui.node(2),"error")
    cg = ui.view_state(ui.g.states[3])
    cg.reverse()
    cg.materialize_edge((cg.relation('c(X,Y)'),cg.node('client'),cg.node('server')))
    cg.materialize_edge((cg.relation('c(X,Y)'),cg.node('client','!=a'),cg.node('=b')))
    cg.gather()
    cg.reverse()
    cg.materialize_edge((cg.relation('c(X,Y)'),cg.node('=a'),cg.node('=b')))
    cg.show_relation(cg.relation('s'),'+')
    cg.gather()
    main_ui.answer('Refine')
    cg.reverse()
    cg.backtrack()
    cg.recalculate()
    cg.backtrack()
    cg.recalculate()
    cg.backtrack()
    cg.recalculate()
    assert ui.node(3).is_bottom(), "state 3 should be bottom"
    ui.mark_node(ui.node(1))
    ui.cover_node(ui.node(2))
#    ui.mainloop()


