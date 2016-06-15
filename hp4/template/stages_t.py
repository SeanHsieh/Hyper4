class GenStages():
  def __init__(self, nstages, nprimitives, test):
    fpath = '../p4src/'
    if test:
      fpath += 'config_' + str(nstages) + str(nprimitives) + '/'
    fpath += 'includes/stages.p4'
    f_stages = open(fpath, 'w')

    std_h = open('std_header', 'r')
    f_stages.write("/*\n")
    f_stages.write(std_h.read())
    f_stages.write("\n")
    std_h.close()

    stages_d = open('docs/stages_d', 'r')
    f_stages.write(stages_d.read())
    stages_d.close()
    f_stages.write("*/\n\n")

    out = "#include \"match.p4\"\n"
    out += "#include \"action.p4\"\n"
    out += "#include \"switch_primitivetype.p4\"\n\n"
    
    f_stages.write(out)

    indent = "  "

    out = "action set_program_state(action_ID, primitive_index, stage_state, next_stage) {\n"
    out += indent + "modify_field(meta_primitive_state.action_ID, action_ID);\n"
    out += indent + "modify_field(meta_primitive_state.primitive_index, primitive_index);\n"
    out += indent + "modify_field(meta_ctrl.stage_state, stage_state);\n"
    out += indent + "modify_field(meta_ctrl.next_stage, next_stage);\n"
    out += "}\n\n"
    f_stages.write(out)

    for i in range(nstages):
      for j in range(nprimitives):
        out = "table set_program_state_" + str(i+1) + str(j+1) + " {\n"
        out += indent + "reads {\n"
        out += indent + indent + "meta_ctrl.program : exact;\n"
        out += indent + indent + "meta_primitive_state.action_ID : exact;\n"
        out += indent + indent + "meta_primitive_state.primitive_index : exact;\n"
        out += indent + "}\n"
        out += indent + "actions {\n"
        out += indent + indent + "set_program_state;\n"
        out += indent + "}\n"
        out += "}\n\n"
        f_stages.write(out)

    for i in range(nstages):
      indent = "  "
      out = "control stage" + str(i+1) + " {\n"
      out += indent + "match_" + str(i+1) + "();\n"
      out += indent + "apply(set_primitive_metadata_" + str(i+1) + "1);\n"
      out += indent + "switch_primitivetype_" + str(i+1) + "1();\n"
      out += indent + "apply(set_program_state_" + str(i+1) + "1);\n"
      for j in range(1, nprimitives):
        out += indent + "if(meta_ctrl.stage_state != COMPLETE) {\n"
        indent += "  "
        out += indent + "apply(set_primitive_metadata_" + str(i+1) + str(j+1) + ");\n"
        out += indent + "switch_primitivetype_" + str(i+1) + str(j+1) + "();\n"
        out += indent + "apply(set_program_state_" + str(i+1) + str(j+1) + ");\n"
      for j in range(1, nprimitives):
        indent = indent[:len(indent)-2]
        out += indent + "}\n"
      out += "}\n\n"
      f_stages.write(out)

    f_stages.close()
