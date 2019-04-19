from nltk import tokenize
from .class_sentence import Sentence

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
        self.docid=input_docid  # docid
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

        if int(self.year) > 2000:  # get path, if date belongs to 2004+
            self.path = "/corpora/LDC/LDC08T25/data/" + self.src.lower() + self.lang.lower() + "/" + \
                        self.src.lower() + self.lang.lower() + "_" + self.date[:-2]+".xml"
            self.docid_inxml = self.docid

        else:
            self.path = "/corpora/LDC/LDC02T31/" + self.src.lower() + "/" + self.year + "/" + \
                        self.date + "_" + self.src2 + self.lang
            self.docid_inxml = self.src + self.date + "." + self.art_id  # APW19980613.0001

        self.headline, self.text = self.get_doc(self.path, self.docid_inxml)
        self.sens = self.tok_toSens(self.text)  # list of sen objects

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
            line = f.readline()
            while "</HEADLINE>" not in line:
                headline += line
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
        sens=tokenize.sent_tokenize(text)  # plain sens
        sens_c=[]  # sens in class structure
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

    def __eq__(self, other):
        return self.docid == other.docid
