import sys
from bs4 import BeautifulSoup
from .class_document import Document
from .base_summary_generator import BaseSummaryGenerator
from .base_content_selector import BaseContentSelector
from .lead_summary_generator import LeadSummaryGenerator
from .lead_sentence_selector import LeadSentenceSelector


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


def get_output_filename(topic_id):
    topic_id1 = topic_id[:-1]
    topic_id2 = topic_id[-1]
    output_file = './outputs/D2/' + topic_id1 + '-A.M.100.' + topic_id2 + '.test'
    return output_file


def main():
    """
    Read in the input files and output summaries
    :return:
    """

    # read in the topics
    topic_filename = sys.argv[1]
    topic_soup = make_soup(topic_filename)

    # read in version
    version = sys.argv[2]

    topics = load_documents_for_topics(topic_soup)

    # for each topic, load the documents and generate the summary
    for topic_id, documents in topics.items():
        if version == '1':
            summarizer = LeadSummaryGenerator(documents, LeadSentenceSelector())
        else:
            summarizer = BaseSummaryGenerator(documents, BaseContentSelector())
        output_file = get_output_filename(topic_id)

        with open(output_file, "a") as f:

            # print summary
            print(summarizer.generate_summary(), file=f)


if __name__ == "__main__":
    main()
