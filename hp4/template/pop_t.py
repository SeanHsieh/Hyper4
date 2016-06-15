class GenPop():
  def __init__(self, nstages, nprimitives, test):
    fpath = '../p4src/'
    if test:
      fpath += 'config_' + str(nstages) + str(nprimitives) + '/'
    fpath += 'includes/pop.p4'
    f_pop = open(fpath, 'w')

    std_h = open('std_header', 'r')
    f_pop.write("/*\n")
    f_pop.write(std_h.read())
    f_pop.write("\n")
    std_h.close()

    pop_d = open('docs/pop_d', 'r')
    f_pop.write(pop_d.read())
    pop_d.close()
    f_pop.write("*/\n\n")

    indent = "  "
    out = ""

    f_pop.write(out)

