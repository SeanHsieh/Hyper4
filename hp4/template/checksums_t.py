class GenChecksums():
  def __init__(self, test):
    fpath = '../p4src/hp4/includes/checksums'
    if test:
      fpath += '_test'
    fpath += '.p4'
    f_chksums = open(fpath, 'w')

    std_h = open('std_header', 'r')
    f_chksums.write("/*\n")
    f_chksums.write(std_h.read())
    f_chksums.write("\n")
    std_h.close()

    checksums_d = open('docs/checksums_d', 'r')
    f_chksums.write(checksums_d.read())
    checksums_d.close()
    f_chksums.write("*/\n\n")

    checksums_src = open('checksums.p4', 'r')
    f_chksums.write(checksums_src.read())
    checksums_src.close()

    f_chksums.close()
