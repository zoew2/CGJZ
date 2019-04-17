import sys
from .base_summary_generator import BaseSummaryGenerator


def main():
    """
    Read in the input files and summarize it
    :return:
    """

    # read in the input documents
    input_filename = sys.argv[1]
    input_file = open(input_filename, "r")
    input = input_file.readlines()

    summarizer = BaseSummaryGenerator(input)

    # read in output filename
    output_file = sys.argv[2]

    with open(output_file, "a") as f:

        # print model file
        print(summarizer.generate_summary(), file=f)


if __name__ == "__main__":
    main()
