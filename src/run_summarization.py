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
from src.helpers.class_wordmap import WordMap
from src.helpers.class_vectors import Vectors
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
    vec.create_freq_vectors(topics)

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
    output_file = args.output_dir + topic_id1 + '-A.M.100.' + topic_id2 + '.' + args.version
    return output_file


def main():
    """
    Read in the input files and output summaries
    :return:
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('topic_file')
    parser.add_argument('version', choices=['lead', 'mead', 'melda'])
    parser.add_argument('--output_dir', default='../outputs/D3/')
    parser.add_argument('--corpus', choices=['B', 'R'], default='B')
    parser.add_argument('--w_c', type=float, default=1)
    parser.add_argument('--w_p', type=float, default=1)
    parser.add_argument('--w_f', type=float, default=1)
    parser.add_argument('--c_threshold', choices=['max', 'mean', 'min', 'zero'], default='max')

    args = parser.parse_args()

    # read in the topics
    topic_soup = make_soup(args.topic_file)

    topics = load_documents_for_topics(topic_soup)
    idf = None

    # for each topic, load the documents and generate the summary
    for topic_id, documents in topics.items():
        if args.version == 'lead':
            summarizer = LeadSummaryGenerator(documents, LeadSentenceSelector())
        elif args.version == 'mead':
            if idf is None:
                idf = MeadSummaryGenerator.get_idf_array(
                    MeadSummaryGenerator(documents, MeadContentSelector(), args))
            summarizer = MeadSummaryGenerator(documents, MeadContentSelector(), args)
        elif args.version == 'melda':
            pass
        else:
            summarizer = BaseSummaryGenerator(documents, BaseContentSelector())
        output_file = get_output_filename(topic_id, args)

        with open(output_file, "w") as f:

            # print summary
            print(summarizer.generate_summary(idf), file=f)


if __name__ == "__main__":
    main()
