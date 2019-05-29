from nltk import tokenize
from .class_sentence import Sentence
import warnings

"""
This is a module file of Document class.
Input: document id. It grabs document from hard-coded path and stores the information of document in the class, including
docid, source, language, date, year, article id, path, headline, text, sentences(list of Sentence objects).

e.g., newdoc = Document("XIN_ENG_20041113.0001")

"""


class Document:
    def __init__(self, input_docid):
        """
        initialize Document class
        :param docid: e.g. "XIN_ENG_20041113.0001"
        """
        self.docid = input_docid  # docid
        ids = self.docid.split(".")
        info = ids[0].split("_")
        if len(info) < 2:
            self.src = ids[0][:3]
            self.src2 = "XIN" if self.src == "XIE" else self.src
            self.lang = "" if self.src == "NYT" else "_ENG"
            self.date = ids[0][3:]
        else:
            self.src = info[0]  # source
            self.src2 = "XIN" if self.src == "XIE" else self.src
            self.lang = "_" + info[1]  # language
            self.date = info[2]  # date - 20041113
        self.year = self.date[:4]  # year - 2004
        self.art_id = ids[1]  # .0001

        if self.src == 'TST':
            self.path = '../tests/test_data/' + self.src.lower() + self.lang.lower() + "_" + self.date[:-2] + ".xml"

            self.docid_inxml = self.docid
        elif int(self.year) > 2000:  # get path, if date belongs to 2004+
            self.path = "/corpora/LDC/LDC08T25/data/" + self.src.lower() + self.lang.lower() + "/" + \
                        self.src.lower() + self.lang.lower() + "_" + self.date[:-2] + ".xml"
            self.docid_inxml = self.docid

        else:
            self.path = "/corpora/LDC/LDC02T31/" + self.src.lower() + "/" + self.year + "/" + \
                        self.date + "_" + self.src2 + self.lang
            self.docid_inxml = self.src + self.date + "." + self.art_id  # APW19980613.0001

        self.headline, self.text = self.get_doc(self.path, self.docid_inxml)
        self.sens = self.tok_toSens(self.text)  # list of sen objects
        self.vectors = []  # placeholder
        self.tdf = []
        self.tokenized_text = []
        if not self.tokenized_text:
            self.__get_tokenized_text()

    def get_doc(self, path, id_xml):
        """
        grab headline and content(text) of the document
        :param path:
        :param id_xml:
        :return: headline, text
        """
        headline = ''
        text = ''
        with open(path) as f:
            line = f.readline()
            while id_xml not in line:
                line = f.readline()
            while "<HEADLINE>" not in line:
                line = f.readline()
            if "</HEADLINE>" in line:
                headline += line[10:-12].strip()
            else:
                line = f.readline()
            while "</HEADLINE>" not in line:
                headline += line.strip()
                line = f.readline()
            while "<TEXT>" not in line:
                line = f.readline()
            line = f.readline().strip('\n').replace("\t", "\n")
            while "</TEXT>" not in line:
                if "<P>" not in line and "</P>" not in line:
                    text += line + ' '
                else:
                    text += '\n'  # separate paragraphs
                line = f.readline().strip('\n').replace("\t", "\n")

        return headline, text

    def tok_toSens(self, text):
        """
        create Sentence class for each sen from text
        :param text:
        :return: sens_c
        """
        sens = tokenize.sent_tokenize(text)  # plain sens
        if not len(sens):
            warnings.warn('No sentence in the document! Document id: ' + self.docid, Warning)

        sens_c = []  # sens in class structure
        for sen_pos in range(len(sens)):

            newsen = Sentence(sens[sen_pos], sen_pos)
            sens_c.append(newsen)


        return sens_c

    def get_sen_bypos(self, sen_pos):
        """
        get a Sen obj by its sentence position
        :param sen_pos:
        :return: self.sens[sen_pos]
        """
        if sen_pos >= len(self.sens):
            raise Exception("Sentence position exceeds length of document! Document id: " + self.docid)
        return self.sens[sen_pos]

    def set_vectors(self, matrix):
        """
        assigns a matrix representing all the sentences in this document to self.vectors
        :param matrix: sparse matrix (dok_matrix????)
        :return:
        """
        self.vectors = matrix

    def set_tdf(self, term_doc_freq_list):
        self.tdf = term_doc_freq_list

    def __get_tokenized_text(self):

        for s in self.sens:
            for t in s.tokens:
                self.tokenized_text.append(t)

    def __eq__(self, other):
        """
        A document is equal to another if they have the same doc id
        :param other:
        :return:
        """
        return self.docid == other.docid
