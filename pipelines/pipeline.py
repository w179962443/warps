
from models.openai import ChatgptAgent
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredFileLoader, TextLoader, CSVLoader
from models.chinese_text_splitter import ChineseTextSplitter
from models.pdf_loader import UnstructuredPaddlePDFLoader
from models.image_loader import UnstructuredPaddleImageLoader

class PipelineSolver:
    
    chatgpt_agent:ChatgptAgent

    def __init__(self) -> None:
        pass


def load_file(filepath, sentence_size=SPLIT_SIZE, using_zh_title_enhance=ZH_TITLE_ENHANCE,return_text=True,is_concat=True):
    if filepath.lower().endswith(".md"):
        loader = UnstructuredFileLoader(filepath, mode="elements")
        docs = loader.load()
    elif filepath.lower().endswith(".txt"):
        loader = TextLoader(filepath, autodetect_encoding=True)
        textsplitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
        docs = loader.load_and_split(textsplitter)
    elif filepath.lower().endswith(".pdf"):
        loader = UnstructuredPaddlePDFLoader(filepath)
        textsplitter = ChineseTextSplitter(pdf=True, sentence_size=sentence_size)
        docs = loader.load_and_split(textsplitter)
    elif filepath.lower().endswith(".jpg") or filepath.lower().endswith(".png"):
        loader = UnstructuredPaddleImageLoader(filepath, mode="elements")
        textsplitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
        docs = loader.load_and_split(text_splitter=textsplitter)
    elif filepath.lower().endswith(".csv"):
        loader = CSVLoader(filepath)
        docs = loader.load()
    else:
        loader = UnstructuredFileLoader(filepath, mode="elements")
        textsplitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
        docs = loader.load_and_split(text_splitter=textsplitter)
    if using_zh_title_enhance:
        docs = zh_title_enhance(docs)
    # write_check_file(filepath, docs)
    # if is_concat:
    #     docs=concat_docs(docs)
    # # #log_file_todisk(new_docs)
    # else:
    #     docs = [doc.page_content for doc in docs]

    # return new_docs
    # if return_text:
    #     docs=[doc.page_content for doc in docs]

    docs=split_file_ad_hoc_fn(docs,is_concat=is_concat)

    return docs


def split_file_ad_hoc_fn(docs,is_concat):
    docs=[doc.page_content for doc in docs]
    docs_0=[]
    for doc in docs:
        newdoc=re.sub("\s{4,}","   ",doc)
        docs_0.append(newdoc)
    
    docs_1=[]
    for doc in docs_0:
        doc=doc.strip()
        if len(doc)>0:
            docs_1.append(doc)

    if is_concat:
        docs_1=concat_docs(docs_1)

    return docs_1
