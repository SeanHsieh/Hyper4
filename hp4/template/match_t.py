class GenMatch():
  def __init__(self, nstages, nprimitives, test):
    fpath = '../p4src/'
    if test:
      fpath += 'config_' + str(nstages) + str(nprimitives) + '/'
    fpath += 'includes/match.p4'
    f_match = open(fpath, 'w')

    std_h = open('std_header', 'r')
    f_match.write("/*\n")
    f_match.write(std_h.read())
    f_match.write("\n")
    std_h.close()

    match_d = open('docs/match_d', 'r')
    f_match.write(match_d.read())
    match_d.close()
    f_match.write("*/\n\n")
    
    part1 = open('match_part1', 'r')
    f_match.write(part1.read())
    part1.close()

    indent = "  "

    for i in range(nstages):
      for src in ["extracted", "metadata", "stdmeta"]:
        out = "\n\ntable t" + str(i+1) + "_" + src + "_exact {\n"
        out += indent + "reads {\n"
        out += indent + indent + "meta_ctrl.program : exact;\n"
        if (src == "extracted"):
          out += indent + indent + "extracted.data : ternary;\n"
        elif (src == "metadata"):
          out += indent + indent + "tmeta.data : ternary;\n"
        out += indent + "}\n"
        out += indent + "actions {\n"
        if (src == "stdmeta"):
          out += indent + indent + "set_meta_stdmeta;\n"
        else:
          out += indent + indent + "init_program_state;\n"
        out += indent + "}\n"
        out += "}"
        f_match.write(out)
      out = "\n\ntable t" + str(i+1) + "_extracted_valid {\n"
      out += indent + "reads {\n"
      out += indent + indent + "meta_ctrl.program : exact;\n"
      out += indent + indent + "extracted.validbits : ternary;\n"
      out += indent + "}\n"
      out += indent + "actions {\n"
      out += indent + indent + "init_program_state;\n"
      out += indent + "}\n"
      out += "}"
      f_match.write(out)

    for i in range(nstages):
      out = "\n\ncontrol match_" + str(i+1) + " {\n"
      out += indent + "if(meta_ctrl.next_table == EXTRACTED_EXACT) {\n"
      out += indent + indent + "apply(t" + str(i+1) + "_extracted_exact);\n"
      out += indent + "}\n"
      out += indent + "else if(meta_ctrl.next_table == METADATA_EXACT) {\n"
      out += indent + indent + "apply(t" + str(i+1) + "_metadata_exact);\n"
      out += indent + "}\n"
      out += indent + "else if(meta_ctrl.next_table == STDMETA_EXACT) {\n"
      out += indent + indent + "apply(t" + str(i+1) + "_stdmeta_exact);\n"
      out += indent + indent + "switch_stdmeta_" + str(i+1) + "();\n"
      out += indent + "}\n"
      out += indent + "else if(meta_ctrl.next_table == EXTRACTED_VALID) {\n"
      out += indent + indent + "apply(t" + str(i+1) + "_extracted_valid);\n"
      out += indent + "}\n"
      out += "}"
      f_match.write(out)

    f_match.close()
