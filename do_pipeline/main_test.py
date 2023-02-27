import os
from .main import Biobakery, debug_input, JAMS, jams_db_path, Woltka
from os.path import abspath

test_input = abspath(os.path.join("testfiles", "READS"))
test_output = abspath("testfiles")


def test_biobakery_input():
    """Make the input for the biobakery pipeline. Test if the output directory contains the bio4.sh file."""
    bio4 = Biobakery("bio4", os.path.join(test_output, "bio4"))
    bio4.make_input(test_input, bio4.output_dir, "fastq")

    assert os.path.exists(os.path.join(bio4.output_dir, "bio4.sh"))


def test_jams_input():
    """Make the input for the JAMS pipeline. Test if the output directory contains the jams.sh file."""
    jams = JAMS("jams", os.path.join(test_output, "jams"), jams_db_path)
    jams.make_input(test_input)

    assert os.path.exists(os.path.join(jams.output_dir, "JAMS.swarm"))
    assert os.path.exists(os.path.join(jams.output_dir, "submit.sh"))


class TestWol:
    def test_bowtie(self):
        wol = Woltka("wol", os.path.join(test_output, "wol"))
        wol.make_bowtie(test_input, wol.output_dir, "fastq")

        assert os.path.exists(os.path.join(
            wol.output_dir, "submit_bowtie.swarm"))

    def test_classify(self):
        wol = Woltka("wol", os.path.join(test_output, "wol"))
        wol.make_classify(test_input, "fastq")

        assert os.path.exists(os.path.join(
            wol.output_dir, "classify", "submit_classify.swarm"))
