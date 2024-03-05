from nltk import PorterStemmer


class Node:
    def __init__(self, docID: str) -> None:
        self.docID = docID
        self.next = None


class PostingList:
    def __init__(self) -> None:
        self.head = None
        self.size = 0

    def insert(self, docID: int) -> None:
        newNode = Node(docID)
        if self.head is None:
            self.head = newNode
        elif self.head.docID >= docID:
            newNode.next = self.head
            self.head = newNode
        else:
            previous = self.head
            current = self.head
            while current is not None and current.docID <= docID:
                previous = current
                current = current.next
            previous.next = newNode
            newNode.next = current
        self.size += 1

    def display(self) -> None:
        current = self.head
        while current is not None:
            print(f"{current.docID} -> ", end="")
            current = current.next
        print("Finished posting list")


class InvertedIndex:
    def __init__(self) -> None:
        self.head = None
        self.index: dict[int, PostingList] = {}

    def create_index(self, tokens: list[str], docID: int) -> None:
        for token in tokens:
            if token not in self.index:
                self.index[token] = PostingList()
            self.index[token].insert(docID)

    def parse_query(self, query: str) -> None:
        if "/" in query.split():
            return None  # For positional queries
        else:
            return self.simple_boolean_query(query)

    def intersect(self, p1: PostingList, p2: PostingList) -> PostingList:
        if p1 is None or p2 is None:
            return None
        p1 = p1.head
        p2 = p2.head
        answer = PostingList()
        while p1 is not None and p2 is not None:
            if p1.docID == p2.docID:
                answer.insert(p1.docID)
                p1 = p1.next
                p2 = p2.next
            elif p1.docID < p2.docID:
                p1 = p1.next
            else:
                p2 = p2.next
        if answer.size == 0:
            return None
        else:
            return answer

    def AND_query(self, *query_terms: str) -> PostingList:
        stemmer = PorterStemmer()
        terms = []
        for term in query_terms:
            terms.append(stemmer.stem(term))
        terms.sort(
            key=lambda term: -self.index[term].size
        )  # For sorting using frequency
        result = self.index.get(terms[-1], None)
        terms.pop()
        while len(terms) > 0 and result is not None:
            result = self.intersect(result, self.index.get(terms[-1], None))
            terms.pop()
        return result

    # def simple_boolean_query(self, query_terms: str) -> PostingList:
    #     stemmer = PorterStemmer()
    #     terms = []
    #     for term in query_terms.split():
    #         terms.append(stemmer.stem(term))
    #     terms.sort(
    #         key=lambda term: -self.index[term].size
    #     )  # For sorting using frequency
    #     result = self.index.get(terms[-1], None)
    #     terms.pop()
    #     while len(terms) > 0 and result is not None:
    #         result = self.intersect(result, self.index.get(terms[-1], None))
    #         terms.pop()
    #     return result
