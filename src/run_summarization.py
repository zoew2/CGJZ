import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from bs4 import BeautifulSoup
from src.helpers.class_document import Document
from src.base_files.base_summary_generator import BaseSummaryGenerator
from src.base_files.base_content_selector import BaseContentSelector
from src.lead_sentence.lead_summary_generator import LeadSummaryGenerator
from src.lead_sentence.lead_sentence_selector import LeadSentenceSelector
from src.mead.mead_summary_generator import MeadSummaryGenerator
from src.mead.mead_content_selector import MeadContentSelector
from src.melda.melda_summary_generator import MeldaSummaryGenerator
from src.melda.melda_content_selector import MeldaContentSelector
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors
from src.helpers.class_preprocessor import Preprocessor
import argparse


def make_soup(topic_filename):
    """
    Parse the SGML
    :param topic_filename:
    :return:
    """
    with open(topic_filename) as topics:
        topic_soup = BeautifulSoup(topics, 'html.parser')
    return topic_soup


def load_documents_for_topics(topic_soup):
    """
    Load documents for each topic
    :param topic_soup:
    :return:
    """
    topics = {}
    for topic in topic_soup.find_all('topic'):
        documents = load_documents(topic)
        topics[topic['id']] = documents

    # At this point, all docs have been loaded and all unique words are stored in WordMap set
    # Need to trigger creation of mapping and of vectors
    WordMap.create_mapping()
    vec = Vectors()
    vec.create_freq_vectors(topics)  # do we need to have this here if we don't run mead based content selection
    vec.create_term_doc_freq(topics)

    return topics


def load_documents(topic):
    """
    Load the documents for the given topic
    :param topic:
    :return:
    """
    documents = []
    for doc in topic.find_all('doc'):
        documents.append(Document(doc['id']))

    return documents


def get_output_filename(topic_id, args):
    topic_id1 = topic_id[:-1]
    topic_id2 = topic_id[-1]
    output_file = args.output_dir + topic_id1 + '-A.M.100.' + topic_id2 + '.' + args.version + '-' + args.corpus + \
                  '-' + args.c_threshold + '-' + str(args.w_c) + str(args.w_p) + str(args.w_f)
    return output_file


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('topic_file')
    parser.add_argument('version', choices=['test', 'lead', 'mead', 'melda'])
    parser.add_argument('--output_dir', default='../outputs/D4_devtest/')
    parser.add_argument('--corpus', choices=['B', 'R'], default='B')
    parser.add_argument('--w_c', type=float, default=1)
    parser.add_argument('--w_p', type=float, default=1)
    parser.add_argument('--w_f', type=float, default=1)
    parser.add_argument('--c_threshold', choices=['max', 'mean', 'min', 'zero'], default='max')
    parser.add_argument('--lda_topics', type=int, default=3)
    parser.add_argument('--n', type=int, default=5)
    return parser.parse_args(args)


def main():
    """
    Read in the input files and output summaries
    :return:
    """

    args = parse_args(sys.argv[1:])

    # load spacy en model for later tokenization, stemming and NER
    Preprocessor.load_models()

    # read in the topics
    topic_soup = make_soup(args.topic_file)

    topics = load_documents_for_topics(topic_soup)
    idf = None

    # for each topic, load the documents and generate the summary
    for topic_id, documents in topics.items():
        if args.version == 'lead':
            summarizer = LeadSummaryGenerator(documents, LeadSentenceSelector(), args)
        elif args.version == 'mead':
            summarizer = MeadSummaryGenerator(documents, MeadContentSelector(), args)
            if idf is None:
                idf = summarizer.get_idf_array()
        elif args.version == 'melda':
            summarizer = MeldaSummaryGenerator(documents, MeldaContentSelector(), args)
            if idf is None:
                idf = summarizer.get_idf_array()
        else:
            summarizer = BaseSummaryGenerator(documents, BaseContentSelector(), args)
        output_file = get_output_filename(topic_id, args)

        with open(output_file, "w") as f:

            # print summary
            print(summarizer.generate_summary(idf), file=f)


if __name__ == "__main__":
    main()
