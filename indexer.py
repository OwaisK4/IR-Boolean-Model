from nltk import PorterStemmer

"""
Node class that will contain each document ID and all positions of given
term in that document ID. Implemented as a self-referential data structure
(singly linked list).
"""
class Node:
    def __init__(self, docID: str, position: int) -> None:
        self.docID = docID
        self.next = None
        self.positions = [position]

"""
Posting list class that will be used throughout the program for all
query processing operations.
"""
class PostingList:
    def __init__(self) -> None:
        self.head = None
        self.size = 0

    """
    Inserts the document ID and position in the posting list as a new node.
    If document ID exists, simply appends the position to the documentID node.
    """
    def insert(self, docID: int, position: int = -1) -> None:
        newNode = Node(docID, position)
        if self.head is None:
            self.head = newNode
        elif self.head.docID == docID:
            self.head.positions.append(position)
            return
        elif self.head.docID > docID:
            newNode.next = self.head
            self.head = newNode
        else:
            previous = self.head
            current = self.head
            while current is not None and current.docID < docID:
                previous = current
                current = current.next
            if current is not None and current.docID == docID:
                current.positions.append(position)
                return
            previous.next = newNode
            newNode.next = current
        self.size += 1

    """
    Displays the whole posting list. Does not print positions of document IDs.
    """
    def display(self) -> None:
        current = self.head
        if current is not None:
            # print(f"{current.docID}: {current.positions}", end="")
            print(f"{current.docID}", end="")
        while current.next is not None:
            current = current.next
            print(f", {current.docID}", end="")
        print()

    """
    Returns the whole posting list as a string. Does not print positions of document IDs.
    """
    def result(self) -> str:
        answer = ""
        current = self.head
        if current is not None:
            answer += f"{current.docID}"
        while current.next is not None:
            current = current.next
            answer += f", {current.docID}"
        return answer

"""
Main Positional index class that performs all query processing operations.
Has the following functionality:
1. Index creation:
    Takes a list of cleaned tokens with their document IDs and creates a
    new positional index using a dictionary where the keys are terms and
    PostingList objects are values.
2. Query Parsing:
    Two types of queries can be parsed.
    i. Simple/Complex Boolean queries:
        Queries of this form can contain the following special keywords:
        AND, OR, NOT (case-sensitive)
        These queries are handled by self.simple_boolean_query() which takes
        the query terms as a string and maintains a stack for processing
        posting lists one by one starting from leftmost.
        Uses the functions: intersect, union and negation for query processing.
    ii. Positional Boolean queries
        These queries are handled by self.positional_boolean_query() which also
        the query terms as a string, but it only works for a positional query of
        2 operands and 1 K value (i.e. hardcoded).
"""
class InvertedIndex:
    def __init__(self) -> None:
        self.head = None
        self.index: dict[int, PostingList] = {}
        self.docIDs: PostingList = PostingList()

    def create_positional_index(
        self, tokens: list[tuple[str, int]], docID: int
    ) -> None:
        for token, position in tokens:
            if token not in self.index:
                self.index[token] = PostingList()
            self.index[token].insert(docID, position)
        self.docIDs.insert(docID)

    def parse_query(self, query: str) -> PostingList:
        if "/" in query.split():
            return self.positional_boolean_query(query)  # For positional queries
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

    def union(self, p1: PostingList, p2: PostingList) -> PostingList:
        if p1 is None and p2 is None:
            return None
        p1 = p1.head if p1 is not None else None
        p2 = p2.head if p2 is not None else None
        answer = PostingList()
        while p1 is not None and p2 is not None:
            if p1.docID == p2.docID:
                answer.insert(p1.docID)
                p1 = p1.next
                p2 = p2.next
            elif p1.docID < p2.docID:
                answer.insert(p1.docID)
                p1 = p1.next
            else:
                answer.insert(p2.docID)
                p2 = p2.next
        while p1 is not None:
            answer.insert(p1.docID)
            p1 = p1.next
        while p2 is not None:
            answer.insert(p2.docID)
            p2 = p2.next
        if answer.size == 0:
            return None
        else:
            return answer

    def negation(self, p: PostingList) -> PostingList:
        p1 = p.head if p is not None else None
        p2 = self.docIDs.head if self.docIDs is not None else None
        answer = PostingList()
        while p1 is not None and p2 is not None:
            while p1.docID > p2.docID:
                answer.insert(p2.docID)
                p2 = p2.next
            p1 = p1.next
            p2 = p2.next
        while p2 is not None:
            answer.insert(p2.docID)
            p2 = p2.next
        if answer.size == 0:
            return None
        else:
            return answer

    def simple_boolean_query(self, query_terms: str) -> PostingList:
        stemmer = PorterStemmer()
        terms = query_terms.split()
        stack = []
        i = 0
        while i < len(terms):
            if terms[i] == "AND":
                posting1 = stack.pop()
                if terms[i + 1] == "NOT":
                    i += 1
                    term = stemmer.stem(terms[i + 1].lower())
                    posting2 = self.index.get(term, None)
                    posting2 = self.negation(posting2)
                else:
                    term = stemmer.stem(terms[i + 1].lower())
                    posting2 = self.index.get(term, None)
                stack.append(self.intersect(posting1, posting2))
                i += 1
            elif terms[i] == "OR":
                posting1 = stack.pop()
                if terms[i + 1] == "NOT":
                    i += 1
                    term = stemmer.stem(terms[i + 1].lower())
                    posting2 = self.index.get(term, None)
                    posting2 = self.negation(posting2)
                else:
                    term = stemmer.stem(terms[i + 1].lower())
                    posting2 = self.index.get(term, None)
                stack.append(self.union(posting1, posting2))
                i += 1
            elif terms[i] == "NOT":
                i += 1
                term = stemmer.stem(terms[i].lower())
                posting = self.index.get(term, None)
                posting = self.negation(posting)
                stack.append(posting)
            else:
                term = stemmer.stem(terms[i].lower())
                posting = self.index.get(term, None)
                stack.append(posting)
            i += 1
        if len(stack) == 1:
            return stack[0]
        else:
            return None

    def positional_boolean_query(self, query_terms: str) -> PostingList:
        stemmer = PorterStemmer()
        terms = query_terms.split()
        if len(terms) != 4:
            print("Invalid postional query. Exiting.")
            return None
        word1 = stemmer.stem(terms[0].lower())
        word2 = stemmer.stem(terms[1].lower())
        try:
            k = int(terms[3])
        except:
            print("Invalid postional query. Exiting.")
            return None
        p1 = self.index.get(word1, None)
        p2 = self.index.get(word2, None)
        if p1 is None or p2 is None:
            return None
        p1 = p1.head
        p2 = p2.head
        answer = PostingList()
        # answer = []
        while p1 is not None and p2 is not None:
            if p1.docID < p2.docID:
                p1 = p1.next
            elif p1.docID > p2.docID:
                p2 = p2.next
            else:
                i, j = 0, 0
                while i < len(p1.positions) and j < len(p2.positions):
                    pos1 = p1.positions[i]
                    pos2 = p2.positions[j]
                    if abs(pos1 - pos2) <= k:
                        answer.insert(p1.docID)
                        break
                    elif pos1 < pos2:
                        i += 1
                    else:
                        j += 1
                p1 = p1.next
                p2 = p2.next

        if answer.size == 0:
            return None
        else:
            return answer