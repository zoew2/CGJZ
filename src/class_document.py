from nltk import tokenize
from class_sentence import Sentence


class Document():
    def __init__(self, docid):
        """

        :param docid: e.g. "XIN_ENG_20041113.0001"
        """
        self.src=docid.split(".")[0].split("_")[0] #source
        self.lang=docid.split(".")[0].split("_")[1] #language
        self.date=docid.split(".")[0].split("_")[2] # date - 20041113
        self.year=self.date[:4] #year - 2004
        self.art_id=docid.split(".")[1] # .0001

        if int(self.year) > 2000:  # get path, if date belongs to 2004+
            self.path = "/corpora/LDC/LDC08T25/data/" + self.src.lower() + "_" + self.lang.lower() + "/" + \
                        self.src.lower() + "_" + self.lang.lower() + "_" + self.date[:-2]+".xml"
            self.docid_inxml=docid


        else:
            self.path = "/corpora/LDC/LDC02T31/" + self.src.lower() + "/" + self.year + "/" + \
                        self.date + "_" + self.src+ "_" + self.lang
            self.docid_inxml=self.src+self.date+"."+self.art_id #APW19980613.0001


        self.headline, self.text=self.get_doc(self.path,self.docid_inxml) # get headline + text
        self.sens=self.tok_toSens(self.text) #sen objects
        # print(self.sens)


    def get_doc(self, path,id_xml):
        """
        grab headline and content(text) of the document
        :param path:
        :param id_xml:
        :return:
        """
        headline=''
        text=''
        with open(path) as f:
            line=f.readline().strip('\n').strip('\t')
            while id_xml not in line:
                line = f.readline().strip('\n').strip('\t')
            while "<HEADLINE>" not in line:
                line = f.readline().strip('\n').strip('\t')
            line = f.readline().strip('\n').strip('\t')
            while "</HEADLINE>" not in line:
                headline+=line
                line = f.readline().strip('\n').strip('\t')
            while "<TEXT>" not in line:
                line = f.readline().strip('\n').strip('\t')
            line = f.readline().strip('\n').strip('\t')
            while "</TEXT>" not in line:
                if "<P>" not in line and "</P>" not in line:
                    text+=line+ ' '
                line = f.readline().strip('\n').replace("\t", "\n")
        # print(headline,text)
        return headline, text

    def tok_toSens(self,text):
        """
        create Sentence class for each sen from text
        :param text:
        :return:
        """
        sens=tokenize.sent_tokenize(text) #plain sens
        sens_c=[] #sens in class structure
        for sen_pos in range(len(sens)):
            newsen=Sentence(sens[sen_pos],sen_pos)
            # newsen=sens[sen_pos]
            # print(sens[sen_pos],sen_pos)
            sens_c.append(newsen)
        return sens_c



def main():


    # newdoc = Document("APW_ENG_19980613.0001")

    newdoc=Document("AFP_ENG_20050801.0031")





# main()  #uncomment this to test

